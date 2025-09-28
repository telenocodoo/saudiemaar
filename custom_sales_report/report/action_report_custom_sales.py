from odoo import api, fields, models


class ReportCustomSales(models.AbstractModel):
    _name = 'report.custom_sales_report.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Custom Sales Report')
        bold = workbook.add_format({'bold': True})
        
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', data['start_date']),
            ('date_order', '<=', data['end_date'])
        ])
        
        
        # Set the width of the columns
        column_widths = [15, 40, 40, 20, 15, 20, 20, 15]
        for col_num, width in enumerate(column_widths):
            sheet.set_column(col_num, col_num, width)

        # Define the headers
        headers = ['DATE', 'Ref', 'Supplier', 'Customer', 'Salesman', 'Qty / Ton', 'Customer invoice', 'Supllier bill', 'GROSS PROFIT']
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, bold)
            
        row = 1
        for order in sale_orders:
            total_qty = sum(line.product_uom_qty for line in order.order_line)
            purchase_order_ids = order._get_purchase_orders().filtered(lambda po: po.state in ['purchase', 'done'])
            supplier_bills = purchase_order_ids.mapped('invoice_ids').filtered(lambda inv: inv.state == 'posted' and inv.move_type == 'in_invoice')
            customer_invoices = order.invoice_ids.filtered(lambda inv: inv.state == 'posted' and inv.move_type == 'out_invoice')
            total_supplier_bill = sum(bill.amount_total for bill in supplier_bills)
            total_customer_invoice = sum(inv.amount_total for inv in customer_invoices)
            gross_profit = total_customer_invoice - total_supplier_bill
            
            sheet.write(row, 0, order.date_order.strftime('%Y-%m-%d'))
            sheet.write(row, 1, order.name)
            sheet.write(row, 2, purchase_order_ids.partner_id.name or '')
            sheet.write(row, 3, order.partner_id.name)
            sheet.write(row, 4, order.user_id.name)
            sheet.write(row, 5, total_qty)
            sheet.write(row, 6, total_customer_invoice)
            sheet.write(row, 7, total_supplier_bill)
            sheet.write(row, 8, gross_profit)
            row += 1
        