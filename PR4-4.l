%{
#include <stdio.h>
#include <string.h>

int lower = 0, upper = 0, digit = 0, symbol = 0;
int length = 0;

void validate_password() {
    if (length >= 9 && length <= 15 && lower > 0 && upper > 0 && digit > 0 && symbol > 0) {
        printf("Valid password\n");
    } else {
        printf("Invalid password\n");
    }
}
%}

%%

[a-z]       { lower++; length++; }
[A-Z]       { upper++; length++; }
[0-9]       { digit++; length++; }
[*,;#$@]     { symbol++; length++; }
\n          { validate_password(); }
.           { printf("Invalid password\n"); return 0;} 

%%

int yywrap(void) {
    return 1;
}

int main(void) {
    yylex();
    return 0;
}
