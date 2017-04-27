
def side_menu(title=None):
    menu_items = {
        'title': title,
        'side_menu_list': [
            ['Search', 'glyphicon glyphicon-search',
             [('Search', '/search/'),
              ('Posts', '/browse/'),
              ('Titles', '/news/'),
              ('Body', '/body/')]],

            ['Browse', 'glyphicon glyphicon-folder-open',
             [('Tags', '/tags/'),
              ('Sasesc', 'http://google.com'),
              ('Salam', 'http://google.com')]],

            ['News', 'glyphicon glyphicon-education',
             [('Status', 'http://google.com'),
              ('Logout', '/logout/')]],

            ['User', 'glyphicon glyphicon-user',
             [('Account settings', '/account/'),
              ('Logout', '/logout/')]],
        ],
    }

    return menu_items