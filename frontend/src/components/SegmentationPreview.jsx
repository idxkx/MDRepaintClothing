import React from 'react';
// 推荐安装 react-compare-image: npm install react-compare-image
import CompareImage from 'react-compare-image';

export default function SegmentationPreview({ originalUrl, segmentedUrl }) {
  if (!originalUrl || !segmentedUrl) return null;
  // 固定宽度，保证比例一致
  const fixedWidth = 384;
  return (
    <div className="mx-auto p-4 border rounded shadow mt-4" style={{ width: fixedWidth }}>
      <h2 className="text-lg font-bold mb-2">分割结果对比</h2>
      <CompareImage
        leftImage={originalUrl}
        rightImage={segmentedUrl}
        leftImageLabel="原图"
        rightImageLabel="分割图"
        sliderLineColor="#22c55e"
      />
      <div className="text-xs text-gray-500 mt-2">可左右拖动滑块对比分割效果</div>
    </div>
  );
} 