import flet as ft
from Buttons import Button
from pathlib import Path 


class Kran_17(ft.Container):
    def __init__(self, page) -> None:
        super().__init__()
        self.page = page

    
    def build(self):
            
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

        # Настройки окна программы
        '''self.page.window.width = 1000
        self.page.window.height = 700
        self.page.window.resizable = False
        self.page.bgcolor = ft.colors.INDIGO_900
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window_min_width, self.page.window_max_width = 1000, 1000
        self.page.window_min_height, self.page.window_max_height = 700, 700'''
        
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
            value='Кран 17',
            color=ft.colors.WHITE,
            size=70,
            width=810,
            text_align=ft.TextAlign.CENTER
        )

        # Создание кнопок для главной страницы
        btn_go_home = Button(val='На главную', page=self.page).create_btn()
        btn_calculate = Button(val='Произвести расчет', page=self.page).create_btn()
        btn_pick_files = Button(val='Выбрать файл', page=self.page).create_btn()
        btn_pick_files.on_click = lambda _: file_picker.pick_files(allow_multiple=True)
        btn_go_home.on_click = lambda _: self.page.go('/')
        btn_calculate.on_click = None
        # Отображаем все созданные объекты
        return ft.Column(
            [
                txt_label,
                btn_go_home,
                btn_calculate,
                btn_pick_files,
                sel_files_names
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        
        