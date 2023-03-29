from typing import Type

from filtering_pkg.operators import AndOperator, BaseOperator, OrOperator, \
    NorOperator, NotOperator


class LogicalContext:
    body = None
    __allowed_logical_operators = {
        "$and": AndOperator,
        "$or": OrOperator,
        "$nor": NorOperator,
        "$not": NotOperator,
    }

    def __init__(self, body: dict):
        self.body = body

    def __iterate_over_body_slice(self, body_slice: list) -> list:
        result = []
        for index, elem in enumerate(body_slice):
            try:
                key = list(elem.keys())[0]
                if not self.__is_operator(key):
                    raise AttributeError
                if self.__if_slice_contains_operator(elem.get(key)):
                    self.__iterate_over_body_slice(
                        elem.get(key)
                    )
                # return logical operator with result of operation
                result = self.__execute_operator(key, elem.get(key))
                body_slice[index] = result
            except AttributeError:
                result = self.__execute_operator("$and", elem)
                body_slice[index] = result
        return result

    def __get_operator_class(self, name: str) -> Type[BaseOperator]:
        return self.__allowed_logical_operators.get(name)

    def exec(self) -> list:
        # start iteration over requested filter to find the deepest logical
        # operator
        list_to_iterate = [self.body]
        return self.__iterate_over_body_slice(list_to_iterate)

    def __if_slice_contains_operator(self, body_slice: list):
        # TODO test test test
        for elem in body_slice:
            keys = list(elem.keys())
            # if keys are logical operations
            if set(self.__allowed_logical_operators.keys()).intersection(set(keys)):
                return True
            if isinstance(elem.values(), list):
                return self.__if_slice_contains_operator(elem.values())
        return False

    def __execute_operator(self, operator_key, datas):
        operator_class_type = self.__get_operator_class(operator_key)
        return operator_class_type.exec(datas)

    def __is_operator(self, key):
        if key in self.__allowed_logical_operators.keys():
            return True
        return False

