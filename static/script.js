// 全局变量
let currentSessionId = 'session_' + Date.now();
let currentTaskFilter = '';
let memoryStats = null;  // 记忆统计信息

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    loadMeetings();
    loadTasks();
    loadAllDocuments();
});

// 初始化导航
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // 移除所有active类
            navItems.forEach(nav => nav.classList.remove('active'));
            document.querySelectorAll('.view').forEach(view => view.classList.remove('active'));
            
            // 添加active类到当前项
            this.classList.add('active');
            const viewName = this.dataset.view;
            document.getElementById(viewName + '-view').classList.add('active');
        });
    });
}

// ==================== 聊天功能 ====================

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 显示用户消息
    addMessage('user', message);
    input.value = '';
    
    // 创建助手消息容器（用于流式显示）
    const assistantMessageDiv = createStreamingMessage();
    
    // 使用流式API
    fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            session_id: currentSessionId
        })
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        
        function readStream() {
            return reader.read().then(({ done, value }) => {
                if (done) {
                    // 流结束，保存完整消息
                    finalizeMessage(assistantMessageDiv, fullResponse);
                    return;
                }
                
                // 解码数据
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        
                        if (data === '[DONE]') {
                            // 流式传输完成
                            finalizeMessage(assistantMessageDiv, fullResponse);
                            return;
                        } else if (data.startsWith('[ERROR]')) {
                            // 错误处理
                            const errorMsg = data.slice(9);
                            assistantMessageDiv.querySelector('.message-content p').textContent = '抱歉，出现错误：' + errorMsg;
                            return;
                        } else if (data.startsWith('[STATS]')) {
                            // 接收记忆统计
                            try {
                                memoryStats = JSON.parse(data.slice(9));
                                updateMemoryStatsDisplay();
                            } catch (e) {
                                console.error('解析记忆统计失败:', e);
                            }
                            return;
                        } else {
                            // 累积响应并更新显示
                            fullResponse += data;
                            updateStreamingMessage(assistantMessageDiv, fullResponse);
                        }
                    }
                }
                
                return readStream();
            });
        }
        
        return readStream();
    })
    .catch(error => {
        assistantMessageDiv.querySelector('.message-content p').textContent = '抱歉，网络请求失败：' + error.message;
    });
}

function createStreamingMessage() {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <p><span class="cursor">|</span></p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return messageDiv;
}

