from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os
from flask_migrate import Migrate
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from datetime import datetime, timedelta   # ← add timedelta
# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biology_system.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Internationalization dictionary
I18N = {
    "en": {
        "site_title": "Biology Study Guide",
        "brand": "BioGuide",
        "nav_home": "Home",
        "nav_guide": "Study Guide",
        "nav_chapters": "Chapters",
        "footer_rights": "All rights reserved",
        "footer_open_guide": "Open Biology Guide",
        "hero_title": "Master Biology with Interactive Learning",
        "hero_subtitle": "Explore comprehensive biology topics in both English and Kurdish. From microscopic structures to complex organisms.",
        "cta_open_guide": "Start Learning",
        "cta_view_chapters": "View All Chapters",
        "card_histology": "Study of tissues and cellular structures under microscope.",
        "card_embryology": "Development processes from conception to birth.",
        "card_plant": "Plant structure, function, and physiological processes.",
        "card_micro": "Microscopic organisms and their biological roles.",
        "chapters_title": "Biology Chapters",
        "chapters_intro": "Comprehensive coverage of essential biology topics.",
        "back_home": "← Back to Home",
        "current_chapter_title": "Interactive Biology Guide",
        "current_chapter_subtitle": "Comprehensive study materials for biology students",
        "all_chapters": "All Study Chapters",
        "chapter": "Chapter",
        "view_chapter": "Study Chapter",
        "ch1_title": "Histology",
        "ch2_title": "Embryology",
        "ch3_title": "Plant Anatomy",
        "ch4_title": "Parasitology",
        "ch5_title": "Hematology",
        "ch6_title": "Microbiology",
        "ch7_title": "Entomology",
        "ch8_title": "Algae Studies",
        "c1": "Study of tissues, epithelial structures, and microscopic anatomy.",
        "c2": "Developmental biology from fertilization through embryonic stages.",
        "c3": "Plant organs, root systems, stems, leaves and their functions.",
        "c4": "Parasitic organisms and their relationships with host species.",
        "c5": "Blood cells, hematological disorders, and diagnostic techniques.",
        "c6": "Bacteria, viruses, fungi and other microscopic life forms.",
        "c7": "Insect anatomy, classification, and ecological importance.",
        "c8": "Algal diversity, classification, and environmental significance.",
        "admin_login_text": "Admin Access",
        "dashboard": "Dashboard",
        "chapters": "Chapters",
        "slides": "Study Materials",
        "users": "Users",
        "analytics": "Analytics",
        "settings": "Settings",
        "logout": "Logout",
        "welcome": "Welcome",
        "total_chapters": "Total Chapters",
        "total_slides": "Study Materials",
        "total_users": "Active Users",
        "activity": "System Activity",
        "recent_activity": "Recent Activity",
        "quick_actions": "Quick Actions",
        "add_new_slide": "Add Study Material",
        "edit_chapters": "Manage Chapters",
        "export_data": "Export Data",
        "view_analytics": "View Reports",
        "backup_system": "System Backup",
        "view_website": "View Website",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "login_required": "Please log in to access this page",
        "invalid_credentials": "Invalid username or password",
        "login_success": "Successfully logged in",
        "logout_success": "Successfully logged out",
        "manage_slides": "Manage Slides",
        "add_chapter": "Add Chapter",
        "edit_chapter": "Edit Chapter",
        "delete_chapter": "Delete Chapter",
        "add_slide": "Add Slide",
        "edit_slide": "Edit Slide",
        "delete_slide": "Delete Slide",
        "chapter_title": "Chapter Title",
        "chapter_description": "Chapter Description",
        "slide_title": "Slide Title",
        "slide_content": "Slide Content",
        "image_url": "Image URL",
        "components": "Components",
        "location": "Location",
        "functions": "Functions",
        "order": "Order",
        "save": "Save",
        "cancel": "Cancel",
        "success_added": "Successfully added",
        "success_updated": "Successfully updated",
        "success_deleted": "Successfully deleted",
        "error_occurred": "An error occurred",
        "users_management": "Users Management",
        "add_user": "Add User",
        "edit_user": "Edit User",
        "user_status": "User Status",
        "role": "Role",
        "email": "Email",
        "last_login": "Last Login",
        "created_at": "Created At",
        "total_activities": "Total Activities",
        "super_admin": "Super Admin",
        "chapter_admin": "Chapter Admin",
        "active": "Active",
        "inactive": "Inactive",
        "never": "Never",
        "system_settings": "System Settings",
        "profile_settings": "Profile Settings",
        "backup_database": "Backup Database",
        "clear_old_logs": "Clear Old Logs",
        "reset_view_counts": "Reset View Counts",
        "current_password": "Current Password",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "system_information": "System Information",
        "database_size": "Database Size",
        "flask_version": "Flask Version",
        "python_version": "Python Version",
        "maintenance": "Maintenance"
    },
    "ckb": {
        "site_title": "ڕێبەری خوێندنی بایۆلۆجی",
        "brand": "ڕێبەری بایۆلۆجی",
        "nav_home": "سەرەکی",
        "nav_guide": "ڕێبەری خوێندن",
        "nav_chapters": "بابەتەکان",
        "footer_rights": "هەموو مافەکان پارێزراون",
        "footer_open_guide": "کردنەوەی ڕێبەری بایۆلۆجی",
        "hero_title": "فێربوونی بایۆلۆجی بە شێوازێکی تەکنەلۆجی",
        "hero_subtitle": "گەڕان لە بابەتە گرنگەکانی بایۆلۆجی بە زمانی ئینگلیزی و کوردی. لە پێکهاتە مایکرۆسکۆپییەکانەوە تا زیندەوەرە ئاڵۆزەکان.",
        "cta_open_guide": "دەستپێکردنی فێربوون",
        "cta_view_chapters": "بینینی هەموو بابەتەکان",
        "card_histology": "خوێندنی شانەکان و پێکهاتە خانەییەکان لەژێر مایکرۆسکۆپ.",
        "card_embryology": "پرۆسەکانی گەشەپێدان لە کتنییەوە تا لەدایکبوون.",
        "card_plant": "پێکهاتە، کارەکان و پرۆسە فیزیۆلۆجیەکانی ڕووەک.",
        "card_micro": "زیندەوەرە مایکرۆسکۆپییەکان و ڕۆڵە بایۆلۆجیەکانیان.",
        "chapters_title": "بابەتەکانی بایۆلۆجی",
        "chapters_intro": "داپۆشینی بەرفراوان بۆ بابەتە گرنگەکانی بایۆلۆجی.",
        "back_home": "← گەڕانەوە بۆ سەرەکی",
        "current_chapter_title": "ڕێبەری تەکنەلۆجی بایۆلۆجی",
        "current_chapter_subtitle": "کەرەستەی خوێندنی بەرفراوان بۆ خوێندکارانی بایۆلۆجی",
        "all_chapters": "هەموو بابەتەکانی خوێندن",
        "chapter": "بابەت",
        "view_chapter": "خوێندنی بابەت",
        "ch1_title": "هیستۆلۆجی",
        "ch2_title": "ئێمبرۆلۆجی",
        "ch3_title": "ئەناتۆمیای ڕووەک",
        "ch4_title": "پاراسیتۆلۆجی",
        "ch5_title": "هیماتۆلۆجی",
        "ch6_title": "مایکرۆبایۆلۆجی",
        "ch7_title": "ئینتۆمۆلۆجی",
        "ch8_title": "خوێندنی ئاڵگا",
        "c1": "خوێندنی شانەکان، پێکهاتە ئەپیتێلیەکان و ئەناتۆمی مایکرۆسکۆپی.",
        "c2": "بایۆلۆجی گەشەپێدان لە کتنییەوە بەنێو قۆناغەکانی ئێمبرۆ.",
        "c3": "ئەندامەکانی ڕووەک، سیستەمی ڕەگ، شەق و گەڵا و کارەکانیان.",
        "c4": "زیندەوەرە گیرۆکەکان و پەیوەندییان بە جۆرە میوان.",
        "c5": "خانەکانی خوێن، نەخۆشی خوێن و تەکنیکەکانی دەستنیشانکردن.",
        "c6": "بەکتریا، ڤایرۆس، کەمترشی و شێوەکانی دیکەی ژیانی مایکرۆسکۆپی.",
        "c7": "ئەناتۆمی مێروو، پۆلێنکردن و گرنگی ژینگەیی.",
        "c8": "جۆراوجۆری ئاڵگا، پۆلێنکردن و گرنگی ژینگەیی.",
        "admin_login_text": "دەستپێگەیشتنی بەڕێوەبەر",
        "dashboard": "داشبۆرد",
        "chapters": "بابەتەکان",
        "slides": "کەرەستەی خوێندن",
        "users": "بەکارهێنەران",
        "analytics": "ڕاپۆرتەکان",
        "settings": "ڕێکخستنەکان",
        "logout": "دەرچوون",
        "welcome": "بەخێرهاتیت",
        "total_chapters": "کۆی بابەتەکان",
        "total_slides": "کەرەستەی خوێندن",
        "total_users": "بەکارهێنەرە چالاکەکان",
        "activity": "چالاکی سیستەم",
        "recent_activity": "چالاکی دوایی",
        "quick_actions": "کردارە خێراکان",
        "add_new_slide": "زیادکردنی کەرەستەی خوێندن",
        "edit_chapters": "بەڕێوەبردنی بابەتەکان",
        "export_data": "ناردنی داتا",
        "view_analytics": "بینینی ڕاپۆرتەکان",
        "backup_system": "پاڵپشتکردنی سیستەم",
        "view_website": "بینینی ماڵپەڕ",
        "username": "ناوی بەکارهێنەر",
        "password": "تێپەڕەوشە",
        "login": "چوونەژوورەوە",
        "login_required": "تکایە بچۆ ژوورەوە بۆ دەستپێگەیشتن بەم لاپەڕەیە",
        "invalid_credentials": "ناوی بەکارهێنەر یان تێپەڕەوشە هەڵەیە",
        "login_success": "بە سەرکەوتووی چوویتە ژوورەوە",
        "logout_success": "بە سەرکەوتووی دەرچوویت",
        "manage_slides": "بەڕێوەبردنی سلایدەکان",
        "add_chapter": "زیادکردنی بابەت",
        "edit_chapter": "دەستکاری بابەت",
        "delete_chapter": "سڕینەوەی بابەت",
        "add_slide": "زیادکردنی سلاید",
        "edit_slide": "دەستکاری سلاید",
        "delete_slide": "سڕینەوەی سلاید",
        "chapter_title": "سەرناوی بابەت",
        "chapter_description": "پێناسەی بابەت",
        "slide_title": "سەرناوی سلاید",
        "slide_content": "ناوەڕۆکی سلاید",
        "image_url": "بەستەری وێنە",
        "components": "پێکهاتەکان",
        "location": "شوێن",
        "functions": "کارەکان",
        "order": "ڕیزبەندی",
        "save": "هەڵگرتن",
        "cancel": "هەڵوەشاندنەوە",
        "success_added": "بە سەرکەوتووی زیادکرا",
        "success_updated": "بە سەرکەوتووی نوێکرایەوە",
        "success_deleted": "بە سەرکەوتووی سڕایەوە",
        "error_occurred": "هەڵەیەک ڕوویدا",
        "users_management": "بەڕێوەبردنی بەکارهێنەران",
        "add_user": "زیادکردنی بەکارهێنەر",
        "edit_user": "دەستکاری بەکارهێنەر",
        "user_status": "دۆخی بەکارهێنەر",
        "role": "ڕۆڵ",
        "email": "ئیمەیڵ",
        "last_login": "دوایین چوونەژوورەوە",
        "created_at": "بەرواری دروستکردن",
        "total_activities": "کۆی چالاکیەکان",
        "super_admin": "بەڕێوەبەری گشتی",
        "chapter_admin": "بەڕێوەبەری بابەت",
        "active": "چالاک",
        "inactive": "ناچالاک",
        "never": "هەرگیز",
        "system_settings": "ڕێکخستنی سیستەم",
        "profile_settings": "ڕێکخستنی پرۆفایل",
        "backup_database": "پاڵپشتکردنی بنکەی دراو",
        "clear_old_logs": "پاککردنەوەی تۆمارە کۆنەکان",
        "reset_view_counts": "گەڕاندنەوەی ئامارەکان",
        "current_password": "تێپەڕەوشەی ئێستا",
        "new_password": "تێپەڕەوشەی نوێ",
        "confirm_password": "پشتڕاستکردنەوەی تێپەڕەوشە",
        "system_information": "زانیاریی سیستەم",
        "database_size": "قەبارەی بنکەی دراو",
        "flask_version": "وەشانی Flask",
        "python_version": "وەشانی Python",
        "maintenance": "چاکسازی"
    }
}


