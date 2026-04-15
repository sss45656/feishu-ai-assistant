# 飞书AI办公协同智能助手

## 项目简介

本项目是**课题二：基于IM的办公协同智能助手**的可运行Demo实现。它是一个智能化的办公助手系统，能够理解自然语言指令，帮助用户高效管理会议、任务和文档等办公场景。

### ✨ 核心特性

- 🤖 **智能对话**: 基于大语言模型的自然语言理解和多轮对话
- 💭 **上下文记忆**: 记住对话历史，实现连贯的交互体验
- ⚡ **流式输出**: 实时逐字显示AI回复，提升用户体验
- 📱 **双界面支持**: Web界面和命令行界面任选
- 🎯 **意图识别**: 自动识别用户意图并执行相应操作

## 功能特性

### 📅 会议管理
- 智能安排会议，自动识别时间、参会人员和地点
- 查看会议日程和安排
- 取消或修改会议

### ✅ 任务管理
- 创建和分配任务，设置优先级和截止日期
- 跟踪任务进度和状态
- 任务提醒和通知

### 📄 文档检索
- 智能搜索云文档
- 根据内容关键词检索
- 文档摘要和标签管理

### 💬 智能对话
- 基于大语言模型的自然语言理解
- 上下文感知的多轮对话
- 意图识别和命令解析

## 技术架构

```
feishu_AI/
├── main.py                 # CLI模式主入口
├── web_app.py              # Web服务主入口
├── config.py               # 配置管理模块
├── ai_engine.py            # AI引擎模块（对接大模型）
├── office_assistant.py     # 办公协同功能模块
├── memory_manager.py       # 上下文记忆管理
├── chat_interface.py       # 命令行交互界面
├── requirements.txt        # 依赖包列表
├── .env.example            # 环境变量示例
├── README.md               # 项目主文档
├── MIGRATION_GUIDE.md      # 迁移配置指南
├── ISSUES_SUMMARY.md       # 开发问题总结
│
├── static/                 # Web静态资源
│   ├── style.css           # CSS样式
│   └── script.js           # JavaScript逻辑
│
├── templates/              # HTML模板
│   └── index.html          # Web主页面
│
└── tests/                  # 测试代码目录
    ├── test_faq.py         # 常见问题测试
    ├── test_memory.py      # 记忆功能测试
    ├── test_api_format.py  # API格式测试
    └── ...                 # 其他测试文件
```

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8 或更高版本。

```bash
python --version  # 检查Python版本
```

### 2. 克隆项目

```bash
git clone https://github.com/sss45656/feishu-ai-assistant.git
cd feishu-ai-assistant
```

### 3. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

**重要**: 需要配置API密钥才能使用真实AI模型。

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# Windows: notepad .env
# macOS/Linux: nano .env
```

详细配置说明请参考：[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

### 6. 运行程序

#### Web界面模式（推荐）

```bash
python web_app.py
```

然后在浏览器访问: http://localhost:5000

#### 命令行模式

```bash
python main.py
```

## 使用示例

### 会议管理

```
👤 你: 明天下午3点安排项目评审会议，参会人员：张三、李四、王五
🤖 助手: 📅 我检测到你想安排会议...

👤 你: 查看我的会议安排
🤖 助手: 📅 我的会议安排
       ========================================
       📅 产品周会
          时间: 2024-04-14 16:00 (60分钟)
          地点: 会议室A
          参会人: 张三, 李四, 王五
          状态: 已确认
```

### 任务管理

```
👤 你: 创建一个任务：完成项目报告，截止日期本周五，优先级高
🤖 助手: ✅ 我检测到你想创建任务...

👤 你: 查看我的待办任务
🤖 助手: ✅ 我的任务列表
       ========================================
       🔴 完成项目需求文档
          截止日期: 2024-04-16
          负责人: 我
          状态: ▶️ 进行中
          描述: 编写Q2产品需求文档
```

### 文档检索

```
👤 你: 搜索关于产品规划的文档
🤖 助手: 🔍 搜索结果（共1个）
       ========================================
       📝 Q2产品规划文档
          类型: 云文档
          作者: 张三
          更新时间: 2024-04-10
          摘要: 包含Q2产品路线图、功能规划和资源分配计划
          标签: 产品, 规划, Q2
