from abc import ABCMeta, abstractmethod

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
    @classmethod
    @abstractmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        pass

    @abstractmethod
    def validate(self):
        pass


class BaseOperator(IOperator):
    __filter_conditions_list: dict[str, ConditionFilterBase] = {
        "$eq": EqualConditionFilter,
        "$ne": NotEqualConditionFilter,
        "$gt": GreaterThanConditionFilter,
        "$gte": GreaterThanEqualConditionFilter,
        "$lt": LessThanConditionFilter,
        "$lte": LessThanEqualConditionFilter
    }

    @classmethod
    def exec(cls, body) -> list:
        # example of filter {"author": "Eliot", "title":"some_title"}
        if isinstance(body, dict):
            return cls.__execute_plain(body)
        else:
            return cls.__execute_nested(body)

    @classmethod
    def __get_filter_class(cls, name: str) -> ConditionFilterBase:
        return cls.__filter_conditions_list.get(name)

    @classmethod
    def __remove_duplicates(cls, lists):
        return [dict(t) for t in {tuple(d.items()) for d in lists}]

    @classmethod
    def __call_operator_specific_method(cls, lists):
        result = cls.__remove_duplicates(
            cls.call_operator_specific_method_uncleaned(lists))
        return result

    @classmethod
    def __exec_with_conditions_plain(cls, elem):
        if not cls.__has_filter_condition(elem):
            filter_condition_key = "$eq"
            filter_condition_value = list(elem.values())[0]
        else:
            filter_condition_key = list(list(elem.values())[0].keys())[0]
            filter_condition_value = list(list(elem.values())[0].values())[0]

        filtered_attribute = list(elem.keys())[0]
        filter_class_type = cls.__get_filter_class(filter_condition_key)
        filter_class = filter_class_type(
            filtered_attribute,
            filter_condition_value,
        )
        result = list(filter(filter_class.execute, data))
        return result

    @classmethod
    def __exec_with_conditions_nested(cls, filter_body):
        condition_results = []
        for elem in filter_body:
            if not cls.__has_filter_condition(elem):
                filter_condition_key = "$eq"
                filter_condition_value = list(elem.values())[0]
            else:
                filter_condition_key = list(list(elem.values())[0].keys())[0]
                filter_condition_value = list(list(elem.values())[0].values())[
                    0]

            filtered_attribute = list(elem.keys())[0]
            filter_class_type = cls.__get_filter_class(filter_condition_key)
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
        return cls.__call_operator_specific_method(condition_results)

    @classmethod
    def __exec_with_filter_conditions(cls, filter_body):
        if isinstance(filter_body, dict):
            return cls.__exec_with_conditions_plain(filter_body)
        else:
            return cls.__exec_with_conditions_nested(filter_body)

    @classmethod
    def __has_filter_condition(cls, body) -> bool:
        if isinstance(body, dict):
            values = list(body.values())
            for elem in values:
                try:
                    keys = list(elem.keys())
                    allowed_keys = list(cls.__filter_conditions_list.keys())
                    if set(keys) <= set(allowed_keys):
                        return True
                except AttributeError:
                    continue
        else:
            for elem in body:
                if cls.__has_filter_condition(elem):
                    return True

    @classmethod
    def __execute_nested(cls, body):
        if cls.__has_filter_condition(body):
            # [{key: {"$condition": value}}...]
            return cls.__exec_with_filter_conditions(body)
        else:
            # [{key:value, key:value},{key:value, key:value}...]
            return cls.__exec_without_conditions(body)

    @classmethod
    def __exec_without_conditions(cls, body):
        lists = []
        for elem in body:
            # if filters in body aren't executed yet
            if isinstance(elem, dict):
                lists.append(cls.__execute_plain(elem))
            # if filters in body already executed. -> concat results
            elif isinstance(elem, list):
                lists.append(elem)
        result = cls.__call_operator_specific_method(lists)
        return result

    @classmethod
    def __execute_plain(cls, body):
        # get elements which contain given attributes
        if not cls.__has_filter_condition(body):
            return [elem for elem in data if body.items() <= elem.items()]
        else:
            return cls.__exec_with_filter_conditions(body)


class OrOperator(BaseOperator):

    @classmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        return cls.__get_union(lists)

    def validate(self):
        pass

    @classmethod
    def __get_union(cls, lists):
        result = []
        for elem in lists:
            result = result + elem
        return result


class AndOperator(BaseOperator):
    @classmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        return cls.__get_intersections(lists)

    def validate(self):
        pass

    @staticmethod
    def __get_intersections(lists):
        result = []
        for elem in lists:
            lists.remove(elem)
            for dct in elem:
                for elem in lists:
                    if dct in elem:
                        result.append(dct)
        return result


class NorOperator(BaseOperator):
    @classmethod
    def call_operator_specific_method_uncleaned(cls, lists):
        return cls.__get_exclusion(lists)

    def validate(self):
        pass

    @classmethod
    def __get_exclusion(cls, lists):
        concat_elems_to_exclude = []
        for elem in lists:
            concat_elems_to_exclude = concat_elems_to_exclude + elem
        result = [x for x in concat_elems_to_exclude + data if x not in
                  concat_elems_to_exclude or x not in data]
        return result


class NotOperator(NorOperator):
    pass
