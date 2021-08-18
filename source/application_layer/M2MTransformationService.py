import json
from typing import List

from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseStory


class InjectTransformer:
    """This class transforms the inject from the domain layer to other datastructures."""

    def transform_inject_to_visjs(self, inject: BaseChoiceInject):
        pass

    @classmethod
    def transform_inject_to_visjs(cls, injects: List[BaseChoiceInject]):
        injects, edges = cls.transform_injects_to_visjs_dict(injects)
        return json.dumps(injects), json.dumps(edges)

    @classmethod
    def transform_injects_to_visjs_dict(cls, injects: List[BaseChoiceInject],
                                        group_id: int = 0, entry_node: str=""):
        """
        :param injects: a list of injects to be transformed
        :param group_id:
        :returns: a dictionary that represents the data structure used by vis.DataSet
        """
        inject_list = []
        edge_list = []
        level = 1
        for inject in injects:
            tmp_nodes, tmp_edges = cls._transform_inject(inject, group_id, level, entry_node)
            inject_list += [*tmp_nodes]
            edge_list += [*tmp_edges]
            level += 1
        return inject_list, edge_list

    @classmethod
    def transform_stories_to_visjs(cls, stories: List[BaseStory]):
        injects, edges = cls.transform_stories_to_visjs_dict(stories)
        return json.dumps(injects), json.dumps(edges)

    @classmethod
    def transform_stories_to_visjs_dict(cls, stories: List[BaseStory]):
        story_index = 0
        all_injects = []
        all_edges = []
        for story in stories:
            injects = [*story.injects.values()]
            new_injects, new_edges = \
                cls.transform_injects_to_visjs_dict(injects, group_id=story_index, entry_node=story.entry_node.slug)
            story_index += 1
            all_injects += [*new_injects]
            all_edges += [*new_edges]
        return all_injects, all_edges

    @classmethod
    def _transform_inject(cls, inject, group_id, level, entry_node=False):
        tmp_edges = []
        tmp_nodes = []
        tmp_id = inject.slug
        if group_id > 0:
            tmp_id += str(group_id)
        x = 200 * group_id
        y = level*-200
        tmp_inject = dict(id=tmp_id, label=inject.label, text=inject.text, group=group_id,
                          fixed={"x": True, "y": True}, x=x, y=y, level=level, slug=inject.slug)
        if inject.slug == entry_node:
            tmp_inject["is_entry_node"] = True
        tmp_nodes.append(tmp_inject)
        if inject.next_inject:
            tmp_edges = cls._transform_edges(inject, tmp_id, group_id)
        if inject.condition:
            condition_id = tmp_id+"_condition"
            condition_title = str(inject.condition)
            tmp_condition = dict(id=condition_id, label="condition", title=condition_title, group=group_id,
                                 level=level)
            tmp_condition_edge = {"from": condition_id, "to": tmp_id, "label": "triggers before"}
            tmp_result_edge = {"from": condition_id, "to": inject.condition.alternative_inject, "label": "leads to"}
            tmp_nodes.append(tmp_condition)
            tmp_edges.append(tmp_condition_edge)
            tmp_edges.append(tmp_result_edge)
        return tmp_nodes, tmp_edges


    @classmethod
    def _transform_edges(cls, inject, tmp_id, group_id):
        next_id = inject.next_inject
        if group_id > 0:
            next_id += str(group_id)
        edge_list = []
        edge_list.append({"from": tmp_id, "to": next_id, "label": "[default]"})
        if inject.has_choices:
            for choice in inject.choices:
                title = choice.label
                outcome = choice.outcome
                if outcome.next_inject:
                    next_id = choice.outcome.next_inject + str(group_id)
                if outcome.variable_changes:
                    title += " | ".join(choice.outcome.variable_changes)
                edge_list.append({"from": tmp_id, "to": next_id, "label": choice.label, "title": title})
        return edge_list

    @classmethod
    def transform_injects_to_visjs(cls, injects):
        injects, edges = cls.transform_injects_to_visjs_dict(injects)
        return json.dumps(injects), json.dumps(edges)
