import flet as ft # Фреймворк для создания графического приложения
import matplotlib # Для визуализации данных с помощью графиков 
import time # Для работы со временем
import sys # Для корректной работы иморта файлов
import warnings
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from flet.matplotlib_chart import MatplotlibChart # Для интеграции графиков в приложение
#from Kran_15.Kran_15_Rez import get_kran_15_rez_data
from scripts.kran15_rez import plots_kran_15_rez
from scripts.forecast_test2 import evaluate_arima_model
matplotlib.use("svg") # Для корректного отображения графиков
warnings.filterwarnings('ignore')

@route('/plot_kran_15_rez')
def plot_kran_15_rez(pg: PageData) -> None:
    
    # Хеш-таблица с файлами, которые выбрал пользователь на предыдущей странице
    sel_files = pg.arguments
    
    # Создадим отдельные списки для имен файлов и путей к ним
    pathes = list(sel_files.values())
    names = list(sel_files.keys())

    # Если длина хеш-таблицы 1, значит был передан только 1 файл, поэтому списки превращаются в строки
    if len(sel_files) == 1:
        pathes = pathes[0]
        names = names[0]
    
    # Функция сохранения текущего графика в формате 'выбранная папка'/'название графика'.png
    def save(e: ft.FilePickerResultEvent) -> None:
        try:
            cur_plot.content.figure.savefig(f"{e.path}/{plot_names[plot_figs.index(cur_plot.content)]}.png") 
        except:
            pass
    
    # Перейти на следующий график
    def next_plot(e) -> None:
        cur_index = plot_figs.index(cur_plot.content)
        if cur_index < len(plot_figs) - 1:
            cur_plot.content = plot_figs[cur_index + 1]
            cur_plot_title.value = plot_names[cur_index + 1]
            if isinstance(plot_figs[cur_index + 1], ft.Column):
                btn_save.disabled = True
            else:
                btn_save.disabled = False
        cur_plot.update()
        cur_plot_title.update()
        btn_save.update()
        
    # Перейти на предыдущий график
    def prev_plot(e) -> None:
        cur_index = plot_figs.index(cur_plot.content)
        if cur_index >= 1:
            cur_plot.content = plot_figs[cur_index - 1]
            cur_plot_title.value = plot_names[cur_index - 1]
            if isinstance(plot_figs[cur_index - 1], ft.Column):
                btn_save.disabled = True
            else:
                btn_save.disabled = False
        cur_plot.update()
        cur_plot_title.update()
        btn_save.update()
        
    def go_home(e) -> None:
        try:
            plot_figs.clear()
            plot_names.clear()
            cur_plot.content = None
            cur_plot_title.value = None
            pg.page.update()
        except:
            pass
        finally:
            time.sleep(0.01)
            pg.navigator.navigate('/', page=pg.page)

    def go_forecast(e) -> None:
        plot_figs.clear()
        plot_names.clear()
        cur_plot.content = None
        cur_plot_title.value = None
        pg.page.update()
        time.sleep(0.01)
        args = {
            'path': pathes,
            'days': int(slider.value),
            'param': dd.value,
            'source': 'kran_15_rez'
        }
        pg.navigator.navigate('/forecast', page=pg.page, args=args)

    # Настройки окна программы
    pg.page.title = 'Кран 15 Rez (графики)'
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

    # Верхняя панель приложенияы
    pg.page.appbar = ft.AppBar(
        title=cur_plot_title,
        center_title=True,
        toolbar_height=110,
        bgcolor=ft.colors.INDIGO_700,
        actions=[btn_go_home, btn_save]
    )

    # Объект для обработки выбора файла/файлов
    file_picker = ft.FilePicker(on_result=save)
    pg.page.overlay.append(file_picker)

    # Создадим кнопки - иконки
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

    # Зададим кнопкам соотвествующие функции
    btn_next_plot.on_click = next_plot
    btn_prev_plot.on_click = prev_plot
    
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

    # Добавляем все созданные объекты на страницу
    all_content = ft.Column(
        [
            ft.Row([btn_prev_plot, cur_plot, btn_next_plot], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    pg.page.add(all_content)

    # Добавляем небольшую задержку перед отображением графиков, для корректной работы перехода между страницами
    time.sleep(0.01)
    
    try:
        # Передаем путь к выбранному файлу, чтобы получить словарь с графиками и их заголовками
        data = plots_kran_15_rez(paths=pathes)
        dict_plots = data['plots']
        values = data['values']
        

        btn_forecast = ft.ElevatedButton(
            content=ft.Text(
                value='Спрогнозировать',
                size=25,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.W_700,
                text_align=ft.TextAlign.CENTER
            ),
            width=400,
            height=100,
            bgcolor=ft.colors.INDIGO_500,
            on_click=go_forecast
        )

        btn_custom_arima = ft.ElevatedButton(
            content=ft.Text(
                value='Расчитать',
                size=25,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.W_700,
                text_align=ft.TextAlign.CENTER
            ),
            width=400,
            height=100,
            bgcolor=ft.colors.INDIGO_500,
            on_click=lambda _: evaluate_arima_model()
        )

        dd = ft.Dropdown(
            value=str(values[0]),
            width=100, 
            options=[ft.dropdown.Option(str(value)) for value in values],
            bgcolor=ft.colors.INDIGO_500
        )

        slider = ft.Slider(
            min=5,
            max=30,
            divisions=10,
            inactive_color=ft.colors.INDIGO_300,
            active_color=ft.colors.WHITE,
            overlay_color=ft.colors.INDIGO_100,
            label="{value} Дней",
        )
        
        selection_card = ft.Column(
            controls=[
                ft.Container(height=50),
                ft.Text(
                    value=f"Выберите прогнозируемый параметр:",
                    size=25,
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    width=700,
                    italic=True
                ),
                dd,
                ft.Container(height=50),
                ft.Text(
                    value=f"Выберите период прогнозирования:",
                    size=25,
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    width=700,
                    italic=True
                ),
                slider,
                btn_forecast
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        arima_params_card = ft.Column(
            controls=[
                ft.Text(
                    value=f"Выберите параметры ARIMA",
                    size=25,
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    width=700,
                    italic=True
                ),
                ft.Row(
                    [
                        ft.TextField(
                            label='p(0;5)',
                            width=100
                        ),
                        ft.TextField(
                            label='d(0;2)',
                            width=100
                        ),
                        ft.TextField(
                            label='q(0;5)',
                            width=100
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER
                ),
                '''ft.Column(
                    controls=[
                        None
                    ]
                )'''
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Создадим отдельные списки для графиков и их заголовков 
        plot_names = []
        plot_figs = []
        
        # Так как у некоторых графиков одинаковые заголовки, выполняем следующий код
        for name, plot in dict_plots.items():
            plot_figs.append(MatplotlibChart(figure=plot, original_size=True, expand=True))
            plot_names.append(name)
        
        plot_figs.append(selection_card)
        plot_names.append('')

        plot_figs.append(arima_params_card)
        plot_names.append('')

        # Выводим текущий график и его заголовок на экран
        cur_plot.content = plot_figs[0]
        cur_plot_title.value = plot_names[0]
        btn_go_home.disabled = False
        pg.page.update()
    except Exception as e:
        cur_plot.content = ft.Text(
            value=f'Ошибка при обработке файла!',
            color=ft.colors.RED,
            size=30,
            italic=True,
            text_align=ft.TextAlign.CENTER
        )
        
        btn_next_plot.disabled = True
        btn_prev_plot.disabled = True
        btn_save.disabled = True
        btn_go_home.disabled = False
        pg.page.update()
        