# Enhanced Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='chapter_admin')
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    chapter = db.relationship('Chapter', backref='assigned_user', foreign_keys=[chapter_id])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'

    @property
    def is_admin(self):
        return self.role in ['super_admin', 'chapter_admin']

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ckb = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_ckb = db.Column(db.Text)
    icon = db.Column(db.String(50), default='fas fa-book')
    order = db.Column(db.Integer, default=1, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    slides = db.relationship('Slide', backref='chapter_ref', lazy='dynamic', cascade='all, delete-orphan')

    def get_title(self, lang='en'):
        return self.title_ckb if lang == 'ckb' else self.title_en

    def get_description(self, lang='en'):
        return self.description_ckb if lang == 'ckb' else self.description_en

    def get_slides_count(self):
        return self.slides.count()

    def get_total_views(self):
        slide_views = sum(slide.view_count for slide in self.slides)
        return self.view_count + slide_views

class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ckb = db.Column(db.String(200), nullable=False)
    content_en = db.Column(db.Text)
    content_ckb = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    order = db.Column(db.Integer, default=1)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    components = db.Column(db.Text)
    location = db.Column(db.Text)
    functions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def get_title(self, lang='en'):
        return self.title_ckb if lang == 'ckb' else self.title_en

    def get_content(self, lang='en'):
        return self.content_ckb if lang == 'ckb' else self.content_en

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='activities')

class SystemStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow().date, unique=True)
    total_views = db.Column(db.Integer, default=0)
    chapter_views = db.Column(db.Integer, default=0)
    slide_views = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Authentication decorators
def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("admin_login", lang=kwargs.get('lang', 'en')))
        if not current_user.is_super_admin:
            flash("Only super admins can access this page.", "danger")
            return redirect(url_for("admin_dashboard", lang=kwargs.get('lang', 'en')))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("admin_login", lang=kwargs.get('lang', 'en')))
        if not current_user.is_admin:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("admin_dashboard", lang=kwargs.get('lang', 'en')))
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Fixed deprecated query.get()


# Helper functions
def pick_lang(lang):
    """Language picker with fallback to English"""
    if lang not in I18N:
        lang = "en"
    return lang, I18N[lang], ("ckb" if lang == "ckb" else "en")


@app.context_processor
def inject_globals():
    lang = request.view_args.get('lang', 'en') if request.view_args else 'en'
    _, t, lang_code = pick_lang(lang)
    return dict(t=t, lang=lang, lang_code=lang_code)


def log_activity(action, target_type, target_id, description=''):
    """Log user activity"""
    if current_user.is_authenticated:
        activity = Activity(
            user_id=current_user.id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            description=description,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )
        db.session.add(activity)
        try:
            db.session.commit()
        except:
            db.session.rollback()


def update_daily_stats():
    """Update daily statistics"""
    today = datetime.utcnow().date()
    stats = SystemStats.query.filter_by(date=today).first()

    if not stats:
        stats = SystemStats(date=today)
        db.session.add(stats)

    # Calculate totals from database
    stats.chapter_views = db.session.query(db.func.sum(Chapter.view_count)).scalar() or 0
    stats.slide_views = db.session.query(db.func.sum(Slide.view_count)).scalar() or 0
    stats.total_views = stats.chapter_views + stats.slide_views
    stats.active_users = User.query.filter_by(is_active=True).count()

    try:
        db.session.commit()
    except:
        db.session.rollback()


