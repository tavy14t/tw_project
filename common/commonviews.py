
def side_menu(title=None):
    menu_items = {
        'title': title,
        'side_menu_list': [
            ['Search', 'glyphicon glyphicon-search',
             [('Search', '/search/'),
              ('Posts', '#'),
              ('Titles', '#'),
              ('Body', '#')]],

            ['Browse', 'glyphicon glyphicon-folder-open',
             [('Tags', '/tags/'),
              ('Sasesc', '#'),
              ('Salam', '#')]],

            ['News', 'glyphicon glyphicon-education',
             [('Status', '#'),
              ('Logout', '/logout/')]],

            ['User', 'glyphicon glyphicon-user',
             [('Account settings', '/account/'),
              ('Logout', '/logout/')]],
        ],
    }

    return menu_items
