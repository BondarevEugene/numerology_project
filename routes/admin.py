from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from sqlalchemy import or_

from flask_login import login_required

from flask import url_for

from core.admin_helpers import get_search_query
from core.admin_stats import build_stats

from core.archetype_profiles import (ARCHETYPE_PROFILES)

from models import (
    db,
    ArchetypeContent,
    ArchetypeCompetency,
    Article,
    Competency,
    DailyCoachTip,
    EvolutionProtocol,
    SessionArchive,
    ProfessionContent,
    VocationIntelligence,
    VocationCompatibility,
    User
)

import time

from core.archetype_profiles import (
    ARCHETYPE_PROFILES
)


admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)


@admin_bp.route('/')
@login_required
def dashboard():
    platform_stats = {

        "users":
            User.query.count(),
        "sessions":
            0,
        "articles":
            Article.query.count(),
        "protocols":
            EvolutionProtocol.query.count()
    }

    knowledge_stats = {

        "archetypes":
            ArchetypeContent.query.count(),
        "professions":
            ProfessionContent.query.count(),
        "daily_coach":
            DailyCoachTip.query.count()
    }

    career_stats = {

        "records":
            VocationIntelligence.query.count(),
        "missing_ru":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.title_ru == None,
                    VocationIntelligence.title_ru == ''
                )
            ).count(),

        "missing_ua":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.title_ua == None,
                    VocationIntelligence.title_ua == ''
                )
            ).count(),

        "missing_keywords":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.keywords == None,
                    VocationIntelligence.keywords == ''
                )
            ).count(),

        "missing_category":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.category == None,
                    VocationIntelligence.category == ''
                )
            ).count()

    }

    nexus_stats = {

        "graph":
            "PLANNED",

        "orchestrator":
            "PLANNED",

        "automation":
            "PLANNED",

        "inspector":
            "PLANNED"

    }
    audit = []
    for n in range(1, 10):
        vocation_count = (
            VocationIntelligence
            .query
            .filter_by(
                vector_id=n
            )
            .count()
        )
        if vocation_count == 0:
            audit.append(
                f"Нет профессий для числа {n}"
            )
    for n in range(1, 10):
        archetype_count = (
            ArchetypeContent
            .query
            .filter_by(
                number=str(n)
            )
            .count()
        )
        if archetype_count == 0:
            audit.append(
                f"Нет архетипа {n}"
            )
    # TEMP DISABLED
    # for n in range(1, 10):
    #     tips_count = (
    #         DailyCoachTip
    #         .query
    #         .filter_by(
    #             number=str(n)
    #         )
    #         .count()
    #     )
    #     if tips_count == 0:
    #         audit.append(
    #             f"Нет Daily Coach для числа {n}"
    #         )
    return render_template(
        'admin/dashboard.html',
        platform_stats=platform_stats,
        knowledge_stats=knowledge_stats,
        career_stats=career_stats,
        nexus_stats=nexus_stats,
        audit=audit
    )


@admin_bp.route('/users')
@login_required
def users():
    content = (
        User
        .query
        .all()
    )

    return render_template(
        'admin/users.html',
        content=content
    )


@admin_bp.route('/protocols')
@login_required
def protocols():
    content = (
        EvolutionProtocol
        .query
        .all()
    )

    return render_template(
        'admin/protocols.html',
        content=content
    )


@admin_bp.route('/archetypes')
@login_required
def archetypes():
    content = (
        ArchetypeContent
        .query
        .order_by(
            ArchetypeContent.number
        )
        .all()
    )

    return render_template(
        'admin/archetypes.html',
        content=content
    )


@admin_bp.route('/professions')
@login_required
def professions():
    content = (
        ProfessionContent
        .query
        .order_by(
            ProfessionContent.number
        )
        .all()
    )

    return render_template(
        'admin/professions.html',
        content=content
    )


@admin_bp.route('/tips')
@login_required
def tips():
    content = (
        DailyCoachTip
        .query
        .order_by(
            DailyCoachTip.archetype_id
        )
        .all()
    )

    return render_template(
        'admin/tips.html',
        content=content
    )


@admin_bp.route('/articles')
@login_required
def articles():
    content = (
        Article
        .query
        .all()
    )

    return render_template(
        'admin/articles.html',
        content=content
    )


