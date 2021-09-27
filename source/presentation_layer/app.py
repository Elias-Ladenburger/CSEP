"""
Development server - do not use for production!
"""
import sys
import os
dirname = os.path.dirname(__file__)
source_dir = os.path.dirname(dirname)
sys.path.append(source_dir)

from presentation_layer.app_factory import AppFactory

app = AppFactory.create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

