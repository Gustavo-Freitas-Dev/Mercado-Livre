# scraper_app.py
import flet as ft
from scraper_core import buscar_produtos

class MercadoLivreScraperApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dados = []
        self.tabela = None
        self.setup_ui()

    def setup_ui(self):
        self.page.title = "Mercado Livre Scraper"
        self.page.window.width = 1000
        self.page.window.height = 750
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 40

        self.input_produto = ft.TextField(
            label="Produto",
            width=450,
            bgcolor=ft.Colors.GREY_100,
            border_radius=20,
            focused_border_color=ft.Colors.BLUE_800,
        )

        self.botao_buscar = ft.ElevatedButton(
            text="Buscar",
            icon=ft.Icons.SEARCH,
            on_click=self.capturar_produto,
            width=100,
        )

        self.botao_salvar_excel = ft.ElevatedButton(
            text="Salvar Excel",
            icon=ft.Icons.SAVE,
            on_click=self.salvar_txt,
            width=150,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            icon_color=ft.Colors.WHITE,
        )

        self.loader = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2, color=ft.Colors.BLUE_900)
        self.lista_tabela = ft.ListView(expand=True, auto_scroll=True)

        self.column_scroll = ft.Column(
            controls=[ft.Row([self.loader], alignment=ft.MainAxisAlignment.CENTER), self.lista_tabela],
            spacing=10,
        )

        self.scroll_container = ft.Container(
            content=self.column_scroll,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=10,
            expand=True,
        )

        self.page.add(
            ft.Column(
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.SHOPPING_CART, color=ft.Colors.BLUE_600, size=32),
                        ft.Text("Mercado Livre Scraper", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                    ], spacing=10),
                    ft.Divider(),
                    self.criar_container("Nome do Produto", self.input_produto, self.botao_buscar),
                    self.scroll_container,
                    ft.Row([self.botao_salvar_excel], alignment=ft.MainAxisAlignment.END),
                ],
                expand=True,
            )
        )

    def criar_container(self, titulo: str, widget: ft.Control, botao: ft.Control = None) -> ft.Container:
        controls = [
            ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Row([widget, botao] if botao else [widget], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]
        return ft.Container(
            content=ft.Column(controls=controls, spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=25,
            border_radius=20,
            bgcolor=ft.Colors.GREY_50,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.GREY_400),
        )

    def capturar_produto(self, e):
        produto = self.input_produto.value.strip()
        if produto:
            self.loader.visible = True
            self.page.update()

            self.dados = buscar_produtos(produto)

            self.loader.visible = False
            self.lista_tabela.controls.clear()

            if self.dados:
                self.criar_tabela()
                self.lista_tabela.controls.append(self.tabela)
            else:
                self.lista_tabela.controls.append(
                    ft.Text("Nenhum resultado encontrado.", color=ft.Colors.RED_600)
                )

        self.page.update()

    def criar_tabela(self):
        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Link", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(idx + 1))),
                    ft.DataCell(ft.Text(d["Título"])),
                    ft.DataCell(ft.Text(d["Preço"])),
                    ft.DataCell(ft.TextButton(text="Abrir", url=d["Link"], style=ft.ButtonStyle(color=ft.Colors.BLUE)))
                ]) for idx, d in enumerate(self.dados)
            ],
            column_spacing=60,
            width=900,
        )

    def salvar_txt(self, e):
        if self.dados:
            def on_result(e: ft.FilePickerResultEvent):
                if e.path:
                    with open(e.path, 'w', encoding='utf-8') as f:
                        for item in self.dados:
                            f.write(f"{item['Título']} - {item['Preço']} - {item['Link']}\n")
                    self.page.snack_bar = ft.SnackBar(ft.Text("Arquivo salvo com sucesso!"))
                    self.page.snack_bar.open = True
                    self.page.update()

            self.file_picker = ft.FilePicker(on_result=on_result)
            self.page.overlay.append(self.file_picker)
            self.page.update()
            self.file_picker.save_file(
                dialog_title="Salvar como...",
                file_name="produtos.txt",
                allowed_extensions=["txt"]
            )
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhum dado para salvar."))
            self.page.snack_bar.open = True
            self.page.update()
