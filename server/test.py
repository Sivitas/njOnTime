from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import remember
from pyramid.renderers import render
import os


def index_view(request):
    index_html = open("../app/test.html", "rU")
    data = index_html.read()
    return Response(data, content_type='text/html')


if __name__ == "__main__":
    config = Configurator()
    config.add_route('index', '/')
    config.add_view(index_view, route_name="index")
    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 8080, app)
    server.serve_forever()
