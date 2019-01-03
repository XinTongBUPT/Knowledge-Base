from util import is_var

class Fact(object):
    """Represents a fact in our knowledge base. Has a statement containing the
        content of the fact, e.g. (isa Sorceress Wizard) and fields tracking
        which facts/rules in the KB it supports and is supported by.

    Attributes:
        name (str): 'fact', the name of this class
        statement (Statement): statement of this fact, basically what the fact actually says
        asserted (bool): boolean flag indicating if fact was asserted instead of
            inferred from other rules/facts in the KB
        supported_by (listof Fact|Rule): Facts/Rules that allow inference of
            the statement
        supports_facts (listof Fact): Facts that this fact supports
        supports_rules (listof Rule): Rules that this fact supports
    """
    def __init__(self, statement, supported_by=[]):
        """Constructor for Fact setting up useful flags and generating appropriate statement

        Args:
            statement (str|Statement): The statement of this fact, basically what the
                fact actually says
            supported_by (listof Fact|Rule): Facts/Rules that allow inference of
                the statement
        """
        super(Fact, self).__init__()
        self.name = "fact"
        self.statement = statement if isinstance(statement, Statement) else Statement(statement)
        self.asserted = not supported_by
        #self.supported_by = supported_by
        self.supported_by = []
        self.supports_facts = []
        self.supports_rules = []
        for pair in supported_by:
           self.supported_by.append(pair)

    def __repr__(self):
        """Define internal string representation
        """
        return 'Fact({!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
                self.name, self.statement,
                self.asserted, self.supported_by,
                self.supports_facts, self.supports_rules)

    def __str__(self):
        """Define external representation when printed
        """
        string = self.name + ":\n"
        string += "\t" + str(self.statement) + "\n"
        string += "\t Asserted:       " + str(self.asserted) + "\n"
        if self.supported_by != []:
            name_strings = [str(x.name) for y in self.supported_by for x in y]
            supported_by_str = ", ".join(name_strings)
            string += "\t Supported by:   [" + supported_by_str + "]\n"
        if self.supports_facts != []:
            name_strings = [str(x.name) for x in self.supports_facts]
            supports_f_str = ", ".join(name_strings)
            string += "\t Supports facts: [" + supports_f_str + "]\n"
        if self.supports_rules != []:
            name_strings = [str(x.name) for x in self.supports_rules]
            supports_r_str = ", ".join(name_strings)
            string += "\t Supports rules: [" + supports_r_str + "]\n"
        return string

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return isinstance(other, Fact) and self.statement == other.statement

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Rule(object):
    """Represents a rule in our knowledge base. Has a list of statements (the LHS)
        containing the statements that need to be in our KB for us to infer the
        RHS statement. Also has fields tracking which facts/rules in the KB it
        supports and is supported by.

    Attributes:
        name (str): 'rule', the name of this class
        lhs (listof Statement): LHS statements of this rule
        rhs (Statement): RHS statment of this rule
        asserted (bool): boolean flag indicating if rule was asserted instead of
            inferred from other rules/facts in the KB
        supported_by (listof Fact|Rule): Facts/Rules that allow inference of
            the statement
        supports_facts (listof Fact): Facts that this rule supports
        supports_rules (listof Rule): Rules that this rule supports
    """
    def __init__(self, rule, supported_by=[]):
        """Constructor for Rule setting up useful flags and generating appropriate LHS & RHS

        Args:
            rule (listof list): Raw representation of statements making up LHS and
                RHS of this rule
            supported_by (listof Fact|Rule): Facts/Rules that allow inference of
                the statement
        """
        super(Rule, self).__init__()
        self.name = "rule"
        self.lhs = [statement if isinstance(statement, Statement) else Statement(statement) for statement in rule[0]]
        self.rhs = rule[1] if isinstance(rule[1], Statement) else Statement(rule[1])
        self.asserted = not supported_by
        self.supported_by = []
        self.supports_facts = []
        self.supports_rules = []
        for pair in supported_by:
            self.supported_by.append(pair)

    def __repr__(self):
        """Define internal string representation
        """
        return 'Rule({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
                self.name, self.lhs, self.rhs,
                self.asserted, self.supported_by,
                self.supports_facts, self.supports_rules)

    def __str__(self):
        """Define external representation when printed
        """
        string = self.name + ":\n"
        string += "\t Left hand:\n"
        for statement in self.lhs:
            string += "\t\t" + str(statement) + "\n"
        string += "\t Right hand:\n\t\t" + str(self.rhs) + "\n"
        string += "\t Asserted:       " + str(self.asserted) + "\n"
        if self.supported_by != []:
            name_strings = [str(x.name) for y in self.supported_by for x in y ]
            supported_by_str = ", ".join(name_strings)
            string += "\t Supported by:   [" + supported_by_str + "]\n"
        if self.supports_facts != []:
            name_strings = [str(x.name) for x in self.supports_facts]
            supports_f_str = ", ".join(name_strings)
            string += "\t Supports facts: [" + supports_f_str + "]\n"
        if self.supports_rules != []:
            name_strings = [str(x.name) for x in self.supports_rules]
            supports_r_str = ", ".join(name_strings)
            string += "\t Supports rules: [" + supports_r_str + "]\n"
        return string

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        is_rule = isinstance(other, Rule)
        return is_rule and self.lhs == other.lhs and self.rhs == other.rhs

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Statement(object):
    """Represents a statement in our knowledge base, e.g. (attacked Ai Nosliw),
        (diamonds Loot), (isa Sorceress Wizard), etc. These statements show up
        in Facts or on the LHS and RHS of Rules

    Attributes:
        terms (listof Term): List of terms (Variable or Constant) in the
            statement, e.g. 'Nosliw' or '?d'
        predicate (str): The predicate of the statement, e.g. isa, hero, needs
    """
    def __init__(self, statement_list=[]):
        """Constructor for Statements with optional list of Statements that are
            converted to appropriate terms (and one predicate)

        Args:
            statement_list (mostly listof str|Term, first element is str): The element at
                index 0 is the predicate of the statement (a str) while the rest of
                the list is either instantiated Terms or strings to be passed to the
                Term constructor
        """
        super(Statement, self).__init__()
        self.terms = []
        self.predicate = ""

        if statement_list:
            self.predicate = statement_list[0]
            self.terms = [t if isinstance(t, Term) else Term(t) for t in statement_list[1:]]

    def __repr__(self):
        """Define internal string representation
        """
        return 'Statement({!r}, {!r})'.format(self.predicate, self.terms)

    def __str__(self):
        """Define external representation when printed
        """
        return "(" + self.predicate + " " + ' '.join((str(t) for t in self.terms)) + ")"

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        if self.predicate != other.predicate:
            return False

        for self_term, other_term in zip(self.terms, other.terms):
            if self_term != other_term:
                return False

        return True

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Term(object):
    """Represents a term (a Variable or Constant) in our knowledge base. Can
        sorta be thought of as a super class of Variable and Constant, though
        there is no inheritance implemented in the code.

    Attributes:
        term (Variable|Constant): The Variable or Constant that this term holds (represents)
    """
    def __init__(self, term):
        """Constructor for Term which converts term to appropriate form

        Args:
            term (Variable|Constant|string): Either an instantiated Variable or
                Constant, or a string to be passed to the appropriate constructor
        """
        super(Term, self).__init__()
        is_var_or_const = isinstance(term, Variable) or isinstance(term, Constant)
        self.term = term if is_var_or_const else (Variable(term) if is_var(term) else Constant(term))

    def __repr__(self):
        """Define internal string representation
        """
        return 'Term({!r})'.format(self.term)

    def __str__(self):
        """Define external representation when printed
        """
        return str(self.term)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return (self is other
            or isinstance(other, Term) and self.term.element == other.term.element
            or ((isinstance(other, Variable) or isinstance(other, Constant))
                and self.term.element == other.element))

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Variable(object):
    """Represents a variable used in statements

    Attributes:
        element (str): The name of the variable, e.g. '?x'
    """
    def __init__(self, element):
        """Constructor for Variable

        Args:
            element (str): The name of the variable, e.g. '?x'
        """
        super(Variable, self).__init__()
        self.element = element

    def __repr__(self):
        """Define internal string representation
        """
        return 'Variable({!r})'.format(self.element)

    def __str__(self):
        """Define external representation when printed
        """
        return str(self.element)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return (self is other
            or isinstance(other, Term) and self.term.element == other.term.element
            or ((isinstance(other, Variable) or isinstance(other, Constant))
                and self.term.element == other.element))

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Constant(object):
    """Represents a constant used in statements

    Attributes:
        element (str): The value of the constant, e.g. 'Nosliw'
    """
    def __init__(self, element):
        """Constructor for Constant

        Args:
            element (str): The value of the constant, e.g. 'Nosliw'
        """
        super(Constant, self).__init__()
        self.element = element

    def __repr__(self):
        """Define internal string representation
        """
        return 'Constant({!r})'.format(self.element)

    def __str__(self):
        """Define external representation when printed
        """
        return str(self.element)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return (self is other
            or isinstance(other, Term) and self.term.element == other.term.element
            or ((isinstance(other, Variable) or isinstance(other, Constant))
                and self.term.element == other.element))

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Binding(object):
    """Represents a binding of a constant to a variable, e.g. 'Nosliw' might be
        bound to'?d'

    Attributes:
        variable (Variable): The name of the variable associated with this binding
        constant (Constant): The value of the variable
    """
    def __init__(self, variable, constant):
        """Constructor for Binding

        Args:
            variable (Variable): The name of the variable associated with this binding
            constant (Constant): The value of the variable
        """
        super(Binding, self).__init__()
        self.variable = variable
        self.constant = constant

    def __repr__(self):
        """Define internal string representation
        """
        return 'Binding({!r}, {!r})'.format(self.variable, self.constant)

    def __str__(self):
        """Define external representation when printed
        """
        return self.variable.element.upper() + " : " + self.constant.element

