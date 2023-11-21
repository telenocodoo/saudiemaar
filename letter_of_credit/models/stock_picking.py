from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    letter_of_credit_id = fields.Many2one('letter.of.credit')

    def _create_backorder(self):
        backorders = super(StockPicking, self)._create_backorder()
        backorders.update({'letter_of_credit_id': self.letter_of_credit_id.id})
        return backorders