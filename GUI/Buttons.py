import flet as ft


# Класс, который отвечает за создание типовых кнопок, которые используются во всем приложении
class Button:
    # Инициализация входных параметров
    def __init__(self, val: str,  page: ft.Page, width=400, ) -> None:
        self.val = val
        self.width = width
        self.page = page

    # Создание кнопки на основе входных параметров
    def create_btn(self) -> ft.ElevatedButton:
        
        txt = ft.Text(value=self.val,
                      color=ft.colors.WHITE,
                      text_align=ft.TextAlign.CENTER,
                      size=30,
                      style=ft.TextStyle()
        )
        
        btn = ft.ElevatedButton(content=txt,
                                text=None,
                                width=self.width,
                                bgcolor=ft.colors.INDIGO_700,
                                height=80,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
        
        return btn
