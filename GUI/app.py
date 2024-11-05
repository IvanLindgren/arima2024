import flet as ft
import matplotlib
import warnings
from flet_navigator import *
from pages.home import home
from pages.kran_15 import kran_15
from pages.kran_17 import kran_17
from pages.balka import balka
from pages.scaner import scaner
from plots.plot_kran_15 import plot_kran_15
from plots.plot_kran_17 import plot_kran_17
matplotlib.use("svg")
warnings.filterwarnings('ignore')


def main(page: ft.Page) -> None:
    navigator = VirtualFletNavigator(
       routes={
           '/': home,
           '/kran_15': kran_15,
           '/kran_17': kran_17,
           '/balka': balka,
           '/scaner': scaner,
           '/plot_kran_15': plot_kran_15,
           '/plot_kran_17': plot_kran_17
       },
       navigator_animation=NavigatorAnimation(NavigatorAnimation.FADE)
       
    )
    
    navigator.render(page)
    
    
if __name__ == '__main__':
    ft.app(target=main)
    