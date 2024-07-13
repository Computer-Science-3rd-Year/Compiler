#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdarg.h>
#include <time.h>

#define OBJECT_DICT_CAPACITY 67

#define bool int
#define true 1
#define false 0

void throwError(const char *note){
    fprintf(stderr, "Invalid: %s\n", note);
    exit(1);
}

typedef struct Atribute
{
    char* key;
    void* value;
    struct Atribute* next;
}Atribute;

typedef struct Object
{
    Atribute** lists;
}Object;

unsigned int hash(char* key, int capacity) {
    unsigned long hash = 5381;
    int c;

    while ((c = *key++))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash % capacity;
}

void addAtribute(Object* object, char* key, void* value){
    if (object == NULL || object->lists == NULL){
        throwError("NULL value");
    }
    unsigned int index  = hash(key, OBJECT_DICT_CAPACITY);
    Atribute* atribute = malloc(sizeof(Atribute)); 
    atribute->key = strdup(key);
    atribute->value = value;
    atribute->next = object->lists[index];
    object->lists[index] = atribute;
}

void* getAtributeValue(Object* object, char* key){
    if (object == NULL || object->lists == NULL){
        throwError("NULL value");
    }
    unsigned int index  = hash(key, OBJECT_DICT_CAPACITY);
    Atribute* curr = object->lists[index];
    while (curr != NULL){
        if(strcmp(curr->key, key) == 0){
            return curr->value;
        }
        curr = curr->next;
    }
    return NULL;
}
Atribute* getAtribute(Object* object, char* key){
    if(object == NULL || object->lists == NULL){
        throwError("NULL Value");
    }
    unsigned int index = hash(key, OBJECT_DICT_CAPACITY);
    Atribute* curr = object->lists[index];

    while(curr != NULL){
        if(strcmp(curr->key, key) == 0){
            return curr;
        }
        curr = curr->next;
    }
    return NULL;
}

void replaceAtribute(Object* object, char* key, void* value){
    if(object == NULL || object->lists == NULL){
        throwError("NULL REFERENCE");
    }
    Atribute* atribute = getAtribute(object, key);
    free(atribute->value);
    atribute->value = value;
}

void removeAtribute(Object* object, char* key){
    if(object == NULL || object->lists == NULL){
        throwError("NULL Value");
    }
    unsigned int index = hash(key, OBJECT_DICT_CAPACITY);
    Atribute* curr = object->lists[index];
    Atribute* previous = NULL;
    
    while(curr != NULL){
        if (strcmp(curr->key, key) == 0){
            if(previous == NULL){
                object->lists[index] = curr->next;
            }
            else
            {
                previous->next = curr->next;
            }
            free(curr->key);
            free(curr->value);
            free(curr);
            return;
        }
        previous = curr;
        curr = curr->next;
    }
}

///////////////// Methods
///Object
Object* createEmptyObject();
Object* createObject();
Object* replaceObject(Object* object1, Object* object2);
Object* method_Object_equals(Object* object1, Object* object2);
Object* method_Object_toString(Object* object1);

//Dynamic
void* getMethodForCurrentType(Object* object, char* method_name, char* base_type);
char* getType(Object* object);
Object* isType(Object* object, char* protocol);
Object* isProtocol(Object* object, char* protocol);
Object* function_print(Object* object);

Object* createNumber(double num);
Object* copyObject(Object* object);
Object* method_Number_toString(Object* num);
Object* method_Number_equals(Object* num1, Object* num2);
Object* numberSum(Object* num1, Object* num2);
Object* numberMinus(Object* num1, Object* num2);
Object* numberMultiplity(Object* num1, Object* num2);
Object* numberDivision(Object* num1, Object* num2);
Object* numberPow(Object* num1, Object* num2);
Object* function_sqrt(Object* num);
Object* function_sin(Object* num);
Object* function_cos(Object* num);
Object* function_exp(Object* num);
Object* function_log(Object* num);
Object* function_rand();
Object* function_parse(Object* string);

