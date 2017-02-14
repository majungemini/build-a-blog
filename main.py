#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
class Blogs(db.Model):
    title = db.StringProperty(required = True)
    context = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        fiveposts = db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("front.html")
        content = t.render(blogs = fiveposts, error = self.request.get("error"))
        self.response.write(content)

class NewPost(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)
    def post(self):
        blogtitle = self.request.get("blog_title")
        blogcontext = self.request.get("blog_context")
        if blogtitle and blogcontext :
            blog = Blogs(title = blogtitle, context = blogcontext)
            blog.put()
            self.redirect("/")
        else:
            error = "We need both a title and a body!"
            t = jinja_env.get_template("newpost.html")
            content = t.render(error = error)
            self.response.write(content)


class BlogDetail(webapp2.RequestHandler):
    def get(self, blog_id):
        blog = blogs.get_by_id(blog_id)
        if not blog:
            self.renderError(404)
        t = jinja_env.get_template("blog_detail.html")
        content = t.render(blog=blog)

        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPost),
    webapp2.Route('/blogs/<blog_id:\d+>', BlogDetail),

], debug=True)
