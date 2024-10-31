import pdfkit
from jinja2 import Environment, FileSystemLoader


def generate_invoice_pdf(data, output_file="invoice.pdf"):

    path_to_wkhtmltopdf = r"utils\wkhtmltopdf\bin\wkhtmltopdf.exe"

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("utils/invoice_template.html")

    html_content = template.render(data)

    pdfkit.from_string(html_content, output_file, configuration=config)
