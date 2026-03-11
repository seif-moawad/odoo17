from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TbSkill(models.Model):
    _name = 'tb.skill'

    category = fields.Selection([
        ('dev','Development'),
        ('design','Design'),
        ('pro','Production'),
        ('test','Testing'),
        ('photograph','Photograph'),
        ('other','Other')
    ],default='dev')