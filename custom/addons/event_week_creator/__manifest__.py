{
    'name': "Event Week Creator",
    'version': '1.0',
    'summary': "Ermöglicht die Erstellung von Veranstaltungen für eine Woche",
    'description': """
        Mit diesem Modul können Benutzer für eine ausgewählte Woche Veranstaltungen anlegen.
        Es können vordefinierte Event-Vorlagen und Wochen-Templates genutzt werden.
    """,
    'category': 'Events',
    'depends': ['base', 'event'],
    'data': [
        'security/ir.model.access.csv',
        'views/event_week_config_view.xml',
        'views/event_week_template_view.xml',
        'views/event_week_menu.xml'


    ],
    'installable': True,
    'application': False,
}
