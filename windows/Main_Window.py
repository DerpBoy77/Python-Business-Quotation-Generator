import customtkinter as ctk
import sqlite3
from CTkMessagebox import CTkMessagebox
from tables import product_table
import utils.table_cells as table_cells
import data.quotation_data as quotation_data
import utils.generate_pdf as generate_pdf

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
            self.labelFrame, text="Select Client by ID:", font=("roboto", 15)
        )
        self.selectClientLabel.grid(row=0, column=0, sticky="w")
        self.clientMenu = ctk.CTkOptionMenu(
            self.labelFrame, values=self.getClients(), font=("roboto", 15)
        )
        self.clientMenu.grid(row=0, column=1, padx=10)

        self.selectProductLabel = ctk.CTkLabel(
            self.labelFrame, text="Select Products:", font=("roboto", 15)
        )
        self.selectProductLabel.grid(row=1, column=0, pady=(70, 0), sticky="w")

        self.productTable = product_table.ProductTable(
            self, product_table.initializeData()
        )
        self.productTable.grid(row=2, column=0, columnspan=2, sticky="news", padx=20)

        self.generateButton = ctk.CTkButton(
            self, text="Generate Quotation", command=self.generate
        )
        self.generateButton.grid(row=3, column=0, sticky="w", padx=20, pady=20)

    def getClients(self):
        self.connection = sqlite3.connect("data/main.db")
        self.cursor = self.connection.cursor()
        self.clientList = []
        try:
            self.cursor.execute("SELECT ClientID FROM clients")
            self.clients = self.cursor.fetchall()
            for client in self.clients:
                self.clientList.append(str(client[0]))
            return self.clientList
        except:
            return ["No Clients Found"]

    def generate(self):
        if not self.productTable.checkedList:
            self.message = CTkMessagebox(
                self, title="Error", message="No Products Selected", icon="cancel"
            )
        else:
            self.cursor.execute(
                f"SELECT * FROM clients WHERE ClientID={self.clientMenu.get()}"
            )
            self.window = GenerateWindow(self, self.cursor.fetchone())


class EntryCells(ctk.CTkEntry):
    def __init__(self, master, data):
        self.var = ctk.StringVar(value=data)
        super().__init__(
            master,
            font=("roboto", 15),
            textvariable=self.var,
            fg_color="transparent",
            border_color=ctk.ThemeManager.theme["CTkButton"]["border_color"],
            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"],
            border_width=2,
            corner_radius=0,
        )


class GenerateWindow(ctk.CTkToplevel):
    def __init__(self, master, clientDetails):
        super().__init__(master)
        self.geometry("800x400")
        self.focus_set()
        self.grab_set()
        self.configure(fg_color=windowColor)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2), weight=1)
        self.resizable(False, False)
        self.checkedList = tuple(self.master.productTable.checkedList)
        self.clientDetails = clientDetails

        ctk.CTkLabel(
            self, text="Insert Price and Quantity", font=("roboto bold", 20)
        ).grid(row=0, column=0, sticky="news", pady=20)
        self.tableFrame = ctk.CTkScrollableFrame(
            self,
            fg_color=windowColor,
            border_color=ctk.ThemeManager.theme["CTkButton"]["border_color"],
            border_width=2,
        )
        self.tableFrame.grid(row=1, column=0, sticky="news", padx=20, pady=20)
        self.tableFrame.columnconfigure((0, 1, 2, 3), weight=1)
        self.getDataButton = ctk.CTkButton(
            self, text="Get Data", command=self.getDataEvent
        )
        self.getDataButton.grid(row=2, column=0, sticky="nw", padx=20)
        self.generateQuotationButton = ctk.CTkButton(
            self, text="Generate Quotation", command=self.generateQuotation
        )
        self.generateQuotationButton.grid(row=2, column=1, padx=20)
        self.table()

    def getDataEvent(self):
        self.data = self.getData()
        self.finalData = []
        for i, j in enumerate(self.data):
            self.finalData.append(
                (
                    j[0],
                    j[1],
                    self.priceEntries[i].var.get(),
                    self.quantityEntries[i].var.get(),
                )
            )
        print(self.finalData)
        return self.finalData

    def generateQuotation(self):
        self.quotationData = quotation_data.QuotationData(
            ["KAVI", "Arnav", "Pune", "arnav@gmail.com", "1234567890"],
            self.clientDetails,
            self.getDataEvent(),
        )
        print(self.quotationData.data())
        generate_pdf.generate_invoice_pdf(self.quotationData.data())

    def getData(self):
        self.connection = sqlite3.connect("data/main.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT * FROM products WHERE SKU IN {self.checkedList}")
        self.data = self.cursor.fetchall()
        return self.data

    def table(self):
        self.priceEntries = []
        self.quantityEntries = []
        self.skuHeader = table_cells.TableCells(self.tableFrame, text="SKU")
        self.skuHeader.grid(row=0, column=0, sticky="news")
        self.productHeader = table_cells.TableCells(
            self.tableFrame, text="Product Name"
        )
        self.productHeader.grid(row=0, column=1, sticky="news")
        self.priceHeader = table_cells.TableCells(self.tableFrame, text="Price")
        self.priceHeader.grid(row=0, column=2, sticky="news")
        self.quantityHeader = table_cells.TableCells(self.tableFrame, text="Quantity")
        self.quantityHeader.grid(row=0, column=3, sticky="news")

        for i, product in enumerate(self.data):
            self.sku = table_cells.TableCells(self.tableFrame, text=product[0])
            self.sku.grid(row=i + 1, column=0, sticky="news")
            self.product = table_cells.TableCells(self.tableFrame, text=product[1])
            self.product.grid(row=i + 1, column=1, sticky="news")
            self.price = EntryCells(self.tableFrame, product[2])
            self.price.grid(row=i + 1, column=2, sticky="news")
            self.priceEntries.append(self.price)
            self.quantity = EntryCells(self.tableFrame, 0)
            self.quantity.grid(row=i + 1, column=3, sticky="news")
            self.quantityEntries.append(self.quantity)
