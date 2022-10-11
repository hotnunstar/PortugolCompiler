# logic_grammar.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

import ply.yacc as pyacc
from pprint import PrettyPrinter
from logic_eval import LogicEval
from logic_eval_c import LogicEvalC
from logic_lexer import LogicLexer


class LogicGrammar:
    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "uminus"),
        ("left", "ou", "xou"),
        ("left", "dif"),
        ("left", "eq"),
        ("left", "maieq"),
        ("left", "meneq"),
        ("left", "e"),
        ("left", "<"),
        ("left", ">"),
    )

    # region P_ERROR
    def p_error(self, p):
        if p:
            raise Exception(f"Parse Error: Unexpected token '{p.type}'")
        else:
            raise Exception("Parse Error: Expecting token")
    # endregion

    # region PORT GRAMMAR
    def p_port1(self, p):
        """ port : Inicio code Fim """
        p[0] = p[2]

    def p_port2(self, p):
        """ port : fun Inicio code Fim """
        p[0] = [p[1]] + p[3]
    # endregion

    # region CODE GRAMMAR
    def p_code1(self, p):
        """ code : com """
        p[0] = [p[1]]

    def p_code2(self, p):
        """ code : code com """
        p[0] = p[1] + [p[2]]
    # endregion

    # region FUN GRAMMAR
    def p_fun1(self, p):
        """ fun : funcao varType varName '(' vars ')' ':' code fim_funcao """
        p[0] = {"op": "fun", "args": [], "data": [p[2], p[3], p[5], p[8]]}

    def p_fun2(self, p):
        """ fun : funcao void varName '(' vars ')' ':' code fim_funcao """
        p[0] = {"op": "fun", "args": [], "data": [p[2], p[3], p[5], p[8]]}
    # endregion

    # region VARS GRAMMAR
    def p_vars1(self, p):
        """ vars : """
        p[0] = []

    def p_vars2(self, p):
        """ vars : varType varName
                 | vars ',' varType varName """
        if len(p) == 3:
            p[0] = {p[1]: p[2]}
        else:
            p[0] = p[1], {p[3]: p[4]}
    # endregion

    # region COM GRAMMAR
    def p_com1(self, p):
        """ com : lines
                | cond
                | cycle """
        p[0] = p[1]
    # endregion

    # region LINES GRAMMAR
    def p_lines1(self, p):
        """ lines : varName assign value ';' """
        p[0] = {"op": "assign", "args": [p[1], p[3]]}

    def p_lines2(self, p):
        """ lines : varType ':' varName_list ';' """
        p[0] = {p[1]: p[3]}

    def p_lines3(self, p):
        """ lines : escreva value_list ';' """
        p[0] = {"op": "escreva", "args": p[2]}

    def p_lines4(self, p):
        """ lines : leia value_list ';' """
        p[0] = {"funct": "leia", "args": p[2]}

    def p_lines5(self, p):
        """ lines : retorna value ';' """
        p[0] = p[2]
    # endregion

    # region COND GRAMMAR
    def p_cond1(self, p):
        """ cond : se value entao code fim_se """
        p[0] = {"op": "if", "args": [p[2]], "data": [p[4]]}

    def p_cond2(self, p):
        """ cond : se value entao code senao code fim_se """
        p[0] = {"op": "if_else", "args": [p[2]], "data": [p[4], p[6]]}
    # endregion

    # region CYCLE GRAMMAR
    def p_cycle1(self, p):
        """ cycle : para varName de value ate value passo value faca code fim_para """
        p[0] = {"op": "for", "args": [p[2], p[4], p[6], p[8]], "data": [p[10]]}

    def p_cycle2(self, p):
        """ cycle : enquanto value_list faca code fim_enquanto"""
        p[0] = {"funct": "while", "args": p[2], "data": [p[4]]}

    def p_cycle3(self, p):
        """ cycle : faca code enquanto value_list fim_enquanto"""
        p[0] = {"funct": "until_while", "args": p[4], "data": [p[2]]}
    # endregion

    # region VALUE GRAMMAR
    def p_value1(self, p):
        """ value : varName """
        p[0] = {'varName': p[1]}

    def p_value2(self, p):
        """ value : bool
                  | calc
                  | string """
        p[0] = p[1]

    def p_value3(self, p):
        """ value : varName '(' value_list ')'
                  | varName '(' ')' """
        p[0] = {"op": "call",
                "args": [],
                "data": [p[1], [] if p[3] == ")" else p[3]]}
    # endregion

    # region VARTYPE GRAMMAR
    def p_varType1(self, p):
        """ varType : inteiro
                    | real
                    | carater
                    | logico """
        p[0] = p[1]
    # endregion

    # region VARNAME_LIST GRAMMAR
    def p_varName_list1(self, p):
        """ varName_list : varName
                         | varName_list ',' varName """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    # endregion

    # region VALUE_LIST GRAMMAR
    def p_value_list1(self, p):
        """ value_list : value
                       | value_list ',' value """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_value_list2(self, p):
        """ value_list : '(' value_list ')' """
        p[0] = p[2]
    # endregion

    # region BOOL GRAMMAR
    def p_bool1(self, p):
        """ bool : opt
                 | value e value
                 | value ou value
                 | value xou value """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = dict(op=p[2], args=[p[1], p[3]])
    # endregion

    # region CALC GRAMMAR
    def p_calc1(self, p):
        """ calc : int
                 | float
                 | '-' value  %prec uminus  """
        p[0] = p[1] if len(p) == 2 else {"op": "-", "args": [0.0, p[2]]}

    def p_calc2(self, p):
        """ calc : value '+' value
                 | value '-' value
                 | value '*' value
                 | value '/' value
                 | value '<' value
                 | value '>' value
                 | value dif value
                 | value eq value
                 | value maieq value
                 | value meneq value """
        p[0] = dict(op=p[2], args=[p[1], p[3]])
    # endregion

    # region OPT GRAMMAR
    def p_opt1(self, p):
        """ opt : verdadeiro """
        p[0] = True

    def p_opt2(self, p):
        """ opt : falso """
        p[0] = False

    def p_opt3(self, p):
        """ opt : nao opt """
        p[0] = dict(op='nao', args=[p[2]])
    # endregion

    def __init__(self):
        self.lexer = LogicLexer()
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self)

    def parse(self, expression):
        ans = self.yacc.parse(lexer=self.lexer.lex, input=expression)
        pp = PrettyPrinter()
        pp.pprint(ans)  # debug rulez!
        print("\n\n\t## EXECUÇÃO DO CÓDIGO ##\n")
        return LogicEval.eval(ans)

    def parse_c(self, expression):
        ans = self.yacc.parse(lexer=self.lexer.lex, input=expression)
        pp = PrettyPrinter()
        pp.pprint(ans)  # debug rulez
        print("\n\n\t## CONVERSÃO EM C ##\n")
        print("\nint main ()\n{")
        LogicEvalC.eval(ans)
        print("}")