'''@admin_bp.route('/courses')
@login_required
def courses():

    content = (
        Course
        .query
        .all()
    )

    return render_template(
        'admin/courses.html',
        content=content
    )'''


@admin_bp.route('/archetypes/new', methods=['GET', 'POST'])
@login_required
def archetype_new():
    if request.method == 'POST':
        item = ArchetypeContent()
        item.number = request.form.get(
            'number'
        )
        item.title = request.form.get(
            'title'
        )
        item.planet = request.form.get(
            'planet'
        )
        item.element = request.form.get(
            'element'
        )
        db.session.add(
            item
        )
        db.session.commit()
        return redirect(
            '/admin/archetypes'
        )
    return render_template(
        'admin/archetype_form.html',
        item=None
    )


@admin_bp.route(
    '/archetypes/edit/<int:item_id>',
    methods=['GET', 'POST']
)
@login_required
def archetype_edit(item_id):
    item = ArchetypeContent.query.get_or_404(
        item_id
    )

    if request.method == 'POST':
        item.number = request.form.get(
            'number'
        )
        item.title = request.form.get(
            'title'
        )
        item.planet = request.form.get(
            'planet'
        )
        item.element = request.form.get(
            'element'
        )
        item.action_power = request.form.get(
            'action_power'
        )
        item.shadow_side = request.form.get(
            'shadow_side'
        )
        item.growth_point = request.form.get(
            'growth_point'
        )
        item.realization = request.form.get(
            'realization'
        )
        item.karmic_tasks = request.form.get(
            'karmic_tasks'
        )
        item.financial_tip = request.form.get(
            'financial_tip'
        )
        item.partner_type = request.form.get(
            'partner_type'
        )
        item.health_tips = request.form.get(
            'health_tips'
        )
        item.mind_power = request.form.get(
            'mind_power'
        )
        item.life_result = request.form.get(
            'life_result'
        )
        db.session.commit()
        return redirect(
            '/admin/archetypes'
        )
    return render_template(
        'admin/archetype_edit.html',
        item=item
    )


@admin_bp.route('/vocations')
@login_required
def vocations():
    q = request.args.get(
        'q',
        ''
    )
    number = request.args.get(
        'number',
        ''
    )
    sort = request.args.get(
        'sort',
        'number'
    )
    query = (
        VocationIntelligence
        .query
    )
    # ПОИСК
    if q:
        query = query.filter(

            or_(

                VocationIntelligence
                .title_en
                .ilike(f"%{q}%"),

                VocationIntelligence
                .title_ru
                .ilike(f"%{q}%"),

                VocationIntelligence
                .title_ua
                .ilike(f"%{q}%"),

                VocationIntelligence
                .keywords
                .ilike(f"%{q}%"),

                VocationIntelligence
                .category
                .ilike(f"%{q}%"),

                VocationIntelligence
                .strategic_role
                .ilike(f"%{q}%")
            )
        )
    # ФИЛЬТР ПО ЧИСЛУ
    if number:
        query = query.filter(
            VocationIntelligence.vector_id == int(number)
        )
    # СОРТИРОВКА
    if sort == 'compatibility_desc':
        query = query.order_by(
            VocationIntelligence
            .compatibility_rate
            .desc()
        )
    elif sort == 'compatibility_asc':
        query = query.order_by(
            VocationIntelligence
            .compatibility_rate
            .asc()
        )
    elif sort == 'title':
        query = query.order_by(
            VocationIntelligence
            .title_en
            .asc()
        )
    else:
        query = query.order_by(
            VocationIntelligence
            .vector_id
            .asc()
        )
    content = query.all()
    return render_template(
        'admin/vocations.html',
        content=content
    )


@admin_bp.route(
    '/vocations/edit/<int:item_id>',
    methods=['GET', 'POST']
)
@login_required
def vocation_edit(item_id):
    item = VocationIntelligence.query.get_or_404(
        item_id
    )
    if request.method == 'POST':
        item.vector_id = request.form.get(
            'vector_id'
        )
        item.category = request.form.get(
            'category'
        )
        item.vocation_title = request.form.get(
            'vocation_title'
        )
        item.skill_stack = request.form.get(
            'skill_stack'
        )
        item.income_potential = request.form.get(
            'income_potential'
        )
        item.compatibility_rate = request.form.get(
            'compatibility_rate'
        )
        item.shadow_risk = request.form.get(
            'shadow_risk'
        )
        item.strategic_role = request.form.get(
            'strategic_role'
        )
        item.mission_statement = request.form.get(
            'mission_statement'
        )
        db.session.commit()
        return redirect(
            '/admin/vocations'
        )
    return render_template(
        'admin/vocation_edit.html',
        item=item
    )


