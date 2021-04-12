from domain.scenario_design.auxiliary import Image
from domain.scenario_design.graphs import GraphNode


class Inject(GraphNode):
    """An inject in a story"""
    def __init__(self, title: str, text="", image: Image = None, id=""):
        super().__init__(title)
        if image is None:
            image = {"image_path": "", "image_position": ""}
        self.text = text
        self.image = image or Image()
        self._id = id

    @property
    def id(self):
        if self._id:
            return self._id
        else:
            return "unset ID"

    def __str__(self):
        return_str = self.id + "\n" + self.label + "\n"
        return_str += self.text
        return return_str