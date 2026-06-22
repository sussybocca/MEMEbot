"""
MEMEBOT Bot Engagement System - Database Module
Handles user accounts, skin submissions, and organic engagement tracking
"""

import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import json


class Database:
    """Local SQLite database for user accounts and skin submissions"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / "data" / "bot_engagement.db"
        
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = str(db_path)
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Skin submissions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    skin_name TEXT NOT NULL,
                    skin_path TEXT NOT NULL,
                    skin_data TEXT,
                    analysis_data TEXT,
                    overall_score REAL DEFAULT 0.0,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    last_engagement_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Reviews table - supports thousands of bot reviews
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER NOT NULL,
                    bot_index INTEGER NOT NULL,
                    bot_name TEXT NOT NULL,
                    bot_persona TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    review_text TEXT NOT NULL,
                    days_elapsed REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (submission_id) REFERENCES submissions(id)
                )
            ''')
            
            # Create index for faster review queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_reviews_submission 
                ON reviews(submission_id, bot_index)
            ''')
            
            # Engagement metrics table with historical tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS engagement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER NOT NULL,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    saves INTEGER DEFAULT 0,
                    comments_count INTEGER DEFAULT 0,
                    average_rating REAL DEFAULT 0.0,
                    days_elapsed REAL DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (submission_id) REFERENCES submissions(id)
                )
            ''')
            
            # Daily engagement snapshots for growth tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS engagement_daily (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER NOT NULL,
                    day_number INTEGER NOT NULL,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    saves INTEGER DEFAULT 0,
                    new_comments INTEGER DEFAULT 0,
                    total_views INTEGER DEFAULT 0,
                    total_likes INTEGER DEFAULT 0,
                    snapshot_date TEXT NOT NULL,
                    FOREIGN KEY (submission_id) REFERENCES submissions(id)
                )
            ''')
            
            # Bot assignment tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER NOT NULL,
                    bot_index INTEGER NOT NULL,
                    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reviewed BOOLEAN DEFAULT FALSE,
                    reviewed_at TIMESTAMP,
                    UNIQUE(submission_id, bot_index),
                    FOREIGN KEY (submission_id) REFERENCES submissions(id)
                )
            ''')
            
            conn.commit()
    
    def create_account(self, username: str, password: str) -> tuple:
        """Create a new user account"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
                conn.commit()
                return True, "Account created successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, created_at FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            user = cursor.fetchone()
            
            if user:
                cursor.execute(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now().isoformat(), user[0])
                )
                conn.commit()
                
                return {
                    'id': user[0],
                    'username': user[1],
                    'created_at': user[2]
                }
        return None
    
    def save_submission(self, user_id: int, skin_name: str, skin_path: str, 
                       skin_data: Dict, analysis_data: Dict) -> int:
        """Save a skin submission with analysis data"""
        overall_score = analysis_data.get('overall_score', 5.0)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO submissions (user_id, skin_name, skin_path, skin_data, 
                                       analysis_data, overall_score, status)
                VALUES (?, ?, ?, ?, ?, ?, 'analyzing')
            ''', (user_id, skin_name, skin_path, json.dumps(skin_data), 
                  json.dumps(analysis_data), overall_score))
            
            submission_id = cursor.lastrowid
            
            # Create initial engagement record
            cursor.execute('''
                INSERT INTO engagement (submission_id, views, likes, shares, saves, 
                                       comments_count, average_rating, days_elapsed)
                VALUES (?, 0, 0, 0, 0, 0, 0.0, 0)
            ''', (submission_id,))
            
            # Create initial daily snapshot for day 0
            cursor.execute('''
                INSERT INTO engagement_daily (submission_id, day_number, views, likes, 
                                            shares, saves, new_comments, total_views, 
                                            total_likes, snapshot_date)
                VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, ?)
            ''', (submission_id, datetime.now().strftime('%Y-%m-%d')))
            
            conn.commit()
            return submission_id
    
    def save_review(self, submission_id: int, bot_index: int, bot_name: str, 
                   bot_persona: str, rating: int, review_text: str, 
                   days_elapsed: float = 0):
        """Save a bot review with bot tracking"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Insert the review
            cursor.execute('''
                INSERT INTO reviews (submission_id, bot_index, bot_name, bot_persona, 
                                   rating, review_text, days_elapsed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (submission_id, bot_index, bot_name, bot_persona, rating, 
                  review_text, days_elapsed))
            
            # Update or insert bot assignment
            cursor.execute('''
                INSERT OR REPLACE INTO bot_assignments 
                (submission_id, bot_index, reviewed, reviewed_at)
                VALUES (?, ?, TRUE, ?)
            ''', (submission_id, bot_index, datetime.now().isoformat()))
            
            # Update engagement metrics
            cursor.execute('''
                UPDATE engagement 
                SET comments_count = (
                    SELECT COUNT(*) FROM reviews WHERE submission_id = ?
                ),
                average_rating = (
                    SELECT AVG(CAST(rating AS REAL)) FROM reviews WHERE submission_id = ?
                ),
                days_elapsed = ?,
                updated_at = ?
                WHERE submission_id = ?
            ''', (submission_id, submission_id, days_elapsed, 
                  datetime.now().isoformat(), submission_id))
            
            conn.commit()
    
    def update_engagement_metrics(self, submission_id: int, views: int, likes: int,
                                 shares: int, saves: int, days_elapsed: float):
        """Update engagement metrics for organic growth"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE engagement 
                SET views = ?, likes = ?, shares = ?, saves = ?,
                    days_elapsed = ?, updated_at = ?
                WHERE submission_id = ?
            ''', (views, likes, shares, saves, days_elapsed, 
                  datetime.now().isoformat(), submission_id))
            
            conn.commit()
    
    def save_daily_snapshot(self, submission_id: int, day_number: int, 
                           day_data: Dict, total_views: int, total_likes: int):
        """Save a daily engagement snapshot"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO engagement_daily 
                (submission_id, day_number, views, likes, shares, saves, 
                 new_comments, total_views, total_likes, snapshot_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                submission_id, day_number,
                day_data.get('views', 0),
                day_data.get('likes', 0),
                day_data.get('shares', 0),
                day_data.get('saves', 0),
                day_data.get('new_comments', 0),
                total_views, total_likes,
                datetime.now().strftime('%Y-%m-%d')
            ))
            
            conn.commit()
    
    def get_daily_snapshots(self, submission_id: int) -> List[Dict]:
        """Get daily engagement snapshots for growth chart"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT day_number, views, likes, shares, saves, new_comments,
                       total_views, total_likes, snapshot_date
                FROM engagement_daily
                WHERE submission_id = ?
                ORDER BY day_number ASC
            ''', (submission_id,))
            
            snapshots = []
            for row in cursor.fetchall():
                snapshots.append({
                    'day_number': row[0],
                    'views': row[1],
                    'likes': row[2],
                    'shares': row[3],
                    'saves': row[4],
                    'new_comments': row[5],
                    'total_views': row[6],
                    'total_likes': row[7],
                    'snapshot_date': row[8]
                })
            return snapshots
    
    def get_submissions(self, user_id: int) -> List[Dict]:
        """Get all submissions for a user with current engagement"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.id, s.skin_name, s.skin_path, s.status, s.submitted_at,
                       s.overall_score, s.last_engagement_update,
                       e.views, e.likes, e.shares, e.saves, e.comments_count, 
                       e.average_rating, e.days_elapsed
                FROM submissions s
                LEFT JOIN engagement e ON s.id = e.submission_id
                WHERE s.user_id = ?
                ORDER BY s.submitted_at DESC
            ''', (user_id,))
            
            submissions = []
            for row in cursor.fetchall():
                submissions.append({
                    'id': row[0],
                    'skin_name': row[1],
                    'skin_path': row[2],
                    'status': row[3],
                    'submitted_at': row[4],
                    'overall_score': row[5],
                    'last_engagement_update': row[6],
                    'views': row[7] or 0,
                    'likes': row[8] or 0,
                    'shares': row[9] or 0,
                    'saves': row[10] or 0,
                    'comments_count': row[11] or 0,
                    'average_rating': row[12] or 0.0,
                    'days_elapsed': row[13] or 0
                })
            return submissions
    
    def get_reviews(self, submission_id: int) -> List[Dict]:
        """Get all reviews for a submission ordered by time"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT bot_name, bot_persona, rating, review_text, 
                       days_elapsed, created_at, bot_index
                FROM reviews
                WHERE submission_id = ?
                ORDER BY created_at ASC
            ''', (submission_id,))
            
            reviews = []
            for row in cursor.fetchall():
                reviews.append({
                    'bot_name': row[0],
                    'bot_persona': row[1],
                    'rating': row[2],
                    'review_text': row[3],
                    'days_elapsed': row[4],
                    'created_at': row[5],
                    'bot_index': row[6]
                })
            return reviews
    
    def get_bot_review_count(self, submission_id: int) -> int:
        """Get number of bots that have reviewed a submission"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM reviews WHERE submission_id = ?",
                (submission_id,)
            )
            return cursor.fetchone()[0]
    
    def get_next_unreviewed_bot(self, submission_id: int, 
                                reviewed_bots: set) -> Optional[int]:
        """Get the next bot index that hasn't reviewed this submission"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT bot_index FROM bot_assignments WHERE submission_id = ? AND reviewed = TRUE",
                (submission_id,)
            )
            assigned_bots = {row[0] for row in cursor.fetchall()}
            
            # Find first unassigned bot
            for i in range(5000):
                if i not in assigned_bots and i not in reviewed_bots:
                    return i
        
        return None
    
    def get_submission_analysis(self, submission_id: int) -> Optional[Dict]:
        """Get the analysis data for a submission"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT analysis_data, overall_score FROM submissions WHERE id = ?",
                (submission_id,)
            )
            row = cursor.fetchone()
            if row and row[0]:
                analysis = json.loads(row[0])
                analysis['overall_score'] = row[1]
                return analysis
        return None
    
    def update_submission_status(self, submission_id: int, status: str):
        """Update submission status"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE submissions SET status = ? WHERE id = ?",
                (status, submission_id)
            )
            conn.commit()
    
    def get_engagement(self, submission_id: int) -> Optional[Dict]:
        """Get current engagement metrics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT views, likes, shares, saves, comments_count, 
                       average_rating, days_elapsed, updated_at
                FROM engagement
                WHERE submission_id = ?
            ''', (submission_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'views': row[0],
                    'likes': row[1],
                    'shares': row[2],
                    'saves': row[3],
                    'comments_count': row[4],
                    'average_rating': row[5],
                    'days_elapsed': row[6],
                    'updated_at': row[7]
                }
        return None
    
    def _get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn