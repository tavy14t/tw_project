
def side_menu(title=None):
    menu_items = {
        'title': title,
        'side_menu_list': [
            ['Search', 'glyphicon glyphicon-search',
             [('Users', '/search/'),
              ('Posts', '#'),
              ('Titles', '#'),
              ]],

            ['Browse', 'glyphicon glyphicon-folder-open',
             [('Filtered', '/tags/'),
              ('Recommanded', '/post/'),
              ('Popular', '#'),
              ('Traending', '#')]],

            ['News', 'glyphicon glyphicon-education',
             [('Last updates', '#')]],

            ['User', 'glyphicon glyphicon-user',
             [('Account settings', '/account/'),
              ('Logout', '/logout/')]],
        ],
    }

    return menu_items
