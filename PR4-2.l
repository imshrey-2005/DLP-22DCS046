%%
charusat { printf("university"); }
CHARUSAT { printf("UNIVERSITY"); }
Charsuat { printf("University"); }
\n	{ printf("\n"); }
. 	{ printf("%s", yytext); }
%%

int yywrap(void) {
    return 1;
}

int main(void) {
    yylex();
    return 0;
}
