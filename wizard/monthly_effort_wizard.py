from odoo import models, fields, api, _


class MonthlyEffort(models.TransientModel):
    _name = 'monthly.effort.wizard'

    def _get_employee_id(self):
        return self.env.user.employee_id

    project_id = fields.Many2one('project.project', string="Project name", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", default=_get_employee_id, required=True)
    effort_month = fields.Date("Month", default=fields.Datetime.now(), required=True)

    monthly_report = fields.Html("Monthly Effort")

    def month_effort_query(self):
        query = f"""
                    SELECT row_number() OVER () AS id,
                        et.start_time,
                        et.duration
                    FROM
                        effort_timesheet et
                    LEFT JOIN hr_employee hr ON hr.id = et.employee_id
        			LEFT JOIN project_project pp ON pp.id = et.project_id
        			WHERE TO_CHAR(et.start_time, 'MM')::int = {self.effort_month.strftime('%m')}
        			AND TO_CHAR(et.start_time, 'YYYY')::int = {self.effort_month.strftime('%Y')}
                """
        query_employee = f"""
                    AND et.employee_id = {self.employee_id.id}
                """
        query_project = f"""
                        AND et.project_id = {self.project_id.id}
                    """
        orderby = f"""
                    ORDER BY start_time
                """
        if self.project_id and self.employee_id:
            self._cr.execute(query + query_employee + query_project + orderby)
        elif self.employee_id:
            self._cr.execute(query + query_employee + orderby)
        else:
            self._cr.execute(query + orderby)
        effort_data = self._cr.dictfetchall()
        return effort_data

    @api.onchange("project_id", "employee_id", "effort_month")
    def action_preview_report(self):
        table = """
                    <table border="1" class="o_list_view table table-condensed table-striped o_list_view_ungrouped">
                        <thead>
                            {thead}
                        </thead>
                        <tbody>
                            {tbody}
                        </tbody>
                    </table>
                """

        thead = """
                    <tr style="text-align: center;">
                        {th}
                    </tr>
                """
        th = """<th>{}</th>\n"""
        td = """<td style="text-align: center;">{}</td>\n"""
        tr = """<tr>{}</tr>\n"""

        head = ''
        body = ''
        column_header = ['Date', 'Worked Hours']
        head += thead.format(th="".join(map(th.format, column_header)))

        effort_data = self.month_effort_query()
        total_duration = 0.0
        count_days = 0
        for i in range(0, len(effort_data)):
            count_days += 1
            column_value = [str(effort_data[i]['start_time'].strftime('%a, %d %B, %Y')), effort_data[i]['duration']]
            total_duration += effort_data[i]['duration']
            body += tr.format("".join(map(td.format, column_value)))
        total_duration_field = [f"Total days: {count_days}", f"Total effort (hours): {total_duration}"]
        body += thead.format(th="".join(map(th.format, total_duration_field)))
        view_report = table.format(thead=head, tbody=body)
        self.write({'monthly_report': view_report})
