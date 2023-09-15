%{
    #undef yywrap
    #define yywrap() 1

    #define ERROR -1;
    #define N 1
    #define PLUS 2
    #define STAR 3
%}

n n
plus [+]
star [*]

%%

{n} return N;
{plus} return PLUS;
{star} return STAR;
. return ERROR;

%%

char* tokenName(int token){
    if(token == N)
        return "n";
    if(token == PLUS)
        return "+";
    if(token == STAR)
        return "*";
    return "ERROR";
}

int main(){
    yyin = fopen("E:\\Acads\\Semester 7\\Compiler Design\\Lab\\lab5\\Parser\\Input\\InputText.txt", "r");
    remove("E:\\Acads\\Semester 7\\Compiler Design\\Lab\\lab5\\Parser\\Output\\OutputTokens.txt");
    // FILE *ptr;
    // ptr = fopen("outputTokens.txt", "w");
    // fclose(ptr);
    int token;
    while((token=yylex())!=0){
        yyout = fopen("E:\\Acads\\Semester 7\\Compiler Design\\Lab\\lab5\\Parser\\Output\\OutputTokens.txt", "a");
        fprintf(yyout, "%s, %s\n", tokenName(token), yytext);
        fclose(yyout);
    }
    return 0;
}