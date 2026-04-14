"""
最终格式验证测试
"""
import urllib.request
import json


def test_format_quality():
    """全面测试回答格式质量"""
    
    test_cases = [
        ("我有哪些任务", ["优先级", "截止日期", "状态"]),
        ("我有哪些会议", ["时间", "地点", "参会人"]),
        ("查看所有文档", ["作者", "标签"])
    ]
    
    print("="*80)
    print("🎯 最终格式质量验证")
    print("="*80)
    
    all_passed = True
    
    for query, required_keywords in test_cases:
        print(f"\n{'='*80}")
        print(f"📝 测试问题: {query}")
        print(f"{'='*80}")
        
        data = {
            'message': query,
            'session_id': f'final_test_{query}'
        }
        
        req = urllib.request.Request(
            'http://localhost:5000/api/chat',
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('success'):
                    text = result['response']
                    
                    # 显示回答
                    print("\n【AI回答】")
                    print(text)
                    print()
                    
                    # 检查格式要求
                    checks = {
                        '包含换行符': '\n' in text,
                        '使用数字编号': any(text.startswith(f'{i}.') for i in range(1, 10)),
                        '使用分号分隔': '；' in text or ';' in text,
                        '末尾有句号': text.strip().endswith('。'),
                    }
                    
                    # 检查必需关键词
                    for keyword in required_keywords:
                        checks[f'包含"{keyword}"'] = keyword in text
                    
                    # 显示检查结果
                    print("【格式检查】")
                    for check_name, passed in checks.items():
                        status = "✅" if passed else "❌"
                        print(f"  {status} {check_name}")
                        if not passed:
                            all_passed = False
                        
                else:
                    print(f"❌ 请求失败: {result.get('error')}")
                    all_passed = False
                    
        except Exception as e:
            print(f"❌ 错误: {e}")
            all_passed = False
    
    print(f"\n{'='*80}")
    if all_passed:
        print("🎉 所有格式检查通过！")
    else:
        print("⚠️  部分检查未通过，请查看上述结果")
    print(f"{'='*80}")


if __name__ == '__main__':
    test_format_quality()
