from odoo import api, fields, models

class EventWeekConfigLine(models.TransientModel):
    _name = 'event.week.config.line'
    _description = 'Zeitslot in der Wochen-Konfiguration'

    config_id = fields.Many2one(
        'event.week.config',
        string="Konfiguration",
        ondelete='cascade'
    )
    name = fields.Char(string="Event Name", required=True)
    start_datetime = fields.Datetime(string="Startzeit", required=True)
    end_datetime = fields.Datetime(string="Endzeit", required=True)
    event_template_id = fields.Many2one(
        'event.type',  # Alternativ kannst du hier ein eigenes Template-Modell verknüpfen.
        string="Event Template"
    )
    description = fields.Text(string="Beschreibung")

    weekday = fields.Selection(
        selection=[
            ('0', 'Montag'),
            ('1', 'Dienstag'),
            ('2', 'Mittwoch'),
            ('3', 'Donnerstag'),
            ('4', 'Freitag'),
            ('5', 'Samstag'),
            ('6', 'Sonntag')
        ],
        string="Wochentag",
        compute="_compute_weekday",
        store=True
    )

    @api.onchange('event_template_id')
    def _onchange_event_template_id(self):
        if self.event_template_id:
            # Übernehme den Namen aus dem Template in das Namensfeld
            self.name = self.event_template_id.name

    @api.depends("start_datetime")
    def _compute_weekday(self):
        for record in self:
            if record.start_datetime:
                record.weekday = str(record.start_datetime.weekday())  # 0 = Montag, 6 = Sonntag
