# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import met.metadataparser.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('metadataparser', '0002_add_entity_fields'),
    ]

    operations = [
        migrations.RunSQL(
            'ALTER TABLE auth_group CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE auth_permission CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE auth_user CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE django_admin_log CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE django_content_type CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE django_migrations CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE django_session CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE django_site CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_contactperson CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_entity CONVERT TO CHARACTER SET utf8;'
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_entitycategory CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_entitycategory CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_entityscope CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_entitystat CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_entitytype CONVERT TO CHARACTER SET utf8;',
        ),
        migrations.RunSQL(
            'ALTER TABLE metadataparser_federation CONVERT TO CHARACTER SET utf8;',
        ),
    ]
