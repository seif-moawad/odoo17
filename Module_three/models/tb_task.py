from odoo import api, fields, models
from odoo.exceptions import ValidationError

class TbTask(models.Model):

    _name = 'tb.task'
    name = fields.Char(required=1,string="Task Name")
    is_done = fields.Boolean(string="Is Done", default=False)

    project_id = fields.Many2one('tb.project', string="Project")
