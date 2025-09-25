#!/usr/bin/env python3
"""
简化版DeepSeek工具调用示例
快速演示基本的工具调用功能
"""

import json
import requests
import os
from datetime import datetime


def get_weather(location: str) -> dict:
    """模拟天气查询工具"""
    return {
        "location": location,
        "temperature": "22°C",
        "condition": "晴朗",
        "humidity": "65%",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def calculate(expression: str) -> dict:
    """安全的数学计算工具"""
    try:
        # 简单的安全检查
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return {"error": "表达式包含不允许的字符"}
        
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def deepseek_tool_call(message: str, api_key: str):
    """
    调用DeepSeek API进行工具调用
    
    Args:
        message: 用户消息
        api_key: DeepSeek API密钥
    """
    
    # 定义可用工具
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "地点名称"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "计算数学表达式",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "数学表达式"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ]
    
    # 构建请求
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": message}],
        "tools": tools,
        "tool_choice": "auto"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 发送请求
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        
        # 检查是否有工具调用
        if "choices" in result and len(result["choices"]) > 0:
            choice = result["choices"][0]
            message_obj = choice.get("message", {})
            
            if "tool_calls" in message_obj:
                print("🔧 AI助手调用了以下工具:")
                
                for tool_call in message_obj["tool_calls"]:
                    function = tool_call.get("function", {})
                    tool_name = function.get("name")
                    arguments = json.loads(function.get("arguments", "{}"))
                    
                    print(f"   工具: {tool_name}")
                    print(f"   参数: {arguments}")
                    
                    # 执行工具
                    if tool_name == "get_weather":
                        tool_result = get_weather(**arguments)
                    elif tool_name == "calculate":
                        tool_result = calculate(**arguments)
                    else:
                        tool_result = {"error": f"未知工具: {tool_name}"}
                    
                    print(f"   结果: {json.dumps(tool_result, ensure_ascii=False)}")
                    print()
            else:
                # 没有工具调用，显示普通回复
                content = message_obj.get("content", "")
                if content:
                    print(f"💬 AI助手: {content}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API请求失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return None


def main():
    """主函数"""
    print("=== 简化版DeepSeek工具调用示例 ===\n")
    
    # 获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 请设置环境变量 DEEPSEEK_API_KEY")
        print("   例如: export DEEPSEEK_API_KEY='your-api-key-here'")
        return
    
    # 预设示例
    examples = [
        "北京今天的天气怎么样？",
        "帮我计算 15 + 25 * 3",
        "上海的天气如何？",
        "计算 (100 - 20) / 4"
    ]
    
    print("📝 预设示例:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    print()
    
    # 交互式模式
    print("💬 交互式模式 (输入数字选择示例，或直接输入问题，'quit'退出):")
    
    while True:
        try:
            user_input = input("\n👤 用户: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见!")
                break
            
            if not user_input:
                continue
            
            # 检查是否是数字选择
            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(examples):
                    user_input = examples[index]
                    print(f"   选择示例: {user_input}")
                else:
                    print("❌ 无效的示例编号")
                    continue
            
            # 调用DeepSeek API
            print("🤖 正在处理...")
            deepseek_tool_call(user_input, api_key)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
