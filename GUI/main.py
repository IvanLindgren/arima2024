import flet as ft # Фреймворк Flet для создания графического интерфейса программы
import shutil # Для работы с с файлами и директориями


def main(page: ft.Page) -> None:
    
    # Выбор нужных файлов
    def pick_files(e: ft.FilePickerResultEvent) -> None:
        if file_picker.result and file_picker.result.files: # Если диалоговое окно закрыто и был выбран хотя бы 1 файл
            
            for file in file_picker.result.files: # Перебираем все выбранные файлы
                if file.name not in sel_files: # Если файла с таким именем нет в хеш-таблице
                    sel_files_names.content.controls.append(ft.Text(file.name, size=12, color=ft.colors.WHITE)) # Выводим имя файла на экран
                    sel_files[file.name] = file.path  # Добавляем файлы в хеш - таблицу
            
            sel_files_names.update() # Обновляем список на экране

    # Загрузка выбранных файлов в директорию проекта
    def upload_files(e) -> None:
        
        for name, path in sel_files.items(): # Перебираем все выбранные файлы
            shutil.copy(path, f"GUI/{name}") # Сохраняем каждый файл в директорию проекта
            
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
    '''sel_files_names = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        width=400,
        height=80,
    )'''
    sel_files_names = ft.Card(
        color=ft.colors.INDIGO_700,
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=400,
            height=80,
        )
    )
    
    # Текст для кнопки 'Выберите файлы'
    txt_btn_pick_files = ft.Text(
        value='Выберите файлы',
        size=20,
        color=ft.colors.WHITE,
    )

    # Кнопка 'Выберите файлы'
    btn_pick_files = ft.ElevatedButton(
        content=txt_btn_pick_files,
        width=400,
        height=80,
        bgcolor=ft.colors.INDIGO_700,
        on_click=lambda _: file_picker.pick_files(allow_multiple=True)
    )

    # Текст для кнопки 'Загрузить файлы'
    txt_btn_upload_files = ft.Text(
        value='Загрузить файлы',
        size=20,
        color=ft.colors.WHITE,
    )

    # Кнопка 'Загрузить файлы'
    btn_upload_files = ft.ElevatedButton(
        content=txt_btn_upload_files,
        width=400,
        height=80,
        bgcolor=ft.colors.INDIGO_700,
        on_click=upload_files
    )

    # Отображаем все созданные объекты
    page.add(
        ft.Column(
            [
                btn_pick_files,
                sel_files_names,
                btn_upload_files
            ]
        )
    )

    
if __name__ == '__main__':
    ft.app(main)