import flet as ft
from pages.home import Home
from pages.kran_15 import Kran_15
from pages.kran_17 import Kran_17
from pages.balka import Balka
from pages.scaner import Scaner


def views_handler(page) -> dict:
    return {
        '/':ft.View(
                route='/',
                controls=[Home(page).build()],
                bgcolor=ft.colors.INDIGO_900,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
        '/kran_15':ft.View(
                route='/kran_15',
                controls=[Kran_15(page).build()],
                bgcolor=ft.colors.INDIGO_900,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
        '/kran_17':ft.View(
                route='/kran_17',
                controls=[Kran_17(page).build()],
                bgcolor=ft.colors.INDIGO_900,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
        '/balka':ft.View(
                route='/balka',
                controls=[Balka(page).build()],
                bgcolor=ft.colors.INDIGO_900,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
        '/scaner':ft.View(
                route='/scaner',
                controls=[Scaner(page).build()],
                bgcolor=ft.colors.INDIGO_900,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

    }
