import django_tables2 as tables
from django.utils.safestring import mark_safe


class TagsTable(tables.Table):
    info = tables.Column(verbose_name='Posts for the selected tags:')

    def __init__(self, *args, **kwargs):
        super(TagsTable, self).__init__(*args, **kwargs)

    def render_info(self, value):
        return mark_safe(value)
