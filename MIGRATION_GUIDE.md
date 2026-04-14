# 项目迁移配置指南

本文档详细说明了飞书AI办公协同智能助手项目的迁移和部署配置要求。

## 一、环境要求

### 1.1 Python版本
- **最低版本**: Python 3.8
- **推荐版本**: Python 3.9 或更高
- **验证命令**: `python --version`

### 1.2 操作系统
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+)

## 二、依赖库安装

### 2.1 核心依赖

使用 pip 安装所有必需的Python库：

```bash
pip install -r requirements.txt
```

### 2.2 依赖清单

**requirements.txt** 包含以下库：

```
openai>=1.0.0          # OpenAI SDK（兼容通义千问等模型）
flask>=3.0.0           # Web框架
flask-cors>=4.0.0      # CORS跨域支持
python-dotenv>=1.0.0   # 环境变量管理
colorama>=0.4.6        # 命令行彩色输出（Windows兼容）
```

### 2.3 手动安装（可选）

如果需要单独安装某个库：

```bash
pip install openai flask flask-cors python-dotenv colorama
```

## 三、OpenAI API 配置

### 3.1 环境变量配置文件

项目使用 `.env` 文件管理敏感配置。

#### 步骤1: 复制示例配置文件

```bash
cp .env.example .env
```

#### 步骤2: 编辑 .env 文件

打开 `.env` 文件，配置以下参数：

```env
# OpenAI API配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-max

# 应用配置
APP_HOST=0.0.0.0
APP_PORT=5000
DEBUG=True
```

### 3.2 配置参数说明

| 参数名 | 说明 | 示例值 | 必填 |
|--------|------|--------|------|
| OPENAI_API_KEY | API密钥 | sk-xxxxx | 是 |
| OPENAI_BASE_URL | API基础URL | https://dashscope.aliyuncs.com/compatible-mode/v1 | 是 |
| MODEL_NAME | 模型名称 | qwen-max | 是 |
| APP_HOST | 服务监听地址 | 0.0.0.0 | 否 |
| APP_PORT | 服务端口 | 5000 | 否 |
| DEBUG | 调试模式 | True/False | 否 |

### 3.3 不同模型的配置示例

#### 通义千问（阿里云）

```env
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-max
```

#### OpenAI GPT

```env
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4
```

#### 其他兼容OpenAI接口的模型

```env
OPENAI_BASE_URL=https://your-api-endpoint/v1
MODEL_NAME=your-model-name
```

### 3.4 获取API密钥

#### 通义千问（推荐）
1. 访问阿里云官网: https://www.aliyun.com/
2. 注册/登录账号
3. 开通通义千问服务
4. 在控制台获取 API Key
5. 确保账户有足够的额度

#### OpenAI
1. 访问 OpenAI 官网: https://platform.openai.com/
2. 注册/登录账号
3. 在 API Keys 页面创建新的密钥
4. 绑定支付方式并充值

## 四、项目启动

### 4.1 Web界面模式（推荐）

```bash
python web_app.py
```

访问地址: http://localhost:5000

### 4.2 命令行模式

```bash
python main.py
```

### 4.3 生产环境部署

#### 使用 Gunicorn（Linux/macOS）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

#### 使用 Waitress（Windows）

```bash
pip install waitress
waitress-serve --port=5000 web_app:app
```

## 五、目录结构说明

```
feishu_AI/
├── .env                    # 环境变量配置（不要提交到Git）
├── .env.example            # 环境变量示例文件
├── .gitignore              # Git忽略文件配置
├── requirements.txt        # Python依赖清单
├── README.md               # 项目主文档
├── MIGRATION_GUIDE.md      # 迁移配置指南（本文档）
│
├── config.py               # 配置管理模块
├── ai_engine.py            # AI引擎核心
├── office_assistant.py     # 办公助手业务逻辑
├── memory_manager.py       # 上下文记忆管理
├── web_app.py              # Flask Web服务
├── chat_interface.py       # 命令行交互界面
├── main.py                 # 主入口文件
│
├── static/                 # 静态资源
│   ├── style.css           # CSS样式
│   └── script.js           # JavaScript逻辑
│
├── templates/              # HTML模板
│   └── index.html          # 主页面
│
└── tests/                  # 测试代码目录
    ├── test_faq.py         # 常见问题测试
    ├── test_memory.py      # 记忆功能测试
    ├── test_api_format.py  # API格式测试
    └── ...                 # 其他测试文件
```

## 六、常见问题

### 6.1 导入错误

**问题**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 
```bash
pip install -r requirements.txt
```

### 6.2 API密钥错误

**问题**: `AuthenticationError: Invalid API key`

**解决**: 
- 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- 确认API密钥没有过期
- 验证账户余额充足

### 6.3 端口占用

**问题**: `Address already in use`

**解决**: 
- 修改 `.env` 中的 `APP_PORT` 为其他端口
- 或者关闭占用端口的程序

### 6.4 CORS错误

**问题**: 前端无法访问后端API

**解决**: 
- 确认已安装 `flask-cors`
- 检查 `web_app.py` 中已启用 `CORS(app)`

## 七、安全注意事项

### 7.1 保护API密钥

⚠️ **重要**: 永远不要将 `.env` 文件提交到版本控制系统！

```bash
# 检查 .gitignore 是否包含 .env
cat .gitignore
```

应该看到：
```
.env
*.pyc
__pycache__/
```

### 7.2 生产环境配置

- 设置 `DEBUG=False`
- 使用强密码和HTTPS
- 限制API调用频率
- 定期更新依赖库

## 八、性能优化建议

### 8.1 内存管理

- 调整 `memory_manager.py` 中的 `max_short_term` 和 `max_long_term` 参数
- 定期清理不需要的会话历史

### 8.2 API调用优化

- 使用流式输出减少等待时间
- 合理设置 `max_tokens` 和 `temperature` 参数
- 缓存常用响应

## 九、技术支持

如遇到问题，请检查：

1. ✅ Python版本是否符合要求
2. ✅ 所有依赖库是否已安装
3. ✅ `.env` 配置是否正确
4. ✅ API密钥是否有效且有余额
5. ✅ 网络连接是否正常

## 十、更新日志

- **v1.0.0** (2024-04-14): 初始版本，包含完整的Web界面和CLI模式
- 添加上下文记忆功能
- 支持流式输出
- 优化回答格式

---

**最后更新**: 2024-04-14  
**维护者**: 项目开发团队
