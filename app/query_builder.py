import operator
import re

AND_OPERATOR = '&'

# Operator mappings
OPERATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '=': operator.eq,
}

# Error which gets thrown if query is called with incorrect number of arguments
class QueryArgumentError(Exception):
    """ Base class for Errors in this module """
    pass

# Removes operators from string and splits
# returns list of operands
def operands(full_str):
    regex = '|'.join(list(OPERATORS.keys()) + [AND_OPERATOR])
    return list(map(lambda x: x.strip(), re.split(regex, full_str)))

# Finds operator to use based on string expression.
# String should only include a single operation.
# Returns function to use for operation
def find_operator(expr):
    for op in list(OPERATORS.keys()):
        if op in expr:
            return OPERATORS[op]

# Performs logical AND of multiple expressions
def logical_and(*args):
    result = True
    for arg in args:
        result = result and arg
    return result

# Builds Query given a string representation
# Returns a *function* which performs the desired comparisons (arguments must be given in the order they appeared)
def build_query(query):
    def build(*args):
        individual_ops = list(map(lambda x: find_operator(x), query.split(AND_OPERATOR)))   # array of functions

        # error checking
        if len(args) != 2 * len(individual_ops):
            raise QueryArgumentError('Incorrect Number of Arguments for this query')

        # evaluate above expression with given args
        individual_results = list(map(lambda i: individual_ops[i](args[2*i], args[2*i+1]), range(len(individual_ops))))
        return logical_and(*individual_results)
    return build
