"""
Development server - do not use for production!
"""

from presentation_layer.app_factory import AppFactory

app = AppFactory.create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