Object* createString(char* str);
Object* stringConcat(Object* string1, Object* string2);
Object* method_string_size(Object* self);
Object* method_String_toString(Object* str);
Object* method_String_equals(Object* string1, Object* string2);

Object* createBoolean(bool boolean);
Object* method_Boolean_toString(Object* boolean);
Object* method_Boolean_equals(Object* bool1, Object* bool2);
Object* invertBoolean(Object* boolean);
Object* boolOr(Object* bool1, Object* bool2);
Object* boolAnd(Object* bool1, Object* bool2);

Object* createVectorFromList(int num_elements, Object** list);
Object* createVector(int num_elements, ...);
Object* method_Vector_size(Object* self);
Object* method_Vector_next(Object* self);
Object* method_Vector_current(Object* self);
Object* getElementOfVector(Object* vector, Object* index);
Object* method_Vector_toString(Object* vector);
Object* method_Vector_equals(Object* vector1, Object* vector2);
Object* function_range(Object* start, Object* end);

Object* createRange(Object* min, Object* max);
Object* method_Range_next(Object* self);
Object* method_Range_current(Object* self);
Object* method_Range_toString(Object* range);
Object* method_Range_equals(Object* range1, Object* range2);

Object* createEmptyObject(){
    return malloc(sizeof(Object));
}
Object* copyObject(Object* object){
    return replaceObject(createEmptyObject(), object);
}
Object* createObject(){
    Object* object = createEmptyObject();
    object->lists = malloc(sizeof(Atribute*) * OBJECT_DICT_CAPACITY);
    for(int i = 0; i < OBJECT_DICT_CAPACITY; i++){
        object->lists[i] = NULL;
    }

    addAtribute(object, "method_Object_toString", *method_Object_toString);
    addAtribute(object, "methd_Object_equals", *method_Object_equals);
    return object;
}

Object* replaceObject(Object* object1, Object* object2){
    if(object1 == NULL && object2 != NULL){
        object1 = copyObject(object2);
    }
    else if(object1 != NULL && object2 == NULL){
        object1->lists = NULL;
    }
    else if(object1 != NULL && object2 != NULL){
        object1->lists = object2->lists;
    }
    return object1;
}

Object* method_Object_equals(Object* object1, Object* object2){
    return createBoolean(object1 == object2);
}
Object* method_Object_toString(Object* object){
    char* address = malloc(50);
    sprintf(address, "%p", (void*)object);
    return createString(address);
}

char* getType(Object* object){
    if(object == NULL){
        throwError("Null value");
    }
    return getAtributeValue(object, "parent_type0");
}

void* getMethodForCurrentType(Object* object, char* method_name, char* base_type){
    if(object == NULL){
        throwError("NULL value");
    }
    bool found_base_type = base_type == NULL;
    
    int index = 0;
    char* initial_parent_type = malloc(128);
    sprintf(initial_parent_type, "%s%d", "parent_type", index++);
    char* type = getAtribute(object, initial_parent_type);
    free(initial_parent_type);

    while(type != NULL){
        if(found_base_type || strcmp(type, base_type) == 0){
            found_base_type = true;

            char* full_name = malloc(128);
            sprintf(full_name, "%s%s%s%s", "method_", type, "_", method_name);

            void* method = getAtributeValue(object, full_name);

            free(full_name);

            if(method != NULL){
                return method;
            }
        }
        char* parent_type = malloc(128);
        sprintf(parent_type, "%s%d", "parent_type",index++);
        type = getAtributeValue(object, parent_type);
        free(parent_type);
    }
    return NULL;
}

