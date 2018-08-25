import os
import jinja2
import json

import webapp2

class Handler(webapp2.RequestHandler):
    def respondToJson(self, json_data):
        '''

        Responds to JSON requests with data

        '''
        self.response.out.write(json.dumps((json_data)))

    def write(self, *a, **kw):
        '''

        Basic writing responses with plain text

        '''
        self.response.out.write(*a, **kw)

    def renderBlank(self, template, **kw):
        '''

        Render a blank template with parameters
        The difference is mainly just that the navbar does not appear when you renderBlank but
        will in just render.

        '''
        self.write(self.render_str(template, **kw))