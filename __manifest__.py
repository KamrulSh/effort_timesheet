{
    'name' : 'Employee Effort Timesheet',
    'sequence': 200,
    'version' : '1.0',
    'summary': 'Employee Effort calculations in timesheet',
    'author': 'Kamrul and Niazi',
    'category': 'Human Resources',
    'description' : 'This is an application where employee can save daily work effort and calculate total effort in a timesheet.',
    'depends' : ['base', 'hr','project'],
    'version': '0.1',
    'data' : [
        'security/ir.model.access.csv',
        'views/effort_timesheet.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}