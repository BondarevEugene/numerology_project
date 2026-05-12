"""
--------------------------------------------------------------------------------
MODULE: main.py (Genesis Evolution Node)
PROJECT: Genesis HR® | Intelligence Systems
VERSION: 2.8.0 (Ultimate Mobile Terminal)
DESCRIPTION: Полная интеграция логики profile.py и интерфейса profile.html.
--------------------------------------------------------------------------------
"""
import flet as ft
import math
from datetime import datetime, date

# --- ЦВЕТОВАЯ СХЕМА GENESIS (ИЗ ВАШЕГО HTML) ---
COLOR_BG = "#050505"
COLOR_PANEL = "#0A0A0A"
COLOR_GOLD = "#b89b5e"
COLOR_GOLD_BRIGHT = "#f4cf6d"
COLOR_SAFE = "#1B5E20"  # Сильный сектор
COLOR_WARN = "#B71C1C"  # Слабый сектор
COLOR_TEXT = "#dcdcdc"


class GenesisEvolutionApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Genesis Evolution Terminal"
        self.page.bgcolor = COLOR_BG
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.DARK

        # Данные пользователя (подтягиваются из вашей логики)
        self.user_data = {
            "name": "АЛЕКСАНДР БОНДАРЬ",
            "birth_date": "15.05.1985",
            "level": "L_14_ADMIN",
            "xp": 0.62
        }

        self._apply_fonts()
        self.init_ui()

    def _apply_fonts(self):
        self.page.fonts = {
            "Cinzel": "https://fonts.gstatic.com/s/cinzel/v22/8vIJ7ww6m9mS3gp_sC6_.woff2",
            "JetBrains": "https://fonts.gstatic.com/s/jetbrainsmono/v18/t6qVr_z_is4vYvI_S8YV0YpTf9E6.woff2"
        }

    # --- ЛОГИКА РАСЧЕТОВ (ИЗ ВАШЕГО PROFILE.PY) ---
    def get_biorhythms(self):
        b_date = datetime.strptime(self.user_data["birth_date"], "%d.%m.%Y").date()
        days = (date.today() - b_date).days
        calc = lambda p: round(math.sin(2 * math.pi * days / p) * 100)
        return {"phys": calc(23), "emot": calc(28), "intel": calc(33)}

    def get_moon_phase(self):
        diff = date.today() - date(2000, 1, 6)
        days = diff.days % 29.53059
        if days < 1.84:
            return ("Новолуние", "🌑")
        elif days < 9.22:
            return ("Растущая", "🌓")
        elif days < 16.61:
            return ("Полнолуние", "🌕")
        return ("Убывающая", "🌗")

    def get_day_status(self):
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "ИНИЦИАЦИЯ (ВРЕМЯ УСТАНОВКИ ВЕКТОРОВ)"
        elif 11 <= hour < 17:
            return "ЭКСПАНСИЯ (АКТИВНАЯ ФАЗА ДЕЙСТВИЯ)"
        return "АНАЛИЗ (КАЛИБРОВКА НАСТРОЕК)"

    # --- ИНТЕРФЕЙС ---
    def init_ui(self):
        # Контейнер для смены контента (вкладок)
        self.content_area = ft.Container(expand=True)

        # Навигационная панель (стиль вашего ЛК)
        self.nav_bar = ft.Container(
            content=ft.Row([
                self._nav_item("CORE", "grid_view", True),
                self._nav_item("BIO", "accessibility", False),
                self._nav_item("EVO", "trending_up", False),
            ], alignment="center", spacing=20),
            padding=20, bgcolor="#000000", border=ft.border.only(top=ft.border.BorderSide(1, "rgba(184,155,94,0.1)"))
        )

        self.page.add(
            self._create_header(),
            self.content_area,
            self.nav_bar
        )
        self.show_core_tab()

    def _create_header(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("NEXUS_OS_V2.8", size=10, color=COLOR_GOLD, font_family="JetBrains"),
                    ft.Text(datetime.now().strftime("%d.%m.%Y"), size=10, color=COLOR_GOLD)
                ], alignment="spaceBetween"),
                ft.Text(self.user_data["name"], size=22, font_family="Cinzel", weight="bold"),
                ft.Row([
                    ft.Text(f"LVL {self.user_data['level']}", size=10, color=COLOR_GOLD),
                    ft.ProgressBar(value=self.user_data["xp"], color=COLOR_GOLD, bgcolor="#111", width=150)
                ], alignment="spaceBetween")
            ]), padding=25, bgcolor="#000000"
        )

    def show_core_tab(self):
        # Матрица Пифагора (Heatmap)
        matrix = {"1": "111", "2": "2", "3": "33", "4": "-", "5": "5", "6": "6", "7": "77", "8": "8", "9": "99"}
        grid = ft.GridView(runs_count=3, spacing=10, run_spacing=10, height=320)

        for k, v in matrix.items():
            # Логика цвета: красный - дефицит, зеленый - сила
            power = 0 if v == '-' else len(v)
            bg = COLOR_SAFE if power >= 3 else (COLOR_WARN if power == 0 else "#111")

            grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"SEC_{k}", size=8, color=COLOR_GOLD),
                        ft.Text(v, size=24, weight="bold"),
                    ], alignment="center", horizontal_alignment="center"),
                    bgcolor=bg, border_radius=12,
                    on_click=lambda e, s=k: self.show_sector_details(s)
                )
            )

        self.content_area.content = ft.ListView([
            ft.Text("МАТРИЦА ПОТЕНЦИАЛА", size=16, font_family="Cinzel", color=COLOR_GOLD),
            grid,
            ft.Divider(height=20, color="transparent"),
            ft.Container(
                content=ft.Text(self.get_day_status(), size=11, color=COLOR_GOLD, text_align="center"),
                padding=15, bgcolor="#0D0D0D", border_radius=10, border=ft.border.all(1, "rgba(184,155,94,0.1)")
            )
        ], padding=20)
        self.page.update()

    def show_bio_tab(self):
        bio = self.get_biorhythms()
        moon_name, moon_icon = self.get_moon_phase()

        self.content_area.content = ft.ListView([
            ft.Text("БИОРИТМЫ И ЦИКЛЫ", size=16, font_family="Cinzel", color=COLOR_GOLD),
            ft.Row([
                self._bio_stat("ФИЗИКА", bio["phys"], "#ff4d4d"),
                self._bio_stat("ЭМОЦИИ", bio["emot"], "#f4cf6d"),
                self._bio_stat("РАЗУМ", bio["intel"], "#4da6ff"),
            ], alignment="spaceAround"),
            ft.Container(
                content=ft.Stack([
                    ft.Image(
                        src="https://raw.githubusercontent.com/flet-dev/flet-static-archive/main/images/vitruvian_man_gold.png",
                        width=300, height=300, opacity=0.2),
                    # Точки Витрувианца (активны при биоритме > 0)
                    self._body_dot(150, 40, bio["intel"] > 0),
                    self._body_dot(150, 140, bio["emot"] > 0),
                    self._body_dot(150, 250, bio["phys"] > 0),
                ]), alignment=ft.alignment.center, height=300
            ),
            ft.Text(f"ФАЗА ЛУНЫ: {moon_name} {moon_icon}", size=12, text_align="center", color=COLOR_GOLD)
        ], padding=20)
        self.page.update()

    def show_evo_tab(self):
        # Вкладка прогресса и заданий
        self.content_area.content = ft.ListView([
            ft.Text("ПРОТОКОЛ ЭВОЛЮЦИИ", size=16, font_family="Cinzel", color=COLOR_GOLD),
            self._evo_task("СЕКТОР 4: ЗДОРОВЬЕ", "Прогулка 20 мин (дефицит ресурса)", 0.2),
            self._evo_task("СЕКТОР 2: ЭНЕРГИЯ", "Дыхательная практика", 0.6),
            self._evo_task("СЕКТОР 9: ПАМЯТЬ", "Чтение профильной литературы", 0.9),
        ], padding=20, spacing=15)
        self.page.update()

    # --- ВСПОМОГАТЕЛЬНЫЕ КОМПОНЕНТЫ ---
    def _nav_item(self, text, icon, active):
        return ft.Column([
            ft.IconButton(icon=icon, icon_color=COLOR_GOLD if active else "#444",
                          on_click=lambda e: self._handle_nav(text)),
            ft.Text(text, size=8, color=COLOR_GOLD if active else "#444")
        ], horizontal_alignment="center", spacing=0)

    def _handle_nav(self, label):
        # Обновление иконок
        for col in self.nav_bar.content.controls:
            is_match = col.controls[1].value == label
            col.controls[0].icon_color = COLOR_GOLD if is_match else "#444"
            col.controls[1].color = COLOR_GOLD if is_match else "#444"

        if label == "CORE":
            self.show_core_tab()
        elif label == "BIO":
            self.show_bio_tab()
        else:
            self.show_evo_tab()

    def _bio_stat(self, name, val, color):
        return ft.Column([
            ft.Text(name, size=9, color="#666"),
            ft.Text(f"{val}%", size=12, weight="bold", color=color),
            ft.ProgressBar(value=abs(val / 100), color=color, width=80, bgcolor="#111")
        ], horizontal_alignment="center")

    def _body_dot(self, left, top, active):
        return ft.Container(
            width=12, height=12, border_radius=6,
            bgcolor=COLOR_GOLD if active else "#222",
            left=left, top=top,
            shadow=ft.BoxShadow(blur_radius=10, color=COLOR_GOLD if active else "transparent")
        )

    def _evo_task(self, title, sub, prog):
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Text(title, size=12, weight="bold"), ft.Text(f"{int(prog * 100)}%", size=10)],
                       alignment="spaceBetween"),
                ft.ProgressBar(value=prog, color=COLOR_GOLD, bgcolor="#111", height=4)
            ]), padding=15, bgcolor="#0D0D0D", border_radius=10
        )

    def show_sector_details(self, sector):
        # Вызов детальной трактовки (имитация вашего BottomSheet)
        self.page.show_snack_bar(ft.SnackBar(ft.Text(f"СЕКТОР {sector}: Расшифровка из базы Genesis...")))


def main(page: ft.Page):
    GenesisEvolutionApp(page)


if __name__ == "__main__":
    ft.app(target=main)