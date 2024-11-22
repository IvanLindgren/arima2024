import flet as ft # Фреймворк для создания графического приложения
from utils.Buttons import Button # Шаблон кнопок
from utils.Banner_text import banner_text # Текст баннера
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from flet_restyle import *


@route('/')
def home(pg:PageData) -> None:
    # Открытие информационного банера
    def open_banner(e) -> None:
        pg.page.open(banner)
        pg.page.update()

    # Закрытие информационного баннера
    def close_banner(e) -> None:
        pg.page.close(banner)
        pg.page.update()

    # Настройки страницы
    pg.page.title = 'Arima'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Верхняя панель приложения
    pg.page.appbar = ft.AppBar(
        title=ft.Text(
            value='ARIMA',
            color=ft.colors.WHITE,
            size=80,
            width=400,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_700,
            style=ft.TextStyle(letter_spacing=20),
        ),
        center_title=True,
        toolbar_height=110,
        bgcolor=ft.colors.INDIGO_700,
        actions=[
            ft.IconButton(
                icon=ft.icons.INFO,
                icon_color=ft.colors.WHITE,
                icon_size=52,
                on_click=open_banner
            )
        ]
    )

    # Баннер
    banner = ft.Banner(
        bgcolor=ft.colors.INDIGO_500,
        content=ft.Text(
            value=banner_text,
            size=25,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.W_300
        ),
        actions=[
            ft.TextButton(
                text="Закрыть", 
                on_click=close_banner,
                style=ft.ButtonStyle(color=ft.colors.WHITE)
            )
        ],
        force_actions_below=True
    )

    # Создание кнопок для главной страницы
    btn_Kran_15 = Button(val='Кран 15', page=pg.page, icon_name=ft.icons.BUILD).create_btn()
    btn_Kran_17 = Button(val='Кран 17', page=pg.page, icon_name=ft.icons.BUILD).create_btn()
    btn_Balka = Button(val='Балка', page=pg.page, icon_name=ft.icons.DASHBOARD).create_btn()
    btn_Scaner= Button(val='Сканер', page=pg.page, icon_name=ft.icons.ADF_SCANNER).create_btn()
    
    # Присваиваем каждой кнопке функцию, которая будет выполняться при нажатии
    btn_Kran_15.on_click = lambda _: pg.navigator.navigate('/kran_15', page=pg.page)
    btn_Kran_17.on_click = lambda _: pg.navigator.navigate('/kran_17', page=pg.page)
    btn_Balka.on_click = lambda _: pg.navigator.navigate('/balka', page=pg.page)
    btn_Scaner.on_click = lambda _: pg.navigator.navigate('/scaner', page=pg.page)

     # Добавляем все созданные объекты на страницу
    pg.page.add(
        ft.Column(
            [
                btn_Kran_15,
                btn_Kran_17,
                btn_Balka,
                btn_Scaner
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
     