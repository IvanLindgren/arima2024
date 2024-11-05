import flet as ft
import matplotlib
from utils.Buttons import Button
from flet_navigator import *
from flet.matplotlib_chart import MatplotlibChart
from plots.test_plot import plot
matplotlib.use('svg')


@route('/plot_kran_17')
def plot_kran_17(pg:PageData) -> None:
        
    # Настройки окна программы
    pg.page.title = 'Кран 17 (графики)'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pg.page.window.min_width, pg.page.window.max_width = 1000, 1000
    pg.page.window.min_height, pg.page.window.max_height = 700, 700
    
    # Текст с названием программы
    txt_label = ft.Text(
        value='Кран 17 (графики)',
        color=ft.colors.WHITE,
        size=70,
        width=810,
        text_align=ft.TextAlign.CENTER
    )

    btn_go_home = Button(val='На главную', page=pg.page).create_btn()
    btn_go_home.on_click = lambda _: pg.navigator.navigate('/', page=pg.page)
    plots = [MatplotlibChart(figure=plot(), original_size=True, expand=True) for _ in range(10)]
    
    btn_next_plot = ft.IconButton(
        icon=ft.icons.ARROW_RIGHT,
        icon_size=40,
        bgcolor=ft.colors.INDIGO_700,
        icon_color=ft.colors.WHITE,
        tooltip='Next plot'
    )

    btn_prev_plot = ft.IconButton(
        icon=ft.icons.ARROW_LEFT,
        icon_size=40,
        bgcolor=ft.colors.INDIGO_700,
        icon_color=ft.colors.WHITE,
        tooltip='Prev plot'
    )

    cur_plot = ft.Card(
        content=plots[0],
        width=400,
        height=400
    )

    pg.page.add(
        ft.Container(
            ft.Column(
                [
                    txt_label,
                    btn_go_home
                ], spacing=20 ,horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )
     