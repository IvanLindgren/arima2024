import flet as ft 
import matplotlib
import time
import sys
sys.path.append('C:/Users/user/Desktop/arima2024')
from utils.Buttons import Button
from flet_navigator import *
from flet.matplotlib_chart import MatplotlibChart
from plots.test_plot import plot, save_plot
from Kran_15.Kran_15 import get_fig_list
matplotlib.use("svg")


@route('/plot_kran_15')
def plot_kran_15(pg: PageData) -> None:
    
    # Хэш-таблица с выбранными файлами
    sel_files = pg.arguments
    pathes = [i for i in sel_files.values()]
    names = [i for i in sel_files.keys()]
    
    def save(e: ft.FilePickerResultEvent):
        save_plot(figure=cur_plot.content.figure, path=e.path, plot_name='График 1.png')
    
    # Перейти на следующий график
    def next_plot(e) -> None:
        cur_index = plots.index(cur_plot.content)
        if cur_index < 6:
            cur_plot.content = plots[cur_index + 1]
        cur_plot.update()

    # Перейти на предыдущий график
    def prev_plot(e) -> None:
        cur_index = plots.index(cur_plot.content)
        if cur_index > 1:
            cur_plot.content = plots[cur_index - 1]
        cur_plot.update()

    # Настройки окна программы
    pg.page.title = 'Кран 15 (графики)'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    pg.page.appbar = ft.AppBar(
        title=ft.Text(
            value='Графики (Кран 15)',
            color=ft.colors.WHITE,
            size=80,
            width=800,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_700,
        ),
        center_title=True,
        toolbar_height=110,
        bgcolor=ft.colors.INDIGO_700,
        actions=[
            ft.IconButton(
                icon=ft.icons.HOME,
                icon_color=ft.colors.WHITE,
                icon_size=52,
                on_click=lambda _: pg.navigator.navigate('/', page=pg.page)
            ),
            ft.IconButton(
                icon=ft.icons.SAVE,
                icon_color=ft.colors.WHITE,
                icon_size=52,
                on_click= lambda _: file_picker.get_directory_path()
                
            )
        ]
    )

    file_picker = ft.FilePicker(on_result=save)
    pg.page.overlay.append(file_picker)

    btn_next_plot = ft.IconButton(
        icon=ft.icons.ARROW_RIGHT,
        icon_size=40,
        bgcolor=ft.colors.INDIGO_700,
        icon_color=ft.colors.WHITE,
        tooltip='Следующий график',
    )
    btn_prev_plot = ft.IconButton(
        icon=ft.icons.ARROW_LEFT,
        icon_size=40,
        bgcolor=ft.colors.INDIGO_700,
        icon_color=ft.colors.WHITE,
        tooltip='Предыдущий график'
    )

    btn_next_plot.on_click = next_plot
    btn_prev_plot.on_click = prev_plot
    
    cur_plot = ft.Card(
        width=800,
        height=500,
        color=ft.colors.INDIGO_700,
        shape=ft.RoundedRectangleBorder(radius=20)
    )
    
    all_content = ft.Column(
        [
            ft.Row([btn_prev_plot, cur_plot, btn_next_plot], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    pg.page.add(all_content)

    time.sleep(0.01)
    
    plots = [MatplotlibChart(figure=fig, expand=True) for fig in get_fig_list(path=pathes[0])]
    #plots = [MatplotlibChart(figure=plot(), original_size=True, expand=True) for _ in range(10)]
    
    cur_plot.content = plots[0]
    cur_plot.update()


   