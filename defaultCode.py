default = '''
#include <stdio.h>
#include <string.h>

char* String(char x[]){
    char* result;
    result = x;
    return result;
}
double* Num(double x){
    double* result = malloc(sizeof(double));
    *result = x;
    return result;
}

double* Sum(double* x, double* y){
    return Num(*x + *y);
}
double* Minus(double* x, double* y){
    return Num(*x - *y);
}
double* Mult(double* x, double* y){
    return Num(*x * *y);
}
double* Division(double* x, double* y){
    return Num(*x / *y);
}
double* Pow(double* x, double* y){
    return Num(pow(*x, *y));
}
double* Resto(double* x, double* y){
    return Num((int)*x + (int)*y);
}
char* ToString(double* numero){
    static char str[400];
    snprintf(str, sizeof(str), "%f", *numero);
    return str;
}
char* ConcatSdd(double* x, double* y){
    char* a = ToString(x);
    char* b = ToString(y);
    
    // Crea una nueva cadena para el resultado
    char* result = malloc((strlen(a) + strlen(b) + 1) * sizeof(char));
    if (result == NULL) {
        // Maneja el error de asignación de memoria
        return NULL;
    }
    
    // Concatena las cadenas en la nueva cadena
    strcpy(result, a);
    strcat(result, b);
    
    return result;
}

char* ConcatSdc(double* x, char* y){
    char* a = ToString(x);
    char* result = malloc((strlen(a) + strlen(y) + 1) * sizeof(char));
    strcpy(result, a);
    strcat(result, y);
    
    return result;
}
char* ConcatScd(char* x, double* y){
    char* a = ToString(y);
    char* result = malloc((strlen(x) + strlen(a) + 1) * sizeof(char));
    strcpy(result, x);
    strcat(result, a);
    return result;
}
char* ConcatScc(char* x, char* y){
    char* result = malloc((strlen(x) + strlen(y) + 1) * sizeof(char));
    strcpy(result, x);
    strcat(result, y);
    return result;
}
double* And(double* x, double* y){
    return Num(*x && *y);
}
double* Or(double* x, double* y){
    return Num(*x || *y);
}
double* Less(double* x, double* y){
    return Num(*x < *y);
}
double* LessE(double* x, double* y){
    return Num(*x <= *y);
}
double* Greater(double* x, double* y){
    return Num(*x > *y);
}
double* GreaterE(double* x, double* y){
    return Num(*x >= *y);
}
double* Equal(double* x, double* y){
    return Num(*x == *y);
}
double* Distint(double* x, double* y){
    return Num(*x != *y);
}
double* sin1(double* x){
    return Num(sin(*x));
}
double* cos1(double* x){
    return Num(cos(*x));
}
double* tan1(double* x){
    return Num(tan(*x));
}
double* sqrt1(double* x){
    return Num(sqrt(*x));
}
'''