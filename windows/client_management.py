import customtkinter as ctk
from tables import client_table
import sqlite3

connection = sqlite3.connect("data/main.db")
cursor = connection.cursor()
windowColor = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]


class ManageClientWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text="Manage Clients", font=("roboto bold", 25)).grid(
            row=0, column=0, columnspan=2, pady=20, sticky="news"
        )
        self.addClientsGrid()

        self.clientTable = client_table.ClientTable(self, initializeClientData())
        self.clientTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)
        self.deleteButton = ctk.CTkButton(self, text="Delete", command=self.delete)
        self.deleteButton.grid(row=7, column=0, padx=10, pady=10, sticky="w")

    def addClientsGrid(self):
        self.formFrame = ctk.CTkFrame(self, fg_color=windowColor)
        self.formFrame.grid(row=1, column=0, sticky="w", padx=20)
        ctk.CTkLabel(
            self.formFrame, text="Add/Modify Clients:", font=("roboto", 15)
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self.formFrame, text="Client ID:", font=("roboto", 15)).grid(
            row=1, column=0, sticky="w"
        )
        self.clientIDEntry = ctk.CTkEntry(self.formFrame)
        self.clientIDEntry.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.formFrame, text="Client Name:", font=("roboto", 15)).grid(
            row=2, column=0, sticky="w"
        )
        self.fetchButton = ctk.CTkButton(
            self.formFrame, text="Fetch", command=self.fetch
        )
        self.fetchButton.grid(row=1, column=2, padx=10)
        self.clientNameEntry = ctk.CTkEntry(self.formFrame)
        self.clientNameEntry.grid(row=2, column=1, padx=10)
        ctk.CTkLabel(self.formFrame, text="Client Address:", font=("roboto", 15)).grid(
            row=3, column=0, sticky="w"
        )
        self.clientAddressEntry = ctk.CTkEntry(self.formFrame)
        self.clientAddressEntry.grid(row=3, column=1, padx=10, pady=10)
        self.clientPhoneLabel = ctk.CTkLabel(
            self.formFrame, text="Client Phone:", font=("roboto", 15)
        )
        self.clientPhoneLabel.grid(row=4, column=0, sticky="w")
        self.clientPhoneEntry = ctk.CTkEntry(self.formFrame)
        self.clientPhoneEntry.grid(row=4, column=1, padx=10)
        self.clientEmailLabel = ctk.CTkLabel(
            self.formFrame, text="Client Email:", font=("roboto", 15)
        )
        self.clientEmailLabel.grid(row=5, column=0, sticky="w")
        self.clientEmailEntry = ctk.CTkEntry(self.formFrame)
        self.clientEmailEntry.grid(row=5, column=1, padx=10, pady=10)
        self.addButton = ctk.CTkButton(self.formFrame, text="Add", command=self.add)
        self.addButton.grid(row=6, column=0, pady=10)
        self.modifyButton = ctk.CTkButton(
            self.formFrame, text="Modify", command=self.modify
        )
        self.modifyButton.grid(row=6, column=1, pady=10)

    def add(self):
        self.clientID = self.clientIDEntry.get()
        self.clientName = self.clientNameEntry.get()
        self.clientAddress = self.clientAddressEntry.get()
        self.clientPhone = self.clientPhoneEntry.get()
        self.clientEmail = self.clientEmailEntry.get()
        cursor.execute(
            f"INSERT INTO clients VALUES ('{self.clientID}','{self.clientName}','{self.clientAddress}',{self.clientPhone},'{self.clientEmail}')"
        )
        connection.commit()
        self.clientIDEntry.delete(0, ctk.END)
        self.clearEntry()
        self.clientTable.destroy()
        self.clientTable = client_table.ClientTable(self, initializeClientData())
        self.clientTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)

    def fetch(self):
        self.clientID = self.clientIDEntry.get()
        cursor.execute(f"SELECT * FROM clients WHERE ClientID='{self.clientID}'")
        data = cursor.fetchone()
        self.clearEntry()
        self.clientNameEntry.insert(0, data[1])
        self.clientAddressEntry.insert(0, data[2])
        self.clientPhoneEntry.insert(0, data[3])
        self.clientEmailEntry.insert(0, data[4])

    def delete(self):
        for i in self.clientTable.checkedList:
            cursor.execute(f"DELETE FROM clients WHERE ClientID = '{i}'")
            connection.commit()
        self.clientTable.destroy()
        self.clientTable = client_table.ClientTable(self, initializeClientData())
        self.clientTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)

    def modify(self):
        self.clientID = self.clientIDEntry.get()
        self.clientName = self.clientNameEntry.get()
        self.clientAddress = self.clientAddressEntry.get()
        self.clientPhone = self.clientPhoneEntry.get()
        self.clientEmail = self.clientEmailEntry.get()
        cursor.execute(
            f"UPDATE clients SET ClientName='{self.clientName}',Address='{self.clientAddress}',Phone={self.clientPhone},Email='{self.clientEmail}' WHERE ClientID='{self.clientID}'"
        )
        connection.commit()
        self.clientIDEntry.delete(0, ctk.END)
        self.clearEntry()
        self.clientTable.destroy()
        self.clientTable = client_table.ClientTable(self, initializeClientData())
        self.clientTable.grid(row=6, column=0, columnspan=2, sticky="news", padx=20)

    def clearEntry(self):
        self.clientNameEntry.delete(0, ctk.END)
        self.clientAddressEntry.delete(0, ctk.END)
        self.clientPhoneEntry.delete(0, ctk.END)
        self.clientEmailEntry.delete(0, ctk.END)


def initializeClientData():
    try:
        cursor.execute("SELECT * FROM clients")
        clientList = []
        for i in cursor.fetchall():
            clientList.append(i)
        return clientList
    except:
        cursor.execute(
            "CREATE TABLE clients (ClientID Integer PRIMARY KEY,ClientName varchar(50), Address varchar(50), Phone INTEGER, Email varchar(50))"
        )
        clientList = []
        return clientList