@admin_bp.route(
    '/vocations/delete/<int:item_id>'
)
@login_required
def vocation_delete(item_id):
    item = (
        VocationIntelligence
        .query
        .get_or_404(item_id)
    )
    db.session.delete(
        item
    )
    db.session.commit()
    return redirect(
        '/admin/vocations'
    )


@admin_bp.route(
    '/vocations/new',
    methods=['GET', 'POST']
)
@login_required
def vocation_new():
    if request.method == 'POST':
        item = VocationIntelligence()
        item.vector_id = request.form.get(
            'vector_id'
        )
        item.category = request.form.get(
            'category'
        )
        item.vocation_title = request.form.get(
            'vocation_title'
        )
        item.skill_stack = request.form.get(
            'skill_stack'
        )
        item.income_potential = request.form.get(
            'income_potential'
        )
        item.compatibility_rate = request.form.get(
            'compatibility_rate'
        )
        item.shadow_risk = request.form.get(
            'shadow_risk'
        )
        item.strategic_role = request.form.get(
            'strategic_role'
        )
        item.mission_statement = request.form.get(
            'mission_statement'
        )
        db.session.add(
            item
        )
        db.session.commit()
        return redirect(
            '/admin/vocations'
        )
    return render_template(
        'admin/vocation_edit.html',
        item=None
    )


@admin_bp.route(
    '/vocations/import',
    methods=['GET', 'POST']
)
@login_required
def vocations_import():
    if request.method == 'POST':
        raw_text = request.form.get(
            'content',
            ''
        )
        lines = raw_text.splitlines()
        created = 0
        skipped = 0
        for line in lines:
            title = line.strip()
            print("=" * 50)
            print("IMPORT:", title)
            if not title:
                continue
            slug = (
                title
                .lower()
                .replace(' ', '-')
                .replace('/', '-')
            )
            exists = (
                VocationIntelligence
                .query
                .filter_by(
                    slug=slug
                )
                .first()
            )
            if exists:
                skipped += 1
                continue
            vocation = VocationIntelligence(
                vector_id=1,  # временно для теста

                slug=slug,

                title_en=title,

                vocation_title=title,

                is_active=True,

                created_at=datetime.utcnow(),

                updated_at=datetime.utcnow()
            )
            db.session.add(
                vocation
            )
            db.session.flush()
            for n in range(1, 10):
                compatibility = (
                    VocationCompatibility(
                        vocation_id=vocation.id,
                        number=n,
                        compatibility_rate=50
                    )
                )
                db.session.add(
                    compatibility
                )
            created += 1
        print("CREATED:", created)
        print("SKIPPED:", skipped)
        db.session.commit()
        flash(
            f'Создано: {created}. '
            f'Пропущено: {skipped}'
        )
        return redirect(
            '/admin/vocations'
        )
    return render_template(
        'admin/vocation_import.html'
    )


