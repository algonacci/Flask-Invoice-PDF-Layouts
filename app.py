import os
from flask import Flask, render_template, request, make_response
from flask_cors import CORS
import pdfkit


app = Flask(__name__)
app.config['WKHTMLTOPDF_PATH'] = '/usr/bin/wkhtmltopdf'
CORS(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    else:
        return render_template("index.html")


@app.route("/generate_invoice", methods=["POST"])
def generate_invoice():
    if request.method == "POST":
        data = request.get_json()
        pdf_content = f"""
        <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <title>Invoice</title>
        </head>
        <body>
            <h1>Invoice</h1>
            <table border="1" class="table table-responsive">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Tanggal</th>
                        <th>Nama Barang</th>
                        <th>Jumlah</th>
                        <th>Total Harga</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{data['no']}</td>
                        <td>{data['tanggal']}</td>
                        <td>{data['nama_barang']}</td>
                        <td>{data['jumlah']}</td>
                        <td>{data['total_harga']}</td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
        """
        pdf = pdfkit.from_string(pdf_content, False)

        # Send the PDF as a response
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=invoice.pdf"
        return response


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
