import customtkinter as ctk


class TableCells(ctk.CTkButton):
    def __init__(self, master, text):
        super().__init__(
            master,
            text=text,
            font=("roboto", 15),
            hover=False,
            fg_color="transparent",
            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"],
            border_width=2,
            corner_radius=0,
        )
