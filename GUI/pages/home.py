import flet as ft
from Buttons import Button

from pathlib import Path 


class Home(ft.UserControl):
    def __init__(self, page) -> None:
        super().__init__()
        self.page = page

    def build(self):
        
        def pick_files(self, e: ft.FilePickerResultEvent) -> None:
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

      

        # Настройки окна программы
        self.page.title = 'Arima'
        self.page.window.width = 1000
        self.page.window.height = 700
        self.page.window.resizable = False
        self.page.bgcolor = ft.colors.INDIGO_900
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        
        # Объект для обработки загрузки файла
        file_picker = ft.FilePicker(on_result=pick_files)
        self.page.overlay.append(file_picker)
        
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
        btn_Kran_15 = Button(val='Кран 15', page=self.page).create_btn()
        btn_Kran_17 = Button(val='Кран 17', page=self.page).create_btn()
        btn_Balka = Button(val='Балка', page=self.page).create_btn()
        btn_Scaner= Button(val='Сканер', page=self.page).create_btn()
        btn_info = Button(val='Информация', page=self.page, width=810).create_btn()

        btn_Kran_15.on_click = lambda _: self.page.go('/kran_15')
        btn_Kran_17.on_click = lambda _: self.page.go('/kran_17')
        btn_Balka.on_click = lambda _: self.page.go('/balka')
        btn_Scaner.on_click = lambda _: self.page.go('/scaner')

        # Отображаем все созданные объекты
        return ft.Column(
                [
                    txt_label,
                    ft.Row([btn_Kran_15, btn_Balka], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([btn_Kran_17, btn_Scaner], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    btn_info
                ], 
                spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        