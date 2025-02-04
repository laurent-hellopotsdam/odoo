from odoo import api, fields, models

class EventWeekTemplate(models.Model):
    _name = 'event.week.template'
    _description = 'Wochen-Template mit vordefinierten Event-Zeitslots'

    name = fields.Char(string="Name des Templates", required=True)
    week_line_ids = fields.One2many(
        'event.week.template.line',
        'template_id',
        string="Zeitslots"
    )

class EventWeekTemplateLine(models.Model):
    _name = 'event.week.template.line'
    _description = 'Zeitslot im Wochen-Template'

    template_id = fields.Many2one(
        'event.week.template',
        string="Template",
        ondelete='cascade',
        required=True
    )
    name = fields.Char(string="Event Name", required=True)
    day_of_week = fields.Selection([
        ('0', 'Montag'),
        ('1', 'Dienstag'),
        ('2', 'Mittwoch'),
        ('3', 'Donnerstag'),
        ('4', 'Freitag'),
        ('5', 'Samstag'),
        ('6', 'Sonntag'),
    ], string="Wochentag", required=True)
    start_time = fields.Float(
        string="Startzeit",
        required=True,
        help="Angabe als Float im 24-Stunden-Format, z.B. 9.30 für 09:30 Uhr"
    )
    end_time = fields.Float(
        string="Endzeit",
        required=True,
        help="Angabe als Float im 24-Stunden-Format"
    )
    event_template_id = fields.Many2one(
        'event.type',
        string="Event Template",
        help="Template für das Event, falls vorhanden"
    )

    @api.onchange('event_template_id')
    def _onchange_event_template_id(self):
        if self.event_template_id:
            # Übernehme den Namen aus dem Template in das Namensfeld
            self.name = self.event_template_id.name
