"""上下文记忆管理模块"""
import json
from datetime import datetime
from typing import List, Dict, Optional


class MemoryManager:
    """记忆管理器 - 管理对话上下文和关键信息"""
    
    def __init__(self, max_short_term=10, max_long_term=50):
        """
        初始化记忆管理器
        
        Args:
            max_short_term: 短期记忆最大条数（对话轮数）
            max_long_term: 长期记忆最大条数（关键信息）
        """
        self.max_short_term = max_short_term
        self.max_long_term = max_long_term
        
        # 短期记忆：最近的对话历史
        self.short_term_memory: List[Dict] = []
        
        # 长期记忆：提取的关键信息
        self.long_term_memory: Dict[str, any] = {
            "user_preferences": {},  # 用户偏好
            "mentioned_entities": {},  # 提到的实体（人名、项目名等）
            "conversation_topics": [],  # 讨论过的主题
            "action_history": []  # 执行过的操作
        }
        
        # 会话元数据
        self.session_metadata = {
            "session_start": datetime.now().isoformat(),
            "total_messages": 0,
            "last_active": datetime.now().isoformat()
        }
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """
        添加消息到短期记忆
        
        Args:
            role: 角色（user/assistant）
            content: 消息内容
            metadata: 额外元数据
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.short_term_memory.append(message)
        self.session_metadata["total_messages"] += 1
        self.session_metadata["last_active"] = datetime.now().isoformat()
        
        # 限制短期记忆大小
        if len(self.short_term_memory) > self.max_short_term * 2:
            self.short_term_memory = self.short_term_memory[-self.max_short_term * 2:]
    
    def extract_key_info(self, message: str, intent: Dict):
        """
        从消息中提取关键信息到长期记忆
        
        Args:
            message: 用户消息
            intent: 意图识别结果
        """
        message_lower = message.lower()
        
        # 提取人名
        import re
        names = re.findall(r'[\u4e00-\u9fa5]{2,3}', message)
        for name in names:
            if len(name) >= 2 and name not in ["会议", "任务", "文档", "今天", "明天"]:
                if "mentioned_entities" not in self.long_term_memory:
                    self.long_term_memory["mentioned_entities"] = {}
                if name not in self.long_term_memory["mentioned_entities"]:
                    self.long_term_memory["mentioned_entities"][name] = {
                        "first_mentioned": datetime.now().isoformat(),
                        "context": intent.get("type", "general")
                    }
        
        # 记录讨论主题
        topic = intent.get("type", "general")
        if topic not in self.long_term_memory.get("conversation_topics", []):
            if "conversation_topics" not in self.long_term_memory:
                self.long_term_memory["conversation_topics"] = []
            self.long_term_memory["conversation_topics"].append(topic)
        
        # 记录操作历史
        if intent.get("type") in ["meeting", "task", "document"]:
            action = {
                "type": intent["type"],
                "action": "query" if any(word in message_lower for word in ["查看", "搜索", "有哪些"]) else "create",
                "timestamp": datetime.now().isoformat()
            }
            if "action_history" not in self.long_term_memory:
                self.long_term_memory["action_history"] = []
            self.long_term_memory["action_history"].append(action)
    
    def get_context_summary(self) -> str:
        """
        获取上下文摘要，用于增强AI回复
        
        Returns:
            上下文摘要文本
        """
        summary_parts = []
        
        # 添加最近的对话历史
        if self.short_term_memory:
            recent_conversations = self.short_term_memory[-self.max_short_term:]
            summary_parts.append("【最近对话】")
            for msg in recent_conversations:
                role_cn = "用户" if msg["role"] == "user" else "助手"
                content_preview = msg["content"][:100]
                summary_parts.append(f"{role_cn}: {content_preview}")
        
        # 添加提到的实体
        entities = self.long_term_memory.get("mentioned_entities", {})
        if entities:
            summary_parts.append("\n【提到的实体】")
            for name, info in list(entities.items())[-5:]:
                summary_parts.append(f"- {name} ({info.get('context', '未知')})")
        
        # 添加讨论主题
        topics = self.long_term_memory.get("conversation_topics", [])
        if topics:
            summary_parts.append(f"\n【讨论主题】{', '.join(topics[-5:])}")
        
        # 添加操作历史
        actions = self.long_term_memory.get("action_history", [])
        if actions:
            summary_parts.append("\n【最近操作】")
            for action in actions[-3:]:
                action_cn = "查询" if action["action"] == "query" else "创建"
                type_cn = {"meeting": "会议", "task": "任务", "document": "文档"}.get(action["type"], "其他")
                summary_parts.append(f"- {action_cn}{type_cn}")
        
        return "\n".join(summary_parts)
    
    def get_relevant_context(self, current_query: str) -> str:
        """
        根据当前查询获取相关的上下文
        
        Args:
            current_query: 当前用户查询
            
        Returns:
            相关的上下文信息
        """
        query_lower = current_query.lower()
        relevant_parts = []
        
        # 检查是否指代之前的内容
        if any(word in query_lower for word in ["刚才", "之前", "那个", "它", "他", "她"]):
            # 获取最近的助手回复
            for msg in reversed(self.short_term_memory):
                if msg["role"] == "assistant":
                    relevant_parts.append(f"【助手上次回复】{msg['content'][:200]}")
                    break
        
        # 如果查询涉及特定主题，提供相关上下文
        if "会议" in query_lower:
            meeting_actions = [a for a in self.long_term_memory.get("action_history", []) 
                             if a["type"] == "meeting"]
            if meeting_actions:
                relevant_parts.append(f"【会议相关操作】最近{len(meeting_actions)}次会议操作")
        
        elif "任务" in query_lower:
            task_actions = [a for a in self.long_term_memory.get("action_history", []) 
                          if a["type"] == "task"]
            if task_actions:
                relevant_parts.append(f"【任务相关操作】最近{len(task_actions)}次任务操作")
        
        elif "文档" in query_lower:
            doc_actions = [a for a in self.long_term_memory.get("action_history", []) 
                         if a["type"] == "document"]
            if doc_actions:
                relevant_parts.append(f"【文档相关操作】最近{len(doc_actions)}次文档操作")
        
        return "\n".join(relevant_parts)
    
    def clear_short_term(self):
        """清空短期记忆"""
        self.short_term_memory.clear()
    
    def clear_long_term(self):
        """清空长期记忆"""
        self.long_term_memory = {
            "user_preferences": {},
            "mentioned_entities": {},
            "conversation_topics": [],
            "action_history": []
        }
    
    def clear_all(self):
        """清空所有记忆"""
        self.clear_short_term()
        self.clear_long_term()
        self.session_metadata = {
            "session_start": datetime.now().isoformat(),
            "total_messages": 0,
            "last_active": datetime.now().isoformat()
        }
    
    def get_memory_stats(self) -> Dict:
        """获取记忆统计信息"""
        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_entities": len(self.long_term_memory.get("mentioned_entities", {})),
            "topics_discussed": len(self.long_term_memory.get("conversation_topics", [])),
            "actions_recorded": len(self.long_term_memory.get("action_history", [])),
            "total_messages": self.session_metadata["total_messages"]
        }
    
    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "short_term_memory": self.short_term_memory,
            "long_term_memory": self.long_term_memory,
            "session_metadata": self.session_metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryManager':
        """从字典恢复"""
        manager = cls()
        manager.short_term_memory = data.get("short_term_memory", [])
        manager.long_term_memory = data.get("long_term_memory", {})
        manager.session_metadata = data.get("session_metadata", {})
        return manager
