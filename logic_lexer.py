# logic_lexer.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

import ply.lex as plex


class LogicLexer:
    varTypes = ("inteiro", "real", "carater", "logico")
    logic = ("verdadeiro", "falso", "e", "ou", "xou")
    conditions = ("se", "fim_se")
    cycles = ("enquanto", "fim_enquanto", "para", "de", "passo", "fim_para")
    other = ("Inicio", "Fim", "escreva", "leia", "retorna", "void")
    keywords = varTypes + logic + conditions + cycles + other
    tokens = keywords + ("funcao", "fim_funcao", "nao", "senao", "entao", "ate", "faca", "dif", "eq", "maieq", "meneq",
                         "varName", "int", "float", "string", "assign")
    literals = "<>()+-/*;[],:="
    t_ignore = " \t\n"

    def t_funcao(self, t):
        r"""função"""
        return t

    def t_fim_funcao(self, t):
        r"""fim_função"""
        return t

    def t_nao(self, t):
        r"""não"""
        return t

    def t_senao(self, t):
        r"""senão"""
        return t

    def t_entao(self, t):
        r"""então"""
        return t

    def t_ate(self, t):
        r"""até"""
        return t

    def t_faca(self, t):
        r"""faça"""
        return t

    def t_dif(self, t):
        r"""!="""
        return t

    def t_eq(self, t):
        r"""=="""
        return t

    def t_maieq(self, t):
        r""">="""
        return t

    def t_meneq(self, t):
        r"""<="""
        return t

    def t_float(self, t):
        r"""[0-9]+\.[0-9]+"""
        t.value = float(t.value)
        return t

    def t_int(self, t):
        r"""[0-9]+"""
        t.value = int(t.value)
        return t

    def t_string(self, t):
        r'"[^"]*"'
        #t.value = t.value[1:-1]
        return t

    def t_assign(self, t):
        r"""<-"""
        return t

    def t_keywords(self, t):
        r"""[\w]+"""
        t.type = t.value if t.value in self.keywords else "varName"
        return t

    def t_error(self, t):
        raise Exception(f"Unexpected token {t.value[:10]}")

    def __init__(self):
        self.lex = plex.lex(module=self)

    def token(self):
        return self.lex.token()
