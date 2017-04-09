
def side_menu(title=None):
    menu_items = {
        'side_menu_list': [
            ['Menu1', 'glyphicon glyphicon-globe',
             [('Paranoia', 'http://google.com'),
              ('Minune', 'http://google.com'),
              ('Valoros', 'http://google.com')]],

            ['Menu2', 'glyphicon glyphicon-cloud-download',
             [('Barosaneala', 'http://google.com'),
              ('Sasesc', 'http://google.com'),
              ('Salam', 'http://google.com')]],

            ['Account', 'glyphicon glyphicon-list-alt',
             [('Status', 'http://google.com'),
              ('Logout', 'logout')]],
        ],
    }

    return menu_items
