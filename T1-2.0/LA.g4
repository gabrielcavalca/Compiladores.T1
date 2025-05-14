grammar LA;

// Lexer

// Palavras-chave
PALAVRA_CHAVE :
    'algoritmo' | 'fim_algoritmo' | 'declare' | 'leia' | 'escreva'
    | 'literal' | 'inteiro' | 'real' | 'logico' | 'constante'
    | 'verdadeiro' | 'falso' | 'se' | 'entao' | 'senao' | 'fim_se'
    | 'caso' | 'seja' | 'fim_caso' | 'para' | 'ate' | 'faca' | 'fim_para'
    | 'enquanto' | 'fim_enquanto' | 'registro' | 'fim_registro' | 'tipo'
    | 'procedimento' | 'fim_procedimento' | 'funcao' | 'fim_funcao'
    | 'retorne' | 'var' | 'e' | 'ou' | 'nao';

// Literais
NUM_INT : [0-9]+ ;
NUM_REAL : [0-9]+ '.' [0-9]+ ;

CADEIA_NAO_FECHADA : '"' (~["\n])* ('\n'|EOF);
CADEIA : '"' (~["\n\r] | '""')* '"' ;

// Comentários

COMENTARIO : '{' ~[}\n]* '}' -> skip ;  
COMENTARIO_NAO_FECHADO : '{' ~[}\n]* ('\n'|EOF) ; 

// Espaços em branco
WS : [ \t\r\n]+ -> skip ;

// Símbolos e operadores pontuais
ASPAS : '"' ;
ABREPAR : '(' ;
FECHAPAR : ')' ;
VIRG : ',' ;
DOIS_PONTOS : ':' ;
ATRIBUICAO : '<-' ;
OP_RELACIONAL : '<=' | '>=' | '<>' | '=' | '<' | '>' ;
OP_ARITMETICO : '+' | '-' | '*' | '/' | '%' ;
PONTO : '.' ;
E_COMERCIAL : '&' ;
COLCHETES : '[' | ']' ;
CIRCUNFLEXO : '^' ;
PONTOS : '..' ;

// Identificadores
IDENT : [a-zA-Z_] [a-zA-Z0-9_]* ;

ERRO : . ;
