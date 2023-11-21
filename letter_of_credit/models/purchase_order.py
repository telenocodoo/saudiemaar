from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    letter_of_credit_id = fields.Many2one('letter.of.credit', string=_('LC'))

    def button_confirm(self):
        res = super().button_confirm()
        self.picking_ids.filtered(lambda p: p.is_dropship).update({'letter_of_credit_id': self.letter_of_credit_id.id})
        return res