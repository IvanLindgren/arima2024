import flet as ft # Фреймворк для создания графического приложения
from utils.Buttons import Button # Шаблон кнопок
from utils.Banner_text import banner_text # Текст баннера
from flet_navigator import * # Дополнение для более удобной навигации между страницами


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
        bgcolor=ft.colors.INDIGO_700,
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
    btn_Kran_15_rez = Button(val='Rez', page=pg.page, height=52).create_popup_button()
    btn_Kran_15_state = Button(val='State', page=pg.page, height=52).create_popup_button()
    btn_Kran_17_rez = Button(val='Rez', page=pg.page, height=52).create_popup_button()
    btn_Kran_17_state = Button(val='State', page=pg.page, height=52).create_popup_button()
    btn_Balka = Button(val='Балка', page=pg.page, icon_name=ft.icons.DASHBOARD).create_btn()
    btn_Scaner= Button(val='Сканер', page=pg.page, icon_name=ft.icons.ADF_SCANNER).create_btn()
    
    # Присваиваем каждой кнопке функцию, которая будет выполняться при нажатии
    btn_Kran_15_rez.on_click = lambda _: pg.navigator.navigate('/kran_15_rez', page=pg.page)
    btn_Kran_15_state.on_click = lambda _: pg.navigator.navigate('/kran_15_state', page=pg.page)
    btn_Kran_17_rez.on_click = lambda _: pg.navigator.navigate('/kran_17_rez', page=pg.page)
    btn_Kran_17_state.on_click = None
    btn_Balka.on_click = lambda _: pg.navigator.navigate('/balka', page=pg.page)
    btn_Scaner.on_click = lambda _: pg.navigator.navigate('/scaner', page=pg.page)

    btn_Kran_15.disabled = True
    btn_Kran_17.disabled = True

    menu_btn_kran_15 = ft.PopupMenuButton(
        content=btn_Kran_15,
        items=[
            btn_Kran_15_rez,
            btn_Kran_15_state
        ],
        bgcolor=ft.colors.INDIGO_500,
        menu_position=ft.PopupMenuPosition.UNDER,
        tooltip='Выберите тип'
    )

    menu_btn_kran_17 = ft.PopupMenuButton(
        content=btn_Kran_17,
        items=[
            btn_Kran_17_rez,
            btn_Kran_17_state
        ],
        bgcolor=ft.colors.INDIGO_500,
        menu_position=ft.PopupMenuPosition.UNDER,
        tooltip='Выберите тип'
    )
    
    # Добавляем все созданные объекты на страницу
    pg.page.add(
        ft.Column(
            [
                menu_btn_kran_15,
                menu_btn_kran_17,
                btn_Balka,
                btn_Scaner,
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
     