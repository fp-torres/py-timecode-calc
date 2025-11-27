import flet as ft
from timecode import Timecode

def main(page: ft.Page):
    # --- 1. Configuração da Janela (Estilo App Desktop) ---
    page.title = "TC Calc Station"
    page.window_width = 400
    page.window_height = 700
    page.bgcolor = "#121212"  # Fundo quase preto
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = False
    page.padding = 20

    # --- 2. Variáveis de Memória ---
    state = {
        "buffer": "",       # O que você digita (ex: "1023" -> 00:00:10:23)
        "stored_tc": None,  # O valor guardado na memória para somar
        "operation": None,  # "+" ou "-"
        "reset_screen": False # Flag para limpar a tela no próximo clique
    }

    # --- 3. Funções Lógicas ---
    
    def get_timecode_string(raw_nums):
        """Transforma '123' em '00:00:01:23'"""
        if not raw_nums: return "00:00:00:00"
        padded = raw_nums.zfill(8) # Garante 8 digitos
        return f"{padded[:2]}:{padded[2:4]}:{padded[4:6]}:{padded[6:]}"

    def update_display(valor=None, cor="#00FFFF"):
        """Atualiza o visor. Se valor=None, usa o buffer atual."""
        if valor:
            display_text.value = valor
        else:
            display_text.value = get_timecode_string(state["buffer"])
        
        display_text.color = cor
        page.update()

    def on_digit(e):
        # Se for evento de teclado, o dado vem diferente
        digit = e.control.data if hasattr(e, "control") else e
        
        # Se acabou de calcular, limpa o buffer para começar novo número
        if state["reset_screen"]:
            state["buffer"] = ""
            state["reset_screen"] = False
            display_text.color = "#00FFFF" # Volta para Ciano

        # Limite de 8 dígitos
        if len(state["buffer"]) < 8:
            state["buffer"] += digit
            update_display(cor="#00FFFF")

    def on_op(e):
        op = e.control.data if hasattr(e, "control") else e
        try:
            fps = fps_dropdown.value
            current_tc_str = get_timecode_string(state["buffer"])
            
            # Guarda o primeiro valor
            state["stored_tc"] = Timecode(fps, current_tc_str)
            state["operation"] = op
            
            # Prepara tela para o segundo número
            state["buffer"] = ""
            state["reset_screen"] = False
            
            # Feedback visual (pisca amarelo/laranja)
            display_text.color = "#FFC107" 
            page.update()
            
        except Exception as err:
            print(f"Erro Op: {err}")
            update_display("ERRO: FPS", "red")

    def on_equal(e):
        if state["stored_tc"] and state["operation"]:
            try:
                fps = fps_dropdown.value
                current_tc_str = get_timecode_string(state["buffer"])
                tc2 = Timecode(fps, current_tc_str)

                if state["operation"] == "+":
                    resultado = state["stored_tc"] + tc2
                elif state["operation"] == "-":
                    resultado = state["stored_tc"] - tc2

                # Mostra Resultado (Verde)
                update_display(str(resultado), "#66BB6A")
                
                # Prepara para continuar a conta a partir desse resultado
                state["buffer"] = str(resultado).replace(":", "")
                state["stored_tc"] = None
                state["operation"] = None
                state["reset_screen"] = True # Próximo digito limpa a tela

            except Exception as err:
                print(f"Erro Calc: {err}")
                update_display("ERRO CALC", "red")

    def on_clear(e):
        state["buffer"] = ""
        state["stored_tc"] = None
        state["operation"] = None
        state["reset_screen"] = False
        update_display(cor="#00FFFF")

    # --- 4. Interface Gráfica (Layout Industrial) ---

    # Visor
    display_text = ft.Text(
        value="00:00:00:00",
        size=45,
        font_family="Courier New", # Fonte Monospaced (Estilo Digital)
        weight=ft.FontWeight.BOLD,
        color="#00FFFF", # Ciano Neon
        text_align=ft.TextAlign.RIGHT
    )

    # Seletor de FPS (Integrado no Visor)
    fps_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("23.976"),
            ft.dropdown.Option("24"),
            ft.dropdown.Option("25"),
            ft.dropdown.Option("29.97"),
            ft.dropdown.Option("30"),
            ft.dropdown.Option("59.94"),
            ft.dropdown.Option("60"),
        ],
        value="29.97",
        width=100,
        text_size=12,
        border_color="transparent", # Sem borda pra parecer embutido
        bgcolor="transparent",
        color="grey"
    )

    # Container do Visor (A caixa preta com borda)
    visor_container = ft.Container(
        content=ft.Column([
            ft.Row([ft.Text("FPS:", color="grey", size=12), fps_dropdown], alignment=ft.MainAxisAlignment.END, spacing=0),
            display_text
        ], spacing=0),
        padding=ft.padding.only(left=20, right=20, top=5, bottom=15),
        bgcolor="#000000",
        border=ft.border.all(2, "#333333"),
        border_radius=5,
        margin=ft.margin.only(bottom=20)
    )

    # Botões
    def btn_style(text, func, color="#2D2D2D", txt_color="white", wide=False):
        return ft.Container(
            content=ft.Text(text, size=20, weight=ft.FontWeight.BOLD, color=txt_color),
            width=160 if wide else 75, # Se for largo ocupa 2 espaços
            height=65,
            bgcolor=color,
            border_radius=8,
            on_click=func,
            data=text,
            alignment=ft.alignment.center,
            ink=True,
            border=ft.border.all(1, "#3E3E3E") 
        )

    # Grid de Botões
    teclado = ft.Column([
        ft.Row([
            btn_style("CLEAR", on_clear, color="#B71C1C", wide=True), # Vermelho Escuro
            btn_style("-", on_op, color="#004D40", txt_color="#00FFFF"), # Verde Petroleo
            btn_style("+", on_op, color="#004D40", txt_color="#00FFFF"),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Row([
            btn_style("7", on_digit), btn_style("8", on_digit), btn_style("9", on_digit),
            btn_style("00", on_digit) 
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Row([
            btn_style("4", on_digit), btn_style("5", on_digit), btn_style("6", on_digit),
            btn_style("ENTER", on_equal, color="#1B5E20", txt_color="#69F0AE")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Row([
            btn_style("1", on_digit), btn_style("2", on_digit), btn_style("3", on_digit),
            btn_style("0", on_digit),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    ], spacing=10)

    # --- 5. Eventos de Teclado Físico ---
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key in ["0","1","2","3","4","5","6","7","8","9"]:
            # Simula envio direto do digito
            on_digit(e.key)
        elif e.key == "+":
            # Cria fake object para operador
            fake_e = type('',(object,),{"control": type('',(object,),{"data": "+"})()})()
            on_op(fake_e)
        elif e.key == "-":
            fake_e = type('',(object,),{"control": type('',(object,),{"data": "-"})()})()
            on_op(fake_e)
        elif e.key == "Enter" or e.key == "=":
            on_equal(None)
        elif e.key == "Backspace" or e.key == "Delete" or e.key == "Escape":
            on_clear(None)

    page.on_keyboard_event = on_keyboard

    # Montagem Final
    layout_principal = ft.Container(
        content=ft.Column([
            ft.Text("TIMECODE PRO", color="#444", weight=ft.FontWeight.BOLD, size=12),
            visor_container,
            teclado
        ]),
        padding=20,
        border_radius=15,
        bgcolor="#1E1E1E", # Corpo da calculadora
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(blur_radius=50, color="#000000")
    )

    page.add(layout_principal)

ft.app(target=main)