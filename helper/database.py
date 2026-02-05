#存储对话和交易信息到SQLite数据库
#结构设计为方便之后迁移到PostgreSQL

import sqlite3
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "pr_agent.db")

def ensure_database():
    """确保数据库目录和表存在"""
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            creator_id TEXT PRIMARY KEY,
            creator_name TEXT,
            status TEXT DEFAULT 'in_progress',
            current_node TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id TEXT,
            sender TEXT,
            content TEXT,
            node TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES sessions(creator_id)
        )
    ''')
    
    # Deal info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deal_info (
            creator_id TEXT PRIMARY KEY,
            maximum_price TEXT,
            collab_type TEXT,
            delivery_type TEXT,
            video_type TEXT,
            schedule TEXT,
            product TEXT,
            creator_link TEXT,
            creator_price TEXT,
            creator_schedule TEXT,
            creator_product_choice TEXT,
            creator_address TEXT,
            FOREIGN KEY (creator_id) REFERENCES sessions(creator_id)
        )
    ''')
    
    # Retry counts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS retry_counts (
            creator_id TEXT,
            node TEXT,
            count INTEGER DEFAULT 0,
            PRIMARY KEY (creator_id, node),
            FOREIGN KEY (creator_id) REFERENCES sessions(creator_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """获取数据库连接"""
    ensure_database()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_session(creator_id: str, creator_name: str, task: list) -> str:
    """
    创建新的会话记录
    
    Args:
        creator_id: 博主唯一标识
        creator_name: 博主名称
        task: 任务列表
    
    Returns:
        creator_id
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    # 插入session
    cursor.execute('''
        INSERT OR REPLACE INTO sessions (creator_id, creator_name, status, current_node, created_at, updated_at)
        VALUES (?, ?, 'in_progress', '', ?, ?)
    ''', (creator_id, creator_name, now, now))
    
    # 插入deal_info
    cursor.execute('''
        INSERT OR REPLACE INTO deal_info (
            creator_id, maximum_price, collab_type, delivery_type, video_type, schedule, product,
            creator_link, creator_price, creator_schedule, creator_product_choice, creator_address
        ) VALUES (?, ?, ?, ?, ?, ?, ?, '', '', '', '', '')
    ''', (
        creator_id,
        task[0].get("maximum_price", ""),
        task[0].get("collab_type", ""),
        task[0].get("delivery_type", ""),
        task[0].get("video_type", ""),
        task[0].get("schedule", ""),
        task[0].get("product", ""),
    ))
    
    # 初始化retry_counts
    nodes = ["greet_run", "type_run", "schedule_run", "product_run", "address_run"]
    for node in nodes:
        cursor.execute('''
            INSERT OR REPLACE INTO retry_counts (creator_id, node, count)
            VALUES (?, ?, 0)
        ''', (creator_id, node))
    
    conn.commit()
    conn.close()
    return creator_id

def session_exists(creator_id: str) -> bool:
    """检查会话是否存在"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM sessions WHERE creator_id = ?', (creator_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_session(creator_id: str) -> Optional[Dict[str, Any]]:
    """获取会话信息"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions WHERE creator_id = ?', (creator_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def add_message(creator_id: str, sender: str, content: str, node: str):
    """
    添加消息到会话记录
    
    Args:
        creator_id: 博主唯一标识
        sender: 发送者 ("ai" 或 "human")
        content: 消息内容
        node: 当前节点名称
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO messages (creator_id, sender, content, node, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (creator_id, sender, content, node, now))
    
    cursor.execute('''
        UPDATE sessions SET current_node = ?, updated_at = ? WHERE creator_id = ?
    ''', (node, now, creator_id))
    
    conn.commit()
    conn.close()

def update_status(creator_id: str, status: str):
    """更新会话状态"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        UPDATE sessions SET status = ?, updated_at = ? WHERE creator_id = ?
    ''', (status, now, creator_id))
    conn.commit()
    conn.close()

def update_current_node(creator_id: str, node: str):
    """更新当前节点"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        UPDATE sessions SET current_node = ?, updated_at = ? WHERE creator_id = ?
    ''', (node, now, creator_id))
    conn.commit()
    conn.close()

def increment_retry_count(creator_id: str, node: str) -> int:
    """增加节点重试次数，返回当前次数"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE retry_counts SET count = count + 1 WHERE creator_id = ? AND node = ?
    ''', (creator_id, node))
    
    cursor.execute('''
        SELECT count FROM retry_counts WHERE creator_id = ? AND node = ?
    ''', (creator_id, node))
    
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0] if result else 0

def get_retry_count(creator_id: str, node: str) -> int:
    """获取节点重试次数"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT count FROM retry_counts WHERE creator_id = ? AND node = ?
    ''', (creator_id, node))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_conversation_history(creator_id: str) -> str:
    """获取完整对话历史，格式化为字符串"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sender, content FROM messages WHERE creator_id = ? ORDER BY timestamp
    ''', (creator_id,))
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        prefix = "AI媒介" if row["sender"] == "ai" else "博主"
        history.append(f"{prefix}: {row['content']}")
    return "\n".join(history)

def get_messages(creator_id: str) -> List[Dict[str, Any]]:
    """获取所有消息"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages WHERE creator_id = ? ORDER BY timestamp
    ''', (creator_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def list_sessions() -> List[Dict[str, Any]]:
    """列出所有会话"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ORDER BY updated_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_deal_info(creator_id: str) -> Optional[Dict[str, Any]]:
    """获取交易信息"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deal_info WHERE creator_id = ?', (creator_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
