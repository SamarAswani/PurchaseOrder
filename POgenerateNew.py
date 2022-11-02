import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import numpy
from datetime import date
from datetime import timedelta
from datetime import datetime
import imgkit
import csv
import pdfkit
import sys
import requests
import json


rows = []
with open('DistributorData.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] != '' and row[1] != '':
            rows.append(row)

distributorDict = {}
for i in rows:
    distributorDict[i[1]] = i[2]



cred = credentials.Certificate("./ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

id="iNwhUT2rx9zBkZsO1u7b"
newcsv = []

doc = db.collection(u'MasterOrders').document(u'%s' % id).get().to_dict()

d1 = date.today().strftime("%d.%m.%Y")
d2= (date.today()+timedelta(days=7)).strftime("%d.%m.%Y")

mastercsv = [doc["communityCode"], doc["createdAt"], doc["address"], doc["name"], "Unpaid",[]]

for i in doc["productsList"]:

    jsonId = {"id": i["_id"]}
    response = requests.post("http://35.154.244.209:8000/product/productById", json=jsonId)
    response= response.json()
    ProductManufacturer = response[0]["manufacturer"]
    mastercsv[5].append({"name": i["name"], "id": i["_id"], "brand": i["brand"], "quantity": i["quantity"], "sp": i["sp"], "manufacturer": ProductManufacturer})
    inArray = False
    for j in newcsv:
        if j[0].strip().lower() == ProductManufacturer.strip().lower():
            # j[6].append({"name": i["name"], "quantity": i["quantity"], "unit_cost": i["sp"]})
            j[3].append({"name": i["name"], "quantity": i["quantity"], "weight": i["weight"], "mrp": i["mrp"]})
            inArray = True
            break
        else:
            continue
    if inArray == False:
            newcsv.append([ProductManufacturer,d1,d2,[{"name": i["name"], "quantity": str(i["quantity"]), "weight": i["weight"], "mrp": i["mrp"]}], doc["address"], distributorDict[ProductManufacturer.strip().lower()]])
        

masterorder = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">

    <style>
    .invoice-box {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
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

    .invoice-box table tr td:nth-child(6) {
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

    .invoice-box table tr.total td:nth-child(6) {
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
            width: 100 %;
            display: block;
            text-align: centre;
        }
    }

    /** RTL **/
    .rtl {
        direction: rtl;
        font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    }

    .rtl table {
        text-align: right;
    }

    .rtl table tr td:nth-child(6) {
        text-align: left;
    }
    </style>
</head>

<body>
    <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">

                    <table>
                        <tr>
                            <td class="title">
                                <img src="https://i.ibb.co/M8f0Z47/grocamie-Mark.jpg" style="width:70%; max-width:300px;">
                            </td>

                            <td>
                                <b>Master Order: </b>""" +id+ """<br><br>

                                <b>Created: </b>"""+ str(mastercsv[1])+ """<br>
                            </td>
                        </tr>
                    </table>


            <tr class="information">
                <td colspan="2">
                    <table>
                        <tr>
                            <td>
                                <b> Bill To: </b><br>
                                Grocamie<br>
                                Villa C55 <br>
                                Green Valley <br>
                                Faridabad <br>
                                Harayana 121004 <br>
                                GSTIN: 06AAICG6879N1ZQ
                                <br>
                                <br>
                                <b> Ship To: </b><br>
                                """+ mastercsv[2] +"""
                            </td>

                            <td>
                                <b> Payment Status: </b><br>
                                """+ mastercsv[4]+ """ <br>
                                <br>
                                <b> Community Code: </b><br>
                                """+ mastercsv[0]+ """ <br>
                                """+ mastercsv[3]+ """
                            </td>

                        </tr>
                    </td>
                </tr>
                    </table>

            <br>
            <br>

            <table cellpadding="0" cellspacing="0">




            <tr class="heading">
                <td>
                    Item
                </td>
                <td>
                    ID
                </td>
                <td>
                    Brand
                </td>
                <td>
                    Manufacturer
                </td>
                <td>
                    Quantity (Pcs)
                </td>
                <td>
                    Price (INR)
                </td>
            </tr>
        """
total = 0
for j in range(len(mastercsv[5])):
    if j == (len(mastercsv[5])-1):
        itemLast = """<tr class="item last">
            <td>
                """+ mastercsv[5][j]["name"]+"""
            </td>
            <td>
                """+ mastercsv[5][j]["id"]+"""
            </td>
            <td>
                """+ mastercsv[5][j]["brand"]+"""
            </td>
            <td>
                """+ mastercsv[5][j]["manufacturer"]+"""
            </td>
            <td>
                """+ str(mastercsv[5][j]["quantity"])+"""
            </td>

            <td>
                """+ str(mastercsv[5][j]["sp"])+"""
            </td>
        </tr>"""
        masterorder += itemLast
    else:
        item = """<tr class="item">
            <td>
                """+ mastercsv[5][j]["name"]+"""
            </td>
            <td>
                """+ mastercsv[5][j]["id"]+"""
            </td>
            <td>
                """+ mastercsv[5][j]["brand"]+"""
            </td>
            <td>
                """+ mastercsv[5][j]["manufacturer"]+"""
            </td>
            <td>
                """+ str(mastercsv[5][j]["quantity"])+"""
            </td>

            <td>
                """+ str(mastercsv[5][j]["sp"])+"""
            </td>
        </tr>"""
        masterorder += item
    total += (mastercsv[5][j]["sp"] * mastercsv[5][j]["quantity"])

end =  """
</table>
<br>
<b> Total: </b> """+str(total)+"""
</div>
</body>
</html>
"""

masterorder += end

pdfkit.from_string(masterorder, 'masterorder:'+id+'.pdf')




count=1
for i in newcsv:
    message = """
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">

        <style>
        .invoice-box {
            max-width: 800px;
            margin: auto;
            padding: 30px;
            border: 1px solid #eee;
            box-shadow: 0 0 10px rgba(0, 0, 0, .15);
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

        .invoice-box table tr td:nth-child(4) {
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

        .invoice-box table tr.total td:nth-child(4) {
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
                text-align: right;
            }
        }

        /** RTL **/
        .rtl {
            direction: rtl;
            font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        }

        .rtl table {
            text-align: right;
        }

        .rtl table tr td:nth-child(4) {
            text-align: left;
        }
        </style>
    </head>

    <body>
        <div class="invoice-box">
            <table cellpadding="0" cellspacing="0">
                        <table>
                            <tr>
                                <td class="title">
                                    <img src="https://i.ibb.co/M8f0Z47/grocamie-Mark.jpg" style="width:100%; max-width:300px;">
                                </td>

                                <td>
                                    Purchase Order: """ +str(count)+ """<br>
                                    Created: """+ i[1]+ """<br>
                                </td>
                            </tr>
                        </table>


                <tr class="information">
                    <td colspan="2">
                        <table>
                            <tr>
                                <td>
                                    <b> Bill To: </b><br>
                                    Grocamie<br>
                                    Villa C55 <br>
                                    Green Valley <br>
                                    Faridabad <br>
                                    Harayana 121004 <br>
                                    GSTIN: 06AAICG6879N1ZQ
                                    <br>
                                    <br>
                                    <b> Ship To: </b><br>
                                    """+ i[4] +"""
                                </td>

                                <td>
                                    """+ i[0]+ """ <br>
                                    """+ i[5]+ """
                                </td>
                            </tr>
                    </td>
                </tr>
                    </table>
                <br>
                <br>

                <table cellpadding="0" cellspacing="0">


                <tr class="heading">
                    <td>
                        Item
                    </td>

                    <td>
                        Weight
                    </td>

                    <td>
                        MRP
                    </td>

                    <td>
                        Quantity (Pcs)
                    </td>
                </tr>
            """

    for j in range(len(i[3])):
        if j == (len(i[3])-1):
            itemLast = """<tr class="item last">
                <td>
                    """+ i[3][j]["name"]+"""
                </td>
                <td>
                    """+ str(i[3][j]["weight"])+"""
                </td>
                <td>
                    """+ str(i[3][j]["mrp"])+"""
                </td>

                <td>
                    """+ str(i[3][j]["quantity"])+"""
                </td>
                </tr>"""
            message += itemLast
        else:
            item = """<tr class="item last">
                <td>
                    """+ i[3][j]["name"]+"""
                </td>
                <td>
                    """+ str(i[3][j]["weight"])+"""
                </td>
                <td>
                    """+ str(i[3][j]["mrp"])+"""
                </td>

                <td>
                    """+ str(i[3][j]["quantity"])+"""
                </td>
                </tr>"""
            message += item

    end =  """
    </table>
    </div>
    </body>
    </html>
    """

    message += end

    # f = open('invoice'+str(count)+'.html','w')
    # f.write(message)
    # f.close()
    pdfkit.from_string(message, 'PurchaseOrder'+i[0]+'.pdf')
    count+=1
