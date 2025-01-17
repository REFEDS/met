# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unicodedata
from django.db import transaction
from django.db import migrations, models
from django.db.utils import OperationalError
from met.metadataparser.utils import get_canonical


def populate_entities(apps, schema_editor):
    Entity = apps.get_model('metadataparser', 'Entity')
    for entity in Entity.objects.filter(name__isnull=False):
        try:
            canonical_name = get_canonical(entity.name)
            entity.canonical_name = canonical_name
            with transaction.atomic():
                entity.save(update_fields=('canonical_name', ))
        except OperationalError:
            entity.canonical_name = unicodedata.normalize('NFKD', canonical_name).encode('ASCII', 'ignore')
            entity.save(update_fields=('canonical_name', ))


def noop(apps, schema_editor):
    return None


class Migration(migrations.Migration):

    dependencies = [
        ('metadataparser', '0004_entity_canonical_name'),
    ]

    operations = [
        migrations.RunPython(populate_entities, noop),
    ]
