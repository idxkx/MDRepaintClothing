import React, { useState } from 'react';
import axios from 'axios';
import imageCompression from 'browser-image-compression';

export default function ImageUploader({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [uploadedUrl, setUploadedUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [compressing, setCompressing] = useState(false);

  // 选择图片后本地预览+压缩
  const handleFileChange = async (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setError('');
    setCompressing(true);
    try {
      const options = {
        maxSizeMB: 1,
        maxWidthOrHeight: 1920,
        useWebWorker: true,
        fileType: selected.type
      };
      const compressedFile = await imageCompression(selected, options);
      // 用原文件名和类型创建新File，保证filename和type都对
      const fixedFile = new File([compressedFile], selected.name, { type: compressedFile.type });
      setFile(fixedFile);
      setPreviewUrl(URL.createObjectURL(fixedFile));
      setUploadedUrl('');
    } catch (err) {
      setError('图片压缩失败，请重试');
      setFile(null);
      setPreviewUrl('');
    } finally {
      setCompressing(false);
    }
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
        onUploaded && onUploaded(res.data.url);
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
        accept="image/*"
        onChange={handleFileChange}
        className="mb-2"
      />
      {compressing && <div className="text-blue-500 mb-2">图片压缩中，请稍候...</div>}
      {previewUrl && (
        <div className="mb-2">
          <div className="text-sm text-gray-500">本地预览（已自动压缩）：</div>
          <img src={previewUrl} alt="预览" className="max-h-48 border" />
        </div>
      )}
      <button
        onClick={handleUpload}
        disabled={loading || !file || compressing}
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