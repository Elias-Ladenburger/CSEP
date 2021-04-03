from domain.scenario.auxiliary import Image
from domain.scenario.graphs import GraphNode


class Inject(GraphNode):
    """An inject in a story"""
    def __init__(self, title: str, description="", image: Image = None):
        super().__init__(title)
        if image is None:
            image = {"image_path": "", "image_position": ""}
        self.description = description
        self.image = image or Image()