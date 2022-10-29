import random
import discord

from datetime import datetime
from typing import Optional
from beanie import Document, Indexed, after_event, Replace 
from pydantic import Field, conint, BaseModel

from config import Channel, Config

class MemberShort(BaseModel):
    member_id: int

class MemberModel(Document):

    member_id: Indexed(conint(strict=True), unique=True)

    gamacoin: conint(ge=0) = 0
    xp: conint(ge=0) = 0

    last_do_daily: Optional[datetime]
    last_do_weekly: Optional[datetime]

    last_level = 1
    last_jackpot = 0

    cmd_guess_use = 0
    cmd_guess_lose = 0
    cmd_guess_won = 0

    wheel_use = 0

    invite_url: Optional[str]

    is_verified: bool = False
    is_staff: bool = False
    is_power: bool = True
    is_leaved: bool = False

    leaved_at: Optional[datetime]
    crated_at: datetime = Field(default_factory=datetime.utcnow)


    class Collection:
        name = "members"

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    @property
    def level(self):
        return (self.xp // 500) + 1

    @property
    def rank(self):
        return (self.level // 10) + 1

    async def get_or_create_invite(self, target_channel: discord.TextChannel):
        if not self.invite_url:
            invite = await target_channel.create_invite(
                max_age=0, 
                max_uses=0,
                unique=True,
            )
            self.invite_url = invite.url
            await self.save()
        return self.invite_url

    @staticmethod
    async def join_member(member: discord.Member, verified: bool = False, client: discord.Client = None):
        member_model = await MemberModel.find_one(MemberModel.member_id == member.id)
        if not member_model:
            activities_channel = await client.fetch_channel(Channel.ACTIVITIES)
            member_model = MemberModel(
                member_id = member.id,
                is_verified = verified
            )
            member_model.gamacoin += Config.INC_COIN_ON_JOIN
            await member_model.save()
            await activities_channel.send(f"<:CHEST:994300228108828734> ● {member.mention} just got 5 <:GamaCoin:994292311271944274> joining the channel!")
        else:
            member_model.is_leaved = False
            member_model.leaved_at = None
            await member_model.save()
    
    @staticmethod
    async def leave_member(member: discord.Member):
        if not member.bot:
            member_model = await MemberModel.find_one(MemberModel.member_id == member.id)
            if member_model:
                member_model.is_leaved = True
                member_model.is_verified = False
                member_model.leaved_at = datetime.now()
                await member_model.save()

    @staticmethod
    async def members_id_list():
        query = await MemberModel.find({}).project(MemberShort).to_list()
        return [member.member_id for member in query]

    @after_event([Replace])
    async def on_update(self):
        if self.level > self.last_level:
            channel: discord.TextChannel = await self.discord_client.fetch_channel(Channel.ACTIVITIES)
            levelup_value = self.level - self.last_level
            won_coin = (random.randint(1, 7)) * levelup_value
            self.gamacoin += won_coin
            self.last_level = self.level
            await self.save()
            await channel.send(f'🎖️ ● <@{self.member_id}> just leveled up to **{self.level}** <:stats:994300647082041534> and won **{won_coin}** <:GamaCoin:994292311271944274>')
        if (self.level // 10) > self.last_jackpot:
            channel: discord.TextChannel = await self.discord_client.fetch_channel(Channel.ACTIVITIES)
            levelup_value = self.level // 10 - self.last_jackpot
            won_coin = (random.randint(5, 20)) * levelup_value
            self.last_jackpot += levelup_value
            self.gamacoin += won_coin
            await self.save()
            await channel.send(f'🎰 ● <@{self.member_id}> got {won_coin} <:GamaCoin:994292311271944274> for Jackpot!')