from filtering_pkg.logical_context import LogicalContext


class ICollection:
    lc: LogicalContext = None

    def find_one(self, filter_arg: dict) -> dict:
        self.lc = self.__setup_context(filter_arg)

        found_data = self.lc.exec()
        return found_data[0] if found_data else None

    def find(self, filter_arg: dict) -> list:
        self.lc = self.__setup_context(filter_arg)

        found_data = self.lc.exec()
        return found_data if found_data else None

    def __setup_context(self, filter_arg: dict):
        self.lc = LogicalContext(body=filter_arg)
        return self.lc
