import logging
import flet as ft
from distutils.spawn import find_executable

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("flet_core").setLevel(logging.INFO)

LOE_FILENAME = ""
BROWSER = ""

def is_app(name):
    """Check whether `name` is on PATH."""

    return find_executable(name) is not None

class ChooseFile(ft.UserControl):
    def build(self):
        self.pick_file_dialog=ft.FilePicker(on_result=self.select_clicked)
        self.page.overlay.append(self.pick_file_dialog)

        self.selected_file = ft.Container(
            content=ft.Text("Click on 'Choose file...' button to select LoE Builder file"),
            border=ft.border.all(1, ft.colors.RED),
            padding=ft.padding.only(10, 5, 10, 5),
            expand=True,
            border_radius=5,
        )
        # Return a row with the TextField and the Select button
        return ft.Row(
            controls=[
                self.selected_file,
                ft.OutlinedButton(
                    "Choose file...",
                    on_click=lambda _: self.pick_file_dialog.pick_files(
                        allow_multiple=False
                    )
                )
            ]
        )

    # Callback for file selection
    def select_clicked(self, e):
        global LOE_FILENAME
        LOE_FILENAME = e.files[-1].name if e.files else ""
        self.selected_file.content.value=LOE_FILENAME if LOE_FILENAME else "Click on 'Choose file...' button to select LoE Builder file"
        self.selected_file.border = ft.border.all(1, ft.colors.GREY_600 if LOE_FILENAME else ft.colors.RED)
        self.update()

class BrowserSelection(ft.UserControl):
    def build(self):
        self.browser_list = ft.Container(
            border=ft.border.all(1, ft.colors.RED),
            border_radius=5,
            expand=True,
            content=ft.RadioGroup(content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(value="Google Chrome", label="Google Chrome", disabled=not(is_app("Google Chrome"))),
                    ft.Radio(value="Firefox", label="Firefox", disabled=not(is_app("Firefox")))
                    ]),
                on_change=self.browser_change
            )
        )
        # Return a row with the Text and the RadioGroup
        return ft.Row([
            ft.Text("Select the browser: "),
            self.browser_list
            ])

    def browser_change(self, e):
        global BROWSER
        BROWSER = e.control.value
        self.browser_list.border = ft.border.all(1, ft.colors.GREY_600)
        self.update()

    
def main(page: ft.Page):
    page.title="LoE File Picker"
    page.theme_mode="LIGHT"

    def window_event(e):
        if e.data == "close":
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()
    
    def close_app(e):
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    def yes_click(e):
        page.window_destroy()

    def no_click(e):
        confirm_dialog.open = False
        page.update()
    
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("LoE File Picker"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.OutlinedButton("Yes", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.window_prevent_close = True
    page.on_window_event = window_event

    page.add(ChooseFile())
    page.add(BrowserSelection())
    page.add(ft.Row(
        expand=True,
        controls=[
            ft.OutlinedButton("Run"),
            ft.OutlinedButton("Close", on_click=close_app)
        ]
    ))

ft.app(target=main)