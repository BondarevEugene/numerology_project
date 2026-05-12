from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from flask_login import UserMixin  # Важно для current_user

db = SQLAlchemy()  # Без привязки к app, её мы делаем в app.py через db.init_app(app)


class ArchetypeContent(db.Model):
    __tablename__ = 'archetype_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(200))
    planet = db.Column(db.String(100))
    element = db.Column(db.String(50))
    tarot_arcane = db.Column(db.Text)
    action_power = db.Column(db.Text)
    shadow_side = db.Column(db.Text)
    growth_point = db.Column(db.Text)
    realization = db.Column(db.Text)
    karmic_tasks = db.Column(db.Text)
    development_cycle = db.Column(db.Text)
    mind_power = db.Column(db.Text)
    life_result = db.Column(db.Text)
    partner_type = db.Column(db.Text)
    financial_tip = db.Column(db.Text)
    health_tips = db.Column(db.Text)
    exit_minus = db.Column(db.Text)
    search_queries = db.Column(db.Text)
    # Связь с советами коуча
    coach_tips = db.relationship('DailyCoachTip', backref='archetype', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True)
    user_email = db.Column(db.String(100))
    amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailyCoachTip(db.Model):
    __tablename__ = 'daily_coach_tips'
    id = db.Column(db.Integer, primary_key=True)
    archetype_id = db.Column(db.Integer, db.ForeignKey('archetype_content.id'))
    day_type = db.Column(db.String(20))
    phys_content = db.Column(db.Text)
    ment_content = db.Column(db.Text)
    harm_content = db.Column(db.Text)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    platform = db.Column(db.String(100))
    link = db.Column(db.String(500))
    archetype_num = db.Column(db.String(10))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ProfessionContent(db.Model):
    __tablename__ = 'profession_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    list_csv = db.Column(db.Text)


# Импорт уже есть в начале вашего файла, просто используем его
class User(db.Model, UserMixin):  # <--- Добавьте UserMixin сюда
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    pattern = db.Column(db.String(100), nullable=True)  # Храним последовательность точек, например "123"
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))  # Поле для регистрации
    gender = db.Column(db.String(10))  # Поле для регистрации
    birth_date = db.Column(db.Date, nullable=False)

    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), unique=True)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)  # ДЛЯ ВОССТАНОВЛЕНИЯ

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    personal_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'


class NexusNode(db.Model):
    __tablename__ = 'nexus_nodes'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)  # например, 'calc_archetype'
    module_path = db.Column(db.String(100))  # 'utils.sum_digits'
    config_json = db.Column(db.Text)  # Настройки ноды
    is_active = db.Column(db.Boolean, default=True)


class UserLog(db.Model):
    __tablename__ = 'user_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(255))
    level = db.Column(db.String(20), default='INFO')  # INFO, WARNING, CRITICAL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
