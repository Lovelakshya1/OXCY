import flet as ft

def main(page: ft.Page):
    page.title = "OXCY Safe Mode"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    
    # Simple UI to prove the app works
    text = ft.Text("OXCY IS ALIVE", size=30, color="green", weight="bold")
    sub = ft.Text("The UI core is working perfectly.", color="white")
    
    def test_click(e):
        text.value = "Button Works!"
        text.color = "yellow"
        page.update()

    btn = ft.ElevatedButton("Test Touch", on_click=test_click, bgcolor="blue", color="white")
    
    page.add(
        ft.Column(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=50),
                text,
                sub,
                ft.Divider(),
                btn
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

ft.app(target=main)
