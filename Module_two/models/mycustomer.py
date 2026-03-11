from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Mycustomer(models.Model):
    _name = 'mycustomer'

    name = fields.Char(required=1)
    date = fields.Datetime(required=True)
    phone = fields.Char(required=1)
    address = fields.Text()
    price = fields.Float()
    exact_price = fields.Float()
    phone_2 = fields.Char()
    diff = fields.Float(compute= '_compute_diff', store = 1)
    shipping_day = fields.Selection([('monday', 'Monday'),
                                     ('tuesday', 'Tuesday'),
                                     ('wednesday', 'Wednesday'),
                                     ('Thursday','Thursday')])

    _sql_constraints = [('unique_constraint', 'unique("name")', 'This name is exist')]

    @api.depends('price','exact_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.price - rec.exact_price

    @api.onchange('exact_price')
    def _onchange_exact_price(self):
        for rec in self:
            print(rec)
            print("inside onchange")
            return {
                'warning' : {'title' : 'warning', 'message' : '-ve value', 'type' : 'notification'}
            }

    def action_btn(self):
        for rec in self:
            print("here")
            rec.price = 1000


    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price == 0:
                raise ValidationError('please enter a price')