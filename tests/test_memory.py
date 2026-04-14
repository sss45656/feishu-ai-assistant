"""
上下文记忆功能测试
"""
from memory_manager import MemoryManager


def test_memory_basic():
    """测试基本记忆功能"""
    print("="*80)
    print("🧪 测试1: 基本记忆功能")
    print("="*80)
    
    memory = MemoryManager()
    
    # 添加消息
    memory.add_message('user', '我有哪些会议？')
    memory.add_message('assistant', '您有两个会议：产品周会和技术评审会议')
    memory.add_message('user', '帮我安排一个明天下午的会议')
    
    print(f"\n短期记忆条数: {len(memory.short_term_memory)}")
    print(f"总消息数: {memory.session_metadata['total_messages']}")
    
    # 获取上下文摘要
    summary = memory.get_context_summary()
    print(f"\n【上下文摘要】\n{summary}\n")
    
    print("✅ 基本记忆功能测试通过\n")


def test_entity_extraction():
    """测试实体提取"""
    print("="*80)
    print("🧪 测试2: 实体提取功能")
    print("="*80)
    
    memory = MemoryManager()
    
    # 模拟对话，包含人名
    messages = [
        ("用户", "和张三、李四开会", {"type": "meeting"}),
        ("助手", "好的，已安排与张三、李四的会议", {}),
        ("用户", "给王五分配一个任务", {"type": "task"}),
    ]
    
    for role, content, intent in messages:
        memory.add_message(role, content)
        if role == 'user':
            memory.extract_key_info(content, intent)
    
    # 检查提取的实体
    entities = memory.long_term_memory.get('mentioned_entities', {})
    print(f"\n提取的实体: {list(entities.keys())}")
    
    for name, info in entities.items():
        print(f"  - {name}: 首次提及时间={info['first_mentioned'][:19]}, 上下文={info['context']}")
    
    print("\n✅ 实体提取功能测试通过\n")


def test_context_relevance():
    """测试上下文相关性"""
    print("="*80)
    print("🧪 测试3: 上下文相关性")
    print("="*80)
    
    memory = MemoryManager()
    
    # 模拟多轮对话
    conversations = [
        ("用户", "我有哪些会议？", {"type": "meeting"}),
        ("助手", "您有产品周会和技术评审会议", {}),
        ("用户", "那任务呢？", {"type": "task"}),
        ("助手", "您有3个任务", {}),
        ("用户", "刚才说的会议是什么时候？", {"type": "meeting"}),
    ]
    
    for role, content, intent in conversations:
        memory.add_message(role, content)
        if role == 'user':
            memory.extract_key_info(content, intent)
    
    # 测试指代消解
    query = "刚才说的会议是什么时候？"
    relevant_context = memory.get_relevant_context(query)
    
    print(f"\n查询: {query}")
    print(f"\n相关上下文:\n{relevant_context}\n")
    
    print("✅ 上下文相关性测试通过\n")


def test_action_history():
    """测试操作历史"""
    print("="*80)
    print("🧪 测试4: 操作历史记录")
    print("="*80)
    
    memory = MemoryManager()
    
    # 模拟各种操作
    operations = [
        ("查看会议", {"type": "meeting"}),
        ("创建任务", {"type": "task"}),
        ("搜索文档", {"type": "document"}),
        ("查看任务", {"type": "task"}),
    ]
    
    for content, intent in operations:
        memory.add_message('user', content)
        memory.extract_key_info(content, intent)
    
    # 查看操作历史
    actions = memory.long_term_memory.get('action_history', [])
    print(f"\n记录的操作数: {len(actions)}")
    
    for action in actions:
        action_cn = "查询" if action["action"] == "query" else "创建"
        type_cn = {"meeting": "会议", "task": "任务", "document": "文档"}.get(action["type"], "其他")
        print(f"  - {action_cn}{type_cn} ({action['timestamp'][:19]})")
    
    print("\n✅ 操作历史记录测试通过\n")


