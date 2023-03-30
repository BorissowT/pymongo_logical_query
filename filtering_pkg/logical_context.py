from typing import Type

from filtering_pkg.operators import AndOperator, BaseOperator, OrOperator, \
    NorOperator, NotOperator


class LogicalContext:
    """LogicalContext is responsible for parsing a filter query into separate
    logical operations

    :param body:  filter dictionary to parse
    :param __allowed_logical_operators: definition of Logical Operators

    """
    body: dict = None
    __allowed_logical_operators = {
        "$and": AndOperator,
        "$or": OrOperator,
        "$nor": NorOperator,
        "$not": NotOperator,
    }

    def __init__(self, body: dict):
        self.body = body

    def __iterate_over_body_slice(self, body_slice: list) -> list:
        """recursive iteration over filter body. Execute from the deepest
        operation up to the last element. Replace operations with results

        :param body_slice: body of operator to execute. Example
        {"$and":[{arg},{arg}]}. We extract value and key. Then pass them as args
        """
        result = []
        # start iteration
        for index, elem in enumerate(body_slice):
            try:
                # extract key
                key = list(elem.keys())[0]
                # if key is not an operator then execute it as $and operator
                # Example: {"author": "Elias"}
                if not self.__is_operator(key):
                    raise AttributeError
                # if slice contains child operations -> execute them and replace
                # with the result
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
        """returns class of Operator by key value

        :param name: key of operation
        :return: Type[BaseOperator] class of Operator
        """
        return self.__allowed_logical_operators.get(name)

    def exec(self) -> list:
        """entry point of every query. Put filter in list and pass as arg to
        iterative execution down to the deepest logical operations
        """
        list_to_iterate = [self.body]
        return self.__iterate_over_body_slice(list_to_iterate)

    def __if_slice_contains_operator(self, body_slice: list):
        """check if a given slice contains child operators

        :param body_slice: value of operation
        :return boolean: True if contains further logical operations
        """
        for elem in body_slice:
            keys = list(elem.keys())
            # if keys are logical operations
            if set(self.__allowed_logical_operators.keys()).intersection(
                    set(keys)):
                return True
            # use recursion to find out if child elements contain operators
            if isinstance(elem.values(), list):
                return self.__if_slice_contains_operator(elem.values())
        return False

    def __execute_operator(self, operator_key: str, filter_slice) -> list:
        """execute operator with given slice of filter

        :param operator_key: key of logical operator
        :param filter_slice: list or dictionary logical filter
        :return: list with result
        """
        operator_class_type = self.__get_operator_class(operator_key)
        return operator_class_type.execute(filter_slice)

    def __is_operator(self, key: str) -> bool:
        """ check if key is registered logical keyword

        :param key:
        :return: bool: True if key is operator. else False
        """
        if key in self.__allowed_logical_operators.keys():
            return True
        return False

