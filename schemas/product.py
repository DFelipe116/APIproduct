from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id : Optional[int] = None
    title : str = Field(min_length=2, max_length=200)
    characteristics : str = Field(min_length=20, max_length=800)
    price : float = Field(ge=0, le=999999999)
    quantity : int = Field(ge=0, le=2000)
    available : int = Field(ge=0, le=2000)
    category : str = Field(min_length=2, max_length=100)
