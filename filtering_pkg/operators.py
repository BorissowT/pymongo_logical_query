from abc import ABCMeta, abstractmethod
from typing import Type

from filtering_pkg.condition_filters import *

data = [
    {"author": "Eliot", "title": "some", "rating": 54, "id": 1},
    {"author": "Eliot", "title": "some2", "rating": 30, "id": 2},
    {"author": "Eliot", "title": "some3", "rating": 12, "id": 3},
    {"author": "Eliot", "title": "some4", "rating": 11, "id": 4},
    {"author": "Eliot", "title": "some", "rating": 66, "id": 5},
    {"author": "David", "title": "some", "rating": 54, "id": 6},
    {"author": "David", "title": "some2", "rating": 30, "id": 7},
    {"author": "David", "title": "some3", "rating": 12, "id": 8},
    {"author": "David", "title": "some4", "rating": 11, "id": 9},
    {"author": "David", "title": "some", "rating": 66, "id": 10},
    {"author": "David", "title": "some", "rating": 76, "id": 13},
    {"author": "David", "title": "sometitle", "rating": 76, "id": 14},
    {"author": "Papi", "title": "some4", "rating": 10, "id": 15},
    {"author": "Papi2", "title": "some4", "rating": 100, "id": 16},
]


class IOperator(metaclass=ABCMeta):
    """interface for logical operations
    """
    @classmethod
    @abstractmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        """Logical operations are operations with lists. For example difference
        or intersection"""
        pass

    @abstractmethod
    def validate(self):
        """validate operation. Not implemented yet"""
        pass


