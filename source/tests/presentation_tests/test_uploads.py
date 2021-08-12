import os
from unittest import TestCase

from werkzeug.datastructures import FileStorage

from presentation_layer.app_factory import AppFactory


class UploadsTest(TestCase):
    def setUp(self) -> None:
        self.app = AppFactory.create_app()

    def test_access_uploaded_file(self):
        value = "cybersecurity001-gr-bo.webp"
        with self.app.test_request_context():
            from presentation_layer.app import app
            path = os.path.abspath(app.root_path) + "/" + app.config["UPLOAD_FOLDER"] + "/" + value
            value = open(path)
            value = FileStorage(value)
            print(value)
