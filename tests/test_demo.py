"""
快速测试脚本 - 验证核心功能
"""
from office_assistant import OfficeAssistant
from ai_engine import AIEngine


def test_office_assistant():
    """测试办公助手功能"""
    print("="*60)
    print("测试办公助手功能")
    print("="*60)
    
    assistant = OfficeAssistant()
    
    # 测试会议管理
    print("\n📅 测试会议管理:")
    print("-" * 60)
    meetings = assistant.meeting_manager.list_meetings()
    print(f"当前会议数量: {len(meetings)}")
    for meeting in meetings:
        print(assistant.meeting_manager.format_meeting_info(meeting))
    
    # 测试任务管理
    print("\n✅ 测试任务管理:")
    print("-" * 60)
    tasks = assistant.task_manager.list_tasks()
    print(f"当前任务数量: {len(tasks)}")
    for task in tasks:
        print(assistant.task_manager.format_task_info(task))
    
    # 测试文档检索
    print("\n📄 测试文档检索:")
    print("-" * 60)
    docs = assistant.document_manager.search_documents("产品")
    print(f"搜索'产品'找到 {len(docs)} 个文档:")
    for doc in docs:
        print(assistant.document_manager.format_document_info(doc))
    
    print("\n✓ 办公助手功能测试通过!\n")


def test_ai_engine():
    """测试AI引擎"""
    print("="*60)
    print("测试AI引擎")
    print("="*60)
    
    engine = AIEngine()
    
    # 测试意图识别
    print("\n🧠 测试意图识别:")
    print("-" * 60)
    
    test_cases = [
        "明天下午3点安排会议",
        "创建一个新任务",
        "搜索产品文档",
        "你好",
        "查看我的日程"
    ]
    
    for test_input in test_cases:
        intent = engine.extract_intent(test_input)
        print(f"输入: {test_input}")
        print(f"意图: {intent['type']}, 置信度: {intent['confidence']}\n")
    
    # 测试对话功能
    print("\n💬 测试对话功能:")
    print("-" * 60)
    
    messages = [{"role": "user", "content": "你好，请介绍一下你自己"}]
    response = engine.chat(messages)
    print(f"用户: {messages[0]['content']}")
    print(f"助手: {response[:200]}...")
    
    print("\n✓ AI引擎功能测试通过!\n")


if __name__ == "__main__":
    try:
        test_office_assistant()
        test_ai_engine()
        
        print("="*60)
        print("🎉 所有测试通过！程序可以正常运行。")
        print("="*60)
        print("\n现在可以运行 'python main.py' 启动交互式界面")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
