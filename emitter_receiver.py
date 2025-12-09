import time
import json
from collections import defaultdict

# 全局数据存储 {id: {"type": type, "value": value, "timestamp": timestamp}}
_emitter_data = defaultdict(dict)
_last_updated = 0

class IntEmitter:
    """整数发射器节点"""
    CATEGORY = "Emitter-Receiver"
    FUNCTION = "emit"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "unique_id"}),
                "value": ("INT", {"default": 0}),
            }
        }
    
    def emit(self, id, value):
        global _last_updated
        _last_updated = time.time()
        _emitter_data[id] = {
            "type": "int",
            "value": value,
            "timestamp": _last_updated
        }
        print(f"[IntEmitter] Emitted id={id}, value={value}")
        return ()
    
    @classmethod
    def IS_CHANGED(cls, id, value):
        # 强制节点每次都重新计算
        return float(time.time())

class FloatEmitter:
    """浮点数发射器节点"""
    CATEGORY = "Emitter-Receiver"
    FUNCTION = "emit"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "unique_id"}),
                "value": ("FLOAT", {"default": 0.0}),
            }
        }
    
    def emit(self, id, value):
        global _last_updated
        _last_updated = time.time()
        _emitter_data[id] = {
            "type": "float",
            "value": value,
            "timestamp": _last_updated
        }
        print(f"[FloatEmitter] Emitted id={id}, value={value}")
        return ()
    
    @classmethod
    def IS_CHANGED(cls, id, value):
        return float(time.time())

class StringEmitter:
    """字符串发射器节点"""
    CATEGORY = "Emitter-Receiver"
    FUNCTION = "emit"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "unique_id"}),
                "value": ("STRING", {"default": ""}),
            }
        }
    
    def emit(self, id, value):
        global _last_updated
        _last_updated = time.time()
        _emitter_data[id] = {
            "type": "string",
            "value": value,
            "timestamp": _last_updated
        }
        print(f"[StringEmitter] Emitted id={id}, value={value}")
        return ()
    
    @classmethod
    def IS_CHANGED(cls, id, value):
        return float(time.time())

class IntReceiver:
    """整数接收器节点"""
    CATEGORY = "Emitter-Receiver"
    FUNCTION = "receive"
    RETURN_TYPES = ("INT",)
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "unique_id"}),
            }
        }
    
    def receive(self, id):
        global _emitter_data, _last_updated
        
        # 获取当前时间戳
        current_time = time.time()
        
        # 检查是否有有效数据
        if id in _emitter_data:
            data = _emitter_data[id]
            # 检查数据是否过期（超过100毫秒）
            if current_time - data["timestamp"] < 0.1:
                print(f"[IntReceiver] Received id={id}, value={data['value']}")
                return (int(data["value"]),)
        
        # 没有有效数据时返回默认值
        print(f"[IntReceiver] No valid data for id={id}, returning 0")
        return (0,)
    
    @classmethod
    def IS_CHANGED(cls, id):
        # 强制节点每次都重新计算
        return float(time.time())

class FloatReceiver:
    """浮点数接收器节点"""
    CATEGORY = "Emitter-Receiver"
    FUNCTION = "receive"
    RETURN_TYPES = ("FLOAT",)
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "unique_id"}),
            }
        }
    
    def receive(self, id):
        global _emitter_data, _last_updated
        
        current_time = time.time()
        
        if id in _emitter_data:
            data = _emitter_data[id]
            if current_time - data["timestamp"] < 0.1:
                print(f"[FloatReceiver] Received id={id}, value={data['value']}")
                return (float(data["value"]),)
        
        print(f"[FloatReceiver] No valid data for id={id}, returning 0.0")
        return (0.0,)
    
    @classmethod
    def IS_CHANGED(cls, id):
        return float(time.time())

class StringReceiver:
    """字符串接收器节点"""
    CATEGORY = "Emitter-Receiver"
    FUNCTION = "receive"
    RETURN_TYPES = ("STRING",)
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": "unique_id"}),
            }
        }
    
    def receive(self, id):
        global _emitter_data, _last_updated
        
        current_time = time.time()
        
        if id in _emitter_data:
            data = _emitter_data[id]
            if current_time - data["timestamp"] < 0.1:
                print(f"[StringReceiver] Received id={id}, value={data['value']}")
                return (str(data["value"]),)
        
        print(f"[StringReceiver] No valid data for id={id}, returning empty string")
        return ("",)
    
    @classmethod
    def IS_CHANGED(cls, id):
        return float(time.time())

# 节点映射
NODE_CLASS_MAPPINGS = {
    "Int Emitter": IntEmitter,
    "Float Emitter": FloatEmitter,
    "String Emitter": StringEmitter,
    "Int Receiver": IntReceiver,
    "Float Receiver": FloatReceiver,
    "String Receiver": StringReceiver
}

# 节点显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "Int Emitter": "📤 Int Emitter",
    "Float Emitter": "📤 Float Emitter",
    "String Emitter": "📤 String Emitter",
    "Int Receiver": "📥 Int Receiver",
    "Float Receiver": "📥 Float Receiver",
    "String Receiver": "📥 String Receiver"
}