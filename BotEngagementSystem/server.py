"""
MEMEBOT Bot Engagement System - Flask Web Server
Serves the dashboard, handles uploads, and manages organic review process
Supports thousands of bots with realistic slow-growth engagement
"""

import os
import sys
import json
import threading
import time
import sqlite3
import importlib
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Any, List, Optional, Tuple

from flask import (
    Flask, render_template, request, redirect, url_for, 
    session, jsonify, send_from_directory, flash
)

sys.path.insert(0, str(Path(__file__).parent))

from database import Database
from skin_analyzer import SkinAnalyzer
from ai_reviewer import AIReviewer
from knowledge_base import get_bot_persona, BOT_PERSONALITIES


app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# Initialize components
db = Database()
analyzer = SkinAnalyzer()
reviewer = AIReviewer(analyzer)

# Configuration
UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'msk'}

# Organic growth settings
BOT_CHECK_INTERVAL = 3600  # Check for new bots every hour (3600 seconds)
ENGAGEMENT_UPDATE_INTERVAL = 86400  # Update engagement daily (86400 seconds)
TOTAL_AVAILABLE_BOTS = 5000

# Active background threads
active_threads = {}


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please sign in to access this page', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================
# AUTH ROUTES
# ============================================

@app.route('/')
def index():
    """Redirect to dashboard or login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        user = db.authenticate(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('register.html')
        
        if password != confirm:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        success, message = db.create_account(username, password)
        if success:
            flash('Account created successfully! Please sign in.', 'success')
            return redirect(url_for('login_page'))
        else:
            flash(message, 'error')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login_page'))


# ============================================
# DASHBOARD ROUTES
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing submissions and organic engagement"""
    user_id = session['user_id']
    username = session.get('username', 'User')
    submissions = db.get_submissions(user_id)
    
    total_views = sum(s.get('views', 0) for s in submissions)
    total_likes = sum(s.get('likes', 0) for s in submissions)
    total_reviews = sum(s.get('comments_count', 0) for s in submissions)
    total_shares = sum(s.get('shares', 0) for s in submissions)
    total_saves = sum(s.get('saves', 0) for s in submissions)
    
    avg_rating = 0.0
    if submissions:
        ratings = [s.get('average_rating', 0) for s in submissions if s.get('average_rating', 0) > 0]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
    
    stats = {
        'total_submissions': len(submissions),
        'total_views': total_views,
        'total_likes': total_likes,
        'total_reviews': total_reviews,
        'total_shares': total_shares,
        'total_saves': total_saves,
        'average_rating': round(avg_rating, 1)
    }
    
    # Calculate growth for each submission
    for submission in submissions:
        days = submission.get('days_elapsed', 0)
        if days < 1:
            submission['growth_phase'] = 'Just started'
        elif days < 7:
            submission['growth_phase'] = 'Early growth'
        elif days < 30:
            submission['growth_phase'] = 'Gaining traction'
        elif days < 90:
            submission['growth_phase'] = 'Growing steadily'
        elif days < 365:
            submission['growth_phase'] = 'Popular'
        else:
            submission['growth_phase'] = 'Established'
    
    return render_template('dashboard.html', 
                         submissions=submissions, 
                         stats=stats,
                         username=username)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    """Upload new skin for organic review process"""
    if request.method == 'POST':
        if 'skin_file' not in request.files:
            flash('No file selected', 'error')
            return render_template('upload.html', username=session.get('username'))
        
        file = request.files['skin_file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return render_template('upload.html', username=session.get('username'))
        
        if not allowed_file(file.filename):
            flash('Only .MSK files are allowed', 'error')
            return render_template('upload.html', username=session.get('username'))
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{file.filename}"
        filepath = UPLOAD_FOLDER / safe_filename
        file.save(str(filepath))
        
        skin_data = None
        
        try:
            possible_paths = [
                Path(__file__).parent.parent,
                Path(__file__).parent.parent / 'Src' / 'Skin',
                Path.cwd() / 'Src' / 'Skin',
            ]
            
            for path in possible_paths:
                skin_encryptor_path = path / 'skin_encryptor.py'
                if skin_encryptor_path.exists():
                    sys.path.insert(0, str(path))
                    SkinEncryptorModule = importlib.import_module('skin_encryptor')
                    SkinEncryptor = SkinEncryptorModule.SkinEncryptor
                    encryptor = SkinEncryptor()
                    skin_data = encryptor.load_skin_file(filepath)
                    if skin_data:
                        break
            
            if not skin_data:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.startswith('SK3'):
                    lines = content.split('\n', 2)
                    if len(lines) >= 3:
                        try:
                            SkinEncryptorModule = importlib.import_module('skin_encryptor')
                            SKCipher = SkinEncryptorModule.SKCipher
                            cipher = SKCipher()
                            decrypted = cipher.decrypt(lines[2])
                            if decrypted:
                                skin_data = json.loads(decrypted.decode('utf-8'))
                        except Exception:
                            pass
                
                if not skin_data:
                    try:
                        skin_data = json.loads(content)
                    except Exception:
                        pass
            
            if not skin_data:
                flash('Failed to read MSK file.', 'error')
                if filepath.exists():
                    filepath.unlink()
                return render_template('upload.html', username=session.get('username'))
            
        except Exception as e:
            flash(f'Error reading skin file: {str(e)}', 'error')
            if filepath.exists():
                filepath.unlink()
            return render_template('upload.html', username=session.get('username'))
        
        analysis = analyzer.analyze_skin_file(skin_data)
        
        skin_name = skin_data.get('name', file.filename.replace('.msk', ''))
        submission_id = db.save_submission(
            session['user_id'], 
            skin_name, 
            str(filepath), 
            skin_data, 
            analysis
        )
        
        # Start the organic growth simulation in background
        thread = threading.Thread(
            target=run_organic_growth_simulation,
            args=(submission_id,),
            daemon=True
        )
        thread.start()
        active_threads[submission_id] = thread
        
        flash(f'Skin "{skin_name}" submitted! Organic engagement will grow naturally over time. First bots will discover it within hours.', 'success')
        return redirect(url_for('submission_detail', submission_id=submission_id))
    
    return render_template('upload.html', username=session.get('username'))


@app.route('/submission/<int:submission_id>')
@login_required
def submission_detail(submission_id: int):
    """View details and reviews for a specific submission"""
    username = session.get('username', 'User')
    submissions = db.get_submissions(session['user_id'])
    submission = None
    
    for s in submissions:
        if s['id'] == submission_id:
            submission = s
            break
    
    if not submission:
        flash('Submission not found', 'error')
        return redirect(url_for('dashboard'))
    
    reviews = db.get_reviews(submission_id)
    snapshots = db.get_daily_snapshots(submission_id)
    
    days_elapsed = submission.get('days_elapsed', 0)
    
    # Calculate growth metrics
    if days_elapsed < 1/24:  # Less than an hour
        growth_stage = 'Just launched'
        next_milestone = 'First views appearing soon'
    elif days_elapsed < 1:
        growth_stage = 'First hours'
        next_milestone = 'Gaining initial traction'
    elif days_elapsed < 3:
        growth_stage = 'Early discovery'
        next_milestone = 'More bots finding your skin'
    elif days_elapsed < 7:
        growth_stage = 'First week'
        next_milestone = 'Building momentum'
    elif days_elapsed < 30:
        growth_stage = 'First month'
        next_milestone = 'Establishing presence'
    elif days_elapsed < 90:
        growth_stage = 'Growing'
        next_milestone = 'Reaching wider audience'
    elif days_elapsed < 365:
        growth_stage = 'Popular'
        next_milestone = 'Becoming well-known'
    else:
        growth_stage = 'Established'
        next_milestone = 'Maintaining popularity'
    
    return render_template(
        'reviews.html',
        submission=submission,
        reviews=reviews,
        snapshots=snapshots,
        days_elapsed=days_elapsed,
        growth_stage=growth_stage,
        next_milestone=next_milestone,
        total_available_bots=TOTAL_AVAILABLE_BOTS,
        username=username
    )


# ============================================
# API ROUTES
# ============================================

@app.route('/api/submission/<int:submission_id>/status')
@login_required
def submission_status(submission_id: int):
    """API endpoint to check real-time submission status"""
    reviews = db.get_reviews(submission_id)
    engagement = db.get_engagement(submission_id)
    
    if not engagement:
        return jsonify({'error': 'Not found'}), 404
    
    submissions = db.get_submissions(session['user_id'])
    submission = None
    for s in submissions:
        if s['id'] == submission_id:
            submission = s
            break
    
    days_elapsed = engagement.get('days_elapsed', 0)
    
    return jsonify({
        'reviews_count': len(reviews),
        'views': engagement.get('views', 0),
        'likes': engagement.get('likes', 0),
        'shares': engagement.get('shares', 0),
        'saves': engagement.get('saves', 0),
        'average_rating': engagement.get('average_rating', 0),
        'days_elapsed': round(days_elapsed, 2),
        'growth_stage': get_growth_stage(days_elapsed),
        'status': submission.get('status', 'active') if submission else 'active'
    })


@app.route('/api/submission/<int:submission_id>/reviews')
@login_required
def get_reviews_api(submission_id: int):
    """API endpoint to get reviews as JSON"""
    reviews = db.get_reviews(submission_id)
    engagement = db.get_engagement(submission_id)
    
    return jsonify({
        'reviews': reviews,
        'count': len(reviews),
        'engagement': engagement
    })


@app.route('/api/submission/<int:submission_id>/growth')
@login_required
def get_growth_data(submission_id: int):
    """API endpoint for growth chart data"""
    snapshots = db.get_daily_snapshots(submission_id)
    
    chart_data = []
    for snap in snapshots:
        chart_data.append({
            'day': snap['day_number'],
            'views': snap['total_views'],
            'likes': snap['total_likes'],
            'comments': snap['new_comments'],
            'date': snap['snapshot_date']
        })
    
    return jsonify({
        'growth_data': chart_data,
        'total_days': len(chart_data)
    })


# ============================================
# ORGANIC GROWTH SIMULATION
# ============================================

def get_growth_stage(days_elapsed: float) -> str:
    """Get the current growth stage based on days elapsed"""
    if days_elapsed < 1/24:
        return 'Just launched'
    elif days_elapsed < 1:
        return 'First hours'
    elif days_elapsed < 3:
        return 'Early discovery'
    elif days_elapsed < 7:
        return 'First week'
    elif days_elapsed < 30:
        return 'First month'
    elif days_elapsed < 90:
        return 'Growing'
    elif days_elapsed < 365:
        return 'Popular'
    else:
        return 'Established'


def run_organic_growth_simulation(submission_id: int):
    """
    Main organic growth simulation that runs in the background.
    Simulates realistic slow growth over days/months/years.
    """
    print(f"\n[Organic Growth] Starting simulation for submission #{submission_id}")
    print(f"[Organic Growth] Bots will discover this skin organically over time")
    print(f"[Organic Growth] First reviews will appear within hours")
    print(f"[Organic Growth] Engagement will grow slowly and naturally\n")
    
    submission_start = datetime.now()
    reviewer_instance = AIReviewer(analyzer)
    reviewer_instance.set_submission_start_time(submission_start)
    reviewer_instance.total_bots_available = TOTAL_AVAILABLE_BOTS
    
    last_daily_snapshot = 0
    last_engagement_update = 0
    
    while True:
        try:
            current_time = datetime.now()
            days_elapsed = (current_time - submission_start).total_seconds() / 86400.0
            day_number = int(days_elapsed)
            
            # Update engagement metrics periodically
            if days_elapsed - last_engagement_update >= 1/24:  # Every hour
                analysis = db.get_submission_analysis(submission_id)
                if analysis:
                    overall_score = analysis.get('overall_score', 5.0)
                    engagement = reviewer_instance.generate_organic_engagement(
                        days_elapsed, overall_score
                    )
                    
                    db.update_engagement_metrics(
                        submission_id,
                        engagement['views'],
                        engagement['likes'],
                        engagement['shares'],
                        engagement['saves'],
                        days_elapsed
                    )
                    
                    last_engagement_update = days_elapsed
            
            # Save daily snapshot
            if day_number > last_daily_snapshot:
                analysis = db.get_submission_analysis(submission_id)
                if analysis:
                    overall_score = analysis.get('overall_score', 5.0)
                    
                    # Calculate today's new views and likes
                    yesterday_engagement = reviewer_instance.generate_organic_engagement(
                        max(0, day_number - 1), overall_score
                    )
                    today_engagement = reviewer_instance.generate_organic_engagement(
                        day_number, overall_score
                    )
                    
                    day_data = {
                        'views': today_engagement['views'] - yesterday_engagement['views'],
                        'likes': today_engagement['likes'] - yesterday_engagement['likes'],
                        'shares': today_engagement['shares'] - yesterday_engagement['shares'],
                        'saves': today_engagement['saves'] - yesterday_engagement['saves'],
                        'new_comments': today_engagement['comments_count'] - yesterday_engagement['comments_count']
                    }
                    
                    db.save_daily_snapshot(
                        submission_id, day_number, day_data,
                        today_engagement['views'], today_engagement['likes']
                    )
                    
                    last_daily_snapshot = day_number
                    print(f"[Organic Growth] Day {day_number}: {today_engagement['views']} views, {today_engagement['likes']} likes, {today_engagement['comments_count']} reviews")
            
            # Check if a new bot should review
            next_bot = reviewer_instance.get_next_bot_to_review(days_elapsed)
            if next_bot:
                analysis = db.get_submission_analysis(submission_id)
                if analysis:
                    # Generate and save the review
                    review = reviewer_instance.generate_review(analysis, next_bot, days_elapsed)
                    
                    db.save_review(
                        submission_id,
                        review['bot_index'],
                        review['bot_name'],
                        review['bot_persona'],
                        review['rating'],
                        review['review_text'],
                        days_elapsed
                    )
                    
                    print(f"[Organic Growth] Bot #{review['bot_index']} ({review['bot_name']}) reviewed after {days_elapsed:.1f} days - Rating: {review['rating']}/5")
                    
                    # Update submission status if enough reviews
                    review_count = db.get_bot_review_count(submission_id)
                    if review_count >= 5:
                        db.update_submission_status(submission_id, 'active')
                    if review_count >= 100:
                        db.update_submission_status(submission_id, 'popular')
                    if review_count >= 1000:
                        db.update_submission_status(submission_id, 'trending')
            
            # Wait before next check (every hour in real time)
            time.sleep(BOT_CHECK_INTERVAL)
            
        except Exception as e:
            print(f"[Organic Growth] Error in simulation: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(60)  # Wait a minute before retrying on error


# ============================================
# STATIC FILES
# ============================================

@app.route('/static/<path:filename>')
def serve_static(filename: str):
    """Serve static files"""
    return send_from_directory('static', filename)


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


# ============================================
# CONTEXT PROCESSOR
# ============================================

@app.context_processor
def inject_now():
    return {'now': datetime.now()}


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("  🎭 MEMEBOT Bot Engagement System")
    print("  AI-Powered Organic Growth Platform")
    print("=" * 60)
    print(f"  Database: {db.db_path}")
    print(f"  Upload folder: {UPLOAD_FOLDER}")
    print(f"  Total available bots: {TOTAL_AVAILABLE_BOTS}")
    print(f"  Bot check interval: {BOT_CHECK_INTERVAL}s")
    print(f"  Engagement update: {ENGAGEMENT_UPDATE_INTERVAL}s")
    print(f"  Server: http://127.0.0.1:5050")
    print("=" * 60)
    print()
    print("  Organic Growth Timeline:")
    print("    Hours 1-3:   First views trickle in (0-5 views)")
    print("    Day 1:       ~5-20 views, first review")
    print("    Day 3:       ~30-60 views, 2-3 reviews")
    print("    Day 7:       ~100-300 views, 5-10 reviews")
    print("    Day 30:      ~500-2000 views, 50-200 reviews")
    print("    Day 90:      ~5K-20K views, 500-2000 reviews")
    print("    Day 365:     ~50K-500K views, 5000+ reviews")
    print("=" * 60)
    print()
    print("  Press Ctrl+C to stop the server")
    print()
    
    app.run(host='127.0.0.1', port=5050, debug=False)