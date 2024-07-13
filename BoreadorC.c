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

typedef struct Vector{
 char* toString;
}Vector;
Vector* initVector(char* v){
Vector* result = malloc(sizeof(Vector));
result->toString = "Vector";
return result;
}
typedef struct Vectordouble{
double** v;
 int index;
 int size;
}Vectordouble;
Vectordouble* initVectordouble(double** vec, int size){
Vectordouble* result = malloc(sizeof(Vectordouble));
 result->v = vec;
result->size = size;
result->index = -1;
 return result;
}

Vectordouble* initv0(){
double** result = malloc(sizeof(double*));
result[0] = Num(1.0);
result[1] = Num(2.0);
result[2] = Num(3.0);
result[3] = Num(4.0);
return initVectordouble(result, 4);
}
int main(int argc, char **argv){
Vectordouble* a = initv0();
printf("el valor es: %lf\n", *a->v[3]);
}