class Bindings(object):
    """Represents Binding(s) used while matching two statements

    Attributes:
        bindings (listof Bindings): bindings involved in match
        bindings_dict (dictof Bindings): bindings involved in match where key is
            bound variable and value is bound value,
            e.g. some_bindings.bindings_dict['?d'] => 'Nosliw'
    """
    def __init__(self):
        """Constructor for Bindings creating initially empty instance
        """
        self.bindings = []
        self.bindings_dict = {}

    def __repr__(self):
        """Define internal string representation
        """
        return 'Bindings({!r}, {!r})'.format(self.bindings_dict, self.bindings)

    def __str__(self):
        """Define external representation when printed
        """
        if self.bindings == []:
            return "No bindings"
        return ", ".join((str(binding) for binding in self.bindings))

    def __getitem__(self,key):
        """Define behavior for indexing, e.g. random_bindings[key] returns
            random_bindings.bindings_dict[key] when the dictionary is not empty
            and the key exists, otherwise None
        """
        return (self.bindings_dict[key] 
                if (self.bindings_dict and key in self.bindings_dict)
                else None)

    def add_binding(self, variable, value):
        """Add a binding from a variable to a value

        Args:
            variable (Variable): the variable to bind to
            value (Constant): the value to bind to the variable
        """
        self.bindings_dict[variable.element] = value.element
        self.bindings.append(Binding(variable, value))

    def bound_to(self, variable):
        """Check if variable is bound. If so return value bound to it, else False.

        Args:
            variable (Variable): variable to check for binding

        Returns:
            Variable|Constant|False: returns bound term if variable is bound else False
        """
        if variable.element in self.bindings_dict.keys():
            value = self.bindings_dict[variable.element]
            if value:
                return Variable(value) if is_var(value) else Constant(value)

        return False

    def test_and_bind(self, variable_term, value_term):
        """Check if variable_term already bound. If so return whether or not passed
            in value_term matches bound value. If not, add binding between
            variable_terma and value_term and return True.

        Args:
            value_term (Term): value to maybe bind
            variable_term (Term): variable to maybe bind to
        
        Returns:
            bool: if variable bound returns whether or not bound value matches value_term,
                else True
        """
        bound = self.bound_to(variable_term.term)
        if bound:
            return value_term.term == bound
            
        self.add_binding(variable_term.term, value_term.term)
        return True


