"""
测试会议查询格式
"""
import urllib.request
import json

def test_meeting_format():
    """测试会议查询的文本格式"""
    
    data = {
        'message': '我有哪些会议',
        'session_id': 'meeting_test'
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
                print("="*80)
                print("📅 会议查询结果:")
                print("="*80)
                print(text)
                print("\n" + "="*80)
                
                # 检查关键字段
                checks = {
                    '时间': '时间' in text,
                    '地点': '地点' in text,
                    '参会人': '参会人' in text,
                    '换行符': '\n' in text,
                    '项目符号': '•' in text
                }
                
                print("格式检查:")
                for field, passed in checks.items():
                    status = "✅" if passed else "❌"
                    print(f"  {status} {field}")
                    
            else:
                print(f"❌ 请求失败: {result.get('error')}")
                
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    test_meeting_format()
