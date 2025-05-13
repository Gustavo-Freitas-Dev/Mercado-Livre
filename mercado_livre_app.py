# main.py
import flet as ft
from scraper_app import MercadoLivreScraperApp

def main(page: ft.Page):
    MercadoLivreScraperApp(page)

ft.app(target=main)
