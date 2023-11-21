from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    have_lc = fields.Boolean(string=_('Have LC?'))
    letter_of_credit_id = fields.Many2one('letter.of.credit', string=_('LC'))
    lc_remaining_amount = fields.Float(compute='get_lc_remaining_amount', string=_('Remaining LC Amount'), store=True)


    @api.depends('letter_of_credit_id', 'letter_of_credit_id.remaining_amount')
    def get_lc_remaining_amount(self):
        for rec in self:
            rec.lc_remaining_amount = rec.letter_of_credit_id.remaining_amount or 0

    @api.onchange('partner_id')
    def on_change_partner_id(self):
        if self.letter_of_credit_id and self.letter_of_credit_id.partner_id != self.partner_id:
            self.letter_of_credit_id = False

    @api.onchange('have_lc')
    def onchange_have_lc(self):
        if not self.have_lc:
            self.letter_of_credit_id = False
        

    def check_is_equal_amount(self):
        return self.amount_untaxed == self.lc_remaining_amount
            

    def check_is_less_or_equal(self):
        return self.amount_untaxed <= self.lc_remaining_amount

    def action_confirm(self):
        if self.letter_of_credit_id:
            if not self.letter_of_credit_id.partial:
                if not self.check_is_equal_amount():
                    raise UserError(_('The amount for the sale order must be equal to %s%s'  %('{:,.2f}'.format(self.lc_remaining_amount), self.currency_id.symbol)))
            else:
                if not self.check_is_less_or_equal():
                    raise UserError(_('The amount of the sale order must be equal or less than %s%s' %('{:,.2f}'.format(self.lc_remaining_amount), self.currency_id.symbol)))
        
        res = super().action_confirm()

        self.picking_ids.update({'letter_of_credit_id': self.letter_of_credit_id.id})
        self._get_purchase_orders().update({'letter_of_credit_id': self.letter_of_credit_id.id})
        return res

    
    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped, final, date)
        moves.update({'letter_of_credit_id': self.letter_of_credit_id.id})
        return moves

    def get_partner_address_for_report(self):
        address = []
        street = self.partner_id.street
        street2 = self.partner_id.street2
        city = self.partner_id.city
        state = self.partner_id.state_id.name
        country = self.partner_id.country_id.name

        if street:
            address.append(street)
        if street2:
            address.append(street2)
        if city:
            address.append(city)
        if state:
            address.append(state)
        if country:
            address.append(country)
        
        return ", ".join(address)