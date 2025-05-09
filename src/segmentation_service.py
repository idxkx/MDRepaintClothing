import os
import logging
from typing import Optional
from PIL import Image
import numpy as np
import time

# 预留：实际部署时替换为真实U2Net模型加载与推理代码
class DummyU2Net:
    def __init__(self):
        pass
    def predict(self, image: Image.Image, threshold: float = 0.5, detail: float = 0.7, invert: bool = False) -> Image.Image:
        gray = image.convert('L')
        arr = np.array(gray)
        mask = (arr < int(255 * threshold)).astype(np.uint8) * 255
        if invert:
            mask = 255 - mask  # 取反
        # 保存mask方便调试（可选）
        # Image.fromarray(mask).save('debug_mask.png')
        return Image.fromarray(mask)

class SegmentationService:
    def __init__(self, model_name: str = 'u2net'):
        self.logger = logging.getLogger('segmentation')
        self.model_name = model_name
        self.model = self._load_model(model_name)
    def _load_model(self, model_name: str):
        # 这里只实现U2Net占位，后续可扩展
        if model_name == 'u2net':
            self.logger.info('加载U2Net分割模型')
            return DummyU2Net()
        else:
            self.logger.error(f'暂不支持的分割模型: {model_name}')
            raise ValueError(f'不支持的模型: {model_name}')
    def segment(self, image_path: str, threshold: float = 0.5, detail: float = 0.7, invert: bool = False) -> Optional[str]:
        try:
            image = Image.open(image_path).convert('RGBA')
            mask = self.model.predict(image, threshold, detail, invert).convert('L')
            arr = np.array(image)
            mask_arr = np.array(mask)
            out_arr = arr.copy()
            # 保存mask图片，便于调试
            Image.fromarray(mask_arr).save('logs/debug_mask.png')
            if not invert:
                # 保留衣服：mask=0的地方变白
                out_arr[mask_arr == 0] = [255, 255, 255, 255]
            else:
                # 强制整张图变红，便于验证前端显示
                out_arr[:, :] = [255, 0, 0, 255]
            out_img = Image.fromarray(out_arr)
            # 分割结果文件名加时间戳，避免缓存
            ts = int(time.time())
            out_path = image_path.replace('.', f'_seg_{ts}.')
            ext = os.path.splitext(out_path)[1].lower()
            # 修复：如果是RGBA且扩展名为jpg/jpeg，强制保存为png
            if out_img.mode == 'RGBA' and ext in ['.jpg', '.jpeg']:
                out_path = out_path.rsplit('.', 1)[0] + '.png'
                out_img.save(out_path)
            elif ext in ['.jpg', '.jpeg']:
                out_img = out_img.convert('RGB')
                out_img.save(out_path)
            else:
                out_img.save(out_path)
            self.logger.info(f'分割完成: {out_path}')
            return out_path
        except Exception as e:
            self.logger.error(f'分割失败: {e}')
            return None 