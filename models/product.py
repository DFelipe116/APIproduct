from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable=False) 
    characteristics = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    