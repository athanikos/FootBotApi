from enum import Enum


class ComputedField:

    def __init__(self, output_field_name, object_to_get, formulas ):
        self.output_field_name = output_field_name
        self.object_to_get = object_to_get
        self.formulas = formulas
        self.result = 0

    def compute(self):
        for cf in ComputedFormula:
            cf.compute()
            if cf.isTrue:
                self.result = cf.result
                break


class ComputedFormula:
    def __init__(self, input_field_name_1, input_field_name_2,operator, true_result, false_result,
                 object_to_get_values_from):
        self.input_field_name_1 = input_field_name_1
        self.input_field_name_2 = input_field_name_2
        self.operator = operator
        self.true_result = true_result
        self.false_result = false_result
        self.object_to_get_values_from = object_to_get_values_from
        self.result = 0
        self.isTrue = False

    def compute(self):
        input_field_1_value = getattr(self.object_to_get_values_from, self.input_field_name_1)
        input_field_2_value = getattr(self.object_to_get_values_from, self.input_field_name_2)
        expr = str(input_field_1_value) + self.operator.value + str(input_field_2_value)
        if eval(expr):
            self.result = self.true_result
            self.isTrue = True
        else:
            self.result = self.false_result


class Operator(Enum):
    GREATER_THAN = '>'
    EQUAL = '='
    LESS_THAN = '<'
