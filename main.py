import customtkinter as ctk
import json
import windows.product_management as product_management
import windows.Main_Window as Main_Window
import windows.client_management as client_management
import windows.settings as settings

windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]

try:
    with open("data/settings.json", "r") as file:
        settingsFile = json.load(file)
        ctk.set_appearance_mode(settingsFile["theme"])
except FileNotFoundError:
    settingsString = {
        "supplierCompany": "",
        "supplierName": "",
        "supplierAddress": "",
        "supplierPhone": "",
        "supplierEmail": "",
        "theme": "Dark",
    }
    with open("data/settings.json", "w") as f:
        json.dump(settingsString, f)


class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.generateButton = ctk.CTkButton(
            self, text="Generate Quotation", command=self.generateButton
        )
        self.generateButton.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.manageProductButton = ctk.CTkButton(
            self, text="Manage Products", command=self.manageProductButtonClick
        )
        self.manageProductButton.grid(row=1, column=0, padx=20, pady=(20, 0))
        self.manageClientButton = ctk.CTkButton(
            self, text="Manage Clients", command=self.manageClientButtonClick
        )
        self.manageClientButton.grid(row=2, column=0, padx=20, pady=(20, 0))
        self.settingsButton = ctk.CTkButton(
            self, text="Settings", command=self.settingsButtonClick
        )
        self.settingsButton.grid(row=3, column=0, padx=20, pady=(20, 0))

    def generateButton(self):
        self.master.createGenerateWindow()

    def manageProductButtonClick(self):
        self.master.createManageProductWindow()

    def manageClientButtonClick(self):
        self.master.createManageClientWindow()

    def settingsButtonClick(self):
        self.master.createSettingsWindow()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x730")
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

    def createManageClientWindow(self):
        for widget in self.mainWindow.winfo_children():
            widget.destroy()
        self.main = client_management.ManageClientWindow(self.mainWindow)
        self.main.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def createSettingsWindow(self):
        for widget in self.mainWindow.winfo_children():
            widget.destroy()
        self.main = settings.SettingsWindow(self.mainWindow)
        self.main.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)


app = App()
app.mainloop()
