from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class EventWeekConfig(models.TransientModel):
    _name = 'event.week.config'
    _description = 'Wizard zur Erstellung von Veranstaltungen für eine Woche'

    week_start = fields.Date(
        string="Wochenstart (Montag)",
        required=True,
        default=fields.Date.context_today
    )
    week_template_id = fields.Many2one(
        'event.week.template',
        string="Vorhandenes Wochen-Template",
        help="Wähle ein Template, um bereits vordefinierte Events zu laden"
    )
    line_ids = fields.One2many(
        'event.week.config.line',
        'config_id',
        string="Event Zeitslots"
    )

    def action_load_week_template(self):
        """Lädt die Event-Zeitslots aus dem ausgewählten Wochen-Template in den Wizard."""
        if not self.week_template_id:
            raise UserError(_("Bitte zuerst ein Wochen-Template auswählen."))
        lines = []
        # Annahme: Das Wochen-Template enthält vordefinierte Zeitslots (week_line_ids)
        for tmpl_line in self.week_template_id.week_line_ids:
            # Berechne das Datum und die Zeit relativ zum gewählten Wochenstart.
            # Hier wird angenommen, dass tmpl_line.day_of_week ein Integer ist (0=Montag, ... 6=Sonntag)
            day_date = fields.Date.from_string(self.week_start) + timedelta(days=tmpl_line.day_of_week)
            start_dt = datetime.combine(day_date, tmpl_line.start_time)
            end_dt = datetime.combine(day_date, tmpl_line.end_time)
            lines.append((0, 0, {
                'name': tmpl_line.name,
                'start_datetime': start_dt,
                'end_datetime': end_dt,
                'event_template_id': tmpl_line.event_template_id.id,
            }))
        self.line_ids = lines

    def action_create_events(self):
        """Erstellt die Events gemäß den konfigurierten Zeitslots im Wizard."""
        event_obj = self.env['event.event']
        for line in self.line_ids:
            # Hier kannst du noch weitere Logik einfügen (z. B. Validierungen)
            event_vals = {
                'name': line.name or _("Neues Event"),
                'start_date': line.start_datetime,
                'stop_date': line.end_datetime,
                'description': line.description,
            }
            # Falls ein Event-Template gesetzt ist, können zusätzliche Felder übernommen werden.
            if line.event_template_id:
                event_vals.update({
                    # Beispiel: Falls das Template ein Feld 'location' hat:
                    'location_id': line.event_template_id.location_id.id,
                    # Oder andere Template-abhängige Felder.
                })
            event_obj.create(event_vals)
        return {'type': 'ir.actions.act_window_close'}

class EventWeekConfigLine(models.TransientModel):
    _name = 'event.week.config.line'
    _description = 'Zeitslot in der Wochen-Konfiguration'

    config_id = fields.Many2one('event.week.config', string="Konfiguration", ondelete='cascade')
    name = fields.Char(string="Event Name", required=True)
    start_datetime = fields.Datetime(string="Startzeit", required=True)
    end_datetime = fields.Datetime(string="Endzeit", required=True)
    event_template_id = fields.Many2one(
        'event.event',  # Alternativ: Ein eigenes Template-Modell, falls vorhanden
        string="Event Template",
        help="Wählt ein Template, um Standardfelder zu übernehmen"
    )
    description = fields.Text(string="Beschreibung")
