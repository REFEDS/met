# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.db import migrations, models
from django.db.utils import OperationalError


def populate_entities(apps, schema_editor):
    Entity = apps.get_model('metadataparser', 'Entity')
    for entity in Entity.objects.filter(name__isnull=False):
        try:
            canonical_name = entity.name['en']
        except KeyError:
            canonical_name = list(entity.name.values())[0]
        try:
            entity.canonical_name = canonical_name
            with transaction.atomic():
                entity.save(update_fields=('canonical_name', ))
        except OperationalError:
            # TODO: Fix it
            entity.canonical_name = 'OperationalError'
            entity.save(update_fields=('canonical_name', ))


def noop(apps, schema_editor):
    return None


class Migration(migrations.Migration):

    dependencies = [
        ('metadataparser', '0002_entity_canonical_name'),
    ]

    operations = [
        migrations.RunPython(populate_entities, noop),
    ]