Object* isType(Object* object, char* type)
{
    if(object == NULL){
        throwError("NULL value");
    }
    int index = 0;
    char* initial_parent_type = malloc(128);
    sprintf(initial_parent_type, "%s%d", "parent_type", index++);
    char* ptype = getAtributeValue(object, initial_parent_type);
    free(initial_parent_type);

    while(ptype != NULL){
        if(strcmp(ptype, type) == 0){
            return createBoolean(true);
        }
        char* parent_type = malloc(128);
        sprintf(parent_type, "%s%d", "parent_type", index++);
        ptype = getAtributeValue(object, parent_type);
        free(parent_type);
    }
    return createBoolean(false);
}
Object* isProtocol(Object* object, char* protocol){
    if(object == NULL){
        throwError("NULL value");
    }
    int index = 0;
    char* initial_protocol = malloc(128);
    sprintf(initial_protocol, "%s%d", "conforms_protocol", index++);
    char* pprotocol = getAtributeValue(object, initial_protocol);
    free(initial_protocol);

    while(pprotocol != NULL)
    {
        if(strcmp(pprotocol, protocol) == 0){
            return createBoolean(true);
        }
        char* cprotocol = malloc(128);
        sprintf(cprotocol, "%s%d", "conforms_protocol", index++);
        pprotocol = getAtribute(object, cprotocol);
        free(cprotocol);
    }
    return createBoolean(false);
}

Object* function_print(Object* object){
    if(object == NULL || object->lists == NULL)
    {
        printf("Null\n");
        return createString("NULL");
    }
    Object* str = ((Object* (*)(Object*))getMethodForCurrentType(object, "toString", 0))(object);

    char* value = getAtributeValue(str, "value");
    printf("%s\n", value);

    return str;
}

Object* createNumber(double num){
    Object* object = createObject();
    double* value = malloc(sizeof(double));
    *value = num;

    addAtribute(object, "value", value);
    addAtribute(object, "parent_type0", "Number");
    addAtribute(object, "parent_type1", "Object");
    addAtribute(object, "method_Number_toString", *method_Number_toString);
    addAtribute(object, "method_Number_equals", *method_Number_equals);

    return object;
}

Object* method_Number_toString(Object* num){
    if(num == NULL){
        throwError("Null Reference");
    }
    double* value = getAtributeValue(num, "value");
    char* str = malloc(30);
    sprintf(str, "%f", *value);
    return createString(str);
}
Object* method_Number_equals(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Reference");
    }
    if(strcmp(getType(num1), "Number") != 0 || strcmp(getType(num2), "Number") != 0){
        return createBoolean(false);
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createBoolean(fabs(*value1 - *value2) < 0.000000001);
}
Object* numberSum(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Reference");
    }
    if(strcmp(getType(num1), "Number") != 0 || strcmp(getType(num2), "Number") != 0){
        return createBoolean(false);
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createNumber(*value1 + *value2);
}
Object* numberMinus(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createNumber(*value1 - *value2);
}
Object* numberMultiplity(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createNumber(*value1 * *value2);
}

Object* numberDivision(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    if(*value2 == 0){
        throwError("Zero Division");
    }
    return createNumber(*value1 / *value2);
}
Object* numberPow(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL value");
    }
    double value1 = *(double*)getAtributeValue(num1, "value");
    double value2 = *(double*)(num2, "value");
    return createNumber(pow(value1, value2));
}

Object* function_sqrt(Object* num){
    if(num == NULL){
        throwError("NULL Value");
    }
    double value = *(double*)getAtributeValue(num, "Value");

    return createNumber(sqrt(value));
}

Object* function_sin(Object* num){
    if(num == NULL){
        throwError("NULL Value");
    }
    double a = *(double*)getAtributeValue(num, "value");
    return createNumber(sin(a));
}
Object* function_cos(Object* num){
    if(num == NULL){
        throwError("NULL Value");
    }
    double a = *(double*)getAtributeValue(num, "value");
    return createNumber(cos(a));
}

Object* function_exp(Object* num){
    if(num == NULL){
        throwError("NULL value");
    }
    double value = *(double*)getAtributeValue(num, "value");

    return createNumber(exp(value));
}
Object* function_log(Object* num){
    if(num == NULL){
        throwError("NULL Value");
    }
    double value = *(double*)getAtributeValue(num, "value");
    return createNumber(log(value));
}
Object* function_rand(){
    return createNumber((double)rand()/ (RAND_MAX + 1.0));
}
Object* numberGreaterThan(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createBoolean(*value1 > *value2);

}
Object* numberGreaterOrEqualThan(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createBoolean(*value1 >= *value2);
}
Object* numberLessThan(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createBoolean(*value1 < *value2);
}
Object* numberLessOrEqualThan(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createBoolean(*value1 <= *value2);   
}
Object* numberMod(Object* num1, Object* num2){
    if(num1 == NULL || num2 == NULL){
        throwError("NULL Value");
    }
    double* value1 = getAtributeValue(num1, "value");
    double* value2 = getAtributeValue(num2, "value");
    return createNumber(((int)*value2) % ((int)*value2));
}

