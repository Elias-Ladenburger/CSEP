from waitress import serve

from presentation_layer.app_factory import AppFactory

app = AppFactory.create_app()


if __name__ == "__main__":
    serve(app, listen='*:80', url_scheme='https')
