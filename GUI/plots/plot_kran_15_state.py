import flet as ft # Фреймворк для создания графического приложения
import matplotlib # Для визуализации данных с помощью графиков 
import time # Для работы со временем
import sys # Для корректной работы иморта файлов
import warnings
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from flet.matplotlib_chart import MatplotlibChart # Для интеграции графиков в приложение
from Kran_15.Kran_15_Rez import get_kran_15_rez_data
from Kran_15.Kran_15_State import get_kran_15_state_data
matplotlib.use("svg") # Для корректного отображения графиков
warnings.filterwarnings('ignore')

@route('/plot_kran_15_state')
def plot_kran_15_state(pg: PageData) -> None:
    
    # Хеш-таблица с файлами, которые выбрал пользователь на предыдущей странице
    sel_files = pg.arguments
    
    # Создадим отдельные списки для имен файлов и путей к ним
    pathes = list(sel_files.values())
    names = list(sel_files.keys())

    # Если длина хеш-таблицы 1, значит был передан только 1 файл, поэтому списки превращаются в строки
    if len(sel_files) == 1:
        pathes = pathes[0]
        names = names[0]
    
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
            cur_plot.content.figure.savefig(f"{e.path}/{plot_names[plot_figs.index(cur_plot.content)]}.png") 
        except:
            pass
        
    # Перейти на следующий график
    def next_plot(e) -> None:
        cur_index = plot_figs.index(cur_plot.content)
        btn_info.disabled = True
        if cur_index < len(plot_figs) - 1:
            cur_plot.content = plot_figs[cur_index + 1]
            cur_plot_title.value = plot_names[cur_index + 1]
            if cur_index + 1 >= 13:
                btn_info.disabled = False
                banner.content = ft.Text(
                    value=metrics[cur_index + 1 - 13],
                    size=25,
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.W_300
                )
        pg.page.update()

    # Перейти на предыдущий график
    def prev_plot(e) -> None:
        cur_index = plot_figs.index(cur_plot.content)
        btn_info.disabled = True
        if cur_index >= 1:
            cur_plot.content = plot_figs[cur_index - 1]
            cur_plot_title.value = plot_names[cur_index - 1]
            if cur_index - 1 >= 13:
                btn_info.disabled = False
                banner.content = ft.Text(
                    value=metrics[cur_index -1 - 13],
                    size=25,
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.W_300
                )
        pg.page.update()

    def go_home(e) -> None:
        try:
            plot_figs.clear()
            plot_names.clear()
            cur_plot.content = None
            cur_plot_title.value = None
            pg.page.update()
            time.sleep(0.01)
        except:
            pass
        finally:
            pg.navigator.navigate('/', page=pg.page)


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
        size=25,
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
        on_click=go_home
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
    
    pr = ft.ProgressRing(width=52, height=52, stroke_width=2, color=ft.colors.WHITE)
    
    # Объект, поверх которого будут выводиться текущий график
    cur_plot = ft.Card(
        width=800,
        height=525,
        color=ft.colors.INDIGO_700,
        shape=ft.RoundedRectangleBorder(radius=20)
    )

    stack = ft.Stack(
        controls=[
            cur_plot,
            ft.Container(
                content=pr,
                alignment=ft.alignment.center,  
            ),
        ],
        width=800,
        height=525,
    )

    cont = ft.Container(stack)

    # Добавляем все созданные объекты на страницу
    all_content = ft.Column(
        [
            ft.Row([btn_prev_plot, cont, btn_next_plot], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    pg.page.add(all_content)

    # Добавляем небольшую задержку перед отображением графиков, для корректной работы перехода между страницами
    time.sleep(0.01)
    
    try:
        # Передаем путь к выбранному файлу, чтобы получить словарь с графиками и их заголовками
        data = get_kran_15_state_data(file_pathes=pathes)
        dict_plots = data['plots']

        # Создадим отдельные списки для графиков и их заголовков 
        plot_names = []
        plot_figs = []
        metrics = []

        # Так как у некоторых графиков одинаковые заголовки, выполняем следующий код
        for name, plot in dict_plots.items():
            if type(plot) == list:
                for subplot in plot:
                    plot_figs.append(MatplotlibChart(figure=subplot, original_size=True, expand=True))
                    plot_names.append(name)
            else:
                plot_figs.append(MatplotlibChart(figure=plot, original_size=True, expand=True))
                plot_names.append(name)

        # Работаем со словарем 'forecasts':
        forecasts = data['forecasts']

        for name, name_data in forecasts.items():
            plot_figs.append(MatplotlibChart(figure=name_data['plot'], original_size=True, expand=True))
            plot_names.append('Прогноз')
            tmp = 'Метрики: '
            for key, value in name_data['parametrs'].items():
                tmp += f'{key}: {value} '
            metrics.append(tmp)

        # Выводим текущий график и его заголовок на экран
        cur_plot.content = plot_figs[0]
        cur_plot_title.value = plot_names[0]
        pr.disabled = True
        pr.visible = False
        pg.page.update()
    except:
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
        pr.disabled = True
        pr.visible = False
        pg.page.update()
    

    
    
    

   