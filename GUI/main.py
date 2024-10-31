import flet as ft # Фреймворк Flet для создания графического интерфейса программы
import shutil # Для работы с с файлами 
from pathlib import Path # Для работы с файлами

def main(page: ft.Page) -> None:
    
    # Выбор нужных файлов
    def pick_files(e: ft.FilePickerResultEvent) -> None:
        
        if file_picker.result and file_picker.result.files: # Если диалоговое окно закрыто и был выбран хотя бы 1 файл
            
            extensions = ['.csv', '.xlsx', '.xlsm', '.xls'] # Допустимые расширения
            
            for file in file_picker.result.files: # Перебираем все выбранные файлы
                if file.name not in sel_files and Path(file.name).suffix in extensions: # Если файла с таким именем нет в хеш-таблице
                    
                    sel_files_names.content.controls.append( # Выводим имя файла на экран
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

    # Загрузка выбранных файлов в директорию проекта
    def upload_files(e) -> None:
        
        for name, path in sel_files.items(): # Перебираем все выбранные файлы
            shutil.copy(path, f"GUI/{name}") # Копируем каждый файл в директорию проекта
            
    # Настройки окна программы
    page.title = 'Arima'
    page.window.width = 1000
    page.window.height = 700
    page.window.resizable = False
    page.bgcolor = ft.colors.INDIGO_900
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
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
    
    # Текст для кнопки 'Выбрать файлы'
    txt_btn_pick_files = ft.Text(
        value='Выбрать файлы',
        size=30,
        color=ft.colors.WHITE,
    )

    # Кнопка 'Выбрать файлы'
    btn_pick_files = ft.ElevatedButton(
        text=None,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        content=txt_btn_pick_files,
        width=400,
        height=80,
        bgcolor=ft.colors.INDIGO_700,
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )

    # Текст для кнопки 'Загрузить файлы'
    txt_btn_upload_files = ft.Text(
        value='Загрузить файлы',
        size=30,
        color=ft.colors.WHITE,
    )

    # Кнопка 'Загрузить файлы'
    btn_upload_files = ft.ElevatedButton(
        text=None,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        content=txt_btn_upload_files,
        width=400,
        height=80,
        bgcolor=ft.colors.INDIGO_700,
        on_click=upload_files
        
    )

    # Текст с названием программы
    txt_label = ft.Text(
        value='ARIMA',
        color=ft.colors.WHITE,
        size=100,
        width=400,
        text_align=ft.TextAlign.CENTER
    )

    # Отображаем все созданные объекты
    page.add(
        ft.Column(
            [
                txt_label,
                btn_pick_files,
                sel_files_names,
                btn_upload_files
            ], 
            spacing=20
        )
    )

    
if __name__ == '__main__':
    ft.app(main)