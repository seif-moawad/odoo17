{
    'name': 'Tech Bridge',
    'author' : 'xyz',
    'version' : '1.0',
    'category' : '',
    'depends' : ['base', 'mail','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/tb_freelancer_view.xml',
        'views/tb_project_view.xml',
        'views/base_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
        'Module_three/static/src/css/style.css',
        ],
    },
    'application' : True,
}