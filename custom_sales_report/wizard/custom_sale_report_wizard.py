from odoo import models, fields, api


class CustomSaleReportWizard(models.TransientModel):
    _name = 'custom.sale.report.wizard'
    _description = 'Custom Sale Report Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def generate_report(self):
        self.ensure_one()
        # domain = [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)]

        # sales_orders = self.env['sale.order'].search(domain)

        report_data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            # 'sales_orders': sales_orders,
        }

        return self.env.ref('custom_sales_report.action_report_custom_sales').report_action(self, data=report_data)