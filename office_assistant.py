"""办公协同功能模块"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class MeetingManager:
    """会议管理助手"""
    
    def __init__(self):
        self.meetings = []  # 存储会议列表
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        now = datetime.now()
        self.meetings = [
            {
                "id": 1,
                "title": "产品周会",
                "time": (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "duration": "60分钟",
                "participants": ["张三", "李四", "王五"],
                "location": "会议室A",
                "status": "已确认"
            },
            {
                "id": 2,
                "title": "技术评审会议",
                "time": (now + timedelta(days=1, hours=5)).strftime("%Y-%m-%d %H:%M"),
                "duration": "90分钟",
                "participants": ["赵六", "钱七"],
                "location": "会议室B",
                "status": "待确认"
            }
        ]
    
    def create_meeting(self, title: str, time: str, participants: List[str], 
                      duration: str = "60分钟", location: str = "待定") -> Dict:
        """创建会议"""
        meeting_id = len(self.meetings) + 1
        meeting = {
            "id": meeting_id,
            "title": title,
            "time": time,
            "duration": duration,
            "participants": participants,
            "location": location,
            "status": "已确认"
        }
        self.meetings.append(meeting)
        return meeting
    
    def list_meetings(self, date: Optional[str] = None) -> List[Dict]:
        """查看会议列表"""
        if date:
            return [m for m in self.meetings if date in m["time"]]
        return self.meetings
    
    def cancel_meeting(self, meeting_id: int) -> bool:
        """取消会议"""
        for meeting in self.meetings:
            if meeting["id"] == meeting_id:
                meeting["status"] = "已取消"
                return True
        return False
    
    def format_meeting_info(self, meeting: Dict) -> str:
        """格式化会议信息"""
        return f"""
📅 {meeting['title']}
   时间: {meeting['time']} ({meeting['duration']})
   地点: {meeting['location']}
   参会人: {', '.join(meeting['participants'])}
   状态: {meeting['status']}
"""


class TaskManager:
    """任务管理助手"""
    
    def __init__(self):
        self.tasks = []  # 存储任务列表
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        now = datetime.now()
        self.tasks = [
            {
                "id": 1,
                "title": "完成项目需求文档",
                "priority": "高",
                "deadline": (now + timedelta(days=2)).strftime("%Y-%m-%d"),
                "assignee": "我",
                "status": "进行中",
                "description": "编写Q2产品需求文档"
            },
            {
                "id": 2,
                "title": "代码审查",
                "priority": "中",
                "deadline": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
                "assignee": "我",
                "status": "待开始",
                "description": "审查新功能的代码实现"
            },
            {
                "id": 3,
                "title": "更新用户手册",
                "priority": "低",
                "deadline": (now + timedelta(days=5)).strftime("%Y-%m-%d"),
                "assignee": "我",
                "status": "已完成",
                "description": "根据新功能更新用户手册"
            }
        ]
    
    def create_task(self, title: str, deadline: str, priority: str = "中",
                   assignee: str = "我", description: str = "") -> Dict:
        """创建任务"""
        task_id = len(self.tasks) + 1
        task = {
            "id": task_id,
            "title": title,
            "priority": priority,
            "deadline": deadline,
            "assignee": assignee,
            "status": "待开始",
            "description": description
        }
        self.tasks.append(task)
        return task
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """查看任务列表"""
        if status:
            return [t for t in self.tasks if t["status"] == status]
        return self.tasks
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """更新任务状态"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                return True
        return False
    
    def format_task_info(self, task: Dict) -> str:
        """格式化任务信息"""
        priority_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(task["priority"], "⚪")
        status_icon = {"待开始": "⏸️", "进行中": "▶️", "已完成": "✅"}.get(task["status"], "❓")
        
        return f"""
{priority_icon} {task['title']}
   截止日期: {task['deadline']}
   负责人: {task['assignee']}
   状态: {status_icon} {task['status']}
   描述: {task['description']}
"""


