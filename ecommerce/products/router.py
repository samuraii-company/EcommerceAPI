from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ecommerce import db
from typing import List
from fastapi.responses import JSONResponse

from . import schemas
from . import services
from . import validator

router = APIRouter(tags=["Products"], prefix="/api/v1/products")


@router.get("/caregory/", response_model=List[schemas.OutCategory])
async def get_all_category(
    database: Session = Depends(db.get_db)
):
    """
    Get all category
    """
    category = await services.get_all_category(database)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found in the system"
        )
    
    return category


@router.post("/caregory/")
async def create_category(
    request: schemas.Category,
    database: Session = Depends(db.get_db)
):
    """
    Create category
    """
     
    category = await services.create_new_category(request, database)
    return category


@router.get("/caregory/{id}/", response_model=schemas.OutCategory)
async def get_category_by_id(
    id: int,
    database: Session = Depends(db.get_db)
):
    """
    Get category by id
    """
    category = await services.get_category_by_id(id, database)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id:{id}, not found in system"
        )
        
    return category


@router.delete("/caregory/{id}/")
async def delete_category_by_id(
    id: int,
    database: Session = Depends(db.get_db)
):
    """
    Delete category by id
    """
    category = await validator.verify_category_exist(id, database)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id:{id}, not found in system"
        )
    await services.delete_category_by_id(id, database)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success"}
    )


@router.post("/")
async def create_product(
    request: schemas.Product,
    database: Session = Depends(db.get_db)
):
    """
    Create new product
    """
    _category = await validator.verify_category_exist(request.category_id, database)
    
    if not _category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some category dose not exists"
        )
    
    product = await services.create_product(request, database)
    return product


@router.get("/", response_model=List[schemas.OutProduct])
async def get_all_products(
    database: Session = Depends(db.get_db)
):
    """
    Get all products
    """
    products = await services.get_all_products(database)
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found in the system"
        )
    
    return products


@router.get("/{id}/", response_model=schemas.OutProduct)
async def get_product_by_id(
    id: int,
    database: Session = Depends(db.get_db)
):
    """
    Get product by id
    """
    product = await services.get_product_by_id(id, database)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id:{id}, not found in system"
        )
        
    return product


@router.delete("/{id}/")
async def delete_product_by_id(
    id: int,
    database: Session = Depends(db.get_db)
):
    """
    Delete product by id
    """
    product = await validator.verify_product_exist(id, database)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id:{id}, not found in system"
        )

    await services.delete_product_by_id(id, database)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success"}
    )