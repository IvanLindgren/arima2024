import flet as ft # Фреймворк Flet для создания графического интерфейса программы
import shutil # Для работы с с файлами 
from pathlib import Path # Для работы с файлами
from Buttons import Button # Импортируем созданный класс для кнопок
from views import views_handler

def main(page: ft.Page) -> None:
    
    # Выбор нужных файлов
    def pick_files(e: ft.FilePickerResultEvent) -> None:
        
        if file_picker.result and file_picker.result.files: # Если диалоговое окно закрыто и был выбран хотя бы 1 файл
            
            extensions = ['.csv', '.xlsx', '.xlsm', '.xls'] # Допустимые расширения
            
            for file in file_picker.result.files:
                # Если файла с таким именем нет в хеш-таблице и у него допустимое расширение
                if file.name not in sel_files and Path(file.name).suffix in extensions: 
                    # Выводим имя файла на экран                                                                
                    sel_files_names.content.controls.append( 
                        ft.Text(
                            file.name,
                            size=20,
                            color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                            width=400
                        )
                    )
                    
                    sel_files[file.name] = file.path  # Добавляем файлы в хеш - таблицу
            
            sel_files_names.update() # Обновляем список на экране

    def route_change(route) -> None:
        page.views.clear()
        page.views.append(
           views_handler(page)
        )

    # Настройки окна программы
    page.title = 'Arima'
    page.window.width = 1000
    page.window.height = 700
    page.window.resizable = False
    page.bgcolor = ft.colors.INDIGO_900
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.on_route_change = route_change
    
    
    
    # Объект для обработки загрузки файла
    file_picker = ft.FilePicker(on_result=pick_files)
    page.overlay.append(file_picker)
    
    # Список выбранных файлов
    sel_files = dict()
    
    # Колонка с именами выбранных файлов
    sel_files_names = ft.Card(
        color=ft.colors.INDIGO_700,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            width=400,
            height=80,
        )
    )
    
    # Текст с названием программы
    txt_label = ft.Text(
        value='ARIMA',
        color=ft.colors.WHITE,
        size=100,
        width=810,
        text_align=ft.TextAlign.CENTER
    )

    # Создание кнопок для главной страницы
    btn_Kran_15 = Button(val='Кран 15', page=page).create_btn()
    btn_Kran_17 = Button(val='Кран 17', page=page).create_btn()
    btn_Balka = Button(val='Балка', page=page).create_btn()
    btn_Scaner= Button(val='Сканер', page=page).create_btn()
    btn_info = Button(val='Информация', page=page, width=810).create_btn()

    btn_Kran_15.on_click = lambda _: page.go('/kran_17')

    # Отображаем все созданные объекты
    page.add(
        ft.Column(
            [
                txt_label,
                ft.Row([btn_Kran_15, btn_Balka], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([btn_Kran_17, btn_Scaner], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                btn_info
            ], 
            spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    
if __name__ == '__main__':
    ft.app(main)