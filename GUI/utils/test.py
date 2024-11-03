import flet as ft
from flet_navigator import *


@route('/')
def home(pg: PageData) -> None:
    pg.page.title = 'Home page'
    pg.page.window.width = 600
    pg.page.window.height = 300
    pg.page.bgcolor = ft.colors.DEEP_PURPLE_700
    
    pg.page.add(
        ft.ElevatedButton(
            text='Go page 2',
            on_click=lambda _: pg.navigator.navigate('/page2', page=pg.page),
            color=ft.colors.DEEP_PURPLE_300
        )
    )


@route('/page2')
def page2(pg: PageData) -> None:
    pg.page.title = 'Page 2'
    pg.page.window.width = 600
    pg.page.window.height = 400
    pg.page.bgcolor = ft.colors.BLUE_GREY_900
    
    pg.page.add(
        ft.ElevatedButton(
            text='Go home',
            on_click=lambda _: pg.navigator.navigate('/', page=pg.page)
        )
    )


def main(page: ft.Page) -> None:
   navigator = VirtualFletNavigator(
       routes={'/': home, '/page2': page2},
       navigator_animation=NavigatorAnimation(NavigatorAnimation.SCALE)
   )
   
   navigator.render(page)


if __name__ == '__main__':
    ft.app(target=main)