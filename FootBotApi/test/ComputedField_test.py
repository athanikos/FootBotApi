from FootBotApi.calculator.ComputedField import ComputedField, ComputedFormula,Operator

class testObject(object):
    a = 10
    b = 2

def test_compute():
    to = testObject()
    cf = ComputedFormula('a','b',Operator.GREATER_THAN,1,0,to)
    cf.compute()
    b = eval('1 > 0 ')
    assert b == 1
    assert  cf.result == 1
    cf1 = ComputedFormula('a','b',Operator.EQUAL,33,0,to)
    cf2 = ComputedFormula('a','b',Operator.GREATER_THAN,66,0,to)
    formulas = [cf1,cf2]
    field = ComputedField(  'test', to, formulas )
    field.compute()
    assert  field.result == 66
    assert to.test == 66
