
from fastapi import APIRouter


router = APIRouter(tags=["TEST"], prefix="/test")


@router.get("/")
async def test_endpoint():
    """Retrieve a list of all timezones."""
    return {
        "data": [
        ],
        "total": 2,
    }