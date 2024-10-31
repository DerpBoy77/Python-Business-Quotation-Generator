import customtkinter as ctk
import sqlite3
import data.product as product
import utils.table_cells as table_cells

conn = sqlite3.connect("data\main.db")
cursor = conn.cursor()
windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


def initializeData():
    ProductList = []
    try:
        cursor.execute("SELECT * FROM products")
        for i in cursor.fetchall():
            ProductList.append(product.Product(i))
        return ProductList
    except:
        cursor.execute(
            "CREATE TABLE products (SKU char(10) PRIMARY KEY,Product varchar(50), DefaultPrice INTEGER)"
        )
        conn.commit()
        cursor.execute("SELECT * FROM products")
        for i in cursor.fetchall():
            ProductList.append(product.Product(i))
        return ProductList


class ProductTable(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.checkedList = []
        self.configure(fg_color=windowColor)
        self.columnconfigure((0, 1), weight=1)
        self.productTable = self.ProductTableChild(self, data)
        self.productTable.grid(row=0, column=0, columnspan=2, sticky="news")
        self.selectedLabelText = ctk.StringVar(
            value=f"Selected: {len(self.checkedList)}"
        )
        self.selectedLabel = ctk.CTkLabel(
            self, textvariable=self.selectedLabelText, font=("roboto", 15)
        )
        self.selectedLabel.grid(row=1, column=0, sticky="w")

    class ProductTableChild(ctk.CTkScrollableFrame):

        def __init__(self, master, data):
            super().__init__(master)
            self.master = master
            self.configure(fg_color=windowColor)
            self.grid_columnconfigure((0, 1, 2, 3), weight=1)
            self.ProductList = data
            self.create_table()

        def create_table(self):
            initializeData()

            def tableHeaders(self):
                self.checkboxlabel = table_cells.TableCells(self, text="Select")
                self.checkboxlabel.grid(row=0, column=0, sticky="news")
                self.quantityLabel = table_cells.TableCells(self, text="SKU")
                self.quantityLabel.grid(row=0, column=1, sticky="news")
                self.productLabel = table_cells.TableCells(self, text="Product")
                self.productLabel.grid(row=0, column=2, sticky="news")
                self.priceLabel = table_cells.TableCells(self, text="Default Price")
                self.priceLabel.grid(row=0, column=3, sticky="news")

            def tableData(self):
                for i, product in enumerate(self.ProductList):
                    var = ctk.StringVar(value=product.sku)
                    checkBoxCell = ctk.CTkCheckBox(
                        self,
                        text="",
                        variable=var,
                        onvalue=product.sku,
                        offvalue=product.sku,
                        command=lambda var=var: self.master.checked(var.get()),
                    )
                    checkBoxCell.deselect()
                    checkBoxCell.grid(row=i + 1, column=0, padx=(80, 0))
                    cell = table_cells.TableCells(self, text=product.sku)
                    cell.grid(row=i + 1, column=1, sticky="news")
                    cell = table_cells.TableCells(self, text=product.productName)
                    cell.grid(row=i + 1, column=2, sticky="news")
                    cell = table_cells.TableCells(self, text=product.defaultPrice)
                    cell.grid(row=i + 1, column=3, sticky="news")

            tableHeaders(self)
            tableData(self)

    def checked(self, var):
        if var not in self.checkedList:
            self.checkedList.append(var)
        else:
            self.checkedList.remove(var)
        self.selectedLabelText.set(f"Selected: {len(self.checkedList)}")
        self.selectedLabel.update()
