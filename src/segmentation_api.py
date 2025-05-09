from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
import logging
from .segmentation_service import SegmentationService

router = APIRouter()
logger = logging.getLogger('segmentation')
service = SegmentationService()

class SegmentationRequest(BaseModel):
    image_path: str
    threshold: Optional[float] = Query(0.5, ge=0.0, le=1.0, description='前景阈值，0-1之间')
    detail: Optional[float] = Query(0.7, ge=0.0, le=1.0, description='细节保留程度，0-1之间')
    model: Optional[str] = 'u2net'
    invert: Optional[bool] = False

@router.post('/segment')
def segment_image(req: SegmentationRequest):
    try:
        logger.info(f'收到分割请求: {req}')
        service = SegmentationService(model_name=req.model)
        out_path = service.segment(req.image_path, req.threshold, req.detail, req.invert)
        if out_path:
            return {"success": True, "segmented_path": out_path}
        else:
            return {"success": False, "msg": "分割失败，请检查图片路径和参数"}
    except Exception as e:
        logger.error(f'分割接口异常: {e}')
        return {"success": False, "msg": str(e)} 