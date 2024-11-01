import flet as ft
from pages.home import Home


def views_handler(page) -> dict:
    return {
        '/':ft.View(
                route='/',
                controls=[
                    Home(page)
                ]
            ),
        '/kran_15':ft.View(
                route='/kran_15',
                controls=[
                    ft.Container(
                        height=700,
                        width=1000,
                        bgcolor=ft.colors.RED
                    )
                ]
            ),
        '/kran_17':ft.View(
                route='/kran_17',
                controls=[
                    ft.Container(
                        height=700,
                        width=1000,
                        bgcolor=ft.colors.GREEN
                    )
                ]
            ),
        '/balka':ft.View(
                route='/balka',
                controls=[
                    ft.Container(
                        height=700,
                        width=1000,
                        bgcolor=ft.colors.BLUE
                    )
                ]
            ),
        '/scaner':ft.View(
                route='/scaner',
                controls=[
                    ft.Container(
                        height=700,
                        width=1000,
                        bgcolor=ft.colors.YELLOW
                    )
                ]
            ),

    }
