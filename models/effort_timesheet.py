from odoo import models, fields, api
from datetime import datetime, timedelta
from datetime import datetime, date, timedelta, time
from dateutil.rrule import rrule, DAILY
from pytz import timezone, UTC


class EffortTimesheet(models.Model):
    _name = 'effort.timesheet'
    _description = 'Here effort timesheet information is stored.'
    _rec_name = 'combination'

    def _get_employee_id(self):
        return self.env.user.employee_id

    project_id = fields.Many2one('project.project', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", default=_get_employee_id, required=True)
    start_time = fields.Datetime("Start Time", default=fields.Datetime.now(), required=True)
    end_time = fields.Datetime("End Time", required=True)
    duration = fields.Float("Duration")

    @api.onchange('start_time', 'end_time')
    def calculate_date(self):
        if self.start_time and self.end_time:
            d1 = datetime.strptime(str(self.start_time), '%Y-%m-%d %H:%M:%S')
            d2 = datetime.strptime(str(self.end_time), '%Y-%m-%d %H:%M:%S')
            d3 = d2 - d1
            self.duration = float(d3.days) * 24 + (float(d3.seconds) / 3600)

    @api.model
    def get_unusual_days(self, start_time, end_time=None):
        # Checking the calendar directly allows to not grey out the leaves taken
        # by the employee
        calendar = self.env.user.employee_id.resource_calendar_id
        if not calendar:
            return {}
        dfrom = datetime.combine(fields.Date.from_string(start_time), time.min).replace(tzinfo=UTC)
        dto = datetime.combine(fields.Date.from_string(end_time), time.max).replace(tzinfo=UTC)

        works = {d[0].date() for d in calendar._work_intervals_batch(dfrom, dto)[False]}
        return {fields.Date.to_string(day.date()): (day.date() not in works) for day in rrule(DAILY, dfrom, until=dto)}

    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.depends('project_id', 'duration')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.project_id.name + ' (' + str(test.duration) + ' hours)'
