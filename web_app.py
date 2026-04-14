"""Flask Web API服务"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ai_engine import AIEngine
from office_assistant import OfficeAssistant
from memory_manager import MemoryManager
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 初始化AI引擎和办公助手
ai_engine = AIEngine()
office_assistant = OfficeAssistant()

# 存储会话历史和记忆
chat_histories = {}
session_memories = {}  # 每个会话的记忆管理器

# 优化的系统提示词 - 使用数字编号和紧凑格式
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


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口（非流式）"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 获取或创建会话历史和记忆
        if session_id not in chat_histories:
            chat_histories[session_id] = []
        if session_id not in session_memories:
            session_memories[session_id] = MemoryManager()
        
        history = chat_histories[session_id]
        memory = session_memories[session_id]
        
        # 识别意图并提取关键信息
        intent = ai_engine.extract_intent(message)
        memory.extract_key_info(message, intent)
        
        # 添加用户消息到记忆
        memory.add_message('user', message)
        history.append({"role": "user", "content": message})
        
        # 获取相关上下文
        context_summary = memory.get_context_summary()
        relevant_context = memory.get_relevant_context(message)
        
        # 构建增强的系统提示词
        enhanced_prompt = SYSTEM_PROMPT
        if context_summary or relevant_context:
            enhanced_prompt += f"\n\n【当前上下文】\n{context_summary}"
            if relevant_context:
                enhanced_prompt += f"\n\n{relevant_context}"
            enhanced_prompt += "\n\n请根据上述上下文信息，提供更连贯、个性化的回复。如果用户指代之前的内容，请结合上下文理解。"
        
        # 调用AI引擎
        response = ai_engine.chat(history, system_prompt=enhanced_prompt)
        
        # 保存助手回复到记忆
        memory.add_message('assistant', response)
        history.append({"role": "assistant", "content": response})
        
        # 限制历史记录长度
        if len(history) > 20:
            chat_histories[session_id] = history[-20:]
        
        return jsonify({
            'success': True,
            'response': response,
            'session_id': session_id,
            'memory_stats': memory.get_memory_stats()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """流式聊天接口"""
    from flask import Response
    
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 获取或创建会话历史和记忆
        if session_id not in chat_histories:
            chat_histories[session_id] = []
        if session_id not in session_memories:
            session_memories[session_id] = MemoryManager()
        
        history = chat_histories[session_id]
        memory = session_memories[session_id]
        
        # 识别意图并提取关键信息
        intent = ai_engine.extract_intent(message)
        memory.extract_key_info(message, intent)
        
        # 添加用户消息到记忆
        memory.add_message('user', message)
        history.append({"role": "user", "content": message})
        
        # 获取相关上下文
        context_summary = memory.get_context_summary()
        relevant_context = memory.get_relevant_context(message)
        
        # 构建增强的系统提示词
        enhanced_prompt = SYSTEM_PROMPT
        if context_summary or relevant_context:
            enhanced_prompt += f"\n\n【当前上下文】\n{context_summary}"
            if relevant_context:
                enhanced_prompt += f"\n\n{relevant_context}"
            enhanced_prompt += "\n\n请根据上述上下文信息，提供更连贯、个性化的回复。如果用户指代之前的内容，请结合上下文理解。"
        
        def generate():
            full_response = ""
            try:
                for chunk in ai_engine.chat_stream(history, system_prompt=enhanced_prompt):
                    full_response += chunk
                    yield f"data: {chunk}\n\n"
                
                # 保存完整回复到记忆和历史
                memory.add_message('assistant', full_response)
                history.append({"role": "assistant", "content": full_response})
                if len(history) > 20:
                    chat_histories[session_id] = history[-20:]
                
                # 发送结束标记和记忆统计
                stats = memory.get_memory_stats()
                yield f"data: [DONE]\n\n"
                yield f"data: [STATS]{json.dumps(stats)}\n\n"
            
            except Exception as e:
                yield f"data: [ERROR] {str(e)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    """获取会议列表"""
    try:
        date = request.args.get('date')
        meetings = office_assistant.meeting_manager.list_meetings(date)
        return jsonify({
            'success': True,
            'meetings': meetings
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meetings', methods=['POST'])
def create_meeting():
    """创建会议"""
    try:
        data = request.json
        meeting = office_assistant.meeting_manager.create_meeting(
            title=data.get('title', '新会议'),
            time=data.get('time', '待定'),
            participants=data.get('participants', []),
            duration=data.get('duration', '60分钟'),
            location=data.get('location', '待定')
        )
        return jsonify({
            'success': True,
            'meeting': meeting
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meetings/<int:meeting_id>/cancel', methods=['POST'])
def cancel_meeting(meeting_id):
    """取消会议"""
    try:
        success = office_assistant.meeting_manager.cancel_meeting(meeting_id)
        if success:
            return jsonify({'success': True, 'message': '会议已取消'})
        else:
            return jsonify({'success': False, 'message': '会议不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表"""
    try:
        status = request.args.get('status')
        tasks = office_assistant.task_manager.list_tasks(status)
        return jsonify({
            'success': True,
            'tasks': tasks
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建任务"""
    try:
        data = request.json
        task = office_assistant.task_manager.create_task(
            title=data.get('title', '新任务'),
            deadline=data.get('deadline', '待定'),
            priority=data.get('priority', '中'),
            assignee=data.get('assignee', '我'),
            description=data.get('description', '')
        )
        return jsonify({
            'success': True,
            'task': task
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """完成任务"""
    try:
        success = office_assistant.task_manager.update_task_status(task_id, '已完成')
        if success:
            return jsonify({'success': True, 'message': '任务已完成'})
        else:
            return jsonify({'success': False, 'message': '任务不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents', methods=['GET'])
def get_documents():
    """获取文档列表"""
    try:
        keyword = request.args.get('keyword')
        if keyword:
            docs = office_assistant.document_manager.search_documents(keyword)
        else:
            docs = office_assistant.document_manager.list_all_documents()
        
        return jsonify({
            'success': True,
            'documents': docs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intent', methods=['POST'])
def detect_intent():
    """意图识别"""
    try:
        data = request.json
        message = data.get('message', '')
        intent = ai_engine.extract_intent(message)
        return jsonify({
            'success': True,
            'intent': intent
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/memory/stats', methods=['GET'])
def get_memory_stats():
    """获取记忆统计"""
    try:
        session_id = request.args.get('session_id', 'default')
        if session_id in session_memories:
            stats = session_memories[session_id].get_memory_stats()
            return jsonify({'success': True, 'stats': stats})
        else:
            return jsonify({'success': True, 'stats': {}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    """清空记忆"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        clear_type = data.get('type', 'all')  # all/short_term/long_term
        
        if session_id in session_memories:
            memory = session_memories[session_id]
            if clear_type == 'all':
                memory.clear_all()
            elif clear_type == 'short_term':
                memory.clear_short_term()
            elif clear_type == 'long_term':
                memory.clear_long_term()
            
            return jsonify({'success': True, 'message': f'已清空{clear_type}记忆'})
        else:
            return jsonify({'success': False, 'message': '会话不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 启动飞书AI办公协同智能助手 Web服务...")
    print("📍 访问地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
