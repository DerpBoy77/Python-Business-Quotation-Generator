class QuotationData:
    def __init__(self, supplierDetails, ClientDetails, ProductDetails):
        self.supplierCompany = supplierDetails[0]
        self.supplerName = supplierDetails[1]
        self.supplierAddress = supplierDetails[2]
        self.supplierEmail = supplierDetails[3]
        self.supplierPhone = supplierDetails[4]
        self.clientName = ClientDetails[0]
        self.clientEmail = ClientDetails[1]
        self.clientPhone = ClientDetails[2]
        self.clientAddress = ClientDetails[3]
        self.items, self.subtotal, self.gst_total, self.net_total = self.configureItems(
            ProductDetails
        )

    def configureItems(self, ProductDetails):
        items = []
        subtotal = 0
        for i in ProductDetails:
            quantity = int(i[2])
            unit_price = int(i[3])
            total = quantity * unit_price
            items.append(
                {
                    "sku": i[0],
                    "name": i[1],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total": total,
                }
            )
            subtotal += total
        return items, subtotal, subtotal * 0.18, subtotal * 1.18

    def data(self):
        dataDict = {
            "supplier_name": self.supplerName,
            "supplier_address": self.supplierAddress,
            "supplier_email": self.supplierEmail,
            "supplier_phone": self.supplierPhone,
            "client_name": self.clientName,
            "client_email": self.clientEmail,
            "client_phone": self.clientPhone,
            "client_address": self.clientAddress,
            "items": self.items,
            "subtotal": self.subtotal,
            "gst_total": self.gst_total,
            "net_total": self.net_total,
        }
        return dataDict
