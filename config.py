"""配置管理模块"""
import os
from dotenv import load_dotenv
from typing import Optional

# 加载环境变量
load_dotenv()


class Config:
    """应用配置类"""
    
    # OpenAI API配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    # 模型配置
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    # 应用配置
    APP_NAME: str = os.getenv("APP_NAME", "Feishu AI Assistant")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    
    @classmethod
    def validate(cls) -> bool:
        """验证配置是否有效"""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your_api_key_here":
            print("⚠️  警告: 未配置OpenAI API Key，将使用模拟模式运行")
            return False
        return True
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """获取配置摘要"""
        return {
            "应用名称": cls.APP_NAME,
            "版本": cls.APP_VERSION,
            "模型": cls.MODEL_NAME,
            "API已配置": bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != "your_api_key_here"),
        }
