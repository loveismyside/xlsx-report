# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _


class DailySaleXLSWizard(models.TransientModel):
    _name = 'dailysale.xls.wizard'

    date_end = fields.Date(string='End Date')
    date_start = fields.Date(string='Start Date')

    #@api.multi
    @api.model_cr
    def action_create_report(self):

        context = dict(self._context)
        if context is None:
            context = {}
        data = self.read()[0] or {}
        datas = {
            'ids': self._ids,
            'data': data,
            'model': 'dailysale.xls.wizard'
        }
        return self.env.ref(
            'dailysale_report_xls.dailysale_xls_report'
        ).report_action(self, data=datas)


        tools.drop_view_if_exists(self._cr, 'account_invoice_line_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW account_invoice_line_report AS (
            SELECT DISTINCT ON (l.id) l.id as id, 
            i.date as Invoice_Date, 
            concat(a.code,' ',a.name) as Account, 
            i.origin as SONumber,
            case when i.type = 'out_refund' then i.number 
                 when i.type = 'out_invoice' then i.reference 
            end as InvoiceNumber, 
            c.ref as CustomerID, c.display_name as CustomerName, 
            p.default_code as ProductID, p.name as ProductName, 
            case when i.type = 'out_refund' and i.type != 'in_invoice' then l.quantity * -1 
                 when i.type = 'out_invoice' and i.type != 'in_invoice' then l.quantity
            end as Quantity,
            case when i.type = 'out_refund' and i.type != 'in_invoice' then l.price_unit * -1
                 when i.type = 'out_invoice' and i.type != 'in_invoice' then l.price_unit 
            end as Price_unit, 
            case when i.type = 'out_refund' and i.type != 'in_invoice' then l.price_subtotal * -1
                 when i.type = 'out_invoice' and i.type != 'in_invoice' then l.price_subtotal
            end as Subtotal, 
            case when i.type = 'out_refund' and i.type != 'in_invoice' then i.amount_untaxed * -1 
                 when i.type = 'out_invoice' and i.type != 'in_invoice' then i.amount_untaxed 
            end as AmountWithoutTax, 
            case when i.type = 'out_invoice' then 'Customer Invoice'
                 when i.type = 'in_invoice' then 'Vendor Bill'
                 when i.type = 'out_refund' then 'Customer Credit Note'
                 when i.type = 'in_refund' then 'Vendor Credit Note' 
            end as InvoiceType,
            (l.quantity * l.price_unit) as Amountbeforediscount,
            pt.name as PaymentTerms, 
            uom.name as UOM, aj.name as Journal, i.state as State
            from account_invoice_line l 
            left join account_invoice i on l.invoice_id = i.id 
            left join account_account a on l.account_id = a.id 
            left join res_partner c on l.partner_id = c.id 
            left join product_product pp on pp.id = l.product_id
            left join product_template p on p.id = pp.product_tmpl_id
            left join account_payment_term pt on i.payment_term_id = pt.id
            left join uom_uom uom on uom.id = l.uom_id
            left join account_journal aj on aj.id = i.journal_id
            left join sale_order so on i.origin = so.name
            left join sale_order_line sol on so.id = sol.order_id and l.product_id = sol.product_id
            Left Join res_users u on i.user_id = u.id
            left join res_partner up on u.partner_id = up.id
            where i.state != 'Draft' and i.state != 'cancel'
            and aj.name != 'Vendor Bills'
            order by l.id, i.date
            )""")
