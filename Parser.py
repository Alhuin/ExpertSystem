from ply import lex, yacc


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Tokens list
    tokens = (
        'ATOM',
        'LPAREN',
        'RPAREN',
        'AND',
        'OR',
        'XOR',
        'IMP',
        'IOI',
        'NOT',
        'QUERIES',
        'FACTS',
    )

    # Lowest to highest precedence
    precedence = (
        ('left', 'XOR'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
    )

    # Regular expression rules for simple tokens
    t_NOT = r'!'
    t_ATOM = r'[A-Z]'
    t_AND = r'\+'
    t_OR = r'\|'
    t_XOR = r'\^'
    t_IOI = r'<=>'
    t_IMP = r'=>'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_QUERIES = r'^\?' + t_ATOM + r'*'
    t_FACTS = r'^\=' + t_ATOM + r'*'

    # Ignored characters
    t_ignore = ' \t\n'

    # ignored lines
    def t_comment(self, t):
        r'\#.*'
        pass

    # Error handling
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


class Parser:
    def __init__(self, lines):
        self.lines = list(lines)
        self.rules = list()
        self.facts = list()
        self.queries = list()
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)

    tokens = Lexer.tokens
    precedence = Lexer.precedence

    # Grammar rules for parsing

    def p_syntaxError(self, p):
        """expression   : ATOM ATOM"""

        self.p_error("")
        raise SyntaxError

    def p_not(self, p):
        """expression   : NOT expression
                        | NOT LPAREN expression RPAREN"""

        if len(p) == 3:
            p[0] = ('not', p[2])
        else:
            p[0] = ('not', p[3])

    def p_rule(self, p):
        """expression   : expression IMP expression
                        | expression IOI expression"""
        p[0] = ('rule', p[1], p[2], p[3])

    def p_operation(self, p):
        """expression   : expression AND expression
                        | expression OR expression
                        | expression XOR expression"""
        p[0] = ('operation', p[1], p[2], p[3])

    def p_parenthesis(self, p):
        """expression   : LPAREN expression RPAREN"""
        p[0] = ('parenthesis', p[2])

    def p_queries(self, p):
        """expression   : QUERIES"""
        p[0] = ('queries', p[1])

    def p_facts(self, p):
        """expression   : FACTS"""
        p[0] = ('facts', p[1])

    def p_atom(self, p):
        """expression   : ATOM"""
        p[0] = ('atom', p[1])

    def p_error(self, p):
        if p is not None:
            if isinstance(p, str):
                print(f"SyntaxError")
                exit(0)
            else:
                print("Position %s, illegal token %s" % (p.lexpos, p.value))

    def run(self):
        for line in self.lines:
            result = self.parser.parse(line)
            # print(result)
            if result is None:
                error_line = line.replace(' ', '').replace('\n', '').replace('\t', '')
                if len(error_line) != 0 and error_line[0] != '#':
                    print(f'SyntaxError : line "{line}" not well formated')
                    exit(0)
            else:
                # print(result)
                if result[0] == 'rule':
                    split = line.replace('\n', '').replace(' ', '').replace('<', '').split('=>')
                    knowledge_str = split[1]
                    if knowledge_str[:2] == '!(' and knowledge_str[-1] == ')':
                        knowledge_str = knowledge_str[1:-1]
                    rule_str = split[0]
                    self.rules.append([rule_str, knowledge_str, result[1], result[2], result[3]])
                elif result[0] == 'queries':
                    for char in result[1][1:]:
                        self.queries.append(char)
                elif result[0] == 'facts':
                    for char in result[1][1:]:
                        self.facts.append(char)
                else:
                    print(f"SyntaxError : {result} is not a rule, not a fact and not a query declaration")
                    exit(0)
        if len(self.rules) == 0:
            print("Error : no rules found")

    def print(self):
        print("\nFacts :")
        for fact in self.facts:
            print(fact)
        print("\nQueries :")
        for query in self.queries:
            print(query)
        print("\nRules :")
        for rule in self.rules:
            print(rule)
