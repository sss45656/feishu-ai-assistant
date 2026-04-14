"""
常见问题测试脚本 - 验证AI回答质量
"""
from ai_engine import AIEngine

# 系统提示词
SYSTEM_PROMPT = """你是飞书AI办公协同智能助手，一个Demo系统。你有内置的会议、任务和文档数据。

重要规则：
1. 当用户询问"我有哪些会议"、"查看会议"等问题时，直接列出下面的会议数据
2. 当用户询问"我有哪些任务"、"查看任务"等问题时，直接列出下面的任务数据
3. 当用户询问"搜索文档"、"查看所有文档"时，直接列出下面的文档数据
4. 回答要简洁直接，不要说"我需要更多信息"或"请提供权限"
5. 你是Demo系统，所有数据都是模拟的，可以直接展示
6. **格式要求（必须严格遵守）**：
   - 使用**数字编号**（1. 2. 3.）而不是项目符号
   - 每个项目的属性用**分号**分隔，放在同一行
   - **每个分点的最后必须加句号**
   - **绝对不能省略**任何字段名称（如"优先级"、"截止日期"、"状态"等）
   - 不同项目之间用**空行**分隔

内置会议数据（**严格按此格式展示**）：
1. 产品周会；时间：今天下午16:00；地点：会议室A；参会人：张三、李四、王五。

2. 技术评审会议；时间：明天上午10:00；地点：会议室B；参会人：赵六、钱七。

内置任务数据（**严格按此格式展示**）：
1. 完成项目需求文档；优先级：高；截止日期：2024-04-16；状态：进行中。

2. 代码审查；优先级：中；截止日期：2024-04-15；状态：待开始。

3. 更新用户手册；优先级：低；截止日期：2024-04-19；状态：已完成。

内置文档数据（**严格按此格式展示**）：
1. Q2产品规划文档；作者：张三；标签：产品、规划、Q2。

2. 技术架构设计文档；作者：李四；标签：技术、架构、设计。

3. 用户增长数据分析报告；作者：王五；标签：数据、分析。

4. 项目周会纪要；作者：赵六；标签：会议、纪要。

**错误示例（禁止这样输出）**：
❌ "• 完成项目需求文档 优先级：高" （使用了项目符号）
❌ "1. 完成项目需求文档\n  优先级：高\n  截止日期：2024-04-16" （使用了换行）
❌ "1. 完成项目需求文档；优先级：高；截止日期：2024-04-16；状态：进行中" （缺少句号）

**正确示例（必须这样输出）**：
✅ "1. 完成项目需求文档；优先级：高；截止日期：2024-04-16；状态：进行中。"

请用友好、简洁的语气直接回答用户问题，展示上述数据。**务必使用数字编号和分号分隔，每个项目占一行，末尾加句号**。"""


def test_faq():
    """测试常见问题"""
    engine = AIEngine()
    
    # 定义测试用例
    test_cases = [
        {
            "question": "我有哪些会议",
            "expected_keywords": ["会议", "产品周会", "技术评审"],
            "category": "会议查询"
        },
        {
            "question": "查看我的会议安排",
            "expected_keywords": ["会议", "时间", "地点"],
            "category": "会议查询"
        },
        {
            "question": "我有哪些任务",
            "expected_keywords": ["任务", "优先级", "截止日期"],
            "category": "任务查询"
        },
        {
            "question": "查看我的待办任务",
            "expected_keywords": ["任务", "进行中", "待开始"],
            "category": "任务查询"
        },
        {
            "question": "搜索产品文档",
            "expected_keywords": ["搜索", "产品", "文档"],
            "category": "文档检索"
        },
        {
            "question": "查看所有文档",
            "expected_keywords": ["文档", "列表", "所有"],
            "category": "文档检索"
        },
        {
            "question": "你好",
            "expected_keywords": ["你好", "帮助", "助手"],
            "category": "问候"
        },
        {
            "question": "帮助",
            "expected_keywords": ["帮助", "会议", "任务", "文档"],
            "category": "帮助"
        },
        {
            "question": "谢谢",
            "expected_keywords": ["不客气", "随时"],
            "category": "感谢"
        },
        {
            "question": "安排一个会议",
            "expected_keywords": ["会议", "信息", "时间"],
            "category": "会议创建"
        },
        {
            "question": "创建一个任务",
            "expected_keywords": ["任务", "提供", "信息"],
            "category": "任务创建"
        }
    ]
    
    print("="*80)
    print("🧪 常见问题测试")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"测试 {i}/{len(test_cases)}: [{test_case['category']}]")
        print(f"问题: {test_case['question']}")
        print("-"*80)
        
        # 获取AI回复
        messages = [{"role": "user", "content": test_case['question']}]
        response = engine.chat(messages, system_prompt=SYSTEM_PROMPT)
        
        print(f"回答:\n{response}\n")
        
        # 检查是否包含预期关键词
        missing_keywords = []
        for keyword in test_case['expected_keywords']:
            if keyword not in response:
                missing_keywords.append(keyword)
        
        if missing_keywords:
            print(f"❌ 测试失败 - 缺少关键词: {', '.join(missing_keywords)}")
            failed += 1
        else:
            print(f"✅ 测试通过 - 包含所有预期关键词")
            passed += 1
        
        # 检查回答长度（不应太短或太长）
        if len(response) < 20:
            print(f"⚠️  警告 - 回答过短 ({len(response)} 字符)")
        elif len(response) > 1000:
            print(f"⚠️  警告 - 回答过长 ({len(response)} 字符)")
    
    # 打印总结
    print("\n" + "="*80)
    print("📊 测试总结")
    print("="*80)
    print(f"总测试数: {len(test_cases)}")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"通过率: {passed/len(test_cases)*100:.1f}%")
    print("="*80)
    
    return failed == 0


def test_conversation_flow():
    """测试对话流程"""
    print("\n\n" + "="*80)
    print("💬 对话流程测试")
    print("="*80)
    
    engine = AIEngine()
    history = []
    
    # 模拟多轮对话
    conversation = [
        "你好",
        "我有哪些会议",
        "帮我安排一个会议",
        "我有哪些任务",
        "谢谢"
    ]
    
    for i, question in enumerate(conversation, 1):
        print(f"\n--- 第 {i} 轮对话 ---")
        print(f"用户: {question}")
        
        history.append({"role": "user", "content": question})
        response = engine.chat(history, system_prompt=SYSTEM_PROMPT)
        history.append({"role": "assistant", "content": response})
        
        print(f"助手: {response[:200]}...")
    
    print("\n✅ 对话流程测试完成")


if __name__ == "__main__":
    try:
        # 运行FAQ测试
        success = test_faq()
        
        # 运行对话流程测试
        test_conversation_flow()
        
        if success:
            print("\n🎉 所有测试通过！")
        else:
            print("\n⚠️  部分测试失败，请检查上述输出")
    
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
