import logical_classes as lc

def is_var(var):
    """Check whether an element is a variable (either instance of Variable, 
        instance of Term (where .term is a Variable) or a string starting with 
        `'?'`, e.g. `'?d'`)

    Args:
        var (any): value to check

    Returns:
        bool
    """
    if type(var) == str:
        return var[0] == "?"
    if isinstance(var, lc.Term):
        return isinstance(var.term, lc.Variable)

    return isinstance(var, lc.Variable)

def match(state1, state2, bindings=None):
    """Match two statements and return the associated bindings or False if there
        is no binding

    Args:
        state1 (Statement): statement to match with state2
        state2 (Statement): statement to match with state1
        bindings (Bindings|None): already associated bindings

    Returns:
        Bindings|False: either associated bindings or no match found
    """
    if len(state1.terms) != len(state2.terms) or state1.predicate != state2.predicate:
        return False
    if not bindings:
        bindings = lc.Bindings()
    return match_recursive(state1.terms, state2.terms, bindings)

def match_recursive(terms1, terms2, bindings):  # recursive...
    """Recursive helper for match

    Args:
        terms1 (listof Term): terms to match with terms2
        terms2 (listof Term): terms to match with terms1
        bindings (Bindings): already associated bindings

    Returns:
        Bindings|False: either associated bindings or no match found
    """
    if len(terms1) == 0:
        return bindings
    if is_var(terms1[0]):
        if not bindings.test_and_bind(terms1[0], terms2[0]):
            return False
    elif is_var(terms2[0]):
        if not bindings.test_and_bind(terms2[0], terms1[0]):
            return False
    elif terms1[0] != terms2[0]:
        return False
    return match_recursive(terms1[1:], terms2[1:], bindings)

def instantiate(statement, bindings):
    """Generate Statement from given statement and bindings. Constructed statement
        has bound values for variables if they exist in bindings.

    Args:
        statement (Statement): statement to generate new statement from
        bindings (Bindings): bindings to substitute into statement
    """
    def handle_term(term):
        if is_var(term):
            bound_value = bindings.bound_to(term.term)
            return lc.Term(bound_value) if bound_value else term
        else:
            return term

    new_terms = [handle_term(t) for t in statement.terms]
    return lc.Statement([statement.predicate] + new_terms)

def factq(element):
    """Check if element is a fact

    Args:
        element (any): element to check

    Returns:
        bool
    """
    return isinstance(element, lc.Fact)

def printv(message, level, verbose, data=[]):
    """Prints given message formatted with data if passed in verbose flag is greater than level

    Args:
        message (str): message to print, if format string data should have values
            to format with
        level (int): value of verbose required to print
        verbose (int): value of verbose flag
        data (listof any): optional data to format message with
    """
    if verbose > level:
        print(message.format(*data) if data else message)