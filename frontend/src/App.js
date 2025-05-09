import React, { useState, useEffect } from 'react';
import './App.css';
import ImageUploader from './components/ImageUploader';
import SegmentationPanel from './components/SegmentationPanel';

function App() {
  const [uploadedUrl, setUploadedUrl] = useState('');
  const [segmentedClothUrl, setSegmentedClothUrl] = useState(''); // 保留衣服
  const [segmentedBgUrl, setSegmentedBgUrl] = useState(''); // 保留背景
  const [version, setVersion] = useState('');

  useEffect(() => {
    fetch('/version.txt')
      .then(res => res.text())
      .then(setVersion)
      .catch(() => setVersion(''));
  }, []);

  // 只处理保留衣服分割图
  const handleSegmented = (clothUrl) => {
    setSegmentedClothUrl(clothUrl.replace('src/uploads/', '/api/image/'));
  };

  return (
    <div className="App min-h-screen bg-gray-50 flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold mb-4">服装图片上传与抠图演示</h1>
      <ImageUploader onUploaded={url => { setUploadedUrl(url); setSegmentedClothUrl(''); }} />
      {uploadedUrl && (
        <SegmentationPanel imageUrl={uploadedUrl} onSegmented={handleSegmented} />
      )}
      {/* 只展示保留衣服分割图 */}
      {uploadedUrl && segmentedClothUrl && (
        <div className="flex flex-col items-center mt-6">
          <div className="text-sm font-bold mb-2">保留衣服分割图</div>
          <img src={segmentedClothUrl} alt="保留衣服分割图" className="max-h-72 border" />
        </div>
      )}
      <div style={{ position: 'fixed', right: 20, bottom: 20, color: '#888', fontSize: 12 }}>
        版本号：{version}
      </div>
    </div>
  );
}

export default App;
