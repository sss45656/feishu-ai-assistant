"""
飞书AI办公协同智能助手 - 主入口
基于IM的办公协同智能助手Demo

课题二：基于IM的办公协同智能助手
"""
import sys
from chat_interface import main


if __name__ == "__main__":
    print("正在启动飞书AI办公协同智能助手...\n")
    
    try:
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("\n请先安装依赖：pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 程序运行错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
