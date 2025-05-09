import React, { useState } from 'react';
import axios from 'axios';

export default function SegmentationPanel({ imageUrl, onSegmented }) {
  const [threshold, setThreshold] = useState(0.5);
  const [detail, setDetail] = useState(0.7);
  const [model, setModel] = useState('u2net');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // 只请求保留衣服分割图
  const handleSegment = async () => {
    if (!imageUrl) {
      setError('请先上传图片');
      return;
    }
    setLoading(true);
    setError('');
    try {
      // 提取图片文件名
      const path = imageUrl.replace(/^.*\/api\/image\//, 'src/uploads/');
      const res = await axios.post('/api/segment', {
        image_path: path,
        threshold,
        detail,
        model,
        invert: false,
      });
      if (res.data.success) {
        onSegmented && onSegmented(res.data.segmented_path);
      } else {
        setError(res.data.msg || '分割失败');
      }
    } catch (err) {
      setError(err.response?.data?.msg || '分割失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 border rounded shadow mt-4">
      <h2 className="text-lg font-bold mb-2">图片抠图参数设置</h2>
      <div className="mb-2">
        <label className="block text-sm font-medium">分割模型：</label>
        <select
          value={model}
          onChange={e => setModel(e.target.value)}
          className="border rounded px-2 py-1"
        >
          <option value="u2net">U^2-Net（推荐）</option>
        </select>
        <div className="text-xs text-gray-500">目前仅支持U^2-Net，后续可扩展</div>
      </div>
      <div className="mb-2">
        <label className="block text-sm font-medium">前景阈值：</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={threshold}
          onChange={e => setThreshold(Number(e.target.value))}
          className="w-full"
        />
        <div className="text-xs text-gray-500">数值越大，抠图越严格。当前：{threshold}</div>
      </div>
      <div className="mb-2">
        <label className="block text-sm font-medium">细节保留：</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={detail}
          onChange={e => setDetail(Number(e.target.value))}
          className="w-full"
        />
        <div className="text-xs text-gray-500">数值越大，保留越多细节。当前：{detail}</div>
      </div>
      <button
        onClick={handleSegment}
        disabled={loading || !imageUrl}
        className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? '抠图中...' : '一键抠图'}
      </button>
      {error && <div className="text-red-500 mt-2">{error}</div>}
    </div>
  );
} 