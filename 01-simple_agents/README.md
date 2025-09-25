# DeepSeek工具调用示例

这个项目演示了如何使用DeepSeek API进行工具调用（Function Calling）。

## 功能特性

- 🌤️ **天气查询**: 获取指定地点的天气信息
- 🧮 **数学计算**: 计算数学表达式
- 🔍 **网络搜索**: 模拟网络搜索功能
- 💬 **交互式对话**: 支持实时对话和工具调用

## 安装依赖

```bash
# 使用UV安装依赖
uv sync
```

## 配置API密钥

1. 获取DeepSeek API密钥：访问 [DeepSeek官网](https://platform.deepseek.com/) 注册并获取API密钥

2. 设置环境变量：
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

或者创建 `.env` 文件：
```
DEEPSEEK_API_KEY=your-api-key-here
```

## 使用方法

### 运行示例

```bash
# 运行完整示例
uv run deepseek_tool_calling_example.py

# 运行简化示例
uv run simple_deepseek_example.py
```

### 代码示例

```python
from deepseek_tool_calling_example import DeepSeekToolCaller

# 初始化客户端
client = DeepSeekToolCaller(api_key="your-api-key")

# 进行工具调用对话
result = client.chat_with_tools("北京今天的天气怎么样？")
print(result)
```

## 支持的工具

### 1. 天气查询 (get_weather)
- **功能**: 获取指定地点的天气信息
- **参数**: 
  - `location` (必需): 地点名称
  - `unit` (可选): 温度单位 (celsius/fahrenheit)

### 2. 数学计算 (calculate)
- **功能**: 计算数学表达式
- **参数**:
  - `expression` (必需): 数学表达式

### 3. 网络搜索 (search_web)
- **功能**: 搜索网络信息
- **参数**:
  - `query` (必需): 搜索查询词
  - `num_results` (可选): 返回结果数量

## 示例对话

```
用户: 北京今天的天气怎么样？
AI助手调用了以下工具:
- get_weather: {'location': '北京', 'unit': 'celsius'}
  结果: {"location": "北京", "temperature": 22, "condition": "晴朗"}

用户: 帮我计算 (25 + 15) * 3 - 10
AI助手调用了以下工具:
- calculate: {'expression': '(25 + 15) * 3 - 10'}
  结果: {"expression": "(25 + 15) * 3 - 10", "result": 110, "success": true}
```

## 自定义工具

要添加新的工具，需要：

1. 在 `DeepSeekToolCaller` 类中添加工具函数
2. 在 `get_available_tools()` 方法中添加工具定义
3. 在 `execute_tool()` 方法中添加工具执行逻辑

### 示例：添加时间工具

```python
def get_current_time(self, timezone: str = "UTC") -> Dict[str, Any]:
    """获取当前时间"""
    from datetime import datetime
    import pytz
    
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    
    return {
        "timezone": timezone,
        "current_time": current_time.isoformat(),
        "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }
```

## 注意事项

1. **API密钥安全**: 不要在代码中硬编码API密钥，使用环境变量
2. **错误处理**: 示例包含了完整的错误处理机制
3. **工具安全**: 数学计算工具包含了安全检查，防止恶意代码执行
4. **模拟数据**: 天气和搜索功能使用模拟数据，实际使用时需要接入真实API

## 添加依赖

```bash
# 添加新依赖
uv add package-name

# 移除依赖
uv remove package-name
```

## 扩展功能

- 添加更多实用工具（文件操作、数据库查询等）
- 实现工具调用的历史记录
- 添加工具调用的权限控制
- 支持异步工具调用

## 许可证

MIT License
