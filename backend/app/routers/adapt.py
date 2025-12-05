from fastapi import APIRouter

from ..models import AdaptationRequest, AdaptationResponse
from ..services.adapt import plan_adjustments

router = APIRouter()


@router.post("/plan", response_model=AdaptationResponse)
async def plan_adjustments_endpoint(payload: AdaptationRequest) -> AdaptationResponse:
    return plan_adjustments(payload)
