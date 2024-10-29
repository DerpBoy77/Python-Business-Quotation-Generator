import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import sqlite3
import product_table
import data.product as products

conn = sqlite3.connect("data\main.db")
cursor = conn.cursor()
ProductList = product_table.ProductList
windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


class ManageProductWindow(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.configure(fg_color=windowColor)
        self.label = ctk.CTkLabel(
            self, text="Manage Products", font=("roboto bold", 25)
        )
        self.label.grid(row=0, column=0, columnspan=2, pady=20, sticky="news")

        self.addModifyGrid()

        self.selectLabel = ctk.CTkLabel(
            self.labelFrame, text="Select Products to delete:", font=("roboto", 15)
        )
        self.selectLabel.grid(row=5, column=0, sticky="w")
        self.productTable = product_table.ProductTable(self)
        self.productTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)
        self.deleteButton = ctk.CTkButton(self, text="Delete", command=self.delete)
        self.deleteButton.grid(row=7, column=0, padx=20, sticky="w")

    def addModifyGrid(self):
        self.labelFrame = ctk.CTkFrame(self, fg_color=windowColor)
        self.labelFrame.grid(row=1, column=0, sticky="w", padx=20)
        self.addModifyLabel = ctk.CTkLabel(
            self.labelFrame, text="Add/Modify Product:", font=("roboto", 15)
        )
        self.addModifyLabel.grid(row=0, column=0, sticky="w")
        self.skuLabel = ctk.CTkLabel(self.labelFrame, text="SKU:", font=("roboto", 15))
        self.skuLabel.grid(row=1, column=0, sticky="w")
        self.skuEntry = ctk.CTkEntry(self.labelFrame)
        self.skuEntry.grid(row=1, column=1, padx=10)
        self.fetchButton = ctk.CTkButton(
            self.labelFrame, text="Fetch", command=self.fetch
        )
        self.fetchButton.grid(row=1, column=2, padx=10)
        self.productLabel = ctk.CTkLabel(
            self.labelFrame, text="Product Name:", font=("roboto", 15)
        )
        self.productLabel.grid(row=2, column=0, sticky="w")
        self.productEntry = ctk.CTkEntry(self.labelFrame)
        self.productEntry.grid(row=2, column=1, padx=10, pady=10)
        self.defaultPriceLabel = ctk.CTkLabel(
            self.labelFrame, text="Default Price:", font=("roboto", 15)
        )
        self.defaultPriceLabel.grid(row=3, column=0, sticky="w")
        self.defaultPriceEntry = ctk.CTkEntry(self.labelFrame)
        self.defaultPriceEntry.grid(row=3, column=1, padx=10)

        self.addButton = ctk.CTkButton(self.labelFrame, text="Add", command=self.add)
        self.addButton.grid(row=4, column=0, pady=10)
        self.modifyButton = ctk.CTkButton(
            self.labelFrame, text="Modify", command=self.modify
        )
        self.modifyButton.grid(row=4, column=1, pady=10)

    def add(self):
        sku = self.skuEntry.get()
        product = self.productEntry.get()
        price = self.defaultPriceEntry.get()
        try:
            cursor.execute(
                f"INSERT INTO products VALUES ('{sku}','{product}',{(price)})"
            )
            conn.commit()
            ProductList.append(products.Product((sku, product, price)))
            self.productTable.destroy()
            self.productTable = product_table.ProductTable(self)
            self.productTable.grid(
                row=6, column=0, columnspan=2, sticky="news", padx=20
            )
        except:
            self.message = CTkMessagebox(
                self, title="Error", message="SKU already exists", icon="cancel"
            )

    def modify(self):
        sku = self.skuEntry.get()
        product = self.productEntry.get()
        price = self.defaultPriceEntry.get()
        cursor.execute(
            f"UPDATE products SET Product='{product}',DefaultPrice={price} WHERE SKU='{sku}'"
        )
        conn.commit()
        self.skuEntry.delete(0, ctk.END)
        self.productEntry.delete(0, ctk.END)
        self.defaultPriceEntry.delete(0, ctk.END)
        self.productTable.destroy()
        self.productTable = product_table.ProductTable(self)
        self.productTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)

    def fetch(self):
        sku = self.skuEntry.get()
        cursor.execute(f"SELECT * FROM products WHERE SKU='{sku}'")
        data = cursor.fetchone()
        self.productEntry.insert(0, data[1])
        self.defaultPriceEntry.insert(0, data[2])

    def delete(self):
        print(self.productTable.checked)
        for i in self.productTable.checked:
            if i:
                cursor.execute(f"DELETE FROM products WHERE SKU = '{i}'")
                conn.commit()
                product_table.initializeData()
        self.productTable.destroy()
        self.productTable = product_table.ProductTable(self)
        self.productTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)
