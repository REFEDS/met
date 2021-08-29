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


class ContactPerson(models.Model):
    """
    Description of an contact person as defined in SAML
    """
    TYPE_TECHNICAL = 1
    TYPE_SUPPORT = 2
    TYPE_ADMINISTRATIVE = 3
    TYPE_BILLING = 4
    TYPE_OTHER = 5
    TYPE_CHOICES = (
        (TYPE_TECHNICAL, 'technical'),
        (TYPE_SUPPORT, 'support'),
        (TYPE_ADMINISTRATIVE, 'administrative'),
        (TYPE_BILLING, 'billing'),
        (TYPE_OTHER, 'other'),
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_('Type'),
        blank=False,
        null=False,
        choices=TYPE_CHOICES,
        default=TYPE_OTHER,
        help_text=_('The type of the contact')
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        blank=True,
        null=True,
        help_text=_('The name of the contact')
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=256,
        blank=True,
        null=True,
        help_text=_('The email of the contact')
    )

    class Meta:
        verbose_name_plural = 'contact people'

    def __str__(self):
        return self.name or self.email

    @classmethod
    def get_type_by_description(cls, description):
        for choice in cls.TYPE_CHOICES:
            if choice[1] == description:
                return choice[0]
        return cls.TYPE_OTHER
