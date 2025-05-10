import pytest
from src.description import description_service

# Mock torch和大模型，避免实际加载
import sys
import types
class DummyModel:
    def eval(self): return self
    def generate(self, **kwargs): return [[1,2,3]]
    def to(self, *args, **kwargs): return self
    @property
    def language_model(self): return self
    def prepare_inputs_embeds(self, **kwargs): return None

def dummy_decode(*args, **kwargs):
    return "Mocked description."

def dummy_processor(*args, **kwargs):
    class Dummy:
        def __call__(self, *a, **k): return {'input_ids': [1,2,3]}
        def decode(self, *a, **k): return "Mocked description."
        @property
        def tokenizer(self):
            class T: eos_token_id=0; bos_token_id=1
            def decode(self, *a, **k): return "Mocked janus description."
            return T()
    return Dummy()

def test_invalid_model_name(monkeypatch):
    with pytest.raises(ValueError):
        description_service.generate_description("fake.jpg", model_name="unknown")

def test_blip2_mock(monkeypatch):
    monkeypatch.setattr(description_service, "Blip2Processor", lambda *a, **k: dummy_processor())
    monkeypatch.setattr(description_service, "Blip2ForConditionalGeneration", lambda *a, **k: DummyModel())
    monkeypatch.setattr(description_service, "torch", types.SimpleNamespace(no_grad=lambda: types.SimpleNamespace(__enter__=lambda s: None, __exit__=lambda s,a,b,c: None)))
    monkeypatch.setattr(description_service, "Image", types.SimpleNamespace(open=lambda x: x))
    desc = description_service.generate_description("fake.jpg", model_name="blip2", lang="en")
    assert "Mocked" in desc

def test_janus_mock(monkeypatch):
    # 仅在Janus依赖可用时测试
    if not getattr(description_service, "JANUS_AVAILABLE", False):
        return
    monkeypatch.setattr(description_service, "VLChatProcessor", lambda *a, **k: dummy_processor())
    monkeypatch.setattr(description_service, "AutoModelForCausalLM", lambda *a, **k: DummyModel())
    monkeypatch.setattr(description_service, "torch", types.SimpleNamespace(device=lambda x: None, bfloat16=None))
    monkeypatch.setattr(description_service, "Image", types.SimpleNamespace(open=lambda x: x))
    desc = description_service.generate_description("fake.jpg", model_name="janus", lang="zh")
    assert "Mocked" in desc 