import flet as ft # Фреймворк для создания графического приложения
import matplotlib # Для визуализации данных с помощью графиков 
import time # Для работы со временем
import warnings
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from flet.matplotlib_chart import MatplotlibChart # Для интеграции графиков в приложение
from Kran_15.Kran_15_Rez import get_kran_15_rez_data
from scripts.kran15_rez import plots_kran_15_rez
from scripts.forecast_test import arima_forecast_and_plot
matplotlib.use("svg") # Для корректного отображения графиков
warnings.filterwarnings('ignore')

@route('/forecast')
def forecast_page(pg: PageData) -> None:
    
    # Получаем аргументы с предыдущей страницы
    args = pg.arguments
    print(args)
    # Открытие информационного банера
    def open_banner(e) -> None:
        pg.page.open(banner)
        pg.page.update()

    # Закрытие информационного баннера
    def close_banner(e) -> None:
        pg.page.close(banner)
        pg.page.update()

    # Функция сохранения текущего графика в формате 'выбранная папка'/'название графика'.png
    def save(e: ft.FilePickerResultEvent) -> None:
        try:
            cur_plot.content.figure.savefig(f"{e.path}/{cur_plot_title.value}.png") 
        except:
            pass
    
    def go_home(e) -> None:
        cur_plot.content = None
        cur_plot_title.value = None
        pg.page.update()
        time.sleep(0.01)
        pg.navigator.navigate('/', page=pg.page)


    # Настройки окна программы
    pg.page.title = 'Прогноз'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Заголовок текущего графика
    cur_plot_title = ft.Text(
        color=ft.colors.WHITE,
        size=35,
        width=800,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER
    )

    btn_save = ft.IconButton(
        icon=ft.icons.SAVE,
        icon_color=ft.colors.WHITE,
        icon_size=52,
        on_click= lambda _: file_picker.get_directory_path()
    )

    btn_go_home = ft.IconButton(
        icon=ft.icons.HOME,
        icon_color=ft.colors.WHITE,
        icon_size=52,
        on_click=go_home,
        disabled=True
    )

    btn_info = ft.IconButton(
        icon=ft.icons.INFO,
        icon_color=ft.colors.WHITE,
        icon_size=52,
        on_click=open_banner,
        disabled=True
    )
    
    # Верхняя панель приложенияы
    pg.page.appbar = ft.AppBar(
        title=cur_plot_title,
        center_title=True,
        toolbar_height=110,
        bgcolor=ft.colors.INDIGO_700,
        actions=[btn_go_home, btn_save, btn_info]
    )

    banner = ft.Banner(
        bgcolor=ft.colors.INDIGO_500,
        content=ft.Text(
            value=None,
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

    # Объект для обработки выбора файла/файлов
    file_picker = ft.FilePicker(on_result=save)
    pg.page.overlay.append(file_picker)

    progress_ring = ft.ProgressRing(width=52, height=52, stroke_width=2, color=ft.colors.WHITE)
    
    # Объект, поверх которого будут выводиться текущий график
    cur_plot = ft.Card(
        content=ft.Container(
                content=progress_ring,
                alignment=ft.alignment.center,  
        ),
        width=800,
        height=525,
        color=ft.colors.INDIGO_700,
        shape=ft.RoundedRectangleBorder(radius=20)
    )

    pg.page.add(cur_plot)

    # Добавляем небольшую задержку перед отображением графиков, для корректной работы перехода между страницами
    time.sleep(0.01)
    
    
    try:
        data = arima_forecast_and_plot(data_source=args['source'], 
                                    column_name=args['param'],
                                    forecast_period=args['days'],
                                    path=args['path']
                                    )
    
        cur_plot_title.value = f"Прогноз для {data['column_name']}"
        cur_plot.content = MatplotlibChart(figure=data['plot_path'], original_size=True, expand=True)
        btn_go_home.disabled = False
        pg.page.update()

    except:
        pass

    
    
    

   