def create_sample_data():
    """Create sample data if database is empty"""
    if Chapter.query.count() == 0:
        # Create chapters with proper data structure
        chapters_data = [
            (1, "Histology", "هیستۆلۆجی",
             "The study of tissues and their microscopic structure, including epithelial, connective, muscle, and nervous tissues.",
             "خوێندنی شانەکان و پێکهاتە مایکرۆسکۆپیەکانیان، لەوانە شانەکانی ئەپیتێلیاڵ، پەیوەست، ماسولکە و نەرڤی.",
             "fas fa-microscope"),

            (2, "Embryology", "ئێمبرۆلۆجی",
             "Developmental biology focusing on embryonic development from fertilization through organogenesis.",
             "بایۆلۆجی گەشەپێدان کە سەرنج دەدات بە گەشەپێدانی ئێمبرۆ لە کتنییەوە تا درووستبوونی ئەندامەکان.",
             "fas fa-baby"),

            (3, "Plant Anatomy", "ئەناتۆمیای ڕووەک",
             "Structure and function of plant organs including roots, stems, leaves, and reproductive structures.",
             "پێکهاتە و کارەکانی ئەندامەکانی ڕووەک لەوانە ڕەگ، شەق، گەڵا و پێکهاتەکانی زاوزێ.",
             "fas fa-leaf"),

            (4, "Parasitology", "پاراسیتۆلۆجی",
             "Study of parasites, their life cycles, host-parasite relationships, and parasitic diseases.",
             "خوێندنی گیرۆکەکان، سوڕی ژیانیان، پەیوەندی میوان-گیرۆکە و نەخۆشیە گیرۆکیەکان.",
             "fas fa-bug"),

            (5, "Hematology", "هیماتۆلۆجی",
             "Study of blood, blood-forming organs, and blood diseases including cellular components and plasma.",
             "خوێندنی خوێن، ئەندامە خوێنساز و نەخۆشیەکانی خوێن لەگەڵ پێکهاتە خانەیی و پلازما.",
             "fas fa-tint"),

            (6, "Microbiology", "مایکرۆبایۆلۆجی",
             "Study of microorganisms including bacteria, viruses, fungi, and their roles in health and disease.",
             "خوێندنی زیندەوەرە مایکرۆسکۆپیەکان لەوانە بەکتریا، ڤایرۆس، کەمترشی و ڕۆڵیان لە تەندروستی و نەخۆشیدا.",
             "fas fa-virus"),

            (7, "Entomology", "ئینتۆمۆلۆجی",
             "Scientific study of insects, their classification, morphology, physiology, and ecological importance.",
             "خوێندنی زانستی مێروو، پۆلێنکردنیان، مۆرفۆلۆجی، فیزیۆلۆجی و گرنگی ژینگەییان.",
             "fas fa-spider"),

            (8, "Algae Studies", "خوێندنی ئاڵگا",
             "Study of algae, their diversity, classification, structure, and ecological significance.",
             "خوێندنی ئاڵگاکان، جۆراوجۆریان، پۆلێنکردن، پێکهاتە و گرنگی ژینگەییان.",
             "fas fa-water")
        ]

        for order, title_en, title_ckb, desc_en, desc_ckb, icon in chapters_data:
            chapter = Chapter(
                order=order,
                title_en=title_en,
                title_ckb=title_ckb,
                description_en=desc_en,
                description_ckb=desc_ckb,
                icon=icon
            )
            db.session.add(chapter)

        # Create super admin user
        admin = User(
            username='admin',
            email='admin@biology.edu',
            role='super_admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create sample chapter admin
        chapter_admin = User(
            username='histology_admin',
            email='histology@biology.edu',
            role='chapter_admin',
            chapter_id=1
        )
        chapter_admin.set_password('histology123')
        db.session.add(chapter_admin)

        try:
            db.session.commit()
            print("Sample data created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating sample data: {e}")


# Routes
@app.route("/")
def root():
    """Redirect to English by default"""
    return redirect(url_for("index", lang="en"))


@app.route("/guide/<lang>")
def guide(lang):
    return render_template("guide.html", lang=lang)


@app.route("/<lang>")
def index(lang):
    """Main homepage - data comes directly from database"""
    lang, t, lang_code = pick_lang(lang)
    chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()
    update_daily_stats()

    # Pass chapters to template
    return render_template("index.html", t=t, lang=lang, lang_code=lang_code, chapters=chapters)


# Replace the existing chapters() function with this updated version
@app.route("/<lang>/chapters")
def chapters(lang):
    """Chapters overview page - data from database"""
    lang, t, lang_code = pick_lang(lang)
    chapters_query = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()

    chapter_data = []
    for chapter in chapters_query:
        slides_count = chapter.get_slides_count()
        total_views = chapter.get_total_views()
        chapter_data.append({
            'chapter': chapter,
            'slides_count': slides_count,
            'total_views': total_views
        })

    return render_template("chapters.html", t=t, lang=lang, lang_code=lang_code, chapters=chapter_data)


@app.route("/<lang>/chapter/<int:chapter_id>")
def chapter(lang, chapter_id):
    """Individual chapter pages - data from database"""
    lang, t, lang_code = pick_lang(lang)
    chapter_obj = Chapter.query.filter_by(id=chapter_id, is_active=True).first_or_404()
    slides = Slide.query.filter_by(chapter_id=chapter_id, is_active=True).order_by(Slide.order).all()

    # Increment view count
    chapter_obj.view_count += 1
    try:
        db.session.commit()
        log_activity('view', 'chapter', chapter_id, f'Viewed chapter: {chapter_obj.get_title(lang)}')
    except:
        db.session.rollback()

    return render_template("chapter_detail.html", t=t, lang=lang, lang_code=lang_code,
                           chapter=chapter_obj, slides=slides)


@app.route("/<lang>/slide/<int:slide_id>")
def slide_detail(lang, slide_id):
    """Individual slide view - data from database"""
    lang, t, lang_code = pick_lang(lang)
    slide_obj = Slide.query.filter_by(id=slide_id, is_active=True).first_or_404()
    chapter_obj = slide_obj.chapter_ref

    # Increment view count
    slide_obj.view_count += 1
    try:
        db.session.commit()
        log_activity('view', 'slide', slide_id, f'Viewed slide: {slide_obj.get_title(lang)}')
    except:
        db.session.rollback()

    other_slides = Slide.query.filter_by(
        chapter_id=chapter_obj.id, is_active=True
    ).filter(Slide.id != slide_id).order_by(Slide.order).all()

    return render_template("slide_detail.html", t=t, lang=lang, lang_code=lang_code,
                           slide=slide_obj, chapter=chapter_obj, other_slides=other_slides)


# Admin Routes
@app.route('/<lang>/admin/login', methods=['GET', 'POST'])
def admin_login(lang):
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard', lang=lang))

    lang, t, lang_code = pick_lang(lang)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_active=True).first()

        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            try:
                db.session.commit()
                log_activity('login', 'user', user.id, f'User {username} logged in')
            except:
                db.session.rollback()

            flash(t['login_success'], 'success')
            return redirect(url_for('admin_dashboard', lang=lang))

        flash(t['invalid_credentials'], 'error')

    return render_template('admin_login.html', t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/logout')
@login_required
def admin_logout(lang):
    lang, t, lang_code = pick_lang(lang)
    if current_user.is_authenticated:
        log_activity('logout', 'user', current_user.id, f'User {current_user.username} logged out')
    logout_user()
    flash(t['logout_success'], 'info')
    return redirect(url_for('index', lang=lang))


@app.route('/<lang>/admin/dashboard')
@login_required
def admin_dashboard(lang):
    """Admin dashboard - all data from database"""
    lang, t, lang_code = pick_lang(lang)

    if current_user.is_super_admin:
        chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()
        total_slides = Slide.query.filter_by(is_active=True).count()
        total_users = User.query.filter_by(is_active=True).count()
    else:
        if current_user.chapter_id:
            chapters = [Chapter.query.get(current_user.chapter_id)]
            total_slides = Slide.query.filter_by(
                chapter_id=current_user.chapter_id, is_active=True
            ).count()
        else:
            chapters = []
            total_slides = 0
        total_users = 1

    if current_user.is_super_admin:
        recent_activities = Activity.query.order_by(Activity.created_at.desc()).limit(10).all()
    else:
        recent_activities = Activity.query.filter_by(
            user_id=current_user.id
        ).order_by(Activity.created_at.desc()).limit(10).all()

    total_chapter_views = sum(chapter.view_count for chapter in chapters) if chapters else 0
    total_slide_views = db.session.query(db.func.sum(Slide.view_count)).filter(
        Slide.chapter_id.in_([c.id for c in chapters]) if chapters else [0]
    ).scalar() or 0

    total_views = total_chapter_views + total_slide_views
    recent_activity_count = len(recent_activities)
    activity_percentage = min(85 + (recent_activity_count * 2), 100)

    stats = {
        'total_chapters': len(chapters),
        'total_slides': total_slides,
        'total_users': total_users,
        'activity_percentage': activity_percentage,
        'total_views': total_views,
        'recent_activities_count': recent_activity_count
    }

    enhanced_chapters = []
    for chapter in chapters:
        slides_count = chapter.get_slides_count()
        chapter_views = chapter.get_total_views()
        enhanced_chapters.append({
            'chapter': chapter,
            'slides_count': slides_count,
            'total_views': chapter_views,
            'last_updated': chapter.updated_at
        })

    return render_template('admin_dashboard.html', chapters=enhanced_chapters, stats=stats,
                           recent_activities=recent_activities, t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/chapters')
@admin_required
def manage_chapters(lang):
    """Chapter management page - data from database"""
    lang, t, lang_code = pick_lang(lang)

    if current_user.is_super_admin:
        chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()
    else:
        chapters = [current_user.chapter] if current_user.chapter else []

    enhanced_chapters = []
    for chapter in chapters:
        slides_count = chapter.get_slides_count()
        total_views = chapter.get_total_views()
        enhanced_chapters.append({
            'chapter': chapter,
            'slides_count': slides_count,
            'total_views': total_views
        })

    return render_template('manage_chapters.html', chapters=enhanced_chapters,
                           t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/chapter/add', methods=['GET', 'POST'])
@super_admin_required
def add_chapter(lang):
    """Add new chapter - only super admins"""
    lang, t, lang_code = pick_lang(lang)

    if request.method == 'POST':
        max_order = db.session.query(db.func.max(Chapter.order)).scalar() or 0
        chapter = Chapter(
            title_en=request.form.get('title_en', ''),
            title_ckb=request.form.get('title_ckb', ''),
            description_en=request.form.get('description_en', ''),
            description_ckb=request.form.get('description_ckb', ''),
            order=max_order + 1,
            icon=request.form.get('icon', 'fas fa-book')
        )

        db.session.add(chapter)
        try:
            db.session.commit()
            log_activity('create', 'chapter', chapter.id, f'Added chapter: {chapter.title_en}')

            if request.headers.get('Content-Type') == 'application/json' or request.is_json:
                return jsonify({'success': True, 'message': t['success_added'], 'chapter_id': chapter.id})
            else:
                flash(t['success_added'], 'success')
                return redirect(url_for('manage_chapters', lang=lang))

        except Exception as e:
            db.session.rollback()
            if request.headers.get('Content-Type') == 'application/json' or request.is_json:
                return jsonify({'success': False, 'message': t['error_occurred']})
            else:
                flash(t['error_occurred'], 'error')

    return render_template('add_chapter.html', t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(lang, chapter_id):
    """Edit chapter - data from database"""
    lang, t, lang_code = pick_lang(lang)
    chapter = Chapter.query.get_or_404(chapter_id)

    if current_user.role == 'chapter_admin' and current_user.chapter_id != chapter_id:
        flash('No permission to edit this chapter', 'error')
        return redirect(url_for('admin_dashboard', lang=lang))

    if request.method == 'POST':
        chapter.title_en = request.form.get('title_en', chapter.title_en)
        chapter.title_ckb = request.form.get('title_ckb', chapter.title_ckb)
        chapter.description_en = request.form.get('description_en', chapter.description_en)
        chapter.description_ckb = request.form.get('description_ckb', chapter.description_ckb)
        chapter.icon = request.form.get('icon', chapter.icon)

        if current_user.is_super_admin:
            new_order = request.form.get('order')
            if new_order and new_order.isdigit():
                chapter.order = int(new_order)

        chapter.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            log_activity('edit', 'chapter', chapter.id, f'Updated chapter: {chapter.title_en}')
            flash(t['success_updated'], 'success')
            return redirect(url_for('manage_chapters', lang=lang))
        except Exception as e:
            db.session.rollback()
            flash(t['error_occurred'], 'error')

    return render_template('edit_chapter.html', chapter=chapter, t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/chapter/<int:chapter_id>/delete', methods=['POST'])
@super_admin_required
def delete_chapter(lang, chapter_id):
    """Delete chapter from database (soft delete)"""
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter_title = chapter.title_en

    try:
        # Soft delete - set is_active to False
        chapter.is_active = False
        chapter.updated_at = datetime.utcnow()

        # Also deactivate all slides in this chapter
        slides = Slide.query.filter_by(chapter_id=chapter_id).all()
        for slide in slides:
            slide.is_active = False
            slide.updated_at = datetime.utcnow()

        db.session.commit()
        log_activity('delete', 'chapter', chapter_id, f'Deleted chapter: {chapter_title}')

        return jsonify({'success': True, 'message': 'Chapter deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error deleting chapter'})


@app.route('/<lang>/admin/chapter/<int:chapter_id>/slides')
@admin_required
def manage_slides(lang, chapter_id):
    """Manage slides - data from database"""
    lang, t, lang_code = pick_lang(lang)

    if current_user.role == 'chapter_admin' and current_user.chapter_id != chapter_id:
        flash('No permission to manage this chapter', 'error')
        return redirect(url_for('admin_dashboard', lang=lang))

    chapter = Chapter.query.get_or_404(chapter_id)
    slides = Slide.query.filter_by(chapter_id=chapter_id, is_active=True).order_by(Slide.order).all()

    enhanced_slides = []
    for slide in slides:
        enhanced_slides.append({
            'slide': slide,
            'views': slide.view_count,
            'last_updated': slide.updated_at
        })

    return render_template('manage_slides.html', chapter=chapter, slides=enhanced_slides,
                           t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/slide/add', methods=['GET', 'POST'])
@admin_required
def add_slide(lang):
    """Add new slide - data saved to database"""
    lang, t, lang_code = pick_lang(lang)

    if request.method == 'POST':
        chapter_id = int(request.form.get('chapter_id'))

        if current_user.role == 'chapter_admin' and current_user.chapter_id != chapter_id:
            return jsonify({'success': False, 'message': 'No permission to add slides to this chapter'})

        max_order = db.session.query(db.func.max(Slide.order)).filter_by(chapter_id=chapter_id).scalar() or 0

        slide = Slide(
            title_en=request.form.get('title_en', ''),
            title_ckb=request.form.get('title_ckb', ''),
            content_en=request.form.get('content_en', ''),
            content_ckb=request.form.get('content_ckb', ''),
            order=max_order + 1,
            chapter_id=chapter_id,
            image_url=request.form.get('image_url', ''),
            components=request.form.get('components', ''),
            location=request.form.get('location', ''),
            functions=request.form.get('functions', '')
        )

        db.session.add(slide)
        try:
            db.session.commit()
            log_activity('create', 'slide', slide.id, f'Added slide: {slide.title_en}')

            if request.is_json:
                return jsonify({'success': True, 'message': t['success_added']})
            else:
                flash(t['success_added'], 'success')
                return redirect(url_for('manage_slides', lang=lang, chapter_id=chapter_id))

        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({'success': False, 'message': t['error_occurred']})
            else:
                flash(t['error_occurred'], 'error')

    if current_user.is_super_admin:
        chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()
    else:
        chapters = [current_user.chapter] if current_user.chapter else []

    return render_template('add_slide.html', chapters=chapters, t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/slide/<int:slide_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_slide(lang, slide_id):
    """Edit slide - data from/to database"""
    lang, t, lang_code = pick_lang(lang)
    slide = Slide.query.get_or_404(slide_id)

    if current_user.role == 'chapter_admin' and current_user.chapter_id != slide.chapter_id:
        flash('No permission to edit this slide', 'error')
        return redirect(url_for('admin_dashboard', lang=lang))

    if request.method == 'POST':
        slide.title_en = request.form.get('title_en', '')
        slide.title_ckb = request.form.get('title_ckb', '')
        slide.content_en = request.form.get('content_en', '')
        slide.content_ckb = request.form.get('content_ckb', '')
        slide.order = int(request.form.get('order', slide.order))
        slide.image_url = request.form.get('image_url', '')
        slide.components = request.form.get('components', '')
        slide.location = request.form.get('location', '')
        slide.functions = request.form.get('functions', '')
        slide.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            log_activity('edit', 'slide', slide.id, f'Updated slide: {slide.title_en}')
            flash(t['success_updated'], 'success')
            return redirect(url_for('manage_slides', lang=lang, chapter_id=slide.chapter_id))
        except Exception as e:
            db.session.rollback()
            flash(t['error_occurred'], 'error')

    return render_template('edit_slide.html', slide=slide, t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/slide/<int:slide_id>/delete', methods=['POST'])
@admin_required
def delete_slide(lang, slide_id):
    """Delete slide from database"""
    slide = Slide.query.get_or_404(slide_id)

    if current_user.role == 'chapter_admin' and current_user.chapter_id != slide.chapter_id:
        return jsonify({'success': False, 'message': 'No permission to delete this slide'})

    slide_title = slide.title_en

    try:
        slide.is_active = False
        slide.updated_at = datetime.utcnow()
        db.session.commit()
        log_activity('delete', 'slide', slide_id, f'Deleted slide: {slide_title}')

        return jsonify({'success': True, 'message': 'Slide deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error deleting slide'})


# API Routes
@app.route('/api/<lang>/chapter/<int:chapter_id>')
@admin_required
def get_chapter_api(lang, chapter_id):
    """API endpoint to get chapter data"""
    chapter = Chapter.query.get_or_404(chapter_id)

    if current_user.role == 'chapter_admin' and current_user.chapter_id != chapter_id:
        return jsonify({'success': False, 'message': 'No permission'})

    return jsonify({
        'success': True,
        'chapter': {
            'id': chapter.id,
            'title_en': chapter.title_en,
            'title_ckb': chapter.title_ckb,
            'description_en': chapter.description_en,
            'description_ckb': chapter.description_ckb,
            'icon': chapter.icon,
            'order': chapter.order
        }
    })


@app.route('/<lang>/admin/chapter/<int:chapter_id>/reorder', methods=['POST'])
@super_admin_required
def reorder_chapter(lang, chapter_id):
    """Reorder chapter"""
    data = request.get_json()
    new_order = data.get('new_order')

    if not new_order or not isinstance(new_order, int):
        return jsonify({'success': False, 'message': 'Invalid order'})

    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        old_order = chapter.order

        if old_order < new_order:
            # Moving down: decrease order of items between old and new positions
            chapters_to_update = Chapter.query.filter(
                Chapter.order > old_order,
                Chapter.order <= new_order,
                Chapter.is_active == True,
                Chapter.id != chapter_id
            ).all()
            for c in chapters_to_update:
                c.order -= 1
        else:
            # Moving up: increase order of items between new and old positions
            chapters_to_update = Chapter.query.filter(
                Chapter.order >= new_order,
                Chapter.order < old_order,
                Chapter.is_active == True,
                Chapter.id != chapter_id
            ).all()
            for c in chapters_to_update:
                c.order += 1

        chapter.order = new_order
        chapter.updated_at = datetime.utcnow()

        db.session.commit()
        log_activity('reorder', 'chapter', chapter_id, f'Reordered chapter to position {new_order}')

        return jsonify({'success': True, 'message': 'Order updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error updating order'})


@app.route('/api/<lang>/dashboard/stats')
@admin_required
def dashboard_stats_api(lang):
    """API endpoint for real-time dashboard statistics"""
    if current_user.is_super_admin:
        total_chapters = Chapter.query.filter_by(is_active=True).count()
        total_slides = Slide.query.filter_by(is_active=True).count()
        total_users = User.query.filter_by(is_active=True).count()
        total_views = (db.session.query(db.func.sum(Chapter.view_count)).scalar() or 0) + \
                      (db.session.query(db.func.sum(Slide.view_count)).scalar() or 0)
    else:
        if current_user.chapter_id:
            total_chapters = 1
            total_slides = Slide.query.filter_by(
                chapter_id=current_user.chapter_id, is_active=True
            ).count()
            chapter_views = Chapter.query.get(current_user.chapter_id).view_count or 0
            slide_views = db.session.query(db.func.sum(Slide.view_count)).filter_by(
                chapter_id=current_user.chapter_id
            ).scalar() or 0
            total_views = chapter_views + slide_views
        else:
            total_chapters = total_slides = total_views = 0
        total_users = 1

    recent_activities = Activity.query.filter(
        Activity.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0)
    ).count()
    activity_percentage = min(85 + recent_activities, 100)

    return jsonify({
        'total_chapters': total_chapters,
        'total_slides': total_slides,
        'total_users': total_users,
        'total_views': total_views,
        'activity_percentage': activity_percentage
    })


# Add these routes to your app.py file after the existing admin routes

# User Management Routes
@app.route('/<lang>/admin/users')
@super_admin_required
def manage_users(lang):
    """User management page - only for super admins"""
    lang, t, lang_code = pick_lang(lang)
    users = User.query.filter_by(is_active=True).order_by(User.created_at.desc()).all()

    # Get chapters for assignment
    chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()

    # Enhanced user data
    enhanced_users = []
    for user in users:
        last_activity = Activity.query.filter_by(user_id=user.id).order_by(Activity.created_at.desc()).first()
        total_activities = Activity.query.filter_by(user_id=user.id).count()

        enhanced_users.append({
            'user': user,
            'last_activity': last_activity,
            'total_activities': total_activities,
            'days_since_login': (datetime.utcnow() - user.last_login).days if user.last_login else None
        })

    return render_template('manage_users.html', users=enhanced_users, chapters=chapters,
                           t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/user/add', methods=['GET', 'POST'])
@super_admin_required
def add_user(lang):
    """Add new user - only super admins"""
    lang, t, lang_code = pick_lang(lang)

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'chapter_admin')
        chapter_id = request.form.get('chapter_id')

        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('add_user.html', t=t, lang=lang, lang_code=lang_code)

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('add_user.html', t=t, lang=lang, lang_code=lang_code)

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('add_user.html', t=t, lang=lang, lang_code=lang_code)

        # Create new user
        user = User(
            username=username,
            email=email,
            role=role,
            chapter_id=int(chapter_id) if chapter_id and chapter_id != '' else None
        )
        user.set_password(password)

        db.session.add(user)
        try:
            db.session.commit()
            log_activity('create', 'user', user.id, f'Created user: {username}')
            flash('User created successfully', 'success')
            return redirect(url_for('manage_users', lang=lang))
        except Exception as e:
            db.session.rollback()
            flash('Error creating user', 'error')

    chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()
    return render_template('add_user.html', chapters=chapters, t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@super_admin_required
def edit_user(lang, user_id):
    """Edit user - only super admins"""
    lang, t, lang_code = pick_lang(lang)
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.role = request.form.get('role', user.role)

        chapter_id = request.form.get('chapter_id')
        user.chapter_id = int(chapter_id) if chapter_id and chapter_id != '' else None

        # Update password if provided
        new_password = request.form.get('password', '').strip()
        if new_password:
            user.set_password(new_password)

        user.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            log_activity('edit', 'user', user.id, f'Updated user: {user.username}')
            flash('User updated successfully', 'success')
            return redirect(url_for('manage_users', lang=lang))
        except Exception as e:
            db.session.rollback()
            flash('Error updating user', 'error')

    chapters = Chapter.query.filter_by(is_active=True).order_by(Chapter.order).all()
    return render_template('edit_user.html', user=user, chapters=chapters, t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/user/<int:user_id>/toggle-status', methods=['POST'])
@super_admin_required
def toggle_user_status(lang, user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)

    # Prevent deactivating yourself
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot deactivate yourself'})

    user.is_active = not user.is_active
    user.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        action = 'activate' if user.is_active else 'deactivate'
        log_activity(action, 'user', user.id, f'{action.title()}d user: {user.username}')

        return jsonify({
            'success': True,
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
            'is_active': user.is_active
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error updating user status'})


# Settings Routes
@app.route('/<lang>/admin/settings')
@admin_required
def settings(lang):
    """Settings page"""
    lang, t, lang_code = pick_lang(lang)

    # Get system statistics
    total_chapters = Chapter.query.filter_by(is_active=True).count()
    total_slides = Slide.query.filter_by(is_active=True).count()
    total_users = User.query.filter_by(is_active=True).count()
    total_views = (db.session.query(db.func.sum(Chapter.view_count)).scalar() or 0) + \
                  (db.session.query(db.func.sum(Slide.view_count)).scalar() or 0)

    # Get recent activities
    recent_activities = Activity.query.order_by(Activity.created_at.desc()).limit(50).all()

    # Database size (approximate)
    db_size = "N/A"  # You can implement actual database size calculation if needed

    system_info = {
        'total_chapters': total_chapters,
        'total_slides': total_slides,
        'total_users': total_users,
        'total_views': total_views,
        'total_activities': len(recent_activities),
        'db_size': db_size,
        'flask_version': '2.3.3',  # Update with actual version
        'python_version': '3.9+',  # Update with actual version
        'database': 'SQLite'
    }

    return render_template('settings.html', system_info=system_info,
                           recent_activities=recent_activities[:10], t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/settings/profile', methods=['GET', 'POST'])
@admin_required
def profile_settings(lang):
    """User profile settings"""
    lang, t, lang_code = pick_lang(lang)

    if request.method == 'POST':
        # Update profile
        current_user.email = request.form.get('email', current_user.email)

        # Update password if provided
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if new_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'error')
                return render_template('profile_settings.html', t=t, lang=lang, lang_code=lang_code)

            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return render_template('profile_settings.html', t=t, lang=lang, lang_code=lang_code)

            current_user.set_password(new_password)

        current_user.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            log_activity('edit', 'profile', current_user.id, 'Updated profile settings')
            flash('Profile updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile', 'error')

    return render_template('profile_settings.html', t=t, lang=lang, lang_code=lang_code)


@app.route('/<lang>/admin/settings/system', methods=['GET', 'POST'])
@super_admin_required
def system_settings(lang):
    """System settings - only super admins"""
    lang, t, lang_code = pick_lang(lang)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'backup_database':
            # Implement database backup logic
            try:
                # Create backup
                backup_filename = f"biology_system_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
                # Copy database file (for SQLite)
                import shutil
                shutil.copy2('biology_system.db', f'backups/{backup_filename}')

                log_activity('backup', 'system', 0, 'Created database backup')
                flash('Database backup created successfully', 'success')
            except Exception as e:
                flash('Error creating backup', 'error')

        elif action == 'clear_logs':
            # Clear old activity logs
            try:
                # Keep only last 30 days
                cutoff_date = datetime.utcnow() - timedelta(days=30)
                old_activities = Activity.query.filter(Activity.created_at < cutoff_date).all()

                for activity in old_activities:
                    db.session.delete(activity)

                db.session.commit()
                log_activity('maintenance', 'system', 0, f'Cleared {len(old_activities)} old activity logs')
                flash(f'Cleared {len(old_activities)} old activity logs', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error clearing logs', 'error')

        elif action == 'reset_views':
            # Reset all view counts
            try:
                Chapter.query.update({Chapter.view_count: 0})
                Slide.query.update({Slide.view_count: 0})
                db.session.commit()

                log_activity('maintenance', 'system', 0, 'Reset all view counts')
                flash('All view counts reset successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error resetting view counts', 'error')

    return render_template('system_settings.html', t=t, lang=lang, lang_code=lang_code)


# API Routes for Settings
@app.route('/api/<lang>/export/data')
@admin_required
def export_data_api(lang):
    """Export system data as JSON"""
    try:
        # Export data based on user permissions
        if current_user.is_super_admin:
            chapters = Chapter.query.filter_by(is_active=True).all()
        else:
            chapters = [current_user.chapter] if current_user.chapter else []

        export_data = {
            'export_date': datetime.utcnow().isoformat(),
            'exported_by': current_user.username,
            'chapters': []
        }

        for chapter in chapters:
            slides = Slide.query.filter_by(chapter_id=chapter.id, is_active=True).all()
            chapter_data = {
                'id': chapter.id,
                'title_en': chapter.title_en,
                'title_ckb': chapter.title_ckb,
                'description_en': chapter.description_en,
                'description_ckb': chapter.description_ckb,
                'order': chapter.order,
                'view_count': chapter.view_count,
                'slides': []
            }

            for slide in slides:
                slide_data = {
                    'id': slide.id,
                    'title_en': slide.title_en,
                    'title_ckb': slide.title_ckb,
                    'content_en': slide.content_en,
                    'content_ckb': slide.content_ckb,
                    'order': slide.order,
                    'view_count': slide.view_count,
                    'image_url': slide.image_url,
                    'components': slide.components,
                    'location': slide.location,
                    'functions': slide.functions
                }
                chapter_data['slides'].append(slide_data)

            export_data['chapters'].append(chapter_data)

        log_activity('export', 'data', 0, 'Exported system data')

        return jsonify({
            'success': True,
            'message': 'Data exported successfully',
            'data': export_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error exporting data'
        })




@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler"""
    return redirect(url_for('index', lang='en'))


@app.before_request
def before_request():
    """Initialize database if needed"""
    if not hasattr(app, 'db_initialized'):
        with app.app_context():
            db.create_all()
            create_sample_data()
            app.db_initialized = True

# ======= place this block LAST in the file =======
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index', lang='en'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
        print("Database initialized!")
        print("Admin credentials - Username: admin, Password: admin123")
        print("Chapter Admin credentials - Username: histology_admin, Password: histology123")

    app.run(debug=True, host="0.0.0.0", port=5000)