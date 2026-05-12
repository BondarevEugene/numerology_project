"""
--------------------------------------------------------------------------------
MODELS: Genesis HR® Core Models
PROJECT: Genesis HR® | Intelligence Systems
VERSION: 2.5.0
DESCRIPTION: Database schema including Users, Content, and Session Vault.
--------------------------------------------------------------------------------
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# --- [ СЕКЦИЯ: ПОЛЬЗОВАТЕЛИ ] ---

# 1. Сначала базовый класс пользователя
class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Убедись, что это имя совпадает с тем, что в Foreign Key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    pattern = db.Column(db.String(100), nullable=True)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date, nullable=False)

    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f'<User {self.email}>'


# --- [ СЕКЦИЯ: АРХИВ СЕССИЙ (VAULT) ] ---

class SessionArchive(db.Model):
    __tablename__ = 'session_archive'

    id = db.Column(db.Integer, primary_key=True)
    # КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: ссылка на 'user.id' (так как __tablename__ у User = 'users')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    arcane_number = db.Column(db.String(10))
    state_tag = db.Column(db.String(50))  # "Alpha", "Stable", "Peak"

    # Снапшоты биоритмов
    bio_physical = db.Column(db.Float)
    bio_emotional = db.Column(db.Float)
    bio_intellectual = db.Column(db.Float)

    notes = db.Column(db.Text)

    # Связь с объектом User
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M'),
            "arcane": self.arcane_number,
            "tag": self.state_tag,
            "bio": {
                "p": self.bio_physical,
                "e": self.bio_emotional,
                "i": self.bio_intellectual
            }
        }


# --- [ СЕКЦИЯ: КОНТЕНТ И ЗНАНИЯ ] ---

class ArchetypeContent(db.Model):
    __tablename__ = 'archetype_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(200))
    planet = db.Column(db.String(100))
    element = db.Column(db.String(100))
    tarot_arcane = db.Column(db.String(100))
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


class ProfessionContent(db.Model):
    __tablename__ = 'profession_content'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    list_csv = db.Column(db.Text)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
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


# --- [ СЕКЦИЯ: СИСТЕМНЫЕ УЗЛЫ ] ---

class NexusNode(db.Model):
    __tablename__ = 'nexus_nodes'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    module_path = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)


"""
--------------------------------------------------------------------------------
MODEL: GenesisProtocols
DESCRIPTION: Хранилище глубоких рекомендаций, диет и квестов.
             Связано с секторами матрицы и архетипами.
--------------------------------------------------------------------------------
"""


class GenesisProtocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))  # NUTRITION, SPORT, MIND, QUEST
    target_sector = db.Column(db.Integer)  # 1-9 (к какому сектору матрицы относится)
    level = db.Column(db.Integer)  # Уровень сложности/глубины
    content = db.Column(db.Text)  # Текст рекомендации
    reward_xp = db.Column(db.Integer)  # Опыт за выполнение (Геймификация)


"""
--------------------------------------------------------------------------------
MODELS: Genesis Evolution System
PROJECT: Genesis HR® | Intelligence Systems
DESCRIPTION: Моделі для зберігання протоколів розвитку, квестів та XP.
--------------------------------------------------------------------------------
"""


# 3. И протоколы (они ни от кого не зависят)
class EvolutionProtocol(db.Model):
    __tablename__ = 'evolution_protocols'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))  # NUTRITION, SPORT, MENTAL, SPIRIT
    sector_trigger = db.Column(db.Integer)  # 1-9 (на який сектор матриці реагує)
    condition = db.Column(db.String(20))  # 'empty', 'overflow', 'normal'
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    xp_reward = db.Column(db.Integer, default=50)


# 2. Потом класс прогресса, который ссылается на User
class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    current_xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    completed_tasks = db.Column(db.JSON)  # Список ID виконаних протоколів

    user = db.relationship('User', backref=db.backref('progress', uselist=False))


def calculate_level(xp):
    """Рассчитывает уровень на основе накопленного опыта"""
    # Формула: уровень = корень из (XP / 100) + 1
    return int((xp / 100) ** 0.5) + 1


def get_rank_name(level):
    """Возвращает название ранга в стиле Genesis"""
    ranks = {1: "NEOPHYTE", 5: "INITIATE", 10: "ADEPT", 20: "MASTER", 50: "PROPHET"}
    for l in sorted(ranks.keys(), reverse=True):
        if level >= l: return ranks[l]
    return "UNKNOWN"
