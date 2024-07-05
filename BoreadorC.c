#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdarg.h>

/*double* Num(double x){
    double* result = malloc(sizeof(double));
    result = &x;
    return result;
}
double* Sum(double* x, double* y){
    //* result = malloc(sizeof(double));
    return Num(*x + *y);
    }
    double* Mult(double* x, double* y){
    double* result;
    *result = *x * *y;
    return result;
    }
double Pow34(double a, double y){
    #include <math.h>
    return pow(a, y);
}

char* String(char x[]){
    char* result;
    result = x;
    return result;
}
int main(int argc, char **argv){
    double x = 5.4;
    double *r = &x;
    double *t = &x;
    double y = pow(5.4, 4.7);
    //r = Num(4);
    double* k;
    *k = *Num(5);
    //*k = *k + *k;
    *t = *Sum(k,r);
    //double* result = Pow(r, r);
    //printf(String("probando"));
    printf("el valor es: %lf\n", *t);

}*/
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

typedef struct A{
    double* x;
    double* y;
}A;
A* initA(double* x, double* y){
A* result = malloc(sizeof(A));
result->x = Sum(x, Num(1.0));
result->y = Sum(y, Num(4.0));
return result;
}
typedef struct B{
    double* x;
    double* y;
    double* z;
}B;
B* initB(double* x, double* y, double* z){
B* result = malloc(sizeof(B));
*result->x = *Sum(x, Num(1.0));
*result->y = *Sum(y, Num(4.0));
*result->z = *Sum(z, Num(4.0));
return result;
}
 int main(int argc, char **argv){
Num(4.0);
double x = 4;
double* y = &x;
initA(y,y);
printf("el valor es: %lf\n", *initA(y,y)->x);
}