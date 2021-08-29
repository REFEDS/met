#################################################################
# MET v2 Metadate Explorer Tool
#
# This Software is Open Source. See License: https://github.com/TERENA/met/blob/master/LICENSE.md
# Copyright (c) 2012, TERENA All rights reserved.
#
# This Software is based on MET v1 developed for TERENA by Yaco Sistemas, http://www.yaco.es/
# MET v2 was developed for TERENA by Tamim Ziai, DAASI International GmbH, http://www.daasi.de
# Current version of MET has been revised for performance improvements by Andrea Biancini,
# Consortium GARR, http://www.garr.it
##########################################################################

from django.contrib import admin
from django.utils.safestring import mark_safe

from met.metadataparser.models import (
    Federation, Entity, EntityCategory, ContactPerson, EntityScope
)


class FederationAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    filter_horizontal = ('editor_users',)


class EntityAdmin(admin.ModelAdmin):
    list_filter = ('federations', )
    search_fields = ('entityid', 'name')
    filter_horizontal = ('editor_users', 'contacts')


class EntityCategoryAdmin(admin.ModelAdmin):
    search_fields = ('category_id', 'name')


class ContactPersonAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_display = ('name', 'email', 'type')
    readonly_fields = ('entity_list', )

    def entity_list(self, instance):
        response = '<ul>'
        for entity in instance.entities.all():
            response += '<li>{}</li>'.format(entity.entityid)
        response += '</ul>'
        return mark_safe(response)
    entity_list.short_description = 'Entities'


class EntityScopeAdmin(admin.ModelAdmin):
    list_display = ('entity', 'name', )


admin.site.register(Federation, FederationAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityCategory, EntityCategoryAdmin)
admin.site.register(ContactPerson, ContactPersonAdmin)
admin.site.register(EntityScope, EntityScopeAdmin)
