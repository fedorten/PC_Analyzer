import flet as ft
import json
from pc_analizer import get_pc_info
from ai import ai_response


def main(page: ft.Page):
    page.title = "PC Анализатор"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    loading = ft.ProgressRing(visible=False, scale=0.8)
    result_container = ft.Column(spacing=15, visible=False)
    ai_result_container = ft.Column(spacing=10, visible=False)

    cpu_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("CPU", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Загрузка: ...", size=14, key="cpu"),
                ]
            ),
            padding=15,
        )
    )

    memory_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Память", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Использовано: ...", size=14, key="memory"),
                ]
            ),
            padding=15,
        )
    )

    disk_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Диск", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Использовано: ...", size=14, key="disk"),
                ]
            ),
            padding=15,
        )
    )

    processes_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Процессы", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Количество: ...", size=14, key="processes"),
                ]
            ),
            padding=15,
        )
    )

    result_container.controls = [
        ft.Row([cpu_card, memory_card], spacing=15),
        ft.Row([disk_card, processes_card], spacing=15),
    ]

    ai_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("AI Анализ (GigaChat)", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Ожидание анализа...", size=14, key="ai_text"),
                ]
            ),
            padding=15,
        )
    )
    ai_result_container.controls = [ai_card]

    async def run_analysis(e):
        loading.visible = True
        result_container.visible = False
        ai_result_container.visible = False
        page.update()

        try:
            info_str = get_pc_info()
            info = json.loads(info_str)

            cpu_val = info.get("cpu", {}).get("user", 0)
            memory_percent = info.get("memory", {}).get("percent", 0)
            disk_percent = info.get("disk", {}).get("percent", 0)
            processes = info.get("processes", 0)

            cpu_card.content.content.controls[1].value = f"Загрузка: {cpu_val}%"
            memory_card.content.content.controls[
                1
            ].value = f"Использовано: {memory_percent}%"
            disk_card.content.content.controls[
                1
            ].value = f"Использовано: {disk_percent}%"
            processes_card.content.content.controls[
                1
            ].value = f"Количество: {processes}"

            result_container.visible = True

            ai_result = ai_response("")
            ai_card.content.content.controls[1].value = ai_result
            ai_result_container.visible = True

        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {str(ex)}"))
            page.snack_bar.open = True

        loading.visible = False
        page.update()

    page.add(
        ft.Text("PC Анализатор", size=32, weight=ft.FontWeight.BOLD),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Запустить анализ",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=run_analysis,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                ),
                loading,
            ],
            spacing=20,
        ),
        ft.Divider(height=30),
        result_container,
        ai_result_container,
    )


ft.run(main)
