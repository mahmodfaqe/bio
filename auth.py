from flask_login import LoginManager
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, request, flash

login_manager = LoginManager()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            lang = kwargs.get('lang', 'en')
            flash('تکایە سەرەتا چووە ژوورەوە', 'warning')
            return redirect(url_for('admin_login', lang=lang))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            lang = kwargs.get('lang', 'en')
            flash('تکایە سەرەتا چووە ژوورەوە', 'warning')
            return redirect(url_for('admin_login', lang=lang))

        if current_user.role not in ['super_admin', 'chapter_admin']:
            lang = kwargs.get('lang', 'en')
            flash('دەسەڵاتت نییە بۆ ئەم کردارە', 'error')
            return redirect(url_for('index', lang=lang))

        return f(*args, **kwargs)

    return decorated_function


def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            lang = kwargs.get('lang', 'en')
            flash('تکایە سەرەتا چووە ژوورەوە', 'warning')
            return redirect(url_for('admin_login', lang=lang))

        if current_user.role != 'super_admin':
            lang = kwargs.get('lang', 'en')
            flash('تەنها بەڕێوەبەری گشتی دەتوانێ ئەم کردارە ئەنجام بدات', 'error')
            return redirect(url_for('admin_dashboard', lang=lang))

        return f(*args, **kwargs)

    return decorated_function