class ListOfBindings(object):
    """Container for multiple Bindings

        Attributes:
            list_of_bindings (listof Bindings): collects Bindings
    """
    def __init__(self):
        """Constructor for ListOfBindings
        """
        super(ListOfBindings, self).__init__()
        self.list_of_bindings = []

    def __repr__(self):
        """Define internal string representation
        """
        return 'ListOfBindings({!r})'.format(self.list_of_bindings)

    def __str__(self):
        """Define external representation when printed
        """
        string = ""
        for binding, associated_fact_rules in self.list_of_bindings:
            string += "Bindings for Facts and Rules: " + str(binding) + "\n"
            string += "Associated Facts and Rules: ["
            string += ", ".join((str(f) for f in associated_fact_rules)) + "]\n"
        return string

    def __len__(self):
        """Define behavior of len, when called on this class, 
            e.g. len(ListOfBindings([])) == 0
        """
        return len(self.list_of_bindings)

    def __getitem__(self,key):
        """Define behavior for indexing, e.g. random_list_of_bindings[i] returns
            random_list_of_bindings[i][0]
        """
        return self.list_of_bindings[key][0]

    def add_bindings(self, bindings, facts_rules=[]):
        """Add given bindings to list of Bindings along with associated rules or facts

            Args:            
                bindings (Bindings): bindings to add
                facts_rules (listof Fact|Rule): rules or facts associated with bindings

            Returns:
                Nothing
        """
        self.list_of_bindings.append((bindings, facts_rules))
