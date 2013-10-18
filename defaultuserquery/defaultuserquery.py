# -*- coding: utf-8 -*-

import re
from functools import partial

from genshi.builder import tag
from genshi.filters import Transformer
from trac.core import Component, implements
from trac.ticket.query import Query
from trac.ticket.query import QueryModule
from trac.util.translation import _
from trac.web import HTTPBadRequest, IRequestHandler
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import add_script_data, add_notice


class DefaultUserQueryModule(Component):
    implements(IRequestHandler, ITemplateStreamFilter)
    '''A #define plugin that allows users to select the default query to be
    executed when visiting the ticket page.'''

    _minimize = partial(re.sub, r'\s*([\s+{}();.,])\s*', r'\1')

    # Js function for replacing standard query links with the default query
    # selected by the user.  This should preferably have been done with a
    # Transformer but that doesn't affect the link in the ribbon.
    _replace_query_links_js = tag.script(_minimize('''
        jQuery(document).ready(function($) {
          $('a[href="' + queryHref + '"]').attr('href', replacementQueryHref);
        });'''), type_='text/javascript')

    # Js function for redirecting the query form from the query module to this
    # plugin prior to submitting.
    _redirect_query_form_js = tag.script(_minimize('''
        jQuery(document).ready(function($) {
          $('#set-default-query-btn').click(function(event) {
            $('form#query').attr('action', defaultUserQueryAction);
          });
        });'''), type_='text/javascript')

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info == '/defaultuserquery'

    def process_request(self, req):

        if req.method != 'POST':
            raise HTTPBadRequest(_("Only POST is supported"))
        query = Query(self.env,
                      constraints=QueryModule(self.env)._get_constraints(req),
                      cols=req.args['col'],
                      desc=req.args.get('desc', 0),
                      group=req.args['group'],
                      groupdesc=req.args.get('groupdesc', 0),
                      max=req.args['max'],
                      order=req.args['order'])
        req.session['default_user_query'] = query.get_href(req.href)
        add_notice(req, _("Your default query has been changed"))
        # Let the query system handle the request
        req.redirect(query.get_href(req.href))

    # ITemplateStreamFilter methods
    def filter_stream(self, req, method, filename, stream, data):
        if 'default_user_query' in req.session:
            # Inject js for replacing all standard query links
            add_script_data(req, (
                ('queryHref', req.href.query()),
                ('replacementQueryHref', req.session['default_user_query'])))
            stream |= Transformer('html/head').append(
                self._replace_query_links_js)
        if req.path_info == '/query':
            # Add a button to the query form for setting the default query
            stream |= Transformer('//button[@name="update"]').after(
                tag.button(tag.i(class_="icon-bookmark icon-white"),
                           _(" Set as default"),
                           id_='set-default-query-btn',
                           type_='submit',
                           class_='btn btn-mini btn-success',
                           name='set-as-default')).after(' ')
            # Add js to redirect the form when the button is clicked
            add_script_data(req, (
                ('defaultUserQueryAction', req.href('defaultuserquery')),))
            stream |= Transformer('html/head').append(
                self._redirect_query_form_js)
        return stream
