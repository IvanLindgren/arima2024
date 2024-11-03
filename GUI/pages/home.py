import flet as ft
from utils.Buttons import Button
from flet_navigator import *


@route('/')
def home(pg:PageData) -> None:
        
    # Настройки окна программы
    pg.page.title = 'Arima'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pg.page.window_min_width, pg.page.window_max_width = 1000, 1000
    pg.page.window_min_height, pg.page.window_max_height = 700, 700
    
    # Текст с названием программы
    txt_label = ft.Text(
        value='ARIMA',
        color=ft.colors.WHITE,
        size=100,
        width=810,
        text_align=ft.TextAlign.CENTER
    )

    # Создание кнопок для главной страницы
    btn_Kran_15 = Button(val='Кран 15', page=pg.page).create_btn()
    btn_Kran_17 = Button(val='Кран 17', page=pg.page).create_btn()
    btn_Balka = Button(val='Балка', page=pg.page).create_btn()
    btn_Scaner= Button(val='Сканер', page=pg.page).create_btn()
    btn_info = Button(val='Информация', page=pg.page, width=810).create_btn()

    btn_Kran_15.on_click = lambda _: pg.navigator.navigate('/kran_15', page=pg.page)
    btn_Kran_17.on_click = lambda _: pg.navigator.navigate('/kran_17', page=pg.page)
    btn_Balka.on_click = lambda _: pg.navigator.navigate('/balka', page=pg.page)
    btn_Scaner.on_click = lambda _: pg.navigator.navigate('/scaner', page=pg.page)

    pg.page.add(
        ft.Container(
            ft.Column(
                [
                    txt_label,
                    ft.Row([btn_Kran_15, btn_Balka], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([btn_Kran_17, btn_Scaner], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    btn_info
                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )
     