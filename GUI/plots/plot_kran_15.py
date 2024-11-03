import flet as ft
from GUI.utils.Buttons import Button


class Home(ft.Column):
    def __init__(self, page) -> None:
        super().__init__()
        self.page = page

    def build(self):
        
        # Настройки окна программы
        self.page.title = 'Arima'
        self.page.window.width = 1000
        self.page.window.height = 700
        self.page.window.resizable = False
        #self.page.bgcolor = ft.colors.INDIGO_900
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window_min_width, self.page.window_max_width = 1000, 1000
        self.page.window_min_height, self.page.window_max_height = 700, 700
        
        # Текст с названием программы
        txt_label = ft.Text(
            value='ARIMA',
            color=ft.colors.WHITE,
            size=100,
            width=810,
            text_align=ft.TextAlign.CENTER
        )

        # Создание кнопок для главной страницы
        btn_Kran_15 = Button(val='Кран 15', page=self.page).create_btn()
        btn_Kran_17 = Button(val='Кран 17', page=self.page).create_btn()
        btn_Balka = Button(val='Балка', page=self.page).create_btn()
        btn_Scaner= Button(val='Сканер', page=self.page).create_btn()
        btn_info = Button(val='Информация', page=self.page, width=810).create_btn()

        btn_Kran_15.on_click = lambda _: self.page.go('/kran_15')
        btn_Kran_17.on_click = lambda _: self.page.go('/kran_17')
        btn_Balka.on_click = lambda _: self.page.go('/balka')
        btn_Scaner.on_click = lambda _: self.page.go('/scaner')

        # Отображаем все созданные объекты
        return ft.Column(
            [
                txt_label,
                ft.Row([btn_Kran_15, btn_Balka], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([btn_Kran_17, btn_Scaner], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                btn_info
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        
        
        