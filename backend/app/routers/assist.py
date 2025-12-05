from fastapi import APIRouter

from ..models import AssistRequest, AssistResponse
from ..services.assist import generate_assistance

router = APIRouter()


@router.post("/assist", response_model=AssistResponse)
async def assist_endpoint(payload: AssistRequest) -> AssistResponse:
    return generate_assistance(payload)
