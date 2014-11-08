from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.renderers import render
from pyramid.static import static_view
import sys, os
import app.js


def index_view(request):
    index_html = open("./app/index.html", "rU")
    data = index_html.read()
    return Response(data, content_type='text/html')


if __name__ == "__main__":
    # add the index.html file
    config = Configurator()
    config.add_route('index', '/')
    config.add_view(index_view, route_name="index")
    config.add_static_view('/', 'app')
    config.scan()

    # make the goddamn server
    web_app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 8080, web_app)
    server.serve_forever()
