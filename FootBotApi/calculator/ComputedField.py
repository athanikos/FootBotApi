from enum import Enum


class ComputedField:

    def __init__(self, output_field_name, object_get, object_to_set, formulas):
        self.output_field_name = output_field_name
        self.object_get = object_get
        self.object_to_set = object_to_set
        self.formulas = formulas
        self.result = 0

    def compute(self):
        for cf in self.formulas:
            cf.compute()
            if cf.is_true:
                self.result = cf.result
                setattr(self.object_to_set, self.output_field_name, self.result)
                return


class ComputedFormula:
    def __init__(self, input_field_name_1, input_field_name_2,operator, true_result, false_result,
                 object_to_get):
        self.input_field_name_1 = input_field_name_1
        self.input_field_name_2 = input_field_name_2
        self.operator = operator
        self.true_result = true_result
        self.false_result = false_result
        self.object_to_get_values_from = object_to_get
        self.result = 0
        self.is_true = False

    def compute(self):
        input_field_1_value = getattr(self.object_to_get_values_from, self.input_field_name_1)
        input_field_2_value = getattr(self.object_to_get_values_from, self.input_field_name_2)
        expr = str(input_field_1_value) + self.operator.value + str(input_field_2_value)
        if eval(expr):
            self.result = self.true_result
            self.is_true = True
        else:
            self.result = self.false_result


class Operator(Enum):
    GREATER_THAN = '>'
    EQUAL = '=='
    LESS_THAN = '<'
