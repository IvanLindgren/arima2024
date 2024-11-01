import flet as ft
from views import views_handler


def main(page: ft.Page) -> None:
    
    def route_change(route) -> None:
        page.views.clear()
        page.views.append(
           views_handler(page)[page.route]
        )
        page.update()

    page.on_route_change = route_change
    page.go('/')
    

if __name__ == '__main__':
    ft.app(target=main)