@admin_bp.route('/vocations/matrix')
@login_required
def vocation_matrix():
    start_time = time.time()

    q = request.args.get(
        'q',
        ''
    )
    audit = request.args.get(
        'audit',
        ''
    )
    query = (
        VocationIntelligence
        .query
    )
    if q:
        query = query.filter(
            or_(
                VocationIntelligence
                .title_en
                .ilike(f"%{q}%"),
                VocationIntelligence
                .title_ru
                .ilike(f"%{q}%"),
                VocationIntelligence
                .title_ua
                .ilike(f"%{q}%"),
                VocationIntelligence
                .keywords
                .ilike(f"%{q}%"),
                VocationIntelligence
                .category
                .ilike(f"%{q}%")
            )
        )
    # AUDIT FILTERS
    if audit == 'missing_ru':
        query = query.filter(
            or_(
                VocationIntelligence.title_ru == None,
                VocationIntelligence.title_ru == ''
            )
        )
    elif audit == 'missing_ua':
        query = query.filter(
            or_(
                VocationIntelligence.title_ua == None,
                VocationIntelligence.title_ua == ''
            )
        )
    elif audit == 'missing_keywords':
        query = query.filter(
            or_(
                VocationIntelligence.keywords == None,
                VocationIntelligence.keywords == ''
            )
        )
    elif audit == 'missing_category':
        query = query.filter(
            or_(
                VocationIntelligence.category == None,
                VocationIntelligence.category == ''
            )
        )
    vocations = (
        query
        .order_by(
            VocationIntelligence.title_en
        )
        .all()
    )

    vocation_ids = [
        item.id
        for item in vocations
    ]

    compatibilities = (
        VocationCompatibility
        .query
        .filter(
            VocationCompatibility
            .vocation_id
            .in_(vocation_ids)
        )
        .all()
    )

    matrix = {}

    for vocation in vocations:
        matrix[vocation.id] = {}

    for item in compatibilities:
        matrix[item.vocation_id][item.number] = item

    stats = {

        "total":
            VocationIntelligence
            .query
            .count(),

        "missing_ru":
            VocationIntelligence
            .query
            .filter(
                or_(
                    VocationIntelligence.title_ru == None,
                    VocationIntelligence.title_ru == ''
                )
            )
            .count(),

        "missing_ua":
            VocationIntelligence
            .query
            .filter(
                or_(
                    VocationIntelligence.title_ua == None,
                    VocationIntelligence.title_ua == ''
                )
            )
            .count(),

        "missing_keywords":
            VocationIntelligence
            .query
            .filter(
                or_(
                    VocationIntelligence.keywords == None,
                    VocationIntelligence.keywords == ''
                )
            )
            .count(),

        "missing_category":
            VocationIntelligence
            .query
            .filter(
                or_(
                    VocationIntelligence.category == None,
                    VocationIntelligence.category == ''
                )
            )
            .count()
    }

    print(
        "MATRIX LOAD:",
        round(
            time.time() - start_time,
            3
        ),
        "sec"
    )

    return render_template(
        'admin/vocation_matrix.html',
        vocations=vocations,
        matrix=matrix,
        stats=stats
    )


@admin_bp.route(
    '/vocations/matrix/update',
    methods=['POST']
)
@login_required
def vocation_matrix_update():
    print("=" * 50)
    print("UPDATE CALLED")

    compatibility_id = request.form.get(
        'compatibility_id'
    )

    value = request.form.get(
        'value'
    )

    item = (
        VocationCompatibility
        .query
        .get_or_404(
            compatibility_id
        )
    )

    item.compatibility_rate = int(
        value
    )

    db.session.commit()

    return {
        "success": True
    }


# ====================================
# BULK CATEGORY
# ====================================

@admin_bp.route(
    '/vocations/bulk/category',
    methods=['POST']
)
@admin_bp.route(
    '/vocations/bulk/category',
    methods=['POST']
)
@login_required
def bulk_category():
    return {
        "success": True,
        "updated": updated
    }


# ====================================
# BULK KEYWORD
# ====================================

@admin_bp.route(
    '/vocations/bulk/keyword',
    methods=['POST']
)
@login_required
def bulk_keyword():
    ids = request.form.getlist(
        'ids[]'
    )

    keyword = request.form.get(
        'keyword',
        ''
    )

    updated = 0

    for vocation_id in ids:

        item = (
            VocationIntelligence
            .query
            .get(vocation_id)
        )

        if not item:
            continue

        current = (
                item.keywords
                or ''
        )

        if keyword not in current:

            if current:

                item.keywords = (
                        current
                        +
                        ', '
                        +
                        keyword
                )

            else:

                item.keywords = keyword

        updated += 1

    db.session.commit()

    return {
        "success": True,
        "updated": updated
    }


# ====================================
# BULK VECTOR
# ====================================

@admin_bp.route(
    '/vocations/bulk/vector',
    methods=['POST']
)
@login_required
def bulk_vector():
    ids = request.form.getlist(
        'ids[]'
    )

    vector = request.form.get(
        'vector'
    )

    updated = 0

    for vocation_id in ids:

        item = (
            VocationIntelligence
            .query
            .get(vocation_id)
        )

        if not item:
            continue

        item.vector_id = int(
            vector
        )

        updated += 1

    db.session.commit()

    return {
        "success": True,
        "updated": updated
    }


