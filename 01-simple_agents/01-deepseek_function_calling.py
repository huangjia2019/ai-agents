#!/usr/bin/env python3
"""
DeepSeek工具调用示例
演示如何使用DeepSeek API进行工具调用（Function Calling）
"""

import json
import requests
from typing import Dict, List, Any, Optional
import os
from datetime import datetime


class DeepSeekToolCaller:
    """DeepSeek工具调用客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        """
        初始化DeepSeek客户端
        
        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_weather(self, location: str, unit: str = "celsius") -> Dict[str, Any]:
        """
        获取天气信息的工具函数
        
        Args:
            location: 地点
            unit: 温度单位 (celsius/fahrenheit)
            
        Returns:
            天气信息字典
        """
        # 模拟天气API调用
        weather_data = {
            "location": location,
            "temperature": 22 if unit == "celsius" else 72,
            "unit": unit,
            "condition": "晴朗",
            "humidity": "65%",
            "wind_speed": "10 km/h",
            "timestamp": datetime.now().isoformat()
        }
        return weather_data
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        计算数学表达式的工具函数
        
        Args:
            expression: 数学表达式
            
        Returns:
            计算结果
        """
        try:
            # 安全的数学表达式计算
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("表达式包含不允许的字符")
            
            result = eval(expression)
            return {
                "expression": expression,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "expression": expression,
                "error": str(e),
                "success": False
            }
    
    def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        模拟网络搜索的工具函数
        
        Args:
            query: 搜索查询
            num_results: 返回结果数量
            
        Returns:
            搜索结果
        """
        # 模拟搜索结果
        results = []
        for i in range(min(num_results, 3)):
            results.append({
                "title": f"关于'{query}'的搜索结果 {i+1}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"这是关于{query}的详细信息..."
            })
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results)
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取可用工具的定义
        
        Returns:
            工具定义列表
        """
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定地点的天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "地点名称，例如：北京、上海"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "温度单位",
                                "default": "celsius"
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
                                "description": "要计算的数学表达式，例如：2+3*4"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "搜索网络信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索查询词"
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "返回结果数量",
                                "default": 5,
                                "minimum": 1,
                                "maximum": 10
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
        return tools
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具函数
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            工具执行结果
        """
        if tool_name == "get_weather":
            return self.get_weather(**arguments)
        elif tool_name == "calculate":
            return self.calculate(**arguments)
        elif tool_name == "search_web":
            return self.search_web(**arguments)
        else:
            return {"error": f"未知的工具: {tool_name}"}
    
    def chat_with_tools(self, message: str, model: str = "deepseek-chat") -> Dict[str, Any]:
        """
        使用工具进行对话
        
        Args:
            message: 用户消息
            model: 使用的模型
            
        Returns:
            对话结果
        """
        tools = self.get_available_tools()
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "tools": tools,
            "tool_choice": "auto"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 处理工具调用
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                message = choice.get("message", {})
                
                if "tool_calls" in message:
                    tool_results = []
                    for tool_call in message["tool_calls"]:
                        function = tool_call.get("function", {})
                        tool_name = function.get("name")
                        arguments = json.loads(function.get("arguments", "{}"))
                        
                        # 执行工具
                        tool_result = self.execute_tool(tool_name, arguments)
                        tool_results.append({
                            "tool_call_id": tool_call.get("id"),
                            "tool_name": tool_name,
                            "arguments": arguments,
                            "result": tool_result
                        })
                    
                    result["tool_results"] = tool_results
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API请求失败: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON解析失败: {str(e)}"}
        except Exception as e:
            return {"error": f"未知错误: {str(e)}"}


def main():
    """主函数 - 演示DeepSeek工具调用"""
    
    # 从环境变量获取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("请设置环境变量 DEEPSEEK_API_KEY")
        print("例如: export DEEPSEEK_API_KEY='your-api-key-here'")
        return
    
    # 创建DeepSeek客户端
    client = DeepSeekToolCaller(api_key)
    
    print("=== DeepSeek工具调用示例 ===\n")
    
    # 示例1: 天气查询
    print("1. 天气查询示例:")
    weather_query = "北京今天的天气怎么样？"
    print(f"用户: {weather_query}")
    
    result = client.chat_with_tools(weather_query)
    if "tool_results" in result:
        for tool_result in result["tool_results"]:
            print(f"工具调用: {tool_result['tool_name']}")
            print(f"参数: {tool_result['arguments']}")
            print(f"结果: {json.dumps(tool_result['result'], ensure_ascii=False, indent=2)}")
    print()
    
    # 示例2: 数学计算
    print("2. 数学计算示例:")
    calc_query = "帮我计算 (25 + 15) * 3 - 10"
    print(f"用户: {calc_query}")
    
    result = client.chat_with_tools(calc_query)
    if "tool_results" in result:
        for tool_result in result["tool_results"]:
            print(f"工具调用: {tool_result['tool_name']}")
            print(f"参数: {tool_result['arguments']}")
            print(f"结果: {json.dumps(tool_result['result'], ensure_ascii=False, indent=2)}")
    print()
    
    # 示例3: 网络搜索
    print("3. 网络搜索示例:")
    search_query = "搜索关于人工智能的最新信息"
    print(f"用户: {search_query}")
    
    result = client.chat_with_tools(search_query)
    if "tool_results" in result:
        for tool_result in result["tool_results"]:
            print(f"工具调用: {tool_result['tool_name']}")
            print(f"参数: {tool_result['arguments']}")
            print(f"结果: {json.dumps(tool_result['result'], ensure_ascii=False, indent=2)}")
    print()
    
    # 交互式模式
    print("4. 交互式模式 (输入 'quit' 退出):")
    while True:
        try:
            user_input = input("\n用户: ").strip()
            if user_input.lower() in ['quit', 'exit', '退出']:
                break
            
            if not user_input:
                continue
            
            result = client.chat_with_tools(user_input)
            
            if "error" in result:
                print(f"错误: {result['error']}")
            elif "tool_results" in result:
                print("AI助手调用了以下工具:")
                for tool_result in result["tool_results"]:
                    print(f"- {tool_result['tool_name']}: {tool_result['arguments']}")
                    print(f"  结果: {json.dumps(tool_result['result'], ensure_ascii=False)}")
            else:
                print("AI助手: 没有需要调用的工具")
                
        except KeyboardInterrupt:
            print("\n\n再见!")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    main()
