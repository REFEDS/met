# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import met.metadataparser.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('metadataparser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.PositiveSmallIntegerField(verbose_name='Type', default=5, choices=[(1, 'technical'), (2, 'support'), (3, 'administrative'), (4, 'billing'), (5, 'other')], help_text='The type of the contact')),
                ('name', models.CharField(verbose_name='Name', max_length=256, blank=True, null=True, help_text='The name of the contact')),
                ('email', models.EmailField(verbose_name='Email', max_length=256, blank=True, null=True, help_text='The email of the contact')),
            ],
            options={
                'verbose_name_plural': 'contact people',
            },
        ),
        migrations.CreateModel(
            name='EntityScope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Scope name', max_length=1000, help_text='The name of the scope')),
            ],
        ),
        migrations.AlterModelOptions(
            name='entitycategory',
            options={'verbose_name_plural': 'entity categories'},
        ),
        migrations.AddField(
            model_name='entity',
            name='organization_display_name',
            field=met.metadataparser.models.base.JSONField(verbose_name='Organization Display Name', max_length=2000, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='organization_name',
            field=met.metadataparser.models.base.JSONField(verbose_name='Organization Name', max_length=2000, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entityscope',
            name='entity',
            field=models.ForeignKey(verbose_name='Entity', to='metadataparser.Entity'),
        ),
        migrations.AddField(
            model_name='entity',
            name='contacts',
            field=models.ManyToManyField(verbose_name='Contact People', related_name='entities', to='metadataparser.ContactPerson'),
        ),
    ]