Object* function_parse(Object* string){
    if(string == NULL){
        throwError("NULL value");
    }
    char* value = getAtributeValue(string, "value");
    return createNumber(strtod(value, NULL));
}

Object* createString(char* str){
    Object* object = createObject();

    addAtribute(object, "value", str);
    addAtribute(object, "parent_type0", "String");
    addAtribute(object, "parent_type1", "Object");

    int *len = malloc(sizeof(int));
    *len = strlen(str);

    addAtribute(object, "len", len);
    addAtribute(object, "method_String_toString", *method_String_toString);
    addAtribute(object, "method_String_equals", *method_String_equals);
    addAtribute(object, "method_String_size", *method_string_size);

    return object;
}

Object* stringConcat(Object* obj1, Object* obj2)
{
    if(obj1 == NULL || obj2 == NULL)
        throwError("Null Reference");

    Object* string1 = ((Object* (*)(Object*))getMethodForCurrentType(obj1, "toString", NULL))(obj1);
    Object* string2 = ((Object* (*)(Object*))getMethodForCurrentType(obj2, "toString", NULL))(obj2);

    char* str1 = getAttributeValue(string1, "value");
    int len1 = *(int*)getAttributeValue(string1, "len");

    char* str2 = getAttributeValue(string2, "value");
    int len2 = *(int*)getAttributeValue(string2, "len");

    char* result = malloc((len1 + len2 + 1) * sizeof(char));
    sprintf(result, "%s%s", str1, str2);
    result[len1 + len2] = '\0';

    return createString(result);
}

Object* method_string_size(Object* self){
    if(self == NULL){
        throwError("NULL Reference");
    }
    return createNumber(*(int*)getAtributeValue(self, "len"));
}

Object* method_String_toString(Object* str) {
    if(str == NULL)
        throwError("Null Reference");

    return str;
}
Object* method_String_equals(Object* string1, Object* string2){
    if(string1 == NULL || string2 == NULL){
        throwError("NULL Value");
    }
    if(strcmp(getType(string1), "String") != 0 || strcmp(getType(string2), "String") != 0){
        return createBoolean(false); 
    }
    char* value1 = getAtributeValue(string1, "value");
    char* value2 = getAtributeValue(string2, "value");

    return createBoolean(strcmp(value1, value2) == 0);
}

Object* createBoolean(bool boolean){
    Object* object = createObject();

    bool* value = malloc(sizeof(bool));
    *value = boolean;

    addAtribute(object, "value", value);
    addAtribute(object, "parent_type0", "Boolean");
    addAtribute(object, "parent_type1", "Object");
    addAtribute(object, "method_Boolean_toString", *method_Boolean_toString);
    addAtribute(object, "method_Boolean_equals", *method_Boolean_equals);

    return object;
}
Object* method_Boolean_toString(Object* boolean){
    if( boolean == NULL){
        throwError("NULL value");
    }
    bool* value = getAtributeValue(boolean, "value");

    if(*value == true){
        return createString("true");
    }
    else{
        return createString("false");
    }
}

Object* method_Boolean_equals(Object* bool1, Object* bool2){
    if(bool1 == NULL || bool2 == NULL){
        throwError("NULL value");
    }
    if(strcmp(getType(bool1), "Boolean") != 0 || strcmp(getType(bool2), "Boolean") != 0)
        return createBoolean(false);
    bool* value1 = getAtributeValue(bool1, "value");
    bool* value2 = getAtributeValue(bool2, "value");

    return createBoolean(value1 == value2);

}
Object* invertBoolean(Object* boolean){
    if(boolean == NULL){
        throwError("NULL value");
    }
    bool* value = getAtributeValue(boolean, "value");
    return createBoolean(!*value);
}