# ====================================
# BULK DELETE
# ====================================

@admin_bp.route(
    '/vocations/bulk/delete',
    methods=['POST']
)
@login_required
def bulk_delete():
    ids = request.form.getlist(
        'ids[]'
    )

    deleted = 0

    for vocation_id in ids:

        item = (
            VocationIntelligence
            .query
            .get(vocation_id)
        )

        if not item:
            continue

        db.session.delete(
            item
        )

        deleted += 1

    db.session.commit()

    return {
        "success": True,
        "deleted": deleted
    }


@login_required
def bulk_category():
    ids = request.form.getlist(
        'ids[]'
    )

    category = request.form.get(
        'category',
        ''
    )

    if not ids:
        return {
            "success": False,
            "message": "No IDs"
        }

    updated = 0

    for vocation_id in ids:

        item = (
            VocationIntelligence
            .query
            .get(vocation_id)
        )

        if not item:
            continue

        item.category = category

        updated += 1

    db.session.commit()

    return {
        "success": True,
        "updated": updated
    }


@login_required
def vocation_matrix_update():
    print("=" * 50)
    print("UPDATE CALLED")
    compatibility_id = request.form.get(
        'compatibility_id'
    )
    value = request.form.get(
        'value'
    )
    print(
        "ID:",
        compatibility_id
    )
    print(
        "VALUE:",
        value
    )
    item = (
        VocationCompatibility
        .query
        .get_or_404(
            compatibility_id
        )
    )
    item.compatibility_rate = int(
        value
    )
    db.session.commit()
    print(
        "SAVED TO DB"
    )
    return {
        "success": True
    }


@admin_bp.route('/content-hub')
@login_required
def content_hub():
    stats = {

        "archetypes":
            ArchetypeContent.query.count(),

        "articles":
            Article.query.count(),

        "protocols":
            EvolutionProtocol.query.count(),

        "daily_coach":
            DailyCoachTip.query.count(),

        "professions":
            ProfessionContent.query.count()

    }

    return render_template(
        'admin/content_hub.html',
        stats=stats
    )


@admin_bp.route('/career-center')
@login_required
def career_center():
    matrix_stats = {

        "records":
            VocationIntelligence.query.count(),

        "missing_ru":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.title_ru == None,
                    VocationIntelligence.title_ru == ''
                )
            ).count(),

        "missing_ua":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.title_ua == None,
                    VocationIntelligence.title_ua == ''
                )
            ).count(),

        "missing_keywords":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.keywords == None,
                    VocationIntelligence.keywords == ''
                )
            ).count(),

        "missing_category":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.category == None,
                    VocationIntelligence.category == ''
                )
            ).count()

    }

    return render_template(
        'admin/career_center.html',
        matrix_stats=matrix_stats
    )


@admin_bp.route('/audit-center')
@login_required
def audit_center():
    audit_data = {

        "missing_ru":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.title_ru == None,
                    VocationIntelligence.title_ru == ''
                )
            ).count(),

        "missing_ua":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.title_ua == None,
                    VocationIntelligence.title_ua == ''
                )
            ).count(),

        "missing_keywords":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.keywords == None,
                    VocationIntelligence.keywords == ''
                )
            ).count(),

        "missing_category":
            VocationIntelligence.query.filter(
                or_(
                    VocationIntelligence.category == None,
                    VocationIntelligence.category == ''
                )
            ).count()

    }

    return render_template(
        'admin/audit_center.html',
        audit_data=audit_data
    )


#### ===================N E X U S =========================
@admin_bp.route('/nexus-hub')
@login_required
def nexus_hub():
    return render_template(
        'admin/nexus_hub.html'
    )


