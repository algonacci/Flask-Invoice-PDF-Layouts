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
        pdf_content = """
                <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Invoice</title>
            <style>
                .invoice-box {
                    max-width: 800px;
                    margin: auto;
                    padding: 30px;
                    border: 1px solid #eee;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
                    font-size: 16px;
                    line-height: 24px;
                    font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
                    color: #555;
                }
                
                .invoice-box table {
                    width: 100%;
                    line-height: inherit;
                    text-align: left;
                }
                
                .invoice-box table td {
                    padding: 5px;
                    vertical-align: top;
                }
                
                .invoice-box table tr td:nth-child(2) {
                    text-align: right;
                }
                
                .invoice-box table tr.top table td {
                    padding-bottom: 20px;
                }
                
                .invoice-box table tr.top table td.title {
                    font-size: 45px;
                    line-height: 45px;
                    color: #333;
                }
                
                .invoice-box table tr.information table td {
                    padding-bottom: 40px;
                }
                
                .invoice-box table tr.heading td {
                    background: #eee;
                    border-bottom: 1px solid #ddd;
                    font-weight: bold;
                }
                
                .invoice-box table tr.details td {
                    padding-bottom: 20px;
                }
                
                .invoice-box table tr.item td{
                    border-bottom: 1px solid #eee;
                }
                
                .invoice-box table tr.item.last td {
                    border-bottom: none;
                }
                
                .invoice-box table tr.total td:nth-child(2) {
                    border-top: 2px solid #eee;
                    font-weight: bold;
                }
                
                @media only screen and (max-width: 600px) {
                    .invoice-box table tr.top table td {
                        width: 100%;
                        display: block;
                        text-align: center;
                    }
                    
                    .invoice-box table tr.information table td {
                        width: 100%;
                        display: block;
                        text-align: center;
                    }
                }
            </style>
        </head>
        <body>
            <div class="invoice-box">
                <table cellpadding="0" cellspacing="0">
                    <tr class="top">
                        <td colspan="4">
                            <table>
                                <tr>
                                    <td class="title">
                                        <img src="https://raw.githubusercontent.com/algonacci/Free-CDN/main/Denanti%20Textile%20(1).png" style="width:100%; max-height:150px;">
                                    </td>
                                    
                                    <td>
                                        Invoice #: 123<br>
                                        Created: January 1, 2023<br>
                                        Due: February 1, 2023
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr class="information">
                        <td colspan="4">
                            <table>
                                <tr>
                                    <td>
                                        PT. INDOCITRA SINAR CEMERLANG<br>
                                        Ronny Suhendra<br>
                                        Citaliktik RT. 04/02 Sukaregang<br>
                                        Cianjur, Jawa Barat
                                    </td>
                                    
                                    <td>
                                        Acme Corp.<br>
                                        John Doe<br>
                                        john@example.com
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr class="heading">
                        <td>
                            Payment Method
                        </td>
                        
                        <td>
                            Check #
                        </td>
                        
                        <td>
                            Invoice Total
                        </td>
                    </tr>
                    
                    <tr class="details">
                        <td>
                            Check
                        </td>
                        
                        <td>
                            1000
                        </td>
                        
                        <td>
                            $1,000.00
                        </td>
                    </tr>
                    
                    <tr class="heading">
                        <td>
                            Item
                        </td>
                        <td>
                            Quantity
                        </td>
                        <td>
                            Price
                        </td>
                    </tr>
                    
                    <tr class="item">
                        <td>
                            Website design
                        </td>
                        <td>
                            1
                        </td>
                        <td>
                            $300.00
                        </td>
                    </tr>
                    
                    <tr class="item">
                        <td>
                            Hosting (3 months)
                        </td>
                        <td>
                            1
                        </td>
                        <td>
                            $75.00
                        </td>
                    </tr>
                    
                    <tr class="item last">
                        <td>
                            Domain name (1 year)
                        </td>
                        <td>
                            1
                        </td>
                        <td>
                            $10.00
                        </td>
                    </tr>
                    
                    <tr class="total">
                        <td></td>
                        
                        <td>
                            Total: $385.00
                        </td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """
        options = {
            'page-size': 'A4',
            'orientation': 'Landscape',
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
