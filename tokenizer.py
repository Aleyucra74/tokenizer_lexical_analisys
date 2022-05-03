import re
from traceback import print_tb
# Constantes
TESTE   = False

# caracteres usados em operadores
OPERADORES = "%*/+-!^="
OPERADORES_REGEX = r"[\%\*\/\+\-\!\^\=]"
# caracteres usados em números inteiros
DIGITOS = "0123456789"
DIGITOS_REGEX = r"[0-9]+"

# ponto decimal
PONTO = "."
PONTO_REGEX = r"\."

# todos os caracteres usados em um números float
FLOATS = DIGITOS + PONTO
FLOATS_REGEX = r"[0-9]+\.[0-9]+"

# caracteres usados em nomes de variáveis
LETRAS  = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETRAS_REGEX = r"[a-zA-Z0-9\_]+"

# abre e fecha parenteses
ABRE_FECHA_PARENTESES = "()"
ABRE_FECHA_PARENTESES_REGEX = r"[\(\)]"

# categorias
OPERADOR   = 1 # para operadores aritméticos e atribuição
NUMERO     = 2 # para números: todos são considerados float
VARIAVEL   = 3 # para variáveis
PARENTESES = 4 # para '(' e ')

# Whitespace characters: space, newline, horizontal tab,
# vertical tab, form feed, carriage return
BRANCOS    = [' ', '\n', '\t', '\v', '\f', '\r']
BRANCOS_REGEX = r"[\s\n\t\v\f\r]+"

# caractere que indica comentário
COMENTARIO = "#"
COMENTARIO_REGEX = r"[\#]"

regex_expressions = [
        ("OPERADOR",OPERADORES_REGEX),
        ("DIGITO",DIGITOS_REGEX),
        ("PONTO",PONTO_REGEX),
        ("FLOAT",FLOATS_REGEX),
        ("LETRAS",LETRAS_REGEX),
        ("PARENTESES",ABRE_FECHA_PARENTESES_REGEX)
        # ("BRANCOS", BRANCOS_REGEX)
        # ("COMENTARIO", COMENTARIO_REGEX)
    ]

regex_expression = '|'.join('(?P<%s>%s)' % op for op in regex_expressions)
token_regex = re.compile(regex_expression)
print(token_regex)
#------------------------------------------------------------
def tokeniza(exp):
    """(str) -> list
    Recebe uma string exp representando uma expressão e cria 
    e retorna uma lista com os itens léxicos que formam a
    expressão.
    Cada item léxico (= token) é da forma
        [item, tipo]
    O componente item de um token é 
        - um float: no caso do item ser um número; ou 
        - um string no caso do item ser um operador ou 
             uma variável ou um abre/fecha parenteses.
    O componente tipo de um token indica a sua categoria
    (ver definição de constantes acima). 
        - OPERADOR;
        - NUMERO; 
        - VARIAVEL; ou 
        - PARENTESES
    A funçao ignora tuo que esta na exp apos o caractere
    COMENTARIO (= "#").
    """
    # escreva o seu código abaixo
    posicao = 0
    tokenizado = []
    while True:
        if re.match(BRANCOS_REGEX, exp):
            exp = exp[1:]
        
        m = token_regex.match(exp)
        #no matches
        if not m: 
            break
        else:
            posicao = m.end()
            if m.lastgroup == 'LETRAS':
                tokname = VARIAVEL
                group_name = m.lastgroup
                tokvalue = m.group(group_name)
            elif m.lastgroup == 'OPERADOR':
                tokname = OPERADOR
                group_name = m.lastgroup
                tokvalue = m.group(group_name)
            elif m.lastgroup == 'DIGITO' or m.lastgroup == 'FLOAT' or m.lastgroup == 'PONTO':
                tokname = NUMERO
                group_name = m.lastgroup
                tokvalue = int(m.group(group_name))
            elif m.lastgroup == 'PARENTESES':
                tokname = PARENTESES
                group_name = m.lastgroup
                tokvalue = m.group(group_name)
            tokenizado.append([tokvalue, tokname])
            exp = exp[posicao:]
    if posicao == len(exp):
        print("ERRO")
    return tokenizado