@admin_bp.route('/nexus/nodes')
@login_required
def nexus_nodes():
    nodes = [

        # ROOT
        {
            "data": {
                "id": "GENESIS",
                "label": "GENESIS",
                "type": "root"
            }
        },

        # LAYERS
        {
            "data": {
                "id": "CLIENT",
                "label": "CLIENT",
                "type": "layer"
            }
        },
        {
            "data": {
                "id": "CONTENT",
                "label": "CONTENT",
                "type": "layer"
            }
        },
        {
            "data": {
                "id": "CAREER",
                "label": "CAREER",
                "type": "layer"
            }
        },
        {
            "data": {
                "id": "ADMIN",
                "label": "ADMIN",
                "type": "layer"
            }
        },
        {
            "data": {
                "id": "NEXUS",
                "label": "NEXUS",
                "type": "layer"
            }
        },
        # CLIENT MODULES
        {
            "data": {
                "id": "DASHBOARD_V3",
                "label": "Dashboard V3",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "PERSONAL_OS",
                "label": "Personal OS",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "PROFESSIONAL_RESONANCE",
                "label": "Professional Resonance",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "PSYCHOMATRIX",
                "label": "Psychomatrix",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "DEVELOPMENT_PROFILE",
                "label": "Development Profile",
                "type": "module"
            }
        },
        # CONTENT MODULES
        {
            "data": {
                "id": "ARCHETYPES",
                "label": "Archetypes",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "ARTICLES",
                "label": "Articles",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "DAILY_COACH",
                "label": "Daily Coach",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "PROTOCOLS",
                "label": "Protocols",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "PROFESSIONS",
                "label": "Professions",
                "type": "module"
            }
        },
        # CAREER MODULES
        {
            "data": {
                "id": "CAREER_CENTER",
                "label": "Career Center",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "CAREER_MATRIX",
                "label": "Career Matrix",
                "type": "module"
            }
        },
        # ADMIN MODULES
        {
            "data": {
                "id": "CONTENT_HUB",
                "label": "Content Hub",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "AUDIT_CENTER",
                "label": "Audit Center",
                "type": "module"
            }
        },
        {
            "data": {
                "id": "USER_CENTER",
                "label": "User Intelligence",
                "type": "module"
            }
        },
        # NEXUS MODULES
        {
            "data": {
                "id": "GRAPH",
                "label": "Graph",
                "type": "module"
            }
        },

        {
            "data": {
                "id": "INSPECTOR",
                "label": "Inspector",
                "type": "module"
            }
        }

    ]

    edges = [

        {"data": {"source": "GENESIS", "target": "CLIENT"}},
        {"data": {"source": "GENESIS", "target": "CONTENT"}},
        {"data": {"source": "GENESIS", "target": "CAREER"}},
        {"data": {"source": "GENESIS", "target": "ADMIN"}},
        {"data": {"source": "GENESIS", "target": "NEXUS"}},

        {"data": {"source": "CLIENT", "target": "DASHBOARD_V3"}},
        {"data": {"source": "CLIENT", "target": "PERSONAL_OS"}},
        {"data": {"source": "CLIENT", "target": "PROFESSIONAL_RESONANCE"}},
        {"data": {"source": "CLIENT", "target": "PSYCHOMATRIX"}},
        {"data": {"source": "CLIENT", "target": "DEVELOPMENT_PROFILE"}},

        {"data": {"source": "CONTENT", "target": "ARCHETYPES"}},
        {"data": {"source": "CONTENT", "target": "ARTICLES"}},
        {"data": {"source": "CONTENT", "target": "DAILY_COACH"}},
        {"data": {"source": "CONTENT", "target": "PROTOCOLS"}},
        {"data": {"source": "CONTENT", "target": "PROFESSIONS"}},

        {"data": {"source": "CAREER", "target": "CAREER_CENTER"}},
        {"data": {"source": "CAREER", "target": "CAREER_MATRIX"}},

        {"data": {"source": "ADMIN", "target": "CONTENT_HUB"}},
        {"data": {"source": "ADMIN", "target": "AUDIT_CENTER"}},
        {"data": {"source": "ADMIN", "target": "USER_CENTER"}},

        {"data": {"source": "NEXUS", "target": "GRAPH"}},
        {"data": {"source": "NEXUS", "target": "INSPECTOR"}}
    ]

    return {
        "nodes": nodes,
        "edges": edges
    }


