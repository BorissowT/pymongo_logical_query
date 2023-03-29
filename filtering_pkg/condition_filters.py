from abc import ABCMeta, abstractmethod


class ConditionFilterBase(metaclass=ABCMeta):
    name = None
    attribute = None

    def __init__(self, attribute, expected_value):
        self.expected_value = expected_value
        self.attribute = attribute

    @abstractmethod
    def execute(self, to_compare):
        pass


class NotEqualConditionFilter(ConditionFilterBase):
    name = "$ne"

    def execute(self,  to_compare):
        if self.attribute in to_compare:
            return to_compare.get(self.attribute) != self.expected_value
        else:
            return False


class EqualConditionFilter(ConditionFilterBase):
    name = "$eq"

    def execute(self,  to_compare):
        if self.attribute in to_compare:
            return to_compare.get(self.attribute) == self.expected_value
        else:
            return False


class GreaterThanConditionFilter(ConditionFilterBase):
    name = "$gt "

    def execute(self, to_compare):
        if self.attribute in to_compare:
            return to_compare.get(self.attribute) > self.expected_value
        else:
            return False


class GreaterThanEqualConditionFilter(ConditionFilterBase):
    name = "$gte"

    def execute(self, to_compare):
        if self.attribute in to_compare:
            return to_compare.get(self.attribute) >= self.expected_value
        else:
            return False


class LessThanConditionFilter(ConditionFilterBase):
    name = "$lt"

    def execute(self, to_compare):
        if self.attribute in to_compare:
            return to_compare.get(self.attribute) < self.expected_value
        else:
            return False


class LessThanEqualConditionFilter(ConditionFilterBase):
    name = "$lte"

    def execute(self, to_compare):
        if self.attribute in to_compare:
            return to_compare.get(self.attribute) <= self.expected_value
        else:
            return False
