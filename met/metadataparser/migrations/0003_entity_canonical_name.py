# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadataparser', '0002_add_entity_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='canonical_name',
            field=models.CharField(verbose_name='Canonical Name', max_length=500, blank=True, null=True, db_index=True),
        ),
    ]
