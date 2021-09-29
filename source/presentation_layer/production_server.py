#!/usr/bin/python3
import sys
import os

import werkzeug

dirname = os.path.dirname(__file__)
source_dir = os.path.dirname(dirname)
sys.path.append(source_dir)

from waitress import serve

from presentation_layer.app_factory import AppFactory

app = AppFactory.create_app()


@werkzeug.serving.run_with_reloader
def run_server():
    app.debug = True # while in development - enables hot reload
    serve(app, listen='*:8080')


if __name__ == "__main__":
    run_server()
