import customtkinter as ctk
import data.product as product
import sqlite3

conn = sqlite3.connect("data\main.db")
cursor = conn.cursor()
ProductList = []
windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


def initializeData():
    ProductList.clear()
    try:
        cursor.execute("SELECT * FROM products")
        for i in cursor.fetchall():
            ProductList.append(product.Product(i))
    except:
        cursor.execute(
            "CREATE TABLE products (SKU char(10) PRIMARY KEY,Product varchar(50), DefaultPrice INTEGER)"
        )
        conn.commit()
        cursor.execute("INSERT INTO products VALUES ('AB_1','Product 1', 100)")
        cursor.execute("INSERT INTO products VALUES ('AB_2','Product 2', 200)")
        cursor.execute("INSERT INTO products VALUES ('AB_3','Product 3', 300)")
        conn.commit()
        cursor.execute("SELECT * FROM products")
        for i in cursor.fetchall():
            ProductList.append(product.Product(i))


class ProductTable(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=windowColor)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.checked = []
        self.create_table()

    class TableCells(ctk.CTkButton):
        def __init__(self, master, text):
            super().__init__(
                master,
                text=text,
                font=("roboto", 15),
                hover=False,
                fg_color="transparent",
                border_width=2,
                corner_radius=0,
            )

    def create_table(self):
        initializeData()

        def tableHeaders(self):
            self.checkboxlabel = self.TableCells(self, text="Select")
            self.checkboxlabel.grid(row=0, column=0, sticky="news")
            self.quantityLabel = self.TableCells(self, text="SKU")
            self.quantityLabel.grid(row=0, column=1, sticky="news")
            self.productLabel = self.TableCells(self, text="Product")
            self.productLabel.grid(row=0, column=2, sticky="news")
            self.priceLabel = self.TableCells(self, text="Default Price")
            self.priceLabel.grid(row=0, column=3, sticky="news")

        def tableData(self):
            for i, product in enumerate(ProductList):
                var = ctk.StringVar(value=product.sku)
                checkBoxCell = ctk.CTkCheckBox(
                    self,
                    text="",
                    variable=var,
                    onvalue=product.sku,
                    command=lambda var=var: self.checked.append(var.get()),
                )
                checkBoxCell.deselect()
                checkBoxCell.grid(row=i + 1, column=0, padx=(80, 0))
                cell = self.TableCells(self, text=product.sku)
                cell.grid(row=i + 1, column=1, sticky="news")
                cell = self.TableCells(self, text=product.productName)
                cell.grid(row=i + 1, column=2, sticky="news")
                cell = self.TableCells(self, text=product.defaultPrice)
                cell.grid(row=i + 1, column=3, sticky="news")

        tableHeaders(self)
        tableData(self)
