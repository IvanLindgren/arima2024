import flet as ft
from views import views_handler
from flet_navigator import PageData, render, anon, route


def main(page: ft.Page) -> None:
    
    def route_change(route) -> None:
        page.views.clear()
        page.views.append(
           views_handler(page)[page.route]
        )
        page.update()

    page.title = 'Arima'
    page.window.width = 1000
    page.window.height = 700
    page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.min_width, page.window.max_width = 1000, 1000
    page.window.min_height, page.window.max_height = 700, 700
    
    page.on_route_change = route_change
    page.go('/')
    
    
if __name__ == '__main__':
    ft.app(target=main)
    