```

## 工作模式

### 模拟模式（默认）
- 无需API Key即可运行
- 基于规则的智能回复
- 完整的功能演示
- 适合快速体验和Demo展示

### 真实API模式
- 需要配置OpenAI兼容的API Key
- 基于大模型的智能对话
- 更自然的语言理解
- 支持更多复杂场景

支持的API服务：
- OpenAI GPT系列
- 阿里云通义千问
- 百度文心一言
- 其他兼容OpenAI API的服务

## 核心模块说明

### AI引擎 (ai_engine.py)
负责与大语言模型交互，提供智能对话能力。
- 支持OpenAI兼容接口的多种模型
- 流式输出支持
- 模拟模式保证无API时也可运行
- 意图识别和命令解析

### 记忆管理 (memory_manager.py)
实现上下文记忆功能，让AI能够记住对话历史。
- **短期记忆**: 保存最近的对话历史（10轮）
- **长期记忆**: 提取关键信息（实体、主题、操作）
- **上下文摘要**: 智能生成对话上下文
- **记忆清理**: 自动管理记忆大小

### 办公助手 (office_assistant.py)
包含三个核心管理器：
- **MeetingManager**: 会议管理（创建、查看、取消）
- **TaskManager**: 任务管理（创建、跟踪、更新）
- **DocumentManager**: 文档管理（搜索、标签、摘要）

### Web服务 (web_app.py)
Flask后端服务，提供RESTful API。
- `/api/chat`: 聊天接口（非流式）
- `/api/chat/stream`: 聊天接口（流式）
- `/api/memory/*`: 记忆管理接口
- CORS跨域支持

### 聊天界面 (chat_interface.py)
提供友好的命令行交互界面。
- 彩色输出和格式化显示
- 意图识别和命令分发
- 对话历史管理
- 帮助系统

## 扩展开发

### 添加新的办公功能

1. 在 `office_assistant.py` 中创建新的管理器类
2. 在 `ChatInterface` 中添加对应的意图处理逻辑
3. 更新帮助文档和示例

### 接入真实的飞书API

1. 安装飞书SDK: `pip install lark-oapi`
2. 在相应管理器中调用飞书API
3. 配置飞书应用的App ID和Secret

### 自定义AI模型

修改 `config.py` 中的模型配置：

```python
# 使用通义千问
MODEL_NAME=qwen-plus
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 使用文心一言
MODEL_NAME=ernie-bot
OPENAI_BASE_URL=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop
```

## 技术栈

- **Python 3.8+**: 主要编程语言
- **OpenAI SDK**: AI模型接口
- **Colorama**: 终端彩色输出
- **python-dotenv**: 环境变量管理
- **python-dateutil**: 日期时间处理

## 项目亮点

1. **双模式运行**: 支持模拟模式和真实API模式，降低使用门槛
2. **模块化设计**: 清晰的模块划分，易于扩展和维护
3. **智能意图识别**: 自动识别用户意图并分发到对应功能模块
4. **上下文记忆**: 记住对话历史，实现连贯的多轮对话
5. **流式输出**: 实时逐字显示AI回复，提升用户体验
6. **双界面支持**: Web界面和命令行界面任选
7. **友好交互**: 彩色输出和格式化显示，提升用户体验
8. **完整测试**: 包含自动化测试用例，保证代码质量

## 注意事项

- 本项目为Demo实现，展示了核心功能和架构设计
- 生产环境需要接入真实的飞书API和企业数据源
- 建议配置真实的AI API以获得更好的对话体验
- 数据存储目前使用内存存储，重启后数据会丢失
- **重要**: `.env`文件包含敏感信息，不要提交到版本控制系统

## 相关文档

- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - 详细的迁移配置指南
- [ISSUES_SUMMARY.md](ISSUES_SUMMARY.md) - 开发过程中的问题总结
- [QUICKSTART.md](QUICKSTART.md) - 快速入门指南
- [PROJECT_DESIGN.md](PROJECT_DESIGN.md) - 项目设计文档

## 测试

运行测试用例：

```bash
# 常见问题测试
python tests/test_faq.py

# 记忆功能测试
python tests/test_memory.py

# 格式验证测试
python tests/test_final_format.py
```

**享受智能办公带来的效率提升！** 🚀
