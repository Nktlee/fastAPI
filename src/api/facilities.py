from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Услуги"])


@router.get("", summary="Получение всех услуг")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавление услуг")
async def create_facility(facility_data: FacilityAdd, db: DBDep):
    facility = await FacilityService(db).create_facility(facility_data)

    return {"status": "ok", "data": facility}
