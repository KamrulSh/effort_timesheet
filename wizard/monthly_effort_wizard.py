from odoo import models, fields, api, _
from datetime import datetime, timedelta


class MonthlyEffort(models.TransientModel):
    _name = 'monthly.effort.wizard'

    project_id = fields.Many2one('project.project', string="Project name")
    employee_id = fields.Many2one('hr.employee', string="Employee name")
    effort_month = fields.Date("Month", default=fields.Datetime.now())

    monthly_report = fields.Html()