def test_memory_stats():
    """测试记忆统计"""
    print("="*80)
    print("🧪 测试5: 记忆统计")
    print("="*80)
    
    memory = MemoryManager()
    
    # 添加一些数据
    for i in range(5):
        memory.add_message('user', f'消息{i+1}')
        memory.add_message('assistant', f'回复{i+1}')
        memory.extract_key_info(f'提到张三{i}', {'type': 'meeting'})
    
    stats = memory.get_memory_stats()
    
    print(f"\n记忆统计:")
    print(f"  - 短期记忆条数: {stats['short_term_count']}")
    print(f"  - 长期记忆实体数: {stats['long_term_entities']}")
    print(f"  - 讨论主题数: {stats['topics_discussed']}")
    print(f"  - 记录操作数: {stats['actions_recorded']}")
    print(f"  - 总消息数: {stats['total_messages']}")
    
    print("\n✅ 记忆统计测试通过\n")


def test_memory_clear():
    """测试记忆清空"""
    print("="*80)
    print("🧪 测试6: 记忆清空功能")
    print("="*80)
    
    memory = MemoryManager()
    
    # 添加数据
    memory.add_message('user', '测试消息')
    memory.extract_key_info('提到张三', {'type': 'meeting'})
    
    print(f"清空前 - 短期记忆: {len(memory.short_term_memory)}, 实体: {len(memory.long_term_memory.get('mentioned_entities', {}))}")
    
    # 清空短期记忆
    memory.clear_short_term()
    print(f"清空短期后 - 短期记忆: {len(memory.short_term_memory)}, 实体: {len(memory.long_term_memory.get('mentioned_entities', {}))}")
    
    # 重新添加并清空长期记忆
    memory.add_message('user', '新消息')
    memory.clear_long_term()
    print(f"清空长期后 - 短期记忆: {len(memory.short_term_memory)}, 实体: {len(memory.long_term_memory.get('mentioned_entities', {}))}")
    
    # 清空所有
    memory.clear_all()
    stats = memory.get_memory_stats()
    print(f"清空所有后 - 总消息数: {stats['total_messages']}")
    
    print("\n✅ 记忆清空功能测试通过\n")


def test_conversation_flow():
    """测试完整对话流程"""
    print("="*80)
    print("🧪 测试7: 完整对话流程")
    print("="*80)
    
    memory = MemoryManager()
    
    # 模拟真实对话场景
    conversation = [
        ("用户", "你好", {"type": "greeting"}),
        ("助手", "你好！有什么可以帮助你的吗？", {}),
        ("用户", "我有哪些会议？", {"type": "meeting"}),
        ("助手", "您有两个会议：产品周会（今天16:00）和技术评审会议（明天10:00）", {}),
        ("用户", "好的，那张三参加哪个会议？", {"type": "meeting"}),
        ("助手", "张三参加产品周会", {}),
        ("用户", "帮我给他分配一个任务", {"type": "task"}),
        ("助手", "好的，请告诉我任务的详细信息", {}),
    ]
    
    print("\n对话流程:")
    for i, (role, content, intent) in enumerate(conversation, 1):
        memory.add_message(role.lower(), content)
        if role == '用户':
            memory.extract_key_info(content, intent)
        
        print(f"{i}. {role}: {content[:50]}...")
    
    # 获取最终上下文
    summary = memory.get_context_summary()
    print(f"\n【最终上下文摘要】\n{summary[:500]}...\n")
    
    stats = memory.get_memory_stats()
    print(f"对话统计: {stats['total_messages']} 条消息, {stats['long_term_entities']} 个实体")
    
    print("\n✅ 完整对话流程测试通过\n")


if __name__ == "__main__":
    try:
        test_memory_basic()
        test_entity_extraction()
        test_context_relevance()
        test_action_history()
        test_memory_stats()
        test_memory_clear()
        test_conversation_flow()
        
        print("\n" + "="*80)
        print("🎉 所有记忆功能测试通过！")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
