import flet as ft # Фреймворк Flet для создания графического интерфейса программы


def main(page: ft.Page) -> None:
    
    def upload_files(e) -> None:
        upload_list = []
        if file_picker.result and file_picker.result.files:
            for f in file_picker.result.files:
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(upload_list)
            
    # Настройки окна программы
    page.window.width = 1000
    page.window.height = 700
    page.window.resizable = False
    page.bgcolor = '#171821'
    page.title = 'Arima'
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Объект для обработки загрузки файла
    file_picker = ft.FilePicker()
    file_picker.allowed_extensions = ['csv', 'xlsx']
    page.overlay.append(file_picker)
    
    # Текст для кнопки 'Выберите файл'
    txt_btn_pick_file = ft.Text(
        value='Выберите файл',
        size=20,
        color=ft.colors.WHITE
    )

    # Текст для кнопки 'Загрузить файл'
    txt_btn_upload_file = ft.Text(
        value='Загрузить файл',
        size=20,
        color=ft.colors.WHITE
    )
    
    # Кнопка 'Выберите файл'
    btn_pick_file = ft.ElevatedButton(
        content=txt_btn_pick_file,
        width=400,
        height=80,
        bgcolor='#2e2f3d',
        on_click=lambda _: file_picker.pick_files(allow_multiple=True)
    )

    # Кнопка 'Загрузить файл'
    btn_upload_file = ft.ElevatedButton(
        content=txt_btn_upload_file,
        width=400,
        height=80,
        bgcolor='#2e2f3d',
        on_click=upload_files
    )
    
    # Отображаем все созданные объекты
    page.add(
        ft.Column(
            [
                btn_pick_file,
                btn_upload_file,
            ]
        )
    )

    
if __name__ == '__main__':
    ft.app(main)