from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='chapter_admin')
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

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
    slides = db.relationship('Slide', backref='chapter', lazy=True, cascade='all, delete-orphan')

class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ckb = db.Column(db.String(200), nullable=False)
    content_en = db.Column(db.Text)
    content_ckb = db.Column(db.Text)
    order = db.Column(db.Integer, default=1)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    image_url = db.Column(db.String(500))
    components = db.Column(db.Text)
    location = db.Column(db.Text)
    functions = db.Column(db.Text)
    view_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)