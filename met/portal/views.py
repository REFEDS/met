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

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from local_settings import BASEURL, LOGIN_URL, LOCAL_DS, GLOBAL_DS, SAML_ENTITYID


def ds(request):
    idp = request.GET.get('entityID', None)
    if idp is not None:
        url = "%s?idp=%s" % (LOGIN_URL, idp)
    else:
        url = "%s/?target=%s&return=%s&entityID=%s" % (GLOBAL_DS, BASEURL, LOCAL_DS, SAML_ENTITYID)

    return redirect(url)

def error403(request):
    response = render_to_response(
        '403.html', {}, context_instance=RequestContext(request))
    response.status_code = 403
    return response


def error404(request):
    response = render_to_response(
        '404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def error500(request):
    response = render_to_response(
        '500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response
