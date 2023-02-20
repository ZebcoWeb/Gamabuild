from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import Field

class VoteModel(Document):

    builder: str
    caption: str
    picture_url: str
    instagram_profile_url: str
    message_id: Optional[int]
    
    voters: List[int] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "votes"

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
    