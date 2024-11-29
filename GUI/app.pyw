import flet as ft # Фреймворк для создания графического приложения
import matplotlib # Для визуализации данных с помощью графиков 
import warnings # Чтобы убрать ненужные предупреждения
from flet_navigator import * # Дополнение для более удобной навигации между страницами
from pages.home import home # Главная страница приложения
from pages.kran_15_rez import kran_15_rez # Страница Кран 15
from pages.kran_15_state import kran_15_state
from pages.kran_17_rez import kran_17_rez # Страница Кран 17
from pages.balka import balka # Страница Балка
from pages.scaner import scaner # Страница Сканер
from plots.plot_kran_15_rez import plot_kran_15_rez # Страница с графиками Кран 15
from plots.plot_kran_15_state import plot_kran_15_state
from plots.plot_kran_17_rez import plot_kran_17_rez # Страница с графиками Кран 17
from plots.plot_balka import plot_balka # Страница с графиками Балка
from plots.plot_scaner import plot_scaner# Страница с графиками Сканер
matplotlib.use("svg") # Для корректного отображения графиков
warnings.filterwarnings('ignore') # Игнорируем ненужные предупреждения


def main(page: ft.Page) -> None:
    
    # Объект, который отвечает за навигацию между страницами
    navigator = VirtualFletNavigator(
       routes={
           '/': home,
           '/kran_15_rez': kran_15_rez,
           '/kran_15_state': kran_15_state,
           '/kran_17': kran_17_rez,
           '/balka': balka,
           '/scaner': scaner,
           '/plot_kran_15_rez': plot_kran_15_rez,
           '/plot_kran_15_state': plot_kran_15_state,
           '/plot_kran_17': plot_kran_17_rez,
           '/plot_balka': plot_balka,
           '/plot_scaner': plot_scaner
        },
        navigator_animation=NavigatorAnimation(NavigatorAnimation.NONE),
    )
    
    navigator.render(page)
    
    
if __name__ == '__main__':
    ft.app(target=main)
