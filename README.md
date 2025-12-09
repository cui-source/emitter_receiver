ComfyUI 广播信号节点 (emitter_receiver)
概述
广播信号节点是一套用于在 ComfyUI 工作流中实现跨节点数据通信的自定义节点。这套节点通过全局频道机制，允许在不直接连接的情况下在不同节点之间传递数据，特别适合需要将同一参数传递给多个节点的场景。

功能特点
跨节点数据传递：无需物理连接即可传递数据

全局频道机制：通过频道ID（channel_id）识别不同的数据流

多种数据类型支持：整数、浮点数、字符串

实时性保证：数据带有时间戳，确保接收最新数据

容错机制：提供默认值，防止数据丢失

完全无缓存：每次执行都重新计算，确保数据同步

节点列表
发射器节点 (Emitters)
节点名称	功能	输入参数	输出
📤 Int Emitter	发射整数数据	id (频道ID), value (整数值)	无
📤 Float Emitter	发射浮点数数据	id (频道ID), value (浮点值)	无
📤 String Emitter	发射字符串数据	id (频道ID), value (字符串值)	无
接收器节点 (Receivers)
节点名称	功能	输入参数	输出
📥 Int Receiver	接收整数数据	id (频道ID)	整数
📥 Float Receiver	接收浮点数数据	id (频道ID)	浮点数
📥 String Receiver	接收字符串数据	id (频道ID)	字符串
安装方法
将节点文件夹放置在 ComfyUI 的 custom_nodes 目录下

重启 ComfyUI 服务

在节点菜单中找到 "Emitter-Receiver" 分类

使用方法
基本用法
放置发射器节点

从节点菜单选择需要的发射器类型

设置 id 参数（如："sampling_steps"）

设置 value 参数（如：25）

放置接收器节点

从节点菜单选择对应的接收器类型

设置相同的 id 参数（如："sampling_steps"）

运行工作流

发射器会将数据广播到指定频道

所有相同频道的接收器会接收到数据

工作流示例
text
[Int Emitter]           [KSampler]
    id: "steps"           ↓
    value: 20         [Int Receiver]
                          id: "steps"
                          → 接收到值: 20
多接收器示例
text
[Int Emitter]
    id: "steps"
    value: 25
    ↓
[KSampler 1] ← [Int Receiver] ← id: "steps" → [Int Receiver] → [KSampler 2]
                                    ↓
                               [Int Receiver] → [KSampler 3]
参数说明
发射器参数
id (字符串): 频道标识符，用于匹配发射器和接收器

value (对应类型): 要广播的数据值

接收器参数
id (字符串): 频道标识符，必须与发射器相同

默认值处理: 如果在100毫秒内没有收到数据，返回默认值

技术原理
数据流机制
全局存储: 使用全局字典 _emitter_data 存储所有频道数据

时间戳同步: 每个数据带有时间戳，确保数据新鲜度

强制重计算: 所有节点都实现 IS_CHANGED 方法，强制每次重新执行

代码结构
python
# 全局数据存储结构
_emitter_data = {
    "channel_1": {
        "type": "int",
        "value": 25,
        "timestamp": 1640995200.123456
    },
    "channel_2": {
        "type": "float",
        "value": 0.5,
        "timestamp": 1640995200.234567
    }
}
高级用法
动态参数控制
python
# 在工作流中动态改变参数
[Text Input] → [String Emitter] → 广播到多个节点
            ↓
        [Conditional Node] → 根据内容选择不同路径
工作流状态同步
python
# 同步多个节点的状态
[Int Emitter: "seed"] → [多个需要相同种子的节点]
常见问题
Q1: 接收器收不到数据怎么办？
A: 检查以下事项：

发射器和接收器的 id 参数是否完全一致

工作流是否完整执行（发射器必须先于接收器执行）

查看控制台输出是否有错误信息

Q2: 数据更新不及时怎么办？
A: 本节点使用100毫秒的数据有效期，如果工作流执行间隔超过这个时间，可能需要：

调整工作流结构，让相关节点更接近

修改代码中的时间阈值（0.1秒）

Q3: 是否支持复杂数据类型？
A: 目前支持整数、浮点数、字符串三种基本类型。如果需要更复杂的数据结构，可以扩展节点类。

调试技巧
查看日志输出
每个节点都会在控制台输出操作日志：

text
[IntEmitter] Emitted id=sampling_steps, value=25
[IntReceiver] Received id=sampling_steps, value=25
验证数据流
添加多个接收器到同一频道

检查所有接收器是否收到相同数据

修改发射器值，确认所有接收器同步更新

扩展开发
添加新数据类型
要添加新的数据类型（如布尔值、列表等），可以按照以下模板：

python
class BoolEmitter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"default": ""}),
                "value": ("BOOLEAN", {"default": False}),
            }
        }
    
    def emit(self, id, value):
        _emitter_data[id] = {
            "type": "bool",
            "value": value,
            "timestamp": time.time()
        }
        return ()
修改数据有效期
在接收器的 receive 方法中调整时间阈值：

python
# 修改为500毫秒有效期
if current_time - data["timestamp"] < 0.5:
    return data["value"]
性能注意事项
全局变量：数据存储在全局字典中，不会在重启后保留

内存管理：长时间运行可能积累大量数据，建议定期清理

执行顺序：确保发射器在接收器之前执行

版本信息
当前版本: 1.0.0

兼容性: ComfyUI 1.0+

依赖: 无需额外依赖

更新日志
v1.0.0 (初始版本)
实现整数、浮点数、字符串的广播功能

添加时间戳机制确保数据新鲜度

完整的发射器/接收器配对

联系支持
如有问题或建议，请通过以下方式联系：

提交GitHub Issue

在ComfyUI社区论坛发帖
