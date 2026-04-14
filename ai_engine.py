"""AI引擎模块 - 提供智能对话能力"""
import json
from typing import List, Dict, Optional
from config import Config

# 尝试导入openai，如果失败则使用模拟模式
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIEngine:
    """AI引擎类，处理与大模型的交互"""
    
    def __init__(self):
        self.config = Config
        self.client = None
        self.is_mock_mode = not Config.validate() or not OPENAI_AVAILABLE
        
        if not self.is_mock_mode:
            try:
                self.client = OpenAI(
                    api_key=self.config.OPENAI_API_KEY,
                    base_url=self.config.OPENAI_BASE_URL
                )
                print("✓ AI引擎初始化成功（真实API模式）")
            except Exception as e:
                print(f"⚠️  AI引擎初始化失败: {e}，切换到模拟模式")
                self.is_mock_mode = True
        else:
            print("✓ AI引擎初始化成功（模拟模式）")
    
    def chat(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表，格式为 [{"role": "user/assistant", "content": "消息内容"}]
            system_prompt: 系统提示词
            
        Returns:
            AI回复内容
        """
        if self.is_mock_mode:
            return self._mock_response(messages, system_prompt)
        
        try:
            # 构建完整的消息列表
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=full_messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            error_msg = f"AI调用失败: {str(e)}"
            print(f"⚠️  {error_msg}")
            return f"抱歉，我遇到了一些问题：{error_msg}"
    
    def chat_stream(self, messages: List[Dict[str, str]], system_prompt: str = ""):
        """
        发送流式聊天请求
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            
        Yields:
            流式输出的文本片段
        """
        if self.is_mock_mode:
            # 模拟模式下，逐字输出
            response = self._mock_response(messages, system_prompt)
            for char in response:
                yield char
            return
        
        try:
            # 构建完整的消息列表
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)
            
            # 调用OpenAI API流式接口
            stream = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=full_messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            error_msg = f"AI调用失败: {str(e)}"
            print(f"⚠️  {error_msg}")
            yield f"抱歉，我遇到了一些问题：{error_msg}"
    
    def _mock_response(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        """
        模拟AI回复（用于演示和测试）- 优化版，更直接回答问题
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            
        Returns:
            模拟的回复内容
        """
        if not messages:
            return "你好！我是你的办公协同智能助手，有什么可以帮助你的吗？"
        
        last_message = messages[-1].get("content", "").lower()
        
        # 更精准的意图识别和回复
        # 查看会议相关
        if any(phrase in last_message for phrase in ["有哪些会议", "查看会议", "我的会议", "今天的会议", "会议安排"]):
            return self._mock_list_meetings()
        elif any(word in last_message for word in ["安排会议", "创建会议", "预约会议"]):
            return self._mock_create_meeting(last_message)
        elif any(word in last_message for word in ["取消会议", "删除会议"]):
            return "要取消会议，请在会议管理页面找到对应会议，点击'取消会议'按钮即可。或者告诉我会议ID，我可以帮你取消。"
        
        # 任务相关
        elif any(phrase in last_message for phrase in ["有哪些任务", "查看任务", "我的任务", "待办任务", "任务列表"]):
            return self._mock_list_tasks()
        elif any(word in last_message for word in ["创建任务", "新增任务", "添加任务"]):
            return self._mock_create_task(last_message)
        elif any(word in last_message for word in ["完成任务", "标记完成"]):
            return "要标记任务完成，请在任务管理页面找到对应任务，点击'标记完成'按钮即可。或者告诉我任务ID，我可以帮你标记。"
        
        # 文档相关
        elif any(phrase in last_message for phrase in ["搜索文档", "查找文档", "文档检索"]):
            return self._mock_search_documents(last_message)
        elif any(phrase in last_message for phrase in ["有哪些文档", "查看所有文档", "文档列表"]):
            return self._mock_list_documents()
        
        # 问候语
        elif any(word in last_message for word in ["你好", "hi", "hello", "您好"]):
            return "你好！很高兴为你服务。我是你的办公协同智能助手，可以帮你：\n\n• 📅 管理会议安排\n• ✅ 跟踪任务进度\n• 📄 检索云文档\n• 💬 回答办公问题\n\n请问有什么需要帮助的吗？"
        
        elif any(word in last_message for word in ["谢谢", "感谢", "thanks"]):
            return "不客气！如果还有其他问题，随时告诉我。😊"
        
        # 帮助信息
        elif any(word in last_message for word in ["帮助", "help", "怎么用", "如何使用"]):
            return self._mock_help()
        
        else:
            return self._mock_general_response(last_message)
    
    def _mock_list_meetings(self) -> str:
        """模拟查看会议列表"""
        return """📅 您的会议安排如下：

• 产品周会
  时间：今天下午 16:00 (60分钟)
  地点：会议室A
  参会人：张三、李四、王五
  状态：已确认

• 技术评审会议
  时间：明天上午 10:00 (90分钟)
  地点：会议室B
  参会人：赵六、钱七
  状态：待确认

💡 提示：您可以在“会议管理”页面查看更多详情或取消会议。"""
    
    def _mock_create_meeting(self, query: str) -> str:
        """模拟创建会议"""
        return """✅ 好的，我来帮您安排会议。

请提供以下信息：
• 会议标题：例如“项目评审会议”
• 会议时间：例如“明天下午3点”
• 参会人员：例如“张三、李四、王五”
• 会议时长：默认60分钟
• 会议地点：例如“会议室A”

或者您可以直接在“会议管理”页面点击“+ 新建会议”按钮填写表单创建。"""
    
    def _mock_list_tasks(self) -> str:
        """模拟查看任务列表"""
        return """✅ 您的任务列表如下：

🔴 高优先级：
• 完成项目需求文档
  截止日期：2024-04-16 | 状态：进行中

🟡 中优先级：
• 代码审查
  截止日期：2024-04-15 | 状态：待开始

🟢 低优先级：
• 更新用户手册
  截止日期：2024-04-19 | 状态：已完成

💡 提示：您可以在“任务管理”页面筛选不同状态的任务，或标记任务为完成。"""
    
    def _mock_create_task(self, query: str) -> str:
        """模拟创建任务"""
        return """✅ 好的，我来帮您创建任务。

请提供以下信息：
• 任务标题：例如“完成项目报告”
• 截止日期：例如“本周五”
• 优先级：高/中/低
• 任务描述：（可选）

或者您可以直接在“任务管理”页面点击“+ 新建任务”按钮填写表单创建。"""
    
    def _mock_search_documents(self, query: str) -> str:
        """模拟搜索文档"""
        keyword = query.replace("搜索", "").replace("查找", "").strip()
        if keyword:
            return f"""🔍 搜索关键词：“{keyword}”

找到以下相关文档：

📝 Q2产品规划文档
   • 作者：张三 | 更新：2024-04-10
   • 摘要：包含Q2产品路线图、功能规划和资源分配计划
   • 标签：产品、规划、Q2

💡 提示：您可以在“文档检索”页面输入关键词进行搜索，或点击“显示全部”查看所有文档。"""
        else:
            return """🔍 请输入要搜索的关键词。

例如：
• “搜索产品规划文档”
• “查找技术架构设计”
• “搜索会议纪要”

或者在“文档检索”页面的搜索框中输入关键词进行搜索。"""
    
    def _mock_list_documents(self) -> str:
        """模拟列出所有文档"""
        return """📄 所有文档列表：

• Q2产品规划文档
  作者：张三 | 更新：2024-04-10
  标签：产品、规划、Q2

• 技术架构设计文档
  作者：李四 | 更新：2024-04-08
  标签：技术、架构、设计

• 用户增长数据分析报告
  作者：王五 | 更新：2024-04-12
  标签：数据、分析、用户增长

• 项目周会纪要 - 第15周
  作者：赵六 | 更新：2024-04-13
  标签：会议、纪要、周报

💡 提示：您可以在“文档检索”页面查看更多详情或搜索特定文档。"""
    
    def _mock_help(self) -> str:
        """模拟帮助信息"""
        return """📖 使用帮助

我可以帮您：

📅 会议管理
• “我有哪些会议” - 查看会议列表
• “安排一个会议” - 创建新会议
• “取消会议” - 取消指定会议

✅ 任务管理
• “我有哪些任务” - 查看任务列表
• “创建一个任务” - 创建新任务
• “完成任务” - 标记任务为完成

📄 文档检索
• “搜索文档” - 搜索特定文档
• “查看所有文档” - 列出所有文档

💬 其他
• “你好” - 打招呼
• “帮助” - 显示此帮助信息
• “谢谢” - 表达感谢

您也可以直接使用界面上的按钮和表单来操作！"""
    
    def _mock_general_response(self, query: str) -> str:
        """通用回复 - 更直接地引导用户"""
        return f"""我理解您想了解关于“{query[:30]}”的信息。

作为办公协同智能助手，我可以帮您：

📅 管理会议 - 例如：“我有哪些会议”、“安排一个会议”
✅ 管理任务 - 例如：“我有哪些任务”、“创建一个任务”
📄 检索文档 - 例如：“搜索产品文档”、“查看所有文档”

请问您需要哪方面的帮助？或者试试上面的示例命令。😊"""
    
    def extract_intent(self, message: str) -> Dict[str, any]:
        """
        提取用户意图（简化版）
        
        Args:
            message: 用户消息
            
        Returns:
            意图识别结果
        """
        message_lower = message.lower()
        
        intent = {
            "type": "general",
            "confidence": 0.5,
            "entities": {}
        }
        
        # 简单的意图分类
        if any(word in message_lower for word in ["会议", "安排", "预约", "日程"]):
            intent["type"] = "meeting"
            intent["confidence"] = 0.8
        elif any(word in message_lower for word in ["任务", "待办", "todo", "工作"]):
            intent["type"] = "task"
            intent["confidence"] = 0.8
        elif any(word in message_lower for word in ["文档", "文件", "搜索", "查找"]):
            intent["type"] = "document"
            intent["confidence"] = 0.8
        elif any(word in message_lower for word in ["你好", "hi", "hello", "_help"]):
            intent["type"] = "greeting"
            intent["confidence"] = 0.9
        
        return intent
