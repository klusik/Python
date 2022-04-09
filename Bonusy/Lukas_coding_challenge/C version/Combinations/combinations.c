#include <stdio.h>
#include <stdlib.h>

typedef struct combinations {
    /** Numbers (linked list) */
    int number_1;
    int number_2;
    int number_3;

    /* Linked list pointer*/
    struct combinations *next;
} COMBINATIONS;

/* Global pointers for first and last item (combination) */
COMBINATIONS    *first  = NULL,
                *last   = NULL;

int add_combination(int number_1, int number_2, int number_3) {
    /** Adding a combination to linked list */

    /* Creating a pointer */
    COMBINATIONS *new_combination = NULL;

    /* Memory handling */
    new_combination = (COMBINATIONS *) malloc(sizeof(COMBINATIONS));

    /* If memory wasn't assigned, stop algorithm */
    if (new_combination == NULL)
        return(0);

    /* Set structure values */
    new_combination->number_1 = number_1;
    new_combination->number_2 = number_2;
    new_combination->number_3 = number_3;

    /* Clearing a pointer to next item */
    new_combination->next = NULL;

    /* Adding to a linked list (if exists) */
    if (first == NULL) {
        /* First item */
        first = new_combination;

        /* First and last item point to the same item */
        last = first;
    }
    else {
        /* Not the first item */

        /* Link the link */
        last->next = new_combination;

        /* Move the pointer */
        last = last->next;
    }
}


int main()
{
    int input_number;
    printf("Enter the whole number (3 or more): ");
    scanf("%d", &input_number);



}
