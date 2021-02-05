from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PosReport(models.TransientModel):
    _name = 'pos.report'

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    all_customer = fields.Boolean()
    is_consolidation = fields.Boolean()
    is_customer = fields.Many2one('res.partner')
    service_type = fields.Many2one('product.category')



    def print_report(self):
        start_date = self.start_date
        end_date = self.end_date
        if  end_date < start_date:
            raise ValidationError(_('Date To %s  Greater than Date From %s')% (self.start_date,self.end_date))


        id=[]
        product_list=[]
        st=[]
        total_value=0.0
        tax_ratio_amount=0.0



        all_invoice = self.env['account.move'].search([('invoice_date', '>=',start_date), ('invoice_date', '<=',end_date),('state','=','posted')])
        is_invoice = self.env['account.move'].search([('invoice_date', '>=', start_date),('invoice_date', '<=', end_date),('invoice_date', '<=', end_date),('state','=','posted'),('partner_id','=',self.is_customer.id)])
        p_categ = self.env['product.product'].search([('categ_id', 'child_of', self.service_type.id)])

        if self.is_consolidation == False:

            if self.all_customer==True and all_invoice:
                print('case1')
                for rec in all_invoice:
                    id.append(rec.id)
                    for p in p_categ:
                        st.append(p.categ_id.id)
            elif self.is_customer and is_invoice:
                print(len(is_invoice))
                for rec in is_invoice:
                    id.append(rec.id)
                    for p in p_categ:
                        st.append(p.categ_id.id)
                    print('>>>>>>>>>>>>>',st)
                    for line in rec.invoice_line_ids:
                        print(line.product_id.name)
                        total_value = line.price_subtotal
                        print(';;;;;;;;', total_value)
                        if line.tax_ids:
                            tax_ratio = line.tax_ids[0].amount
                        tax_ratio_amount = tax_ratio * total_value / 100



            else:
                raise ValidationError(_("Records Can Not Found Between  %s  to  %s Dates") % (self.start_date, self.end_date))

            print('9999999999999',st)
            data = {
                'ids':self.ids,
                'model': self._name,
                'form': {
                    'date_from': self.start_date,
                    'date_to': self.end_date,
                    'product_data':id,
                    'serv':st,
                    't':tax_ratio_amount
                },
            }
            return self.env.ref('customer_invoice_report.action_report_daily_sales').report_action(self, data=data)
        else:
            if self.is_customer:
                customer_list = []
                discription = []
                flag=False
                invoice_number = ''
                partner_name_arabic=''
                partner_street=''
                invoice_date = ''
                vat_no = ''
                street = ''
                p=''
                tax_ratio = 0.0
                total_value = 0.0
                tax_ratio_amount=0.0
                i = 0.0
                j = 0.0
                for rec  in is_invoice:
                    p = ''.join(rec.partner_id.name)
                    partner_name_arabic = rec.partner_id.partner_name_arabic
                    partner_street = rec.partner_id.partner_address_arabic
                    vat_no = rec.partner_id.vat
                    street = rec.partner_id.street
                    amount_untaxed = rec.amount_untaxed,
                    i = ''.join(map(str, amount_untaxed))
                    j += float(i)
                    invoice_number = str(rec.partner_id.name[:3]) + '-' + str(rec.invoice_date) + ','
                    invoice_date = str(rec.invoice_date) + ','

                    p_categ = self.env['product.product'].search([('categ_id', 'child_of', self.service_type.id)])
                    for pp in p_categ:
                        st.append(pp.categ_id.id)

                    for line in rec.invoice_line_ids.filtered(lambda x: x.product_id.categ_id.id in st):
                        flag=True
                        print('>>>>>>>>>>>>>>>>>>',flag)
                        total_value += line.price_subtotal
                        print(';;;;;;;;',total_value)
                        if line.tax_ids:
                            tax_ratio = line.tax_ids[0].amount
                        tax_ratio_amount=tax_ratio * total_value / 100
                        vals = {
                            'disc': line.product_id.name,
                            'name2':line.product_id.product_name_arabic,
                            'due_date': rec.invoice_date_due,
                            'amount_sar': line.price_subtotal,

                        }
                        discription.append(vals)
                print(partner_name_arabic)
                vals = {

                    'partner_name': p,
                    'partner_name2': partner_name_arabic,
                    'partner_address2': partner_street,
                    'invoice_number': invoice_number,
                    'invoice_date': invoice_date,
                    'tax_no': vat_no,
                    'address': street,
                    'line_items': discription,
                    'amount_untax':total_value,
                    'tax_value': tax_ratio * total_value / 100,
                    'total_value': tax_ratio_amount+ total_value

                }
                customer_list.append(vals)
                print(customer_list)
                data = {
                    'ids': self.ids,
                    'model': self._name,
                    'form': {
                        'date_from': self.start_date,
                        'date_to': self.end_date,
                        'f':flag,
                        'product_data2':customer_list

                    },
                }
                return self.env.ref('customer_invoice_report.action_report_daily_sales2').report_action(self, data=data)


class test(models.AbstractModel):
    _name = 'report.customer_invoice_report.daily_sales_report_new'
    _description = "Emp logs Report"

    @api.model
    def _get_report_values(self,docids,data=None):
        date_f = data['form']['date_from']
        date_t = data['form']['date_to']
        tt = data['form']['t']
        s_type = data['form']['serv']
        product_data1 = data['form']['product_data']
        product_data1 = self.env['account.move'].browse(product_data1)


        return {
            'doc_ids':product_data1,
            'docs':product_data1,
            'doc_model':'account.move',
            'df': date_f,
            'dt': date_t,
            's':s_type,
            'tax_ratio':tt


        }



class test2(models.AbstractModel):
    _name = 'report.customer_invoice_report.daily_sales_report_new2'
    _description = "Emp logs Report"

    @api.model
    def _get_report_values(self,docids,data=None):
        date_f = data['form']['date_from']
        date_t = data['form']['date_to']
        ff = data['form']['f']
        product_data2 = data['form']['product_data2']

        return {
            'doc_ids':product_data2,
            'docs':product_data2,
            'doc_model':'account.move',
            'df': date_f,
            'dt': date_t,
            'flag':ff


        }










   






