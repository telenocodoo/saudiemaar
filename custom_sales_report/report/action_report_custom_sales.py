from odoo import api, fields, models


class ReportCustomSales(models.AbstractModel):
    _name = 'report.custom_sales_report.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Sales Report')

        bold = workbook.add_format({'bold': True})
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9EAD3',
            'border': 1
        })
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#B6D7A8',
            'border': 1
        })
        normal_format = workbook.add_format({'border': 1})

        # Set the width of the columns
        column_widths = [15, 10, 40, 20, 15, 20, 20, 15, 20]
        for col_num, width in enumerate(column_widths):
            sheet.set_column(col_num, col_num, width)

        # Report title (merge across columns)
        sheet.merge_range(0, 0, 0, len(column_widths)-1, "Sales Report", title_format)

        # Subtitle (date range)
        sheet.merge_range(1, 0, 1, len(column_widths)-1, 
            f"From {data['start_date']} To {data['end_date']}", bold)

        # Define the headers
        headers = [
            'DATE', 'Ref', 'Supplier', 'Customer', 'Salesman',
            'Qty / Ton', 'Customer invoice', 'Supplier bill', 'GROSS PROFIT'
        ]
        for col_num, header in enumerate(headers):
            sheet.write(3, col_num, header, header_format)
            
        # Fetch data
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', data['start_date']),
            ('date_order', '<=', data['end_date'])
        ])
        
        row = 4
        for order in sale_orders:
            total_qty = sum(line.product_uom_qty for line in order.order_line)
            purchase_order_ids = order._get_purchase_orders().filtered(lambda po: po.state in ['purchase', 'done'])
            customer_invoices = order.invoice_ids.filtered(lambda inv: inv.state == 'posted' and inv.move_type == 'out_invoice')
            total_customer_invoice = sum(inv.amount_total for inv in customer_invoices)
            
            for purchase_order in purchase_order_ids:
                supplier_name = purchase_order.partner_id.name or ''
                supplier_bills = purchase_order.mapped('invoice_ids').filtered(lambda inv: inv.state == 'posted' and inv.move_type == 'in_invoice')
                total_supplier_bill = sum(bill.amount_total for bill in supplier_bills)
                gross_profit = total_customer_invoice - total_supplier_bill
            
                sheet.write(row, 0, order.date_order.strftime('%Y-%m-%d'), normal_format)
                sheet.write(row, 1, order.name, normal_format)
                sheet.write(row, 2, supplier_name, normal_format)
                sheet.write(row, 3, order.partner_id.name, normal_format)
                sheet.write(row, 4, order.user_id.name, normal_format)
                sheet.write(row, 5, total_qty, normal_format)
                sheet.write(row, 6, total_customer_invoice, normal_format)
                sheet.write(row, 7, total_supplier_bill, normal_format)
                sheet.write(row, 8, gross_profit, normal_format)
                row += 1
