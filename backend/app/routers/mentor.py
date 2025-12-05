from fastapi import APIRouter

from ..models import MentorRequest, MentorResponse
from ..services.mentor import craft_response

router = APIRouter()


@router.post("/coach", response_model=MentorResponse)
async def mentor_endpoint(payload: MentorRequest) -> MentorResponse:
    return craft_response(payload)