@admin_bp.route('/nexus/inspect')
@login_required
def nexus_inspect():
    path = request.args.get(
        'path',
        ''
    )

    descriptions = {

        "GENESIS":
            """
            GENESIS PLATFORM

            Root ecosystem node

            Status: ACTIVE
            Version: V3
            """,

        "CLIENT":
            """
            CLIENT LAYER

            Dashboard V3
            Personal Operating System
            Professional Resonance
            Psychomatrix
            Development Profile

            Status: ACTIVE
            """,

        "DASHBOARD_V3":
            """
            CLIENT DASHBOARD

            Main user entry point

            Status: ACTIVE
            """,

        "PERSONAL_OS":
            """
            PERSONAL OPERATING SYSTEM

            User operating profile

            Status: ACTIVE
            """,

        "PROFESSIONAL_RESONANCE":
            """
            PROFESSIONAL RESONANCE

            Career matching engine

            Status: ACTIVE
            """,

        "PSYCHOMATRIX":
            """
            PSYCHOMATRIX

            Matrix analysis module

            Status: ACTIVE
            """,

        "DEVELOPMENT_PROFILE":
            """
            DEVELOPMENT PROFILE

            Growth trajectory engine

            Status: ACTIVE
            """,

        "CONTENT":
            """
            CONTENT LAYER

            Archetypes
            Articles
            Daily Coach
            Protocols
            Professions

            Status: ACTIVE
            """,

        "ARCHETYPES":
            f"""
            ARCHETYPE ENGINE

            Records:
            {ArchetypeContent.query.count()}

            Status: ACTIVE
            """,

        "ARTICLES":
            f"""
            ARTICLE DATABASE

            Records:
            {Article.query.count()}

            Status: ACTIVE
            """,

        "DAILY_COACH":
            f"""
            DAILY COACH

            Records:
            {DailyCoachTip.query.count()}

            Status: ACTIVE
            """,

        "PROTOCOLS":
            f"""
            PROTOCOL ENGINE

            Records:
            {EvolutionProtocol.query.count()}

            Status: ACTIVE
            """,

        "PROFESSIONS":
            f"""
            PROFESSION DATABASE

            Records:
            {ProfessionContent.query.count()}

            Status: ACTIVE
            """,

        "CAREER":
            """
            CAREER LAYER

            Career Intelligence
            Career Matrix
            Recommendations

            Status: ACTIVE
            """,

        "CAREER_CENTER":
            """
            CAREER CENTER

            Main intelligence dashboard

            Status: ACTIVE
            """,

        "CAREER_MATRIX":
            f"""
            CAREER MATRIX

            Records:
            {VocationIntelligence.query.count()}

            Status: ACTIVE
            """,

        "ADMIN":
            """
            ADMIN LAYER

            Dashboard
            Content Hub
            Audit Center

            Status: ACTIVE
            """,

        "CONTENT_HUB":
            """
            CONTENT HUB

            Central content management

            Status: ACTIVE
            """,

        "AUDIT_CENTER":
            """
            AUDIT CENTER

            Quality control

            Status: ACTIVE
            """,

        "USER_CENTER":
            """
            USER INTELLIGENCE

            User analytics

            Status: PLANNED
            """,

        "NEXUS":
            """
            NEXUS CORE

            Graph
            Inspector
            Automation
            Orchestrator

            Status: IN DEVELOPMENT
            """,

        "GRAPH":
            """
            NEXUS GRAPH

            Ecosystem visualization

            Status: IN DEVELOPMENT
            """,

        "INSPECTOR":
            """
            NEXUS INSPECTOR

            Dependency explorer

            Status: IN DEVELOPMENT
            """
    }

    return descriptions.get(
        path,
        f"""
        UNKNOWN NODE

        {path}

        Status: UNREGISTERED
        """
    )


###==========Career Center =========
@admin_bp.route('/career-center')
@login_required
def career_center():
    stats = {
        "competencies": 0,
        "profession_links": 0,
        "archetype_links": 0,
        "recommendations": 0
    }

    return render_template(
        'admin/career_center.html',
        stats=stats
    )



@admin_bp.route('/competencies')
@login_required
def competencies():

    content = (
        Competency
        .query
        .order_by(
            Competency.category,
            Competency.title
        )
        .all()
    )

    return render_template(
        'admin/competencies.html',
        content=content
    )

@admin_bp.route('/archetype-mapping')
@login_required
def archetype_mapping():

    competencies = (
        Competency
        .query
        .order_by(
            Competency.category,
            Competency.title
        )
        .all()
    )

    mappings = (
        ArchetypeCompetency
        .query
        .all()
    )

    return render_template(
        'admin/archetype_mapping.html',
        profiles=ARCHETYPE_PROFILES,
        competencies=competencies,
        mappings=mappings
    )