class DocumentManager:
    """文档检索助手"""
    
    def __init__(self):
        self.documents = []  # 存储文档列表
        self._init_sample_data()
    
    def _init_sample_data(self):
        """初始化示例数据"""
        self.documents = [
            {
                "id": 1,
                "title": "Q2产品规划文档",
                "type": "云文档",
                "author": "张三",
                "update_time": "2024-04-10",
                "summary": "包含Q2产品路线图、功能规划和资源分配计划",
                "tags": ["产品", "规划", "Q2"]
            },
            {
                "id": 2,
                "title": "技术架构设计文档",
                "type": "云文档",
                "author": "李四",
                "update_time": "2024-04-08",
                "summary": "系统整体架构设计，包括微服务划分和技术选型",
                "tags": ["技术", "架构", "设计"]
            },
            {
                "id": 3,
                "title": "用户增长数据分析报告",
                "type": "表格",
                "author": "王五",
                "update_time": "2024-04-12",
                "summary": "Q1用户增长数据分析和Q2预测",
                "tags": ["数据", "分析", "用户增长"]
            },
            {
                "id": 4,
                "title": "项目周会纪要 - 第15周",
                "type": "云文档",
                "author": "赵六",
                "update_time": "2024-04-13",
                "summary": "本周项目进展、风险点和下周计划",
                "tags": ["会议", "纪要", "周报"]
            }
        ]
    
    def search_documents(self, keyword: str) -> List[Dict]:
        """搜索文档"""
        keyword_lower = keyword.lower()
        results = []
        for doc in self.documents:
            if (keyword_lower in doc["title"].lower() or 
                keyword_lower in doc["summary"].lower() or
                any(keyword_lower in tag.lower() for tag in doc["tags"])):
                results.append(doc)
        return results
    
    def get_document_by_id(self, doc_id: int) -> Optional[Dict]:
        """根据ID获取文档"""
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None
    
    def list_all_documents(self) -> List[Dict]:
        """列出所有文档"""
        return self.documents
    
    def format_document_info(self, doc: Dict) -> str:
        """格式化文档信息"""
        type_icon = {"云文档": "📝", "表格": "📊", "思维导图": "🧠"}.get(doc["type"], "📄")
        
        return f"""
{type_icon} {doc['title']}
   类型: {doc['type']}
   作者: {doc['author']}
   更新时间: {doc['update_time']}
   摘要: {doc['summary']}
   标签: {', '.join(doc['tags'])}
"""


class OfficeAssistant:
    """办公协同助手 - 统一管理各个功能模块"""
    
    def __init__(self):
        self.meeting_manager = MeetingManager()
        self.task_manager = TaskManager()
        self.document_manager = DocumentManager()
    
    def handle_meeting_command(self, command: str, params: Dict) -> str:
        """处理会议相关命令"""
        if command == "create":
            meeting = self.meeting_manager.create_meeting(
                title=params.get("title", "新会议"),
                time=params.get("time", "待定"),
                participants=params.get("participants", []),
                duration=params.get("duration", "60分钟"),
                location=params.get("location", "待定")
            )
            return f"✅ 会议创建成功！\n{self.meeting_manager.format_meeting_info(meeting)}"
        
        elif command == "list":
            meetings = self.meeting_manager.list_meetings(params.get("date"))
            if not meetings:
                return "📅 暂无会议安排"
            
            result = "📅 我的会议安排\n" + "="*40
            for meeting in meetings:
                result += self.meeting_manager.format_meeting_info(meeting)
            return result
        
        elif command == "cancel":
            meeting_id = params.get("meeting_id")
            if meeting_id and self.meeting_manager.cancel_meeting(meeting_id):
                return f"✅ 会议 {meeting_id} 已取消"
            return "❌ 取消会议失败，请检查会议ID"
        
        return "❓ 未知的会议命令"
    
    def handle_task_command(self, command: str, params: Dict) -> str:
        """处理任务相关命令"""
        if command == "create":
            task = self.task_manager.create_task(
                title=params.get("title", "新任务"),
                deadline=params.get("deadline", "待定"),
                priority=params.get("priority", "中"),
                assignee=params.get("assignee", "我"),
                description=params.get("description", "")
            )
            return f"✅ 任务创建成功！\n{self.task_manager.format_task_info(task)}"
        
        elif command == "list":
            tasks = self.task_manager.list_tasks(params.get("status"))
            if not tasks:
                return "✅ 暂无任务"
            
            result = "✅ 我的任务列表\n" + "="*40
            for task in tasks:
                result += self.task_manager.format_task_info(task)
            return result
        
        elif command == "complete":
            task_id = params.get("task_id")
            if task_id and self.task_manager.update_task_status(task_id, "已完成"):
                return f"✅ 任务 {task_id} 已标记为完成"
            return "❌ 更新任务状态失败，请检查任务ID"
        
        return "❓ 未知的任务命令"
    
    def handle_document_command(self, command: str, params: Dict) -> str:
        """处理文档相关命令"""
        if command == "search":
            keyword = params.get("keyword", "")
            docs = self.document_manager.search_documents(keyword)
            if not docs:
                return f'🔍 未找到与"{keyword}"相关的文档'
            
            result = f"🔍 搜索结果（共{len(docs)}个）\n" + "="*40
            for doc in docs:
                result += self.document_manager.format_document_info(doc)
            return result
        
        elif command == "list":
            docs = self.document_manager.list_all_documents()
            result = "📄 所有文档\n" + "="*40
            for doc in docs:
                result += self.document_manager.format_document_info(doc)
            return result
        
        return "❓ 未知的文档命令"
