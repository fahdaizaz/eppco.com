
{
    "name": "Customer Invoice Report",
    "version": "13.0.0.0.1",
    "category": "Report",
    "author": "",
    "website": "",
    "license": "AGPL-3",
    "depends": [
        'base','account','product'
    ],
    "data": [
        "wizard/report_view.xml",
        "security/ir.model.access.csv",
        "report/customer_invoice_report.xml",
        "views/res_company.xml",
        "views/res_partner.xml"



    ],
    "installable": True,
}
