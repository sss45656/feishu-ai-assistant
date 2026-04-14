"""
测试API返回格式
"""
import urllib.request
import urllib.parse
import json

def test_api_format():
    """测试API返回的文本格式"""
    
    # 准备请求数据
    data = {
        'message': '我有哪些任务',
        'session_id': 'format_test'
    }
    
    # 发送POST请求
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
                print("="*80)
                print("📝 API返回的原始文本:")
                print("="*80)
                print(repr(text))
                print("\n" + "="*80)
                print("📄 格式化后的显示:")
                print("="*80)
                print(text)
                print("\n" + "="*80)
                
                # 检查是否包含换行符
                if '\n' in text:
                    print("✅ 文本中包含换行符")
                    line_count = text.count('\n') + 1
                    print(f"   共 {line_count} 行")
                else:
                    print("❌ 文本中不包含换行符")
                
                # 检查是否包含项目符号
                if '•' in text or '-' in text:
                    print("✅ 文本中包含项目符号")
                else:
                    print("⚠️  文本中不包含项目符号")
                    
            else:
                print(f"❌ 请求失败: {result.get('error')}")
                
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    test_api_format()
