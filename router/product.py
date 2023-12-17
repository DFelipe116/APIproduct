from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.product import Product as ProductModel
from schemas.product import Product
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

product_router = APIRouter()

@product_router.get("/products", tags=['products'], response_model=List[Product], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_products() -> List[Product]:
    db = Session()
    result = db.query(ProductModel).all()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@product_router.get("/products/{id}", tags=['products'], response_model=Product, status_code=status.HTTP_200_OK)
def get_product(id:int = Path(ge=1, le=2000)):
    db = Session()
    result = db.query(ProductModel).filter(ProductModel.id == id).first()
    response = JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
    if not result:
        response = JSONResponse(content={"message": "Product not found"},
                                status_code=status.HTTP_404_NOT_FOUND)
    return response

@product_router.get("/products/", tags=['products'], response_model=List[Product])
def get_products_by_category(category:str = Query(min_length=5, max_length=12)):
    db = Session()
    result = db.query(ProductModel).filter(ProductModel.category == category).all()
    response = JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
    if not result:
        response = JSONResponse(content={"message": "Category not found"},
                                status_code=status.HTTP_404_NOT_FOUND)
    return response

@product_router.post("/products", tags=['products'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    db = Session()
    new_product = ProductModel(**product.model_dump())
    db.add(new_product)
    db.commit()
    return JSONResponse(content={"message": "Product created successfully"},
                        status_code=status.HTTP_201_CREATED)

@product_router.put("/products/{id}", tags=['products'])
def update_product(id: int, product: Product):
    db = Session()
    result = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not result:
        return JSONResponse(content={"message": "Not found"},
                                status_code=status.HTTP_404_NOT_FOUND)
    result.title = product.title
    result.characteristics = product.characteristics
    result.price = product.price
    result.quantity = product.quantity
    result.category = product.category
    result.available = product.available
    db.commit()
    return JSONResponse(content={"message": "Product update successfully"},
                        status_code=status.HTTP_200_OK)

@product_router.delete("/products/{id}", tags=['products'], response_model=dict)
def delete_product(id: int):
    db = Session()
    result = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={'message': 'Not Found'})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Product deleted successfully"},
                        status_code=status.HTTP_200_OK)

@product_router.post("/market/{id}", tags=['products'], response_model=dict)
def shopping_cart(id: int, quantity: int):
    db = Session()
    result = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={'message': 'Not Found'})
    available = available - quantity
    db.add(result)
    db.commit()
    return JSONResponse(content={"message": "Product add to shopping cart successfully"},
                        status_code=status.HTTP_202_ACCEPTED)
