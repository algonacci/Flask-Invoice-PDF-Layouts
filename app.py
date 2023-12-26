import os
from flask import Flask, render_template, request, make_response
from flask_cors import CORS, cross_origin
import pdfkit
from firebase import db


app = Flask(__name__)
app.config['WKHTMLTOPDF_PATH'] = '/usr/bin/wkhtmltopdf'
CORS(app)


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def index():
    sales_ref = db.collection('sales')
    sales = sales_ref.stream()

    sales_list = []

    for sale in sales:
        item_data = sale.to_dict()
        item_data['id'] = sale.id
        sales_list.append(item_data)
    return render_template("index.html", sales=sales_list)


@app.route("/generate_invoice", methods=["POST"])
@cross_origin()
def generate_invoice():
    if request.method == "POST":
        data = request.get_json()

        # Retrieve sale data from your database (Firebase)
        # Replace this with your actual data retrieval logic from Firebase
        sale_data = {
            "id": data["no"],
            "created_date": data["tanggal"],
            "buyer": data["nama_pembeli"],
            "total_items": data["jumlah"],
            "total_price": data["total_harga"],
        }

        # Render the PDF content using Jinja2 template
        pdf_content = render_template("invoice_template.html", sale=sale_data)

        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None
        }
        pdf = pdfkit.from_string(pdf_content, False, options=options)

        # Send the PDF as a response
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=invoice.pdf"
        return response


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