function updateStreamingMessage(messageDiv, content) {
    const contentElement = messageDiv.querySelector('.message-content p');
    contentElement.innerHTML = formatMessage(content) + '<span class="cursor">|</span>';
    
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function finalizeMessage(messageDiv, content) {
    const contentElement = messageDiv.querySelector('.message-content p');
    contentElement.innerHTML = formatMessage(content);
}

// 更新记忆统计显示
function updateMemoryStatsDisplay() {
    if (!memoryStats) return;
    
    // 可以在侧边栏或状态栏显示记忆统计
    const statusText = document.getElementById('status-text');
    if (statusText && memoryStats.total_messages > 0) {
        statusText.textContent = `在线 | 对话: ${memoryStats.total_messages} 条`;
    }
}

// 清空记忆
function clearMemory(type = 'all') {
    if (!confirm(`确定要清空${type === 'all' ? '所有' : type === 'short_term' ? '短期' : '长期'}记忆吗？`)) {
        return;
    }
    
    fetch('/api/memory/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_id: currentSessionId,
            type: type
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            if (type === 'all' || type === 'short_term') {
                // 清空聊天界面
                document.getElementById('chat-messages').innerHTML = `
                    <div class="message assistant">
                        <div class="message-avatar">🤖</div>
                        <div class="message-content">
                            <p>记忆已清空。有什么可以帮助你的吗？</p>
                        </div>
                    </div>
                `;
            }
            memoryStats = null;
            updateMemoryStatsDisplay();
        } else {
            alert('操作失败：' + data.message);
        }
    })
    .catch(error => {
        alert('网络错误：' + error.message);
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function addMessage(role, content) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = role === 'user' ? '👤' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${formatMessage(content)}</p>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addLoadingMessage() {
    const messagesContainer = document.getElementById('chat-messages');
    const loadingId = 'loading-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = loadingId;
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="loading"></div>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return loadingId;
}

function removeLoadingMessage(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

function formatMessage(content) {
    // 增强格式化：处理换行、列表等
    if (!content) return '';
    
    // 首先转义HTML特殊字符，防止XSS
    let formatted = content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // 将换行符转换为<br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    // 处理多个连续空格（保留缩进）
    formatted = formatted.replace(/  /g, '&nbsp;&nbsp;');
    
    return formatted;
}

function clearChat() {
    if (confirm('确定要清空对话历史和记忆吗？')) {
        // 清空前端显示
        document.getElementById('chat-messages').innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <p>对话已清空。有什么可以帮助你的吗？</p>
                </div>
            </div>
        `;
        
        // 生成新的会话ID
        currentSessionId = 'session_' + Date.now();
        memoryStats = null;
        updateMemoryStatsDisplay();
    }
}

// ==================== 会议管理功能 ====================

function loadMeetings() {
    fetch('/api/meetings')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayMeetings(data.meetings);
        }
    })
    .catch(error => console.error('加载会议失败:', error));
}

function displayMeetings(meetings) {
    const container = document.getElementById('meetings-list');
    
    if (meetings.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">📅</div>
                <p>暂无会议安排</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = meetings.map(meeting => `
        <div class="card">
            <div class="card-header">
                <div class="card-title">📅 ${meeting.title}</div>
                <span class="card-badge badge-status">${meeting.status}</span>
            </div>
            <div class="card-body">
                <div class="card-info">
                    <span class="label">时间:</span>
                    <span>${meeting.time}</span>
                </div>
                <div class="card-info">
                    <span class="label">时长:</span>
                    <span>${meeting.duration}</span>
                </div>
                <div class="card-info">
                    <span class="label">地点:</span>
                    <span>${meeting.location}</span>
                </div>
                <div class="card-info">
                    <span class="label">参会人:</span>
                    <span>${meeting.participants.join(', ')}</span>
                </div>
            </div>
            ${meeting.status !== '已取消' ? `
            <div class="card-footer">
                <button class="btn btn-secondary" onclick="cancelMeeting(${meeting.id})">取消会议</button>
            </div>
            ` : ''}
        </div>
    `).join('');
}

function showCreateMeetingForm() {
    document.getElementById('create-meeting-form').style.display = 'block';
}

function hideCreateMeetingForm() {
    document.getElementById('create-meeting-form').style.display = 'none';
    // 清空表单
    document.getElementById('meeting-title').value = '';
    document.getElementById('meeting-time').value = '';
    document.getElementById('meeting-participants').value = '';
    document.getElementById('meeting-duration').value = '60分钟';
    document.getElementById('meeting-location').value = '';
}

function createMeeting() {
    const title = document.getElementById('meeting-title').value.trim();
    const time = document.getElementById('meeting-time').value.trim();
    const participantsStr = document.getElementById('meeting-participants').value.trim();
    const duration = document.getElementById('meeting-duration').value.trim();
    const location = document.getElementById('meeting-location').value.trim();
    
    if (!title || !time) {
        alert('请填写会议标题和时间');
        return;
    }
    
    const participants = participantsStr.split(/[,，]/).map(p => p.trim()).filter(p => p);
    
    fetch('/api/meetings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            time: time,
            participants: participants,
            duration: duration || '60分钟',
            location: location || '待定'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('会议创建成功！');
            hideCreateMeetingForm();
            loadMeetings();
        } else {
            alert('创建失败：' + data.error);
        }
    })
    .catch(error => {
        alert('网络错误：' + error.message);
    });
}

function cancelMeeting(meetingId) {
    if (!confirm('确定要取消这个会议吗？')) return;
    
    fetch(`/api/meetings/${meetingId}/cancel`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('会议已取消');
            loadMeetings();
        } else {
            alert('取消失败：' + data.message);
        }
    })
    .catch(error => {
        alert('网络错误：' + error.message);
    });
}

// ==================== 任务管理功能 ====================

function loadTasks() {
    const url = currentTaskFilter 
        ? `/api/tasks?status=${encodeURIComponent(currentTaskFilter)}`
        : '/api/tasks';
    
    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayTasks(data.tasks);
        }
    })
    .catch(error => console.error('加载任务失败:', error));
}

function displayTasks(tasks) {
    const container = document.getElementById('tasks-list');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">✅</div>
                <p>暂无任务</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = tasks.map(task => {
        const priorityClass = task.priority === '高' ? 'badge-high' : 
                             task.priority === '中' ? 'badge-medium' : 'badge-low';
        const statusIcon = task.status === '已完成' ? '✅' : 
                          task.status === '进行中' ? '▶️' : '⏸️';
        
        return `
        <div class="card">
            <div class="card-header">
                <div class="card-title">${task.title}</div>
                <span class="card-badge ${priorityClass}">${task.priority}</span>
            </div>
            <div class="card-body">
                <div class="card-info">
                    <span class="label">截止日期:</span>
                    <span>${task.deadline}</span>
                </div>
                <div class="card-info">
                    <span class="label">负责人:</span>
                    <span>${task.assignee}</span>
                </div>
                <div class="card-info">
                    <span class="label">状态:</span>
                    <span>${statusIcon} ${task.status}</span>
                </div>
                ${task.description ? `
                <div class="card-info">
                    <span class="label">描述:</span>
                    <span>${task.description}</span>
                </div>
                ` : ''}
            </div>
            ${task.status !== '已完成' ? `
            <div class="card-footer">
                <button class="btn btn-primary" onclick="completeTask(${task.id})">标记完成</button>
            </div>
            ` : ''}
        </div>
    `}).join('');
}

function filterTasks(status) {
    currentTaskFilter = status;
    
    // 更新按钮状态
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    loadTasks();
}

function showCreateTaskForm() {
    document.getElementById('create-task-form').style.display = 'block';
}

function hideCreateTaskForm() {
    document.getElementById('create-task-form').style.display = 'none';
    // 清空表单
    document.getElementById('task-title').value = '';
    document.getElementById('task-deadline').value = '';
    document.getElementById('task-priority').value = '中';
    document.getElementById('task-description').value = '';
}

function createTask() {
    const title = document.getElementById('task-title').value.trim();
    const deadline = document.getElementById('task-deadline').value.trim();
    const priority = document.getElementById('task-priority').value;
    const description = document.getElementById('task-description').value.trim();
    
    if (!title || !deadline) {
        alert('请填写任务标题和截止日期');
        return;
    }
    
    fetch('/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            deadline: deadline,
            priority: priority,
            description: description
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('任务创建成功！');
            hideCreateTaskForm();
            loadTasks();
        } else {
            alert('创建失败：' + data.error);
        }
    })
    .catch(error => {
        alert('网络错误：' + error.message);
    });
}

function completeTask(taskId) {
    if (!confirm('确定要标记这个任务为已完成吗？')) return;
    
    fetch(`/api/tasks/${taskId}/complete`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('任务已完成！');
            loadTasks();
        } else {
            alert('操作失败：' + data.message);
        }
    })
    .catch(error => {
        alert('网络错误：' + error.message);
    });
}

// ==================== 文档检索功能 ====================

function loadAllDocuments() {
    fetch('/api/documents')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayDocuments(data.documents);
        }
    })
    .catch(error => console.error('加载文档失败:', error));
}

function searchDocuments() {
    const keyword = document.getElementById('document-search').value.trim();
    
    if (!keyword) {
        loadAllDocuments();
        return;
    }
    
    fetch(`/api/documents?keyword=${encodeURIComponent(keyword)}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayDocuments(data.documents);
        }
    })
    .catch(error => console.error('搜索文档失败:', error));
}

function handleSearchKeyPress(event) {
    if (event.key === 'Enter') {
        searchDocuments();
    }
}

function displayDocuments(documents) {
    const container = document.getElementById('documents-list');
    
    if (documents.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="icon">🔍</div>
                <p>未找到相关文档</p>
            </div>
        `;
        return;
    }
    
    const typeIcons = {
        '云文档': '📝',
        '表格': '📊',
        '思维导图': '🧠'
    };
    
    container.innerHTML = documents.map(doc => `
        <div class="card">
            <div class="card-header">
                <div class="card-title">${typeIcons[doc.type] || '📄'} ${doc.title}</div>
                <span class="card-badge badge-status">${doc.type}</span>
            </div>
            <div class="card-body">
                <div class="card-info">
                    <span class="label">作者:</span>
                    <span>${doc.author}</span>
                </div>
                <div class="card-info">
                    <span class="label">更新时间:</span>
                    <span>${doc.update_time}</span>
                </div>
                <div class="card-info">
                    <span class="label">摘要:</span>
                    <span>${doc.summary}</span>
                </div>
                <div class="card-info">
                    <span class="label">标签:</span>
                    <span>${doc.tags.join(', ')}</span>
                </div>
            </div>
        </div>
    `).join('');
}
