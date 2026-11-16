from fastapi import Depends

from ..core.exceptions import NotFoundError
from ..services.base_service import BaseCRUDService
from ..database.models import Product
from ..repository.product_repository import ProductRepository, get_product_repo


class ProductService(BaseCRUDService):
    model = Product
    def __init__(self, repo: ProductRepository):
        super().__init__(repo)
        
    async def fetch_by_id(
        self, 
        id: int, 
        fields: list[str] | None = None,
        include_embedding: bool = False) -> Product:
        instance = await self.repo.get_by_id(
            id=id,
            fields=fields,
            include_embedding=include_embedding
        )
        if instance is None:
            raise NotFoundError()
        return instance

def get_product_service(repo: ProductRepository = Depends(get_product_repo)) -> ProductService:
      return ProductService(repo=repo)