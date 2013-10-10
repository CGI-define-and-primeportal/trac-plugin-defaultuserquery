from genshi.builder import tag
from pkg_resources import resource_filename
from trac.core import Component, implements
from trac.util.presentation import to_json
from trac.util.translation import _
from trac.web import IRequestHandler
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import (ITemplateProvider, add_ctxtnav, add_script,
                             add_script_data)


class DefaultUserQueryModule(Component):
    implements(IRequestHandler, ITemplateStreamFilter, ITemplateProvider)
    '''A #define plugin that allows users to select the default query to be
    executed when visiting the ticket page.'''

    # ITemplateProvider methods
    def get_htdocs_dirs(self):
        return [('defaultuserquery', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return []

    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info == '/defaultuserquery'

    def process_request(self, req):
        self._write_default_user_query(req.authname, req.query_string)
        req.send_header('Content-Type', 'application/json;charset=utf-8')
        req.send(to_json({
            'new_default_user_query': req.query_string}))

    # ITemplateStreamFilter methods
    def filter_stream(self, req, method, filename, stream, data):

        # There will always be at least one link to '/query' on all #define
        # pages because of the ribbon.
        add_script(req, 'defaultuserquery/js/defaultuserquery.js')
        standard_query_href = req.href.query()
        replacement_query = self._read_default_user_query(req.authname)
        replacement_query_href = ('{0}?{1}'.format(standard_query_href,
                                                   replacement_query)
                                  if replacement_query
                                  else standard_query_href)
        add_script_data(req, (
            # This is needed as a js variable to be able to select all standard
            # query links
            ('standard_query_href', standard_query_href),
            # This will replace the targets of all standard query links
            ('replacement_query_href', replacement_query_href)))
        if req.path_info == '/query':
            # Add a link in the ribbon to save the current query as default
            add_ctxtnav(req,
                        tag.a(tag.id(class_="icon-bookmark"),
                              _("Set as default query"),
                              id_='make-query-default',
                              href=req.href('defaultuserquery')))
        return stream

    # Internal methods
    def _read_default_user_query(self, sid):
        db = self.env.get_read_db()
        cursor = db.cursor()
        cursor.execute('SELECT value FROM session_attribute '
                       'WHERE sid=%s AND name=%s', (sid, 'default_user_query'))
        for query, in cursor:
            return query

    def _write_default_user_query(self, sid, query_string, db=None):

        @self.env.with_transaction(db)
        def do_write(db):
            cursor = db.cursor()
            self.env.log.debug('Attempting to update default query for %s to '
                               '%s', sid, query_string)
            cursor.execute(
                'UPDATE session_attribute SET value=%s '
                'WHERE sid=%s and name=%s',
                (query_string, sid, 'default_user_query'))

            if cursor.rowcount < 1:
                self.env.log.debug('Updating of default user query failed. '
                                   'Inserting default query %s for %s',
                                   query_string, sid)
                cursor.execute(
                    'INSERT INTO session_attribute '
                    '(sid, authenticated, name, value) '
                    'values (%s, %s, %s, %s)',
                    (sid, 1, 'default_user_query', query_string))
