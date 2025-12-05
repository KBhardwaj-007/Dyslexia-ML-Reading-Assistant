from fastapi import APIRouter

from ..models import AttentionRequest, AttentionResponse
from ..services.attention import analyze_attention

router = APIRouter()


@router.post("/analyze", response_model=AttentionResponse)
async def analyze_attention_endpoint(payload: AttentionRequest) -> AttentionResponse:
    return analyze_attention(payload)
