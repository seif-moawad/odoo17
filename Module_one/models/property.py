from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=1, default='well smith')
    description = fields.Text()
    postcode = fields.Char(required=1, size=4)
    date = fields.Date()
    price = fields.Integer(digits=(0,5))
    bedrooms = fields.Integer()
    garage = fields.Boolean()
    gareden_orientation = fields.Selection([
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('diagonal', 'Diagonal'),
    ],default='vertical')

    owner_id = fields.Many2one('owner')

    _sql_constraints = [('unique_constraint','unique("name")','This name is exist')]

    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price == 0:
                raise ValidationError('please enter a price')


    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        print('create res')
        return res

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset, limit, order, access_rights_uid)
        print("search res")
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        print("write res")
        return res

    def unlink(self):
        res = super(Property, self).unlink()
        print("unlink res")
        return res