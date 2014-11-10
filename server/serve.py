from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.renderers import render
from pyramid.static import static_view
import sys, os
from toolbox import departure_vision

#@view_config(renderer="", request_method="GET", route_name="")
def index_view(request):
    index_html = open("./app/index.html", "rU")
    data = index_html.read()
    return Response(data, content_type='text/html')

@view_config(renderer="json", request_method="GET", route_name="train_data.json")
def get_train_data(self):
    return departure_vision.get_train_schedule()

def main():
    config = Configurator()
    config.add_route('index', '/')
    config.add_route('train_data.json', 'train_data.json')
    config.add_view(index_view, route_name="index")
    config.add_static_view('/', 'app')
    config.scan()
    web_app = config.make_wsgi_app()
    return web_app


if __name__ == "__main__":
    web_app = main()
    server = make_server("0.0.0.0", 8080, web_app)
    server.serve_forever()