class BaseOperator(IOperator):
    """base implementation of operators.

    __filter_conditions_list: registered operators
    """
    _filter_conditions_list: dict[str, Type[ConditionFilterBase]] = {
        "$eq": EqualConditionFilter,
        "$ne": NotEqualConditionFilter,
        "$gt": GreaterThanConditionFilter,
        "$gte": GreaterThanEqualConditionFilter,
        "$lt": LessThanConditionFilter,
        "$lte": LessThanEqualConditionFilter
    }

    @classmethod
    def execute(cls, body) -> list:
        """entrypoint of every operator. Body can be whether a dictionary with
        listed attributes to filter or a list with conditions

        :param body: dict or list with attributes to filter
        :return: a list with results
        """
        # example of filter {"author": "Eliot", "title":"some_title"}
        if isinstance(body, dict):
            return cls._execute_plain(body)
        else:
            return cls._execute_nested(body)

    @classmethod
    def _get_filter_class(cls, name: str) -> Type[ConditionFilterBase]:
        """returns filter class by name to execute

        :param name: name of filter
        :return: a class derived from ConditionFilterBase
        """
        return cls._filter_conditions_list.get(name)

    @classmethod
    def _remove_duplicates(cls, lists: list[dict]) -> list:
        """remove duplicates of dictionaries.

        :param lists: list of dictionaries
        :return: list without duplicates
        """
        return [dict(t) for t in {tuple(d.items()) for d in lists}]

    @classmethod
    def _call_operator_specific_method(cls, lists: list[list]) -> list:
        """

        :param lists: all condition filters are executed and passed as lists
        :return: resulted list
        """
        result = cls._remove_duplicates(
            cls.call_operator_specific_method_uncleaned(lists))
        return result

    @classmethod
    def _exec_with_conditions_plain(cls, body) -> list:
        """first we execute all filter conditions and replace their declarations
        with results. plain means there is no specific logical operation is 
        specified.
        
        :param body: dictionary of attributes to filter
        :return: list with results
        """
        # if there is no explicit declaration of condition filter, execute as
        # equal ($eq)
        if not cls._has_filter_condition(body):
            filter_condition_key = "$eq"
            filter_condition_value = list(body.values())[0]
        else:
            filter_condition_key = list(list(body.values())[0].keys())[0]
            filter_condition_value = list(list(body.values())[0].values())[0]

        filtered_attribute = list(body.keys())[0]
        filter_class_type = cls._get_filter_class(filter_condition_key)
        filter_class = filter_class_type(
            filtered_attribute,
            filter_condition_value,
        )
        result = list(filter(filter_class.execute, data))
        return result

    @classmethod
    def _exec_with_conditions_nested(cls, filter_body: list) -> list:
        """execute all condition filters and replace them with result. resulted
        list pass to operator function. Example:
        [{'rating': {'$gt': 65}}, {'id': {'$eq': 10}}]


        :param filter_body:
        :return: resulted list
        """
        condition_results = []
        for elem in filter_body:
            if not cls._has_filter_condition(elem):
                filter_condition_key = "$eq"
                filter_condition_value = list(elem.values())[0]
            else:
                filter_condition_key = list(list(elem.values())[0].keys())[0]
                filter_condition_value = list(list(elem.values())[0].values())[
                    0]

            filtered_attribute = list(elem.keys())[0]
            filter_class_type = cls._get_filter_class(filter_condition_key)
            filter_class = filter_class_type(
                filtered_attribute,
                filter_condition_value,
            )
            condition_results.append(
                list(filter(
                    filter_class.execute,
                    data
                ))
            )
        return cls._call_operator_specific_method(condition_results)

    @classmethod
    def _has_filter_condition(cls, body) -> bool:
        """checks recursively if there are any filter conditions. True if yes,
        else False

        :param body:
        :return:
        """
        if isinstance(body, dict):
            values = list(body.values())
            for elem in values:
                try:
                    keys = list(elem.keys())
                    allowed_keys = list(cls._filter_conditions_list.keys())
                    if set(keys) <= set(allowed_keys):
                        return True
                except AttributeError:
                    continue
        else:
            for elem in body:
                if cls._has_filter_condition(elem):
                    return True
        return False

    @classmethod
    def _execute_nested(cls, body: list) -> list:
        """execute nested filters. Example:
        [{'author': 'Eliot'}, {'title': 'some'}]
        [{'rating': {'$gt': 65}}, {'id': {'$eq': 10}}]

        :param body: list with filters
        :return: resulted list
        """
        if cls._has_filter_condition(body):
            # [{key: {"$condition": value}}...]
            return cls._exec_with_conditions_nested(body)
        else:
            # [{key:value, key:value},{key:value, key:value}...]
            return cls._exec_without_conditions_nested(body)

    @classmethod
    def _exec_without_conditions_nested(cls, body):
        """execute nested filters without condition filters. Example:
        [{'author': 'Eliot'}, {'title': 'some'}]

        :param body:
        :return:
        """
        lists = []
        for elem in body:
            # if filters in body aren't executed yet
            if isinstance(elem, dict):
                # TODO here not sure if element is the same logical operator
                lists.append(cls.execute(elem))
            # if filters in body already executed. -> concat results
            elif isinstance(elem, list):
                lists.append(elem)
        result = cls._call_operator_specific_method(lists)
        return result

    @classmethod
    def _execute_plain(cls, body: dict) -> list:
        """get elements which contain given attributes. plain means there is
         only one set to execute.

        :param body: dict contains attributes to find
        :return: result list
        """
        # here execute filter conditions
        if not cls._has_filter_condition(body):
            return [elem for elem in data if body.items() <= elem.items()]
        else:
            return cls._exec_with_conditions_plain(body)


class OrOperator(BaseOperator):

    @classmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        return cls._get_union(lists)

    def validate(self):
        pass

    @classmethod
    def _get_union(cls, lists):
        result = []
        for elem in lists:
            result = result + elem
        return result


class AndOperator(BaseOperator):
    @classmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        return cls._get_intersections(lists)

    def validate(self):
        pass

    @staticmethod
    def _get_intersections(lists):
        concat_list = []
        amount_of_searched_duplicates = len(lists)
        result = []
        for elem in lists:
            for d in elem:
                concat_list.append(d)
        for elem in concat_list:
            if concat_list.count(elem) == amount_of_searched_duplicates:
                result.append(elem)
                concat_list = list(filter(lambda a: a != elem, concat_list))
        return result


class NorOperator(BaseOperator):
    @classmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        return cls._get_exclusion(lists)

    def validate(self):
        pass

    @classmethod
    def _get_exclusion(cls, lists):
        concat_elems_to_exclude = []
        for elem in lists:
            concat_elems_to_exclude = concat_elems_to_exclude + elem
        result = [x for x in concat_elems_to_exclude + data if x not in
                  concat_elems_to_exclude or x not in data]
        return result


class NotOperator(NorOperator):
    pass
