import operator

AND_OPERATOR = '&'

# Operator mappings
OPERATORS = {
    '-gt': operator.gt,
    '-lt': operator.lt,
    '-eq': operator.eq,
    AND_OPERATOR: operator.and_
}

# Finds operator to use based on string expression.
# String should only include a single operation.
# Returns function to use for operation
def find_operator(expr):
    for op in list(OPERATORS.keys()):
        if op in expr:
            return OPERATORS[op]


# Builds Query given a string representation
def build_query(query):
    return find_operator(query)