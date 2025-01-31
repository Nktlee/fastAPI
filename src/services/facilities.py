from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def create_facility(self, facility_data: FacilityAdd):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        return facility