Object* boolOr(Object* bool1, Object* bool2){
    if(bool1 == NULL || bool2 == NULL){
        throwError("NULL Reference");
    }
    bool vbool1 = *(bool*)getAtributeValue(bool1, "value");
    bool vbool2 = *(bool*)getAtributeValue(bool2, "value");

    return createBoolean(vbool1 || vbool2);
}
Object* boolAnd(Object* bool1, Object* bool2){
    if(bool1 == NULL || bool2 == NULL){
        throwError("NULL Reference");
    }
    bool vbool1 = *(bool*)getAtributeValue(bool1, "value");
    bool vbool2 = *(bool*)getAtributeValue(bool2, "value");

    return createBoolean(vbool1 && vbool2);
}

Object* createVectorFromList(int num_elements, Object** list){
    Object* vector = createObject();

    addAtribute(vector, "parent_type0", "Vector");
    addAtribute(vector, "parent_type1", "Object");

    addAtribute(vector, "conforms_protocol0", "Iterable");

    addAtribute(vector, "method_Vector_toString", *method_Vector_toString);
    addAtribute(vector, "method_Vector_equals", *method_Vector_equals);

    int* size = malloc(sizeof(int));
    *size = num_elements;
    addAtribute(vector, "size", size);
    addAtribute(vector, "list", list);
    addAtribute(vector, "current", createNumber(-1));
    addAtribute(vector, "method_Vector_size", *method_Vector_size);
    addAtribute(vector, "method_Vector_next", *method_Vector_next);
    addAtribute(vector, "method_Vector_current", *method_Vector_current);
    return vector;
}

Object* createVector(int num_elements, ...){
    va_list elements;
    va_start(elements, num_elements);

    Object** list = malloc(num_elements* sizeof(Object*));
    for(int i = 0; i < num_elements; i++){
        list[i] = va_arg(elements, Object*);
    }
    va_end(elements);

    return createVectorFromList(num_elements, list);
}

Object* method_Vector_size(Object* self){
    if(self == NULL){
        throwError("NULL value");
    }
    return createNumber(*(int*)getAtributeValue(self, "size"));
}
Object* method_Vector_next(Object* self){
    if(self == NULL){
        throwError("NULL Reference");
    }
    int size = *(int*)getAtributeValue(self, "size");
    double* current = getAtributeValue((Object*)getAtributeValue(self, "current"), "value");
    if(*current + 1 < size){
        *current += 1;
        return createBoolean(true);
    }

    return createBoolean(false);
}
Object* method_Vector_current(Object* self){
    if(self == NULL){
        throwError("NULL Reference");
    }
    return getElementOfVector(self, getAtributeValue(self, "current"));

}

Object* getElementOfVector(Object* vector, Object* index){
    if(vector == NULL || index == NULL){
        throwError("NULL Value");
    }
    int i = (int)*(double*)getAtributeValue(index, "value");
    int size = *(int*)getAtributeValue(vector, "size");

    if(i >= size){
        throwError("Index out of range");
    }

    return ((Object**)getAtributeValue(vector, ""))[i];
}
Object* method_Vector_toString(Object* vector){
    if(vector == NULL){
        throwError("NULL value");
    }
    int* size = getAtributeValue(vector, "size");

    int total_size = 3 + ((*size > 0 ? *size : 1) - 1) * 2;
    Object** list = getAtributeValue(vector, "list");
    Object** strs = malloc(*size * sizeof(Object*));

    for(int i = 0; i < *size; i++){
        strs[i] = ((Object* (*)(Object*)) getMethodForCurrentType(list[i], "toString", 0))(list[i]);
        total_size += *(int*)getAtributeValue(strs[i],"len");
    }
    char* result = malloc(total_size * sizeof(char));
    result[0] = '\0';
    strcat(result, "[");
    for(int i = 0; i < *size; i++){
        strcat(result, (char*)getAtributeValue(strs[i], "value"));
        free(strs[i]);

        if(i + 1 < *size){
            strcat(result, ", ");
        }
    }
    strcat(result, "]");
    free(strs);
    return createString(result);
}
Object* method_Vector_equals(Object* vector1, Object* vector2){
    if(vector1 == NULL || vector2 == NULL){
        throwError("NULL value");
    }
    if(strcmp(getType(vector1), "Vector") != 0 || strcmp(getType(vector2), "Vector") != 0){
        return createBoolean(false);
    }
    int* size1 = getAtributeValue(vector1, "size");
    Object** list1 = getAtributeValue(vector1, "list");

    int* size2 = getAtributeValue(vector2, "size");
    Object** list2 = getAtributeValue(vector2, "list");

    if(*size1 != *size2){
        return createBoolean(false);
    }
    for(int i = 0; i < *size1; i++){
        bool* equal = getAtributeValue(((Object* (*)(Object*, Object*))getMethodForCurrentType(list1[i], "equals", 0))(list1[i], list2[i]), "value");
        if(!*equal){
            return createBoolean(false);
        }
    }
    return createBoolean(true);
}

