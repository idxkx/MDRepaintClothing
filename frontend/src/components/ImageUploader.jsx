import React, { useState } from 'react';
import axios from 'axios';

export default function ImageUploader() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [uploadedUrl, setUploadedUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // 选择图片后本地预览
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    const allowed = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowed.includes(selected.type)) {
      setError('仅支持jpg/png/webp格式图片');
      setFile(null);
      setPreviewUrl('');
      return;
    }
    if (selected.size > 5 * 1024 * 1024) {
      setError('图片大小不能超过5MB');
      setFile(null);
      setPreviewUrl('');
      return;
    }
    setError('');
    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));
    setUploadedUrl('');
  };

  // 上传图片到后端
  const handleUpload = async () => {
    if (!file) {
      setError('请先选择图片');
      return;
    }
    setLoading(true);
    setError('');
    setUploadedUrl('');
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('/api/upload-image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (res.data.success) {
        setUploadedUrl(res.data.url);
      } else {
        setError(res.data.error || '上传失败');
      }
    } catch (err) {
      setError(err.response?.data?.detail || '上传失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 border rounded shadow">
      <h2 className="text-lg font-bold mb-2">图片上传与预览</h2>
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp"
        onChange={handleFileChange}
        className="mb-2"
      />
      {previewUrl && (
        <div className="mb-2">
          <div className="text-sm text-gray-500">本地预览：</div>
          <img src={previewUrl} alt="预览" className="max-h-48 border" />
        </div>
      )}
      <button
        onClick={handleUpload}
        disabled={loading || !file}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? '上传中...' : '上传图片'}
      </button>
      {error && <div className="text-red-500 mt-2">{error}</div>}
      {uploadedUrl && (
        <div className="mt-4">
          <div className="text-sm text-green-600">上传成功，正式图片：</div>
          <img src={uploadedUrl} alt="已上传" className="max-h-48 border" />
        </div>
      )}
    </div>
  );
} 