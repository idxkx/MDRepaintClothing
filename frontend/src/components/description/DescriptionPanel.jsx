import React, { useState } from 'react';
import CopyButton from './CopyButton';
import StyleSelector from './StyleSelector';

// 结构化描述的Mock数据示例
const mockDescription = {
  lang: 'zh',
  style: 'detailed',
  sections: [
    { label: '款式类型', value: '长袖衬衫' },
    { label: '剪裁与版型', value: '修身，标准衣长，常规袖口' },
    { label: '各部位颜色', value: '主体为白色，袖口为蓝色，领口为灰色' },
    { label: '材质/面料', value: '纯棉' },
    { label: '关键细节', value: '蓝色竖条纹，白色纽扣，左胸单口袋，翻领' },
    { label: '风格与适用场景', value: '商务休闲' },
    { label: '独特特征', value: '下摆微弧形，后背有褶皱装饰' },
  ],
  raw: '一件长袖修身白色棉质衬衫，主体为白色，袖口为蓝色，领口为灰色，蓝色竖条纹，白色纽扣，左胸单口袋，翻领，下摆微弧形，后背有褶皱装饰，风格为商务休闲。'
};

export default function DescriptionPanel({ description = mockDescription, onStyleChange }) {
  const [editableDesc, setEditableDesc] = useState(description.raw);
  const [isEditing, setIsEditing] = useState(false);

  // 结构化分段展示
  const renderSections = () => (
    <div className="space-y-2">
      {description.sections.map((sec, idx) => (
        <div key={idx} className="flex flex-row items-start">
          <span className="font-semibold w-32 text-gray-700">{sec.label}：</span>
          <span className="text-gray-900">{sec.value}</span>
        </div>
      ))}
    </div>
  );

  // 编辑区
  const renderEditable = () => (
    <textarea
      className="w-full border rounded p-2 text-gray-900 mt-2"
      rows={4}
      value={editableDesc}
      onChange={e => setEditableDesc(e.target.value)}
    />
  );

  return (
    <div className="bg-white rounded shadow p-6 max-w-2xl mx-auto mt-6">
      <div className="flex flex-row justify-between items-center mb-4">
        <h2 className="text-lg font-bold text-blue-700">服装结构化描述</h2>
        <StyleSelector lang={description.lang} style={description.style} onChange={onStyleChange} />
      </div>
      {renderSections()}
      <div className="mt-4 flex flex-row gap-2 items-center">
        <CopyButton text={isEditing ? editableDesc : description.raw} />
        <button
          className="px-3 py-1 border rounded text-sm text-blue-600 hover:bg-blue-50"
          onClick={() => setIsEditing(e => !e)}
        >
          {isEditing ? '完成编辑' : '编辑描述'}
        </button>
      </div>
      {isEditing && renderEditable()}
    </div>
  );
} 