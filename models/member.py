import discord

from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field, conint, BaseModel

class MemberShort(BaseModel):
    member_id: int

class MemberModel(Document):

    member_id: Indexed(conint(strict=True), unique=True)

    gamacoin: conint(ge=0) = 0
    xp: conint(ge=0) = 0

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


    @staticmethod
    async def join_member(member: discord.Member, verified: bool = False):
        if not member.bot:
            member_model = await MemberModel.find_one(MemberModel.member_id == member.id)
            if not member_model:
                member_model = MemberModel(
                    member_id = member.id,
                    is_verified = verified
                )
                await member_model.save()
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