from datetime import datetime
from typing import List, Optional

from beanie import Document, Link
from pydantic import Field

from .member import MemberModel


class ProductModel(Document):

    title: str
    message_id: int
    price: int
    media_url: Optional[str]
    product_url: Optional[str]
    
    buyers: List[Link[MemberModel]] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "products"

    class Config:
        arbitrary_types_allowed = True
    