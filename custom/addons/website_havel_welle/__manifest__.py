{
    'name': 'Havelwelle Theme',
    'description': '...',
    'category': 'Website/Theme',
    'version': '1.0',
    'depends': ['website'],
    'data': [
        'views/snippets/s_flick_flack.xml',
        'views/snippets/options.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_havel_welle/static/src/scss/base.scss'
        ],
        'web._assets_primary_variables': [
              ('append', 'website_havel_welle/static/src/scss/primary_variables.scss'),
           ]
    }
}