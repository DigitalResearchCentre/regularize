import django_tables2 as tables

class ChangeTable(tables.Table):
    originals = tables.Column()
