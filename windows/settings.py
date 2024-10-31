import customtkinter as ctk
import json

windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


class SettingsWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.settings = {}

        ctk.CTkLabel(self, text="Settings", font=("roboto bold", 25)).grid(
            row=0, column=0, columnspan=2, pady=20, sticky="news"
        )
        self.supplierInformationGrid()
        self.settingsGUI()
        self.getSettings()

    def supplierInformationGrid(self):
        self.formFrame = ctk.CTkFrame(self, fg_color=windowColor)
        self.formFrame.grid(row=1, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            self.formFrame, text="Supplier Information:", font=("roboto", 15)
        ).grid(row=0, column=0, sticky="w")

        self.supplierCompanyLabel = ctk.CTkLabel(
            self.formFrame, text="Company Name:", font=("roboto", 15)
        )
        self.supplierCompanyLabel.grid(row=1, column=0, sticky="w")
        self.supplierCompanyEntry = ctk.CTkEntry(self.formFrame)
        self.supplierCompanyEntry.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.formFrame, text="Name:", font=("roboto", 15)).grid(
            row=2, column=0, sticky="w"
        )
        self.supplierNameEntry = ctk.CTkEntry(self.formFrame)
        self.supplierNameEntry.grid(row=2, column=1, padx=10)
        ctk.CTkLabel(self.formFrame, text="Address:", font=("roboto", 15)).grid(
            row=3, column=0, sticky="w"
        )
        self.supplierAddressEntry = ctk.CTkEntry(self.formFrame)
        self.supplierAddressEntry.grid(row=3, column=1, padx=10, pady=10)
        self.supplierPhoneLabel = ctk.CTkLabel(
            self.formFrame, text="Phone:", font=("roboto", 15)
        )
        self.supplierPhoneLabel.grid(row=4, column=0, sticky="w")
        self.supplierPhoneEntry = ctk.CTkEntry(self.formFrame)
        self.supplierPhoneEntry.grid(row=4, column=1, padx=10)
        self.supplierEmailLabel = ctk.CTkLabel(
            self.formFrame, text="Email:", font=("roboto", 15)
        )
        self.supplierEmailLabel.grid(row=5, column=0, sticky="w")
        self.supplierEmailEntry = ctk.CTkEntry(self.formFrame)
        self.supplierEmailEntry.grid(row=5, column=1, padx=10, pady=10)
        self.saveButton = ctk.CTkButton(self.formFrame, text="Save", command=self.save)
        self.saveButton.grid(row=6, column=0, pady=10)

    def settingsGUI(self):
        self.settingsFrame = ctk.CTkFrame(self, fg_color=windowColor)
        self.settingsFrame.grid(row=1, column=1, sticky="nw", padx=20)
        ctk.CTkLabel(self.settingsFrame, text="Settings:", font=("roboto", 15)).grid(
            row=0, column=0, sticky="w"
        )
        self.settingsFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.chooseThemeLabel = ctk.CTkLabel(
            self.settingsFrame, text="Choose Theme:", font=("roboto", 15)
        )
        self.chooseThemeLabel.grid(row=1, column=0, sticky="w")
        self.themeMenu = ctk.CTkOptionMenu(
            self.settingsFrame, values=["Dark", "Light"], font=("roboto", 15)
        )
        self.themeMenu.grid(row=1, column=1, padx=10)

    def getSettings(self):
        with open("data/settings.json", "r") as f:
            settings = json.load(f)
        self.settings = settings
        self.supplierCompanyEntry.insert(0, settings["supplierCompany"])
        self.supplierNameEntry.insert(0, settings["supplierName"])
        self.supplierAddressEntry.insert(0, settings["supplierAddress"])
        self.supplierPhoneEntry.insert(0, settings["supplierPhone"])
        self.supplierEmailEntry.insert(0, settings["supplierEmail"])
        self.themeMenu.set(settings["theme"])

    def save(self):
        with open("data/settings.json", "w") as f:
            self.settings = {
                "supplierCompany": self.supplierCompanyEntry.get(),
                "supplierName": self.supplierNameEntry.get(),
                "supplierAddress": self.supplierAddressEntry.get(),
                "supplierPhone": self.supplierPhoneEntry.get(),
                "supplierEmail": self.supplierEmailEntry.get(),
                "theme": self.themeMenu.get(),
            }
            json.dump(self.settings, f)
        self.supplierCompanyEntry.delete(0, ctk.END)
        self.supplierNameEntry.delete(0, ctk.END)
        self.supplierAddressEntry.delete(0, ctk.END)
        self.supplierPhoneEntry.delete(0, ctk.END)
        self.supplierEmailEntry.delete(0, ctk.END)

        self.getSettings()
