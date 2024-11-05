import flet as ft
import matplotlib
from flet_navigator import *
from test_plot2 import plot

from flet.matplotlib_chart import MatplotlibChart
matplotlib.use('svg')


@route('/')
def main_page(pg: PageData) -> None:
    pg.page.title = 'home'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pg.page.window.min_width, pg.page.window.max_width = 1000, 1000
    pg.page.window.min_height, pg.page.window.max_height = 700, 700
    
    btn = ft.ElevatedButton(
        text='Go page 2',
        on_click=lambda _: pg.navigator.navigate('/page2', page=pg.page)
    )
    
    pg.page.add(
        ft.Column(
            [btn, btn, btn, btn, btn],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


@route('/page2')
def page2(pg: PageData) -> None:
    pg.page.title = '2'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pg.page.window.min_width, pg.page.window.max_width = 1000, 1000
    pg.page.window.min_height, pg.page.window.max_height = 700, 700
    
    btn = ft.ElevatedButton(
        text='Go page 3',
        on_click=lambda _: pg.navigator.navigate('/page3', page=pg.page)
    )
    
    pg.page.add(
        ft.Column(
            [btn, btn, btn, btn, btn],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


@route('/page3')
def page3(pg: PageData) -> None:
    pg.page.title = '3'
    pg.page.window.width = 1000
    pg.page.window.height = 700
    pg.page.window.resizable = False
    pg.page.bgcolor = ft.colors.INDIGO_900
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pg.page.window.min_width, pg.page.window.max_width = 1000, 1000
    pg.page.window.min_height, pg.page.window.max_height = 700, 700
    
    btn = ft.ElevatedButton(
        text='Go home',
        on_click=lambda _: pg.navigator.navigate('/', page=pg.page)
    )
    
    #plot1 = MatplotlibChart(figure=plot(), original_size=False, isolated=True)
    img = ft.Image(src='plot_Uvx_20.png', width=400, height=400),
        
    
    pg.page.add(
        ft.Column(
            [img],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )



def main(page: ft.Page) -> None:
    navigator = VirtualFletNavigator(
        routes={
            '/': main_page,
            '/page2': page2,
            '/page3': page3
        },
        navigator_animation=NavigatorAnimation(NavigatorAnimation.FADE)
    )

    navigator.render(page)


if __name__ == '__main__':
    ft.app(target=main)