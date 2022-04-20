/*
Convert number to reversed array of digits

Given a random non-negative number, you have
to return the digits of this number within an array in reverse order.

Example:
348597 => [7,9,5,8,4,3]
0 => [0]
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NUMBER_SIZE 2000

#define TRUE    1
#define FALSE   0

/**
    Returns TRUE if valid number, else returns FALSE.
*/
int is_number(char *number) {
    register int i;

    if (number != NULL) {
        for (i = 0; i < strlen(number); i++) {
            /* Only valid chars are between 0 and 9 inc */
            if (number[i] >= '0' && number[i] <= '9') {
                continue;
            }
            else {
                return FALSE;
            }
        }
    }
    else {
        return FALSE;
    }
    return TRUE;
}

/**
    Input from user.

    Returns *char with a string if valid.
*/
char *input_from_user() {

    char *number = NULL;


    register int i;

    if ((number = (char *)malloc(MAX_NUMBER_SIZE*sizeof(char))) != NULL) {
        printf("Enter a number: ");
        scanf("%s", number);
        if (is_number(number)) {
                return(number);
        }
        else {
            printf("Not a valid number.");
        }
    }
    else {
        /* Memory allocation issue */
        return NULL;
    }
}

int main()
{
    /* Declarations */
    char *input_number = NULL;
    register int i;
    int *arr_numbers = NULL;

    /* User input */
    if ((input_number = input_from_user()) != NULL) {

        /* Here goes the magic */
        /* Creating an array (list) of numbers */
        arr_numbers = (int*)malloc(strlen(input_number)*sizeof(int));
        for (i = 0; i < strlen(input_number); i++) {
            if (arr_numbers != NULL) {
                /* Now read the array from back and save numbers */
                arr_numbers[strlen(input_number)-i-1] =  input_number[i]-'0';
            }
            else {
                printf("Can't allocate a memory for this number.");
            }
        }

    }
    else {
        printf("Not enough memory.");
    }

    /* Printing out the array */
    printf("[ ");
    for (i = 0; i < strlen(input_number); i++) {
        if (i == (strlen(input_number)-1)) {
            printf("%d ", arr_numbers[i]);
        }
        else {
            printf("%d, ", arr_numbers[i]);
        }

    }
    printf("]\n");


}
