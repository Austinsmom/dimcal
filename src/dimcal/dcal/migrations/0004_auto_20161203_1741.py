# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 17:41
from __future__ import unicode_literals
from django.db import migrations, connection, transaction
from pathlib import Path
from itertools import chain, zip_longest

@transaction.non_atomic_requests
def forwards_func(apps, schema_editor):
    # Thanks: http://stackoverflow.com/a/13955271
    # Much of the proxy is not defined until this is done
    force_proxy = connection.cursor()
    realconn = connection.connection
    old_isolation_level = realconn.isolation_level
    realconn.set_isolation_level(0)
    cursor = realconn.cursor()
    cursor.execute('VACUUM ANALYZE dim_calendar;')
    realconn.set_isolation_level(old_isolation_level)

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    """
    Populate hol_* columns
    """

    dependencies = [
        ('dcal', '0003_auto_20161203_1655'),
    ]

    file_sql = [ Path(file).read_text() for file in sorted(Path('./sql/').glob('hol_*.sql'))]
    if not file_sql:
        raise FileNotFoundError

    # intersperse SQL files with VACUUMs to keep db size down, for Travis.
    tmp_ops = [migrations.RunSQL( sql ) for sql in file_sql]

    operations = []
    every_n = 5
    for start_index in range(0, len(tmp_ops), every_n):
        operations.extend(tmp_ops[start_index:start_index + every_n])
        operations.append(migrations.RunPython(forwards_func, reverse_func, atomic=False))

