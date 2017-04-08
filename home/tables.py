import django_tables2 as tables
from django.utils.html import escape
from django.utils.safestring import mark_safe


class UsersTable(tables.Table):
    name = tables.Column(verbose_name='name')
    username = tables.Column(verbose_name='username')

    def __init__(self, *args, **kwargs):
        super(UsersTable, self).__init__(*args, **kwargs)

    def render_name(self, value):
        return mark_safe('<strong>{}</strong>'.format(escape(value)))

    def render_username(self, value):
        return mark_safe('<strong>{}</strong>'.format(escape(value)))
