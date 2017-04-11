import django_tables2 as tables
from django.utils.html import escape
from django.utils.safestring import mark_safe


class InfoTable(tables.Table):
    info = tables.Column(verbose_name='info')
    value = tables.Column(verbose_name='value')

    def __init__(self, *args, **kwargs):
        super(InfoTable, self).__init__(*args, **kwargs)

    def render_info(self, value):
        return mark_safe('{0}'.format(escape(value)))

    def render_value(self, value):
        return mark_safe('{0}'.format(escape(value)))