Object* function_range(Object* start, Object* end){
    if(start == NULL || end == NULL){
        throwError("NULL value");
    }
    return createRange(start, end);
}
Object* createRange(Object* min, Object* max){
    if(min == NULL || max == NULL){
        throwError("Null Value");
    }
    Object* object = createObject();
    addAtribute(object, "min", min);
    addAtribute(object, "max", max);
    addAtribute(object, "current", numberMinus(min, createNumber(1)));

    int* size = malloc(sizeof(int));
    *size = (int)(*(double*)getAtributeValue(max, "value")) - (int)(*(double*)getAtributeValue(min, "value"));

    addAtribute(object, "size", size);
    addAtribute(object, "parent_type0", "Range");
    addAtribute(object, "parent_type1", "Object");
    addAtribute(object, "conforms_protocol0", "Iterbale");
    addAtribute(object, "method_Range_toString", *method_Range_toString);
    addAtribute(object, "method_Range_equals", *method_Range_equals);

    return object;
}

Object* method_Range_next(Object* self){
    if(self == NULL){
        throwError("NULL value");
    }
    int max = *(double*)getAtributeValue((Object*)getAtributeValue(self, "max"), "value");
    double* current = getAtributeValue((Object*)getAtributeValue(self, "current"), "value");

    if(*current + 1 < max){
        *current += 1;
        return createBoolean(true);
    }    
    return createBoolean(false);
}
Object* method_Range_current(Object* self){
    if(self == NULL){
        throwError("NULL Value");
    }
    return getAtributeValue(self, "current");
}

Object* method_Range_toString(Object* range){
    if(range == NULL){
        throwError("NULL value");
    }
    Object* min = getAtributeValue(range, "min");
    Object* max = getAtributeValue(range, "max");
    int total_size = 6;

    Object* min_str = ((Object*(*)(Object*))getMethodForCurrentType(min, "toString", 0))(min);
    total_size += *(int*)getAtributeValue(min_str, "len");

    Object* max_str = ((Object*(*)(Object*))getMethodForCurrentType(max, "toString", 0))(max);
    total_size += *(int*)getAtributeValue(max_str, "len");

    char* result = malloc(total_size * sizeof(char));
    sprintf(result, "[%s - %s]", (char*)getAtributeValue(min_str, "value"), (char*)getAtributeValue(max_str, "value"));

    free(min_str);
    free(max_str);
    return createString(result);
}
Object* method_Range_equals(Object* range1, Object* range2){
    if(range1 == NULL || range2 == NULL){
        throwError("Null Reference");
    }
    if(strcmp(getType(range1), "Range") != 0 || strcmp(getType(range2), "Range") != 0){
        return createBoolean(false);
    }
    Object* min1 = getAtributeValue(range1, "min");
    Object* max1 = getAtributeValue(range1, "max");
    Object* min2 = getAtributeValue(range2, "min");
    Object* max2 = getAtributeValue(range2, "max");
    return boolAnd(method_Number_equals(min1, min2), method_Number_equals(max1, max2));
}

