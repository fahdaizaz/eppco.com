from odoo import models, fields, exceptions, api, tools, _
class InheritedCompanyDetails(models.Model):
    _inherit = "res.company"

    company_name_arabic = fields.Char()
    company_address_arabic = fields.Char()
    company_address_arabic2 = fields.Char()
    company_details = fields.Html()
    fax=fields.Char()
    account_no = fields.Char(string='VAT NO')


class InheritedPartner(models.Model):
    _inherit = "res.partner"

    partner_name_arabic = fields.Char()
    partner_address_arabic = fields.Char()

class InheritedProduct(models.Model):
    _inherit = "product.template"

    product_name_arabic = fields.Char()