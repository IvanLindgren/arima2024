import flet as ft
from flet_navigator import *
from pages.home import home
from pages.kran_15 import kran_15
from pages.kran_17 import kran_17
from pages.balka import balka
from pages.scaner import scaner


def main(page: ft.Page) -> None:
    navigator = VirtualFletNavigator(
       routes={
           '/': home,
           '/kran_15': kran_15,
           '/kran_17': kran_17,
           '/balka': balka,
           '/scaner': scaner
       },
       navigator_animation=NavigatorAnimation(NavigatorAnimation.FADE)
    )
    
    navigator.render(page)
    
    
if __name__ == '__main__':
    ft.app(target=main)
    