import sys
import re

# Lista de palavras-chave da linguagem LA
KEYWORDS = {
    "algoritmo", "fim_algoritmo", "declare", "leia", "escreva",
    "literal", "inteiro", "real", "logico", "constante",
    "verdadeiro", "falso",
    "se", "entao", "senao", "fim_se",
    "caso", "seja", "fim_caso",
    "para", "ate", "faca", "fim_para",
    "enquanto", "fim_enquanto",
    "registro", "fim_registro",
    "tipo", "var",
    "procedimento", "funcao", "retorne", "fim_procedimento", "fim_funcao",
    # operadores lógicos que também são palavras-chave:
    "e", "ou", "nao"
}

# Expressões regulares para tokens
TOKEN_REGEX = [
    (r'\{[^\n]*\}', None),                  # Comentário em linha (ignorado)
    (r'"[^"\n]*"', "CADEIA"),               # Cadeia de caracteres
    (r'\d+\.\d+', "NUM_REAL"),              # Número real
    (r'\d+', "NUM_INT"),                    # Número inteiro
    (r'[a-zA-Z_]\w*', "IDENT_OR_KEYWORD"),  # Identificador ou palavra-chave

    # Operadores compostos — precisam vir antes!
    (r'<-|<=|>=|<>|!=|==|\.\.', "SYMBOL"),

    # Símbolos simples
    (r'[:(),.+\-*/=<>.^&%[\]]', "SYMBOL"),
]

# Ignorar espaços e tabulações
WHITESPACE = ' \t'

def tokenize_line(line, line_number):
    tokens = []
    i = 0
    line = line.rstrip('\n')

    # Linha com comentário isolado
    stripped_line = line.strip()
    if stripped_line.startswith('{') and stripped_line.endswith('}'):
        return [], None

    while i < len(line):
        ch = line[i]

        if ch in WHITESPACE:
            i += 1
            continue

        # Comentário no meio da linha
        if ch == '{':
            end = line.find('}', i)
            if end == -1:
                return None, f"Linha {line_number}: comentario nao fechado"
            i = end + 1
            continue

        if ch == '"':
            end = line.find('"', i + 1)
            if end == -1:
                return None, f"Linha {line_number}: cadeia de caracteres nao fechada"
            lexeme = line[i:end + 1]
            tokens.append((lexeme, "CADEIA"))
            i = end + 1
            continue

        match = None
        for regex, token_type in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(line, i)
            if match:
                lexeme = match.group()
                if token_type == "IDENT_OR_KEYWORD":
                    token_type = lexeme if lexeme in KEYWORDS else "IDENT"
                elif token_type == "SYMBOL":
                    token_type = lexeme
                tokens.append((lexeme, token_type))
                i = match.end()
                break

        if not match:
            # Se o símbolo não for reconhecido, reporta o erro apenas para o símbolo atual
            return tokens, f"Linha {line_number}: {ch} - simbolo nao identificado"

    return tokens, None


def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    entrada_path = sys.argv[1]
    saida_path = sys.argv[2]

    try:
        with open(entrada_path, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        sys.exit(1)

    saida = []
    for num_linha, linha in enumerate(linhas, 1):
        tokens, erro = tokenize_line(linha, num_linha)
        if erro:
            for lexema, tipo in tokens:
                if tipo.isupper():  # Se o tipo for maiúsculo, não coloca aspas
                    saida.append(f"<'{lexema}',{tipo}>\n")
                else:  # Se o tipo for minúsculo, coloca aspas
                    saida.append(f"<'{lexema}','{tipo}'>\n")
            saida.append(f"{erro}\n")
            break
        for lexema, tipo in tokens:
            if tipo.isupper():  # Se o tipo for maiúsculo, não coloca aspas
                saida.append(f"<'{lexema}',{tipo}>\n")
            else:  # Se o tipo for minúsculo, coloca aspas
                saida.append(f"<'{lexema}','{tipo}'>\n")

    with open(saida_path, 'w', encoding='utf-8') as f_out:
        f_out.writelines(saida)

if __name__ == "__main__":
    main()
