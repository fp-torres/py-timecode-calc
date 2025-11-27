import flet as ft
from timecode import Timecode

def main(page: ft.Page):
    # --- Configurações da Janela ---
    page.title = "Timecode Calculator Pro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK  # Visual Dark moderno
    page.window_width = 400
    page.window_height = 600

    # --- Lógica de Cálculo ---
    def calcular_click(e):
        try:
            # Pega os valores da tela
            fps = fps_dropdown.value
            tc1_val = tc1_input.value
            tc2_val = tc2_input.value
            op = operacao_dropdown.value

            # Cria objetos Timecode
            t1 = Timecode(fps, tc1_val)
            t2 = Timecode(fps, tc2_val)

            # Faz a conta
            if op == "Somar (+)":
                resultado = t1 + t2
            else:
                resultado = t1 - t2

            # Atualiza o resultado na tela
            result_text.value = str(resultado)
            result_text.color = "green"  # CORRIGIDO: Usando string
            page.update()

        except Exception as erro:
            # Se der erro (ex: formato inválido), avisa o usuário
            result_text.value = "Erro: Use formato 00:00:00:00"
            result_text.color = "red"    # CORRIGIDO: Usando string
            page.update()

    # --- Elementos Visuais (Widgets) ---
    
    # Título
    header = ft.Text("Timecode Calc", size=30, weight=ft.FontWeight.BOLD)
    
    # Input: Frame Rate
    fps_dropdown = ft.Dropdown(
        label="Frame Rate",
        width=300,
        options=[
            ft.dropdown.Option("23.976"),
            ft.dropdown.Option("24"),
            ft.dropdown.Option("25"),
            ft.dropdown.Option("29.97"),
            ft.dropdown.Option("30"),
            ft.dropdown.Option("59.94"),
            ft.dropdown.Option("60"),
        ],
        value="24"
    )

    # Input: Timecode 1
    tc1_input = ft.TextField(label="Timecode A", hint_text="00:00:00:00", width=300, text_align=ft.TextAlign.CENTER)

    # Input: Operação
    operacao_dropdown = ft.Dropdown(
        label="Operação",
        width=300,
        options=[
            ft.dropdown.Option("Somar (+)"),
            ft.dropdown.Option("Subtrair (-)"),
        ],
        value="Somar (+)"
    )

    # Input: Timecode 2
    tc2_input = ft.TextField(label="Timecode B", hint_text="00:00:00:00", width=300, text_align=ft.TextAlign.CENTER)

    # Botão de Calcular
    calc_btn = ft.ElevatedButton(text="CALCULAR", on_click=calcular_click, width=300, height=50)

    # Área de Resultado
    result_label = ft.Text("Resultado:", size=15)
    result_text = ft.Text("00:00:00:00", size=40, weight=ft.FontWeight.BOLD)

    # --- Montagem da Tela ---
    container = ft.Container(
        content=ft.Column(
            [
                header,
                ft.Divider(),
                fps_dropdown,
                tc1_input,
                operacao_dropdown,
                tc2_input,
                ft.Divider(),
                calc_btn,
                ft.Divider(),
                result_label,
                result_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=30,
        bgcolor="surfaceVariant", # CORRIGIDO: Usando string
        border_radius=20,
    )

    page.add(container)

ft.app(target=main)