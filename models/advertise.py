import random

from datetime import datetime
from typing import Optional


from beanie import Document, after_event, Replace
from pydantic import Field


class AdvertiseModel(Document):

    advertiser: int
    title: str
    context: str
    url: Optional[str]
    banner_url: Optional[str]
    display_time: int = 1
    random_index: int
    is_active: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_display_dattime: Optional[datetime]

    class Collection:
        name = "advertise"

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
    

    @after_event([Replace])
    async def delete_zero_display_time(self):
        if self.display_time == 0:
            await self.delete()