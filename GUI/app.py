import flet as ft # Фреймворк для создания графического приложения
import matplotlib # Для визуализации данных с помощью графиков 
import warnings # Чтобы убрать ненужные предупреждения
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from pages.home import home # Главная страница приложения
from pages.forecast_page import forecast_page # Страница с прогнозом
from pages.file_pick_page import file_pick_page # Страница выбора файлов
from pages.plots_page import plots_page # Страница с графиками
matplotlib.use("svg") # Для корректного отображения графиков
warnings.filterwarnings('ignore') # Игнорируем ненужные предупреждения


def main(page: ft.Page) -> None:
    
    # Объект, который отвечает за навигацию между страницами
    navigator = VirtualFletNavigator(
       routes={
           '/': home,
           '/file_pick_page': file_pick_page,
           '/plots_page': plots_page,
           '/forecast_page': forecast_page
        }
    )
    
    navigator.render(page)
    
    
if __name__ == '__main__':
    ft.app(target=main)
