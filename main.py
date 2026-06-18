import flet as ft
import threading
import time

from metrics import CPUMetric, RAMMetric, DiskMetric, NetworkMetric


class MonitorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Монитор ресурсов"
        self.page.window.width = 480
        self.page.window.height = 640
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.bgcolor = "#13131f"

        self.running = True

        self._build_ui()
        self._start_update()

    def _make_card(self, title, bar_ref, label_ref, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color="#e0e0e0"),
                    ft.ProgressBar(
                        ref=bar_ref,
                        value=0,
                        color=color,
                        bgcolor="#2a2a3e",
                        height=12,
                        border_radius=6,
                    ),
                    ft.Text(ref=label_ref, value="загрузка...", size=12, color="#aaaacc"),
                ],
                spacing=8,
            ),
            padding=16,
            border_radius=14,
            bgcolor="#1c1c2e",
            margin=ft.Margin(top=0, right=0, bottom=10, left=0),
        )

    def _make_text_card(self, title, label_ref):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color="#e0e0e0"),
                    ft.Text(ref=label_ref, value="загрузка...", size=12, color="#aaaacc"),
                ],
                spacing=8,
            ),
            padding=16,
            border_radius=14,
            bgcolor="#1c1c2e",
        )

    def _build_ui(self):
        cpu_bar, cpu_text = ft.Ref[ft.ProgressBar](), ft.Ref[ft.Text]()
        ram_bar, ram_text = ft.Ref[ft.ProgressBar](), ft.Ref[ft.Text]()
        disk_bar, disk_text = ft.Ref[ft.ProgressBar](), ft.Ref[ft.Text]()
        net_text = ft.Ref[ft.Text]()

        # каждый элемент: (объект Metric, ссылка на прогресс-бар или None, ссылка на текст)
        # цикл обновления ниже работает с любым Metric одинаково — это полиморфизм
        self.metrics = [
            (CPUMetric(), cpu_bar, cpu_text),
            (RAMMetric(), ram_bar, ram_text),
            (DiskMetric("C:\\"), disk_bar, disk_text),
            (NetworkMetric(), None, net_text),
        ]

        cpu_card = self._make_card("Процессор", cpu_bar, cpu_text, "#4fc3f7")
        ram_card = self._make_card("Оперативная память", ram_bar, ram_text, "#81c784")
        disk_card = self._make_card("Диск  C:", disk_bar, disk_text, "#ffb74d")
        net_card = self._make_text_card("Сеть (за всё время сессии)", net_text)

        self.page.add(
            ft.Text(
                "Монитор ресурсов",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color="#ffffff",
            ),
            ft.Divider(height=14, color="transparent"),
            cpu_card,
            ram_card,
            disk_card,
            net_card,
        )

    def _refresh(self):
        for metric, bar_ref, text_ref in self.metrics:
            metric.update()
            if bar_ref is not None:
                bar_ref.current.value = metric.get_percent() / 100
            text_ref.current.value = metric.get_info()

        self.page.update()

    def _start_update(self):
        def loop():
            while self.running:
                self._refresh()
                time.sleep(2)

        t = threading.Thread(target=loop, daemon=True)
        t.start()


def main(page: ft.Page):
    MonitorApp(page)


ft.run(main)
