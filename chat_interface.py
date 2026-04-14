"""命令行交互界面 - 提供友好的用户交互体验"""
import sys
from colorama import init, Fore, Style
from ai_engine import AIEngine
from office_assistant import OfficeAssistant
from config import Config

# 初始化colorama
init(autoreset=True)


class ChatInterface:
    """聊天界面类"""
    
    def __init__(self):
        self.ai_engine = AIEngine()
        self.assistant = OfficeAssistant()
        self.conversation_history = []
        self.is_running = True
        
        # 系统提示词
        self.system_prompt = """你是一个专业的办公协同智能助手，集成在飞书IM中。你的职责是：

1. 帮助用户安排和管理会议
2. 协助用户创建和跟踪任务
3. 帮助用户搜索和管理文档
4. 回答办公相关的常见问题

请用友好、专业的语气与用户交流。如果用户的问题涉及会议、任务或文档，可以调用相应的功能模块来帮助用户。"""
    
    def display_welcome(self):
        """显示欢迎信息"""
        print("\n" + "="*60)
        print(Fore.CYAN + Style.BRIGHT + "🚀 飞书AI办公协同智能助手")
        print("="*60)
        
        config_summary = Config.get_config_summary()
        print(Fore.YELLOW + f"\n应用: {config_summary['应用名称']} v{config_summary['版本']}")
        print(Fore.YELLOW + f"模型: {config_summary['模型']}")
        
        if config_summary['API已配置']:
            print(Fore.GREEN + "状态: ✓ 真实API模式")
        else:
            print(Fore.YELLOW + "状态: ⚠ 模拟模式（演示用）")
        
        print("\n" + Fore.CYAN + "💡 我可以帮你:")
        print(Fore.WHITE + "  • 📅 安排和管理会议")
        print(Fore.WHITE + "  • ✅ 创建和跟踪任务")
        print(Fore.WHITE + "  • 📄 搜索和管理文档")
        print(Fore.WHITE + "  • 💬 回答办公相关问题")
        
        print("\n" + Fore.CYAN + "📝 示例命令:")
        print(Fore.WHITE + '  • "明天下午3点安排项目评审会议"')
        print(Fore.WHITE + '  • "创建一个任务：完成报告，截止日期本周五"')
        print(Fore.WHITE + '  • "搜索关于产品规划的文档"')
        print(Fore.WHITE + '  • "查看我的会议安排"')
        
        print("\n" + Fore.YELLOW + "输入 'help' 查看更多帮助 | 输入 'quit' 或 'exit' 退出")
        print("="*60 + "\n")
    
    def display_help(self):
        """显示帮助信息"""
        print("\n" + Fore.CYAN + Style.BRIGHT + "📖 帮助文档")
        print("="*60)
        
        print(Fore.YELLOW + "\n【会议管理】")
        print(Fore.WHITE + '  • 安排会议："明天下午3点安排项目会议，参会人员：张三、李四"')
        print(Fore.WHITE + '  • 查看会议："查看我的会议" 或 "查看今天的会议"')
        print(Fore.WHITE + '  • 取消会议："取消会议1"')
        
        print(Fore.YELLOW + "\n【任务管理】")
        print(Fore.WHITE + '  • 创建任务："创建任务：完成报告，截止日期本周五，优先级高"')
        print(Fore.WHITE + '  • 查看任务："查看我的任务" 或 "查看待办任务"')
        print(Fore.WHITE + '  • 完成任务："完成任务1"')
        
        print(Fore.YELLOW + "\n【文档管理】")
        print(Fore.WHITE + '  • 搜索文档："搜索产品规划文档"')
        print(Fore.WHITE + '  • 查看所有文档："列出所有文档"')
        
        print(Fore.YELLOW + "\n【其他命令】")
        print(Fore.WHITE + "  • help - 显示此帮助信息")
        print(Fore.WHITE + "  • quit/exit - 退出程序")
        print(Fore.WHITE + "  • clear - 清空对话历史")
        
        print("\n" + "="*60 + "\n")
    
    def process_command(self, user_input: str) -> str:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入
            
        Returns:
            回复内容
        """
        user_input_lower = user_input.lower().strip()
        
        # 特殊命令处理
        if user_input_lower in ["quit", "exit", "q"]:
            self.is_running = False
            return Fore.YELLOW + "感谢使用，再见！👋"
        
        elif user_input_lower in ["help", "h", "?"]:
            self.display_help()
            return ""
        
        elif user_input_lower in ["clear", "cls"]:
            self.conversation_history.clear()
            return Fore.GREEN + "✓ 对话历史已清空"
        
        # 意图识别
        intent = self.ai_engine.extract_intent(user_input)
        
        # 根据意图分发到不同处理器
        if intent["type"] == "meeting":
            return self._handle_meeting_intent(user_input, intent)
        elif intent["type"] == "task":
            return self._handle_task_intent(user_input, intent)
        elif intent["type"] == "document":
            return self._handle_document_intent(user_input, intent)
        elif intent["type"] == "greeting":
            # 问候语直接使用AI引擎
            pass
        
        # 通用对话 - 使用AI引擎
        return self._handle_general_chat(user_input)
    
    def _handle_meeting_intent(self, user_input: str, intent: dict) -> str:
        """处理会议相关意图"""
        user_input_lower = user_input.lower()
        
        # 简单的命令解析
        if any(word in user_input_lower for word in ["查看", "列表", "我的"]):
            return self.assistant.handle_meeting_command("list", {})
        
        elif any(word in user_input_lower for word in ["取消", "删除"]):
            # 提取会议ID（简化版）
            import re
            match = re.search(r'会议\s*(\d+)', user_input)
            if match:
                meeting_id = int(match.group(1))
                return self.assistant.handle_meeting_command("cancel", {"meeting_id": meeting_id})
            return "❌ 请指定要取消的会议ID，例如：取消会议1"
        
        elif any(word in user_input_lower for word in ["安排", "创建", "预约"]):
            # 这里应该用AI提取参数，简化版直接返回提示
            return (Fore.YELLOW + '📅 我检测到你想安排会议。\n\n' +
                   Fore.WHITE + '请使用以下格式：\n' +
                   '  "安排[时间]的[会议名称]，参会人员：[姓名1]、[姓名2]..."\n\n' +
                   Fore.WHITE + '例如：\n' +
                   '  "明天下午3点安排项目评审会议，参会人员：张三、李四、王五"\n\n' +
                   Fore.YELLOW + '或者你可以直接告诉我详细信息，我会帮你整理。')
        
        # 默认使用AI引擎回答
        return self._handle_general_chat(user_input)
    
    def _handle_task_intent(self, user_input: str, intent: dict) -> str:
        """处理任务相关意图"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["查看", "列表", "我的", "待办"]):
            status = None
            if "已完成" in user_input_lower:
                status = "已完成"
            elif "进行中" in user_input_lower:
                status = "进行中"
            elif "待开始" in user_input_lower or "未开始" in user_input_lower:
                status = "待开始"
            return self.assistant.handle_task_command("list", {"status": status})
        
        elif any(word in user_input_lower for word in ["完成", "标记"]):
            import re
            match = re.search(r'任务\s*(\d+)', user_input)
            if match:
                task_id = int(match.group(1))
                return self.assistant.handle_task_command("complete", {"task_id": task_id})
            return "❌ 请指定要完成的任务ID，例如：完成任务1"
        
        elif any(word in user_input_lower for word in ["创建", "新增", "添加"]):
            return (Fore.YELLOW + '✅ 我检测到你想创建任务。\n\n' +
                   Fore.WHITE + '请使用以下格式：\n' +
                   '  "创建任务：[任务名称]，截止日期[日期]，优先级[高/中/低]"\n\n' +
                   Fore.WHITE + '例如：\n' +
                   '  "创建任务：完成项目报告，截止日期本周五，优先级高"\n\n' +
                   Fore.YELLOW + '或者你可以直接告诉我详细信息，我会帮你整理。')
        
        # 默认使用AI引擎回答
        return self._handle_general_chat(user_input)
    
    def _handle_document_intent(self, user_input: str, intent: dict) -> str:
        """处理文档相关意图"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["所有", "全部", "列出"]):
            return self.assistant.handle_document_command("list", {})
        
        elif any(word in user_input_lower for word in ["搜索", "查找", "找"]):
            # 提取关键词（简化版）
            keywords = user_input.replace("搜索", "").replace("查找", "").replace("找", "").strip()
            if keywords:
                return self.assistant.handle_document_command("search", {"keyword": keywords})
            return "❌ 请指定搜索关键词，例如：搜索产品规划文档"
        
        # 默认使用AI引擎回答
        return self._handle_general_chat(user_input)
    
    def _handle_general_chat(self, user_input: str) -> str:
        """处理通用对话"""
        # 添加用户消息到历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 调用AI引擎
        response = self.ai_engine.chat(
            messages=self.conversation_history,
            system_prompt=self.system_prompt
        )
        
        # 添加AI回复到历史
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # 限制历史记录长度
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    def run(self):
        """运行聊天界面"""
        self.display_welcome()
        
        while self.is_running:
            try:
                # 获取用户输入
                user_input = input(Fore.GREEN + Style.BRIGHT + "👤 你: " + Style.RESET_ALL)
                
                if not user_input.strip():
                    continue
                
                # 处理命令
                response = self.process_command(user_input)
                
                # 显示回复
                if response:
                    print(Fore.CYAN + Style.BRIGHT + "🤖 助手: " + Style.RESET_ALL + response + "\n")
            
            except KeyboardInterrupt:
                print("\n\n" + Fore.YELLOW + "感谢使用，再见！👋\n")
                break
            except EOFError:
                print("\n\n" + Fore.YELLOW + "感谢使用，再见！👋\n")
                break
            except Exception as e:
                print(Fore.RED + f"❌ 发生错误: {e}\n")


def main():
    """主函数"""
    interface = ChatInterface()
    interface.run()


if __name__ == "__main__":
    main()
