import customtkinter as ctk
import sqlite3
import windows.client_management as client_management
import utils.table_cells as table_cells

windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


class ClientTable(ctk.CTkFrame):
    def __init__(self, master, clientList):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.configure(fg_color=windowColor)
        self.clientList = clientList
        self.checkedList = []
        ctk.CTkLabel(self, text="Select Clients to Delete:", font=("roboto", 15)).grid(
            row=0, column=0, pady=(20, 0), sticky="w"
        )
        self.table()

        self.selectedLabelText = ctk.StringVar(
            value=f"Selected: {len(self.checkedList)}"
        )
        self.selectedLabel = ctk.CTkLabel(
            self, textvariable=self.selectedLabelText, font=("roboto", 15)
        )
        self.selectedLabel.grid(row=2, column=0, sticky="w")

    def table(self):
        self.data = client_management.initializeClientData()
        self.table = ctk.CTkScrollableFrame(self, fg_color=windowColor)
        self.table.grid(row=1, column=0, columnspan=2, sticky="news")
        self.table.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.selectHeader = table_cells.TableCells(self.table, text="Select")
        self.selectHeader.grid(row=0, column=0, sticky="news")
        self.clientIDHeader = table_cells.TableCells(self.table, text="Client ID")
        self.clientIDHeader.grid(row=0, column=1, sticky="news")
        self.clientNameHeader = table_cells.TableCells(self.table, text="Client Name")
        self.clientNameHeader.grid(row=0, column=2, sticky="news")
        self.clientAddressHeader = table_cells.TableCells(
            self.table, text="Client Address"
        )
        self.clientAddressHeader.grid(row=0, column=3, sticky="news")
        self.clientPhoneHeader = table_cells.TableCells(self.table, text="Client Phone")
        self.clientPhoneHeader.grid(row=0, column=4, sticky="news")
        self.clientEmailHeader = table_cells.TableCells(self.table, text="Client Email")
        self.clientEmailHeader.grid(row=0, column=5, sticky="news")

        for i, data in enumerate(self.clientList):
            var = ctk.IntVar(value=data[0])
            checkBoxCell = ctk.CTkCheckBox(
                self.table,
                text="",
                variable=var,
                onvalue=data[0],
                offvalue=data[0],
                command=lambda var=var: self.checked(var.get()),
            )
            checkBoxCell.deselect()
            checkBoxCell.grid(row=i + 1, column=0, padx=(80, 0))
            cell = table_cells.TableCells(self.table, text=data[0])
            cell.grid(row=i + 1, column=1, sticky="news")
            cell = table_cells.TableCells(self.table, text=data[1])
            cell.grid(row=i + 1, column=2, sticky="news")
            cell = table_cells.TableCells(self.table, text=data[2])
            cell.grid(row=i + 1, column=3, sticky="news")
            cell = table_cells.TableCells(self.table, text=data[3])
            cell.grid(row=i + 1, column=4, sticky="news")
            cell = table_cells.TableCells(self.table, text=data[4])
            cell.grid(row=i + 1, column=5, sticky="news")

    def checked(self, var):
        if var not in self.checkedList:
            self.checkedList.append(var)
        else:
            self.checkedList.remove(var)
        self.selectedLabelText.set(f"Selected: {len(self.checkedList)}")
        self.selectedLabel.update()
