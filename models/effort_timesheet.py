from odoo import models, fields, api
from datetime import datetime, timedelta


class EffortTimesheet(models.Model):
    _name = 'effort.timesheet'
    _description = 'Here effort timesheet information is stored.'

    def _get_employee_id(self):
        return self.env.user.employee_id

    project_id = fields.Many2one('project.project', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", default=_get_employee_id, required=True)
    start_time = fields.Datetime("Start Time", default=fields.Datetime.now(), required=True)
    end_time = fields.Datetime("End Time", required=True)
    duration = fields.Float("Duration")

    # def onchange_start_time(self):
    #     # self.start_time = fields.Datetime.from_string(self.start_time)
    #     # self.end_time = fields.Datetime.from_string(self.end_time)
    #     self.duration = float(self.end_time - self.start_time)

    @api.onchange('start_time', 'end_time')
    def calculate_date(self):
        if self.start_time and self.end_time:
            d1 = datetime.strptime(str(self.start_time), '%Y-%m-%d %H:%M:%S')
            d2 = datetime.strptime(str(self.end_time), '%Y-%m-%d %H:%M:%S')
            d3 = d2 - d1
            self.duration = float(d3.days) * 24 + (float(d3.seconds) / 3600)
