import customtkinter as ctk
import product_table

windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


class QuotationWindow(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.configure(fg_color=windowColor)
        self.label = ctk.CTkLabel(
            self, text="Create Quotation", font=("roboto bold", 25)
        )
        self.label.grid(row=0, column=0, columnspan=2, pady=20, sticky="news")

        self.labelFrame = ctk.CTkFrame(self, fg_color=windowColor)
        self.labelFrame.grid(row=1, column=0, sticky="w", padx=20)
        self.selectClientLabel = ctk.CTkLabel(
            self.labelFrame, text="Select Client:", font=("roboto", 15)
        )
        self.selectClientLabel.grid(row=0, column=0, sticky="w")
        self.clientMenu = ctk.CTkOptionMenu(
            self.labelFrame, values=["Client 1", "Client 2", "Client 3"]
        )
        self.clientMenu.grid(row=0, column=1, padx=10)

        self.selectProductLabel = ctk.CTkLabel(
            self.labelFrame, text="Select Products:", font=("roboto", 15)
        )
        self.selectProductLabel.grid(row=1, column=0, pady=(70, 0), sticky="w")

        self.productTable = product_table.ProductTable(self)
        self.productTable.grid(row=2, column=0, columnspan=2, sticky="news", padx=20)
