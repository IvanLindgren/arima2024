import flet as ft # Фреймворк Flet для создания графического интерфейса программы
import shutil # Для работы с с файлами и директориями


def main(page: ft.Page) -> None:
    
    # Выбираем нужные файлы
    def pick_files(e: ft.FilePickerResultEvent) -> None:
        if file_picker.result and file_picker.result.files:
            
            for file in file_picker.result.files:
                if file not in selected_files:
                    selected_files_names.controls.append(ft.Text(file.name))
                    selected_files.append(file)

            selected_files_names.update()

    # Загрузка выбранных файлов в директорию проекта
    def upload_files(e) -> None:
        
        for file in selected_files:
            shutil.copy(file.path, f"GUI/{file.name}")
            
    # Настройки окна программы
    page.window.width = 1000
    page.window.height = 700
    page.window.resizable = False
    page.bgcolor = '#171821'
    page.title = 'Arima'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    # Объект для обработки загрузки файла
    file_picker = ft.FilePicker(on_result=pick_files)
    
    # Список выбранных файлов
    selected_files = []
    
    # Колонка с именами выбранных файлов
    selected_files_names = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        width=400,
        height=80,
    )
    page.overlay.append(file_picker)
    
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
        bgcolor='#2e2f3d',
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
        bgcolor='#2e2f3d',
        on_click=upload_files
    )

    # Отображаем все созданные объекты
    page.add(
        ft.Column(
            [
                btn_pick_files,
                selected_files_names,
                btn_upload_files
            ]
        )
    )

    
if __name__ == '__main__':
    ft.app(main)