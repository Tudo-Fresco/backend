from typing import List
from uuid import UUID
from api.controllers.models.demand.demand_response_model import DemandResponseModel
from api.controllers.models.post.post_response_model import PostResponseModel
from api.controllers.models.user.user_response_model import UserResponseModel
from api.enums.demand_status import DemandStatus
from api.enums.product_type import ProductType
from api.services.demand_service import DemandService
from api.services.service_response import ServiceResponse
from api.shared.logger import Logger


class ReelService():

    def __init__(self, demand_service: DemandService):
        self.logger = Logger('ReelService')
        self.demand_service = demand_service

    async def get_posts(self,
                        user: UserResponseModel,
                        store_uuid: UUID,
                        status: DemandStatus = DemandStatus.ANY,
                        page: int = 1,
                        per_page: int = 20,
                        radius_meters: int = 10000,
                        product_type: ProductType = ProductType.ANY) -> ServiceResponse[PostResponseModel]:
        service_response = await self.demand_service.list_by_store(user, store_uuid, status, page, per_page, radius_meters, product_type)
        demands = service_response.payload or []
        posts = self.convert_demands_to_post_response(demands)
        return ServiceResponse(
            status=service_response.status,
            message=f'Found {len(demands)} posts for the store {store_uuid}',
            payload=posts
        )

    def convert_demands_to_post_response(self, demands: List[DemandResponseModel]) -> List[PostResponseModel]:
        posts = []
        for demand in demands:
            post = PostResponseModel(**demand.model_dump())
            posts.append(post)
        return posts