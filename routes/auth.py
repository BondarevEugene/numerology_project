from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_mail import Message
from datetime import datetime
import uuid
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1. Сбор данных из формы
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        birth_date_str = request.form.get('birth_date')
        # НОВОЕ: Получаем графический ключ
        pattern = request.form.get('pattern')

        print(f"--- [REG_PROTOCOL] Инициация субъекта: {email} ---")

        # 2. Проверка на дубликат
        if User.query.filter_by(email=email).first():
            print(f"⚠️ Ошибка: Субъект {email} уже существует.")
            flash('Этот Email уже зарегистрирован в системе.')
            # ИСПРАВЛЕНО: возвращаем на регистрацию, а не в профиль
            return redirect(url_for('auth.register'))

        try:
            # 3. Создание пользователя
            token = str(uuid.uuid4())
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password),
                pattern=pattern,  # НОВОЕ: Сохраняем паттерн (нужно поле в models.py!)
                full_name=full_name,
                phone=phone,
                gender=gender,
                birth_date=datetime.strptime(birth_date_str, '%Y-%m-%d').date(),
                verification_token=token,
                is_verified=False
            )

            db.session.add(new_user)
            db.session.commit()
            # В файле auth.py внутри def register():
            if not User.query.filter_by(email=email).first():
                new_user = User(...)
                db.session.add(new_user)
                db.session.commit()

                # ВОТ ЗДЕСЬ ВСТАВЛЯЕМ ОТПРАВКУ
                try:
                    msg = Message("Genesis | Initialization Protocol",
                                  sender=current_app.config['MAIL_USERNAME'],
                                  recipients=[email])
                    msg.html = render_template('emails/welcome.html', user_name=full_name)
                    mail.send(msg)
                except Exception as e:
                    print(f"Ошибка отправки почты: {e}")

                flash('Протокол завершен. Добро пожаловать.')
                return redirect(url_for('auth.login'))
            print("✅ [SYSTEM]: Данные успешно синхронизированы с Neon.")

            # 4. Отправка почты (фоновый процесс)
            try:
                from app import mail
                msg = Message("Genesis | Подтверждение доступа",
                              sender="projectnumerology@gmail.com",
                              recipients=[email])
                link = url_for('auth.verify_email', token=token, _external=True)
                msg.body = f"Субъект {full_name}, подтвердите ваш доступ по ссылке: {link}"
                mail.send(msg)
                print("📧 [MAIL]: Инструкции отправлены.")
            except Exception as mail_err:
                print(f"⚠️ [MAIL_WARN]: Сервер почты недоступен: {mail_err}")

            # 5. Авторизация
            login_user(new_user, remember=True)
            session['user_id'] = new_user.id  # Для совместимости с profile.py

            print(f"🚀 [SYSTEM]: Протокол завершен. Добро пожаловать, {full_name}")
            flash(f'Протокол инициализирован. Добро пожаловать, {full_name}')
            return redirect(url_for('profile.dashboard'))

        except Exception as e:
            db.session.rollback()
            print(f"❌ [CRITICAL_ERROR]: {e}")
            flash("Критический сбой инициализации. Попробуйте позже.")
            return redirect(url_for('auth.register'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        pattern = request.form.get('pattern')

        user = User.query.filter_by(email=email).first()

        # 1. Защита от перебора: не говорим прямо "пользователь не найден"
        # Лучше использовать общую фразу, чтобы злоумышленник не знал, существует ли email
        if not user:
            flash("Ошибка аутентификации: проверьте данные.")
            return redirect(url_for('auth.login'))

        # 2. ГИБРИДНАЯ ПРОВЕРКА (Улучшенная логика)
        # В твоей версии был 'elif', то есть если введен паттерн, пароль даже не проверялся.
        # Обычно в таких системах либо требуют ОБА (2FA), либо делают проверку независимой.

        auth_success = False

        # Если есть паттерн, проверяем его
        if pattern and user.pattern == pattern:
            auth_success = True
            print("✅ [AUTH]: Графический ключ верифицирован.")

        # Если паттерн не подошел или не введен, проверяем пароль
        # Добавляем 'not auth_success', чтобы не делать лишний тяжелый хэш-чек, если ключ уже подошел
        if not auth_success and password:
            if check_password_hash(user.password_hash, password):
                auth_success = True
                print("✅ [AUTH]: Текстовый пароль верифицирован.")

        if auth_success:
            # 3. Проверка верификации
            if hasattr(user, 'is_verified') and not user.is_verified:
                flash("Доступ заблокирован: требуется подтверждение почты.")
                return redirect(url_for('auth.login'))

            # 4. Финализация
            login_user(user, remember=True)
            session['user_id'] = user.id  # Твой профиль завязан на это

            # Обновляем время последнего входа (если такое поле есть в БД)
            # user.last_login = datetime.utcnow()
            # db.session.commit()

            flash(f'Доступ разрешен. Добро пожаловать, {user.full_name}')
            return redirect(url_for('profile.dashboard'))

        else:
            flash("Ошибка аутентификации: неверные данные.")
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear() # Полная очистка
    flash("Сессия завершена. Доступ ограничен.")
    return redirect(url_for('main.index'))


@auth_bp.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first_or_404()
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    flash('Доступ активирован! Теперь вы можете войти.')
    return redirect(url_for('auth.login'))


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # 1. Генерируем уникальный токен
            user.reset_token = str(uuid.uuid4())
            db.session.commit()

            # 2. Подготавливаем письмо
            from app import mail  # Локальный импорт, если mail инициализирован в app

            msg = Message(
                "Genesis | Access Recovery Protocol",
                sender=current_app.config.get('MAIL_USERNAME', "projectnumerology@gmail.com"),
                recipients=[email]
            )

            # Ссылка для подтверждения
            link = url_for('auth.reset_password_confirm', token=user.reset_token, _external=True)

            # 3. Рендерим красивый HTML-шаблон, который мы создали
            msg.html = render_template(
                'emails/reset_password.html',
                user_name=user.full_name,
                reset_code=user.reset_token,  # Можно передать код или ссылку
                reset_url=link
            )

            # Текстовая версия на случай, если HTML не отобразится
            msg.body = f"Для сброса пароля перейдите по ссылке: {link}"

            try:
                mail.send(msg)
                print(f"✅ [SYSTEM]: Инструкции по восстановлению отправлены на {email}")
            except Exception as e:
                print(f"❌ [MAIL_ERROR]: {e}")
                flash("Ошибка отправки почты. Попробуйте позже.")

        # Безопасность: всегда говорим, что отправили письмо,
        # чтобы не выдавать существование email в базе
        flash("Если данный адрес зарегистрирован в Genesis, инструкции будут отправлены в ближайшее время.")
        return redirect(url_for('auth.login'))

    return render_template('reset_request.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    user = User.query.filter_by(reset_token=token).first_or_404()
    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None
        db.session.commit()
        flash("Пароль обновлен.")
        return redirect(url_for('auth.login'))
    return render_template('reset_password_new.html')