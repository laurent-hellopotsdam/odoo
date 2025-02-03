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
        'event.event',  # Alternativ kannst du hier ein eigenes Template-Modell verknüpfen.
        string="Event Template"
    )
    description = fields.Text(string="Beschreibung")
