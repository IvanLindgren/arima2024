import flet as ft # Фреймворк для создания графического приложения
import matplotlib # Для визуализации данных с помощью графиков 
import time # Для работы со временем
import warnings
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from flet.matplotlib_chart import MatplotlibChart # Для интеграции графиков в приложение
from matplotlib.figure import Figure
from scripts.Kran15_rez import get_data_kran_15_rez
from scripts.forecast import arima_forecast_and_plot, evaluate_arima_model
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

     # Перейти на следующий график
    def next_plot(e) -> None:
        cur_index = plot_figs.index(cur_plot.content)
        if cur_index < len(plot_figs) - 1:
            cur_plot.content = plot_figs[cur_index + 1]
            cur_plot_title.value = plot_names[cur_index + 1]
            
        cur_plot.update()
        cur_plot_title.update()
        
        
    # Перейти на предыдущий график
    def prev_plot(e) -> None:
        cur_index = plot_figs.index(cur_plot.content)
        if cur_index >= 1:
            cur_plot.content = plot_figs[cur_index - 1]
            cur_plot_title.value = plot_names[cur_index - 1]
            
        cur_plot.update()
        cur_plot_title.update()
        

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
        bgcolor=ft.colors.INDIGO_700,
        content=None,
        actions=[
            ft.TextButton(
                text="Закрыть", 
                on_click=close_banner,
                style=ft.ButtonStyle(color=ft.colors.WHITE)
            )
        ],
        force_actions_below=True
    )

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
        tooltip='Предыдущий график',
    )

    btn_next_plot.on_click = next_plot
    btn_prev_plot.on_click = prev_plot

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

    pg.page.add(
        ft.Column(
                [
                    ft.Row([btn_prev_plot, cur_plot, btn_next_plot], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Добавляем небольшую задержку перед отображением графиков, для корректной работы перехода между страницами
    time.sleep(0.01)
    
    
    try:
        data = arima_forecast_and_plot(data_source=args['source'], 
                                    column_name=args['param'],
                                    forecast_period=args['days'],
                                    paths=args['path'],
                                    custom_order=args['order']
                                    )
        
        print(data)
        banner_data = ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(f"Параметр: {data['column_name']}", size=11),
                        ft.Text(f"Источник: {data['data_source']}", size=11),
                        ft.Text(f"Период предсказания: {data['forecast_period']}", size=11),
                        ft.Text(f"Последняя дата: {data['last_date']}", size=11),
                    ]
                ),
                ft.Text(f"Метрики: {data['metrics']}", size=11),
                ft.Text(f"Предсказанные значения: {data['forecast_values']}", size=11),
                ft.Text(f"Предсказанные индексы: {data['forecast_index']}", size=11),
                ft.Text(f"Реальные значения {data['actual_values']}", size=11),
                ft.Text(f"Реальные индексы: {data['actual_index']}", size=11),
                ft.Text(f"Тесты на стационарность: {data['stationarity_tests']}", size=11),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.START
        )

        

        

        plot_names = [
            f"Прогноз для {data['column_name']}",
        ]
        plot_figs = [
            MatplotlibChart(figure=data['plot'], original_size=True, expand=True),
        ]

        if isinstance(args['path'], list) and len(args['path']) != 1 and not 'error' in data['decomposition'] and isinstance(data['acf_pacf_plot'], Figure):
            banner_data.controls.extend(
                [
                    ft.Text(f"Декомпозиция: Тренд: {data['decomposition']['trend']}", size=11),
                    ft.Text(f"Декомпозиция: Сезонность: {data['decomposition']['seasonal']}", size=11),
                    ft.Text(f"Декомпозиция: Resid: {data['decomposition']['resid']}", size=11)
                ]
            )
            plot_figs.extend(
                [
                    MatplotlibChart(figure=data['decomposition']['plot'], original_size=True, expand=True),
                    MatplotlibChart(figure=data['acf_pacf_plot'], original_size=True, expand=True)
                ]
            )
            plot_names.extend(
                [
                    f"График декомпозиции для {data['column_name']}",
                    f"Графики ACF, PACF для {data['column_name']}"
                ]
            )


        banner.content = banner_data
        cur_plot.content = plot_figs[0]
        cur_plot_title.value = plot_names[0]
        btn_go_home.disabled = False
        pg.page.update()

    except:
        cur_plot.content = ft.Text(
            value=f'Ошибка при прогнозировании!',
            color=ft.colors.RED,
            size=30,
            italic=True,
            text_align=ft.TextAlign.CENTER
        )
        btn_save.disabled = True
        btn_go_home.disabled = False
        pg.page.update()

    
    
    

   