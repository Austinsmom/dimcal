# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 16:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    """
    Set up indexes and populate PK
    """

    dependencies = [
        ('dcal', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # Migrations are inside a transation block so no CONCURRENTLY allowed
            sql="""
CREATE INDEX  IF NOT EXISTS idx_dim_calendar_calendar_date
ON dim_calendar(calendar_date);
""", reverse_sql="""
DROP INDEX idx_dim_calendar_calendar_date;
"""),

        migrations.RunSQL(
            sql="""
BEGIN;

DELETE FROM
dim_calendar;

INSERT
INTO
dim_calendar(dim_calendar_pk, calendar_date)
SELECT
CAST(to_char(calendar_date, 'yyyymmdd')
AS
INT), calendar_date
FROM
generate_series('1970-01-01'::timestamp, '2038-01-19'::timestamp, '1 day'::interval) calendar_date
;

COMMIT;
""", reverse_sql="""
TRUNCATE TABLE dim_calendar;
"""
    )
    ]