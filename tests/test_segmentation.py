import os
import pytest
from src.segmentation_service import SegmentationService
from PIL import Image

def test_model_load():
    service = SegmentationService('u2net')
    assert service.model is not None

def test_segment_success(tmp_path):
    # 创建一张测试图片
    img = Image.new('RGB', (10, 10), color='white')
    img_path = tmp_path / 'test.jpg'
    img.save(img_path)
    service = SegmentationService('u2net')
    out_path = service.segment(str(img_path), threshold=0.5, detail=0.7)
    assert out_path is not None
    assert os.path.exists(out_path)

def test_segment_fail():
    service = SegmentationService('u2net')
    # 输入不存在的图片路径
    out_path = service.segment('not_exist.jpg')
    assert out_path is None

def test_invalid_model():
    with pytest.raises(ValueError):
        SegmentationService('invalid_model') 