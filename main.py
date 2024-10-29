import customtkinter as ctk
import product_management, product_table, Main_Window

windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.generateButton = ctk.CTkButton(
            self, text="Generate Quotation", command=self.generateButton
        )
        self.generateButton.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.manageProductButton = ctk.CTkButton(
            self, text="Manage Products", command=self.button2
        )
        self.manageProductButton.grid(row=1, column=0, padx=20, pady=(20, 0))

    def generateButton(self):
        self.master.createGenerateWindow()

    def button2(self):
        self.master.createManageProductWindow()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x600")
        self.title("Quotation Generator")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.mainWindow = ctk.CTkFrame(self, fg_color=["gray92", "gray14"])
        self.mainWindow.grid_columnconfigure(0, weight=1)
        self.mainWindow.grid_rowconfigure(0, weight=1)
        self.mainWindow.grid(row=0, column=1, sticky="nsew")
        self.createGenerateWindow()

    def createGenerateWindow(self):
        for widget in self.mainWindow.winfo_children():
            widget.destroy()
        self.main = Main_Window.QuotationWindow(self.mainWindow)
        self.main.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def createManageProductWindow(self):
        for widget in self.mainWindow.winfo_children():
            widget.destroy()
        self.main = product_management.ManageProductWindow(self.mainWindow)
        self.main.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)


app = App()
app.mainloop()
