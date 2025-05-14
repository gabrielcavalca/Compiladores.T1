from antlr4 import *
from LALexer import LALexer
import sys

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 analisador_lexico.py entrada.txt saida.txt")
        sys.exit(1)

    entrada_path = sys.argv[1]
    saida_path = sys.argv[2]

    try:
        input_stream = FileStream(entrada_path, encoding='utf-8')
        lexer = LALexer(input_stream)
        stream = CommonTokenStream(lexer)
        stream.fill()

        token_names = lexer.symbolicNames

        with open(saida_path, 'w', encoding='utf-8') as output_file:
            for token in stream.tokens:
                if token.type == Token.EOF:
                    continue

                try:
                    token_name = token_names[token.type]
                    token_text = token.text

                    if token_name == "PALAVRA_CHAVE":
                        output_file.write(f"<'{token_text}','{token_text}'>\n")
                    elif token_name == "IDENT":
                        output_file.write(f"<'{token_text}',IDENT>\n")
                    elif token_name == "CADEIA":
                        output_file.write(f"<'{token_text}',CADEIA>\n")
                    elif token_name == "NUM_INT":
                        output_file.write(f"<'{token_text}',NUM_INT>\n")
                    elif token_name == "NUM_REAL":
                        output_file.write(f"<'{token_text}',NUM_REAL>\n")
                    elif token_name == "ERRO":
                        output_file.write(f"Linha {token.line}: {token_text} - simbolo nao identificado\n")
                        break
                    elif token_name == "COMENTARIO_NAO_FECHADO":
                        output_file.write(f"Linha {token.line}: comentario nao fechado\n")
                        break
                    elif token_name == "CADEIA_NAO_FECHADA":
                        output_file.write(f"Linha {token.line}: cadeia literal nao fechada\n")
                        break
                    else:
                        output_file.write(f"<'{token_text}','{token_text}'>\n")

                except IndexError:
                    output_file.write(f"Token type {token.type} não encontrado na lista de símbolos\n")

    except Exception as e:
        print(f"Erro durante a análise: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
