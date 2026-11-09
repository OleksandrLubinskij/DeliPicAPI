from fastapi import Depends
from ..services.base_service import BaseCRUDService
from ..database.models import Product
from ..repository.product_repository import ProductRepository, get_product_repo


class ProductService(BaseCRUDService):
    model = Product
    def __init__(self, repo: ProductRepository):
        super().__init__(repo)

def get_product_service(repo: ProductRepository = Depends(get_product_repo)) -> ProductService:
      return ProductService(repo=repo)