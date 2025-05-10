import React, { useState } from 'react';

const modelOptions = [
  { value: 'janus', label: 'Janus（推荐）' },
  { value: 'blip2', label: 'BLIP2' }
];
const LANG_OPTIONS = [
  { value: 'zh', label: '中文' },
  { value: 'en', label: 'English' },
];

export default function DescribePanel({ imageUrl, segmentedUrl }) {
  const [model, setModel] = useState('deepseek');
  const [lang, setLang] = useState('zh');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleDescribe = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      // 取图片路径（去掉/api/image/前缀，适配后端）
      const image_path = imageUrl.replace('/api/image/', 'src/uploads/');
      const segmented_path = segmentedUrl.replace('/api/image/', 'src/uploads/');
      const resp = await fetch('/api/describe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_path, segmented_path, model, lang })
      });
      const data = await resp.json();
      if (data.success) {
        setResult(data);
      } else {
        setError(data.msg || '描述生成失败');
      }
    } catch (e) {
      setError('网络错误或服务器异常');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-xl bg-white rounded shadow p-6 mt-8">
      <div className="flex flex-row gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium mb-1">模型选择</label>
          <select value={model} onChange={e => setModel(e.target.value)} className="border rounded px-2 py-1">
            {modelOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">语言</label>
          <select value={lang} onChange={e => setLang(e.target.value)} className="border rounded px-2 py-1">
            {LANG_OPTIONS.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
          </select>
        </div>
        <div className="flex items-end">
          <button onClick={handleDescribe} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
            {loading ? '生成中...' : '生成描述'}
          </button>
        </div>
      </div>
      {error && <div className="text-red-500 mb-2">{error}</div>}
      {result && (
        <div className="mt-4">
          <div className="font-bold mb-2">原图描述：</div>
          <div className="bg-gray-100 p-2 rounded mb-4 whitespace-pre-line">{result.origin_desc}</div>
          <div className="font-bold mb-2">去背景图描述：</div>
          <div className="bg-gray-100 p-2 rounded whitespace-pre-line">{result.segmented_desc}</div>
          <div className="text-xs text-gray-400 mt-2">Prompt: {result.prompt}</div>
        </div>
      )}
    </div>
  );
} 