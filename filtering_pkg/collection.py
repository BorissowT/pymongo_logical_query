from filtering_pkg.logical_context import LogicalContext


class Collection:
    """Collection is a data entity representation.

    :param lc: LogicalContext object is next layer that executes a filter
    argument
    """
    lc: LogicalContext = None

    def find_one(self, filter_arg: dict) -> dict:
        """find one method returns first element of filter operation

        :param filter_arg: a dictionary representing a logical query
        :return: first element of executed query
        """
        self.lc = self.__setup_context(filter_arg)

        found_data = self.lc.exec()
        return found_data[0] if found_data else None

    def find(self, filter_arg: dict) -> list:
        """find function returns list of object after filter query is executed

        :param filter_arg: a dictionary representing a logical query
        :return: result of executed query
        """
        self.lc = self.__setup_context(filter_arg)

        found_data = self.lc.exec()
        return found_data if found_data else None

    def __setup_context(self, filter_arg: dict) -> LogicalContext:
        """initiates a new logical context for a new query

        :param filter_arg: pass filter query to logical context
        :return: LogicalContext instance
        """
        self.lc = LogicalContext(body=filter_arg)
        return self.lc
