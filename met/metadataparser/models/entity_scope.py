##########################################################################
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

from django.db import models
from django.utils.translation import ugettext_lazy as _


class EntityScope(models.Model):
    """
    Description of an entity scope as defined in SAML here:
    https://docs.oasis-open.org/security/saml-subject-id-attr/v1.0/cs01/saml-subject-id-attr-v1.0-cs01.html#_Toc536097238
    """
    entity = models.ForeignKey(
        'Entity',
        verbose_name=_('Entity'),
        blank=False,
        null=False,
    )

    name = models.CharField(
        verbose_name='Scope name',
        max_length=1000,
        blank=False,
        null=False,
        help_text=_('The name of the scope')
    )

    def __str__(self):
        return self.name
