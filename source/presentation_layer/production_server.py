#!/usr/bin/python3
import sys
import os
dirname = os.path.dirname(__file__)
source_dir = os.path.dirname(dirname)
sys.path.append(source_dir)

from waitress import serve

from presentation_layer.app_factory import AppFactory

app = AppFactory.create_app()


if __name__ == "__main__":
    serve(app, listen='*:8080')
