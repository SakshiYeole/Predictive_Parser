%{
    #undef yywrap
    #define yywrap() 1
    #define ERROR -1
    #define IF 1
    #define ELSE 2
    #define AND 3
    #define END 4
    #define ID 5
    #define IC 6
    #define INT 7
    #define DO 8
    #define FC 9
    #define FLOAT 10
    #define NOT 11
    #define OR 12
    #define PRINT 13 
    #define PROG 14
    #define SCAN 15
    #define STR 16
    #define THEN 17
    #define WHILE 18
    #define ASSIGN 19
    #define SEMICOLON 20
    #define PLUS 21
    #define MINUS 22
    #define MULTIPLY 23
    #define DIVIDE 24
    #define EQUAL 25
    #define LT 26
    #define GT 27
    #define LPAREN 28
    #define RPAREN 29
    #define LCBRACE 30
    #define RCBRACE 31
%}

digit [0-9]
digits {digit}+
letter [a-zA-Z]
if if
else else
and and
end end
id {letter}({letter}|{digit})*
ic {digits}(E[+-]?{digits})?
int int
do do
fc {digits}(.{digits})(E[+-]?{digits})?
float float
not not
or or
print print
prog prog
scan scan
str \"..*\"
then then
while while
assignment :=
semicolon ;
plus [+]
minus [-]
multiply [*]
divide [/]
equal =
lt <
gt >
lparen [(]
rparen [)]
lcbrace [{]
rcbrace [}]
delimiter [ \t\n]

%%
{if} return IF;
{else} return ELSE;
{and} return AND;
{end} return END;
{ic} return IC;
{int} return INT;
{do} return DO;
{fc} return FC;
{float} return FLOAT;
{not} return NOT;
{or} return OR;
{print} return PRINT;
{prog} return PROG;
{scan} return SCAN;
{str} return STR;
{then} return THEN;
{while} return WHILE;
{assignment} return ASSIGN;
{semicolon} return SEMICOLON;
{plus} return PLUS;
{minus} return MINUS;
{multiply} return MULTIPLY;
{divide} return DIVIDE;
{equal} return EQUAL;
{lt} return LT;
{gt} return GT;
{lparen} return LPAREN;
{rparen} return RPAREN;
{lcbrace} return LCBRACE;
{rcbrace} return RCBRACE;
{id} return ID;
{delimiter} {}
. return ERROR;
%%

char* tokenName(int token){
    if(token == IF)
        return "if";
    if(token == ELSE)
        return "else";
    if(token == AND)
        return "and";
    if(token == END)
        return "end";
    if(token == IC)
        return "ic";
    if(token == ID)
        return "id";
    if(token == INT)
        return "int";
    if(token == DO)
        return "do";
    if(token == FC)
        return "fc";
    if(token == FLOAT)
        return "float";
    if(token == NOT)
        return "not";
    if(token == OR)
        return "or";
    if(token == PRINT)
        return "print";
    if(token == PROG)
        return "prog";
    if(token == SCAN)
        return "scan";
    if(token == STR)
        return "str";
    if(token == THEN)
        return "then";
    if(token == WHILE)
        return "while";
    if(token == ASSIGN)
        return ":=";
    if(token == SEMICOLON)
        return ";";
    if(token == PLUS)
        return "+";
    if(token == MINUS)
        return "-";
    if(token == MULTIPLY)
        return "*";
    if(token == DIVIDE)
        return "/";
    if(token == EQUAL)
        return "=";
    if(token == LT)
        return "<";
    if(token == GT)
        return ">";
    if(token == LPAREN)
        return "(";
    if(token == RPAREN)
        return ")";
    if(token == LCBRACE)
        return "{";
    if(token == RCBRACE)
        return "}";
    return "ERROR";
}

int main(){
    yyin = fopen("E:\\Acads\\Semester 7\\Compiler Design\\Lab\\lab5\\Parser\\Input\\InputText.txt", "r");
    remove("E:\\Acads\\Semester 7\\Compiler Design\\Lab\\lab5\\Parser\\Output\\OutputTokens.txt");

    int token;
    while((token=yylex())!=0){
        yyout = fopen("E:\\Acads\\Semester 7\\Compiler Design\\Lab\\lab5\\Parser\\Output\\OutputTokens.txt", "a");
        fprintf(yyout, "%s, %s\n", tokenName(token), yytext);
        fclose(yyout);
    }
    // fclose(ptr);
    return 0;
}
