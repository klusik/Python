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

    /* Everything went well */
    return(1);
}

int create_combinations(int input_number) {
    /** Creates all combinations & saves them into the linked list */

    /* Register iterators */
    register int number_1, number_2;

    /* Number 3 as an integer */
    int number_3;

    int success_counter;

    /* Looping the loops */
    for (number_1 = 1; number_1 <= input_number; number_1++) {
        for (number_2 = number_1; number_2 <= (input_number-number_1); number_2++) {
            /* Number_3 should be just a subtraction from input_number */
            number_3 = input_number - (number_1 + number_2);

            /* Good runs counter */
            success_counter = 0;

            /* Adding to a list (all permutations) */
            success_counter += add_combination(number_1, number_2, number_3);
            success_counter += add_combination(number_1, number_3, number_2);
            success_counter += add_combination(number_2, number_1, number_3);
            success_counter += add_combination(number_2, number_3, number_1);
            success_counter += add_combination(number_3, number_2, number_1);
            success_counter += add_combination(number_3, number_1, number_2);

            /* Check if everything okay */
            if (success_counter == 6) {
                success_counter = 0;
            }
            else {
                return(0);
            }
        }
    }

    /* Everything went well */
    return(1);
}

int main()
{
    int input_number = 0;

    /* User input */
    while (input_number < 3) {
        printf("Enter the whole number (3 or more): ");
        scanf("%d", &input_number);
    }

    /* Creating combinations */
    if (create_combinations(input_number)) {
        printf("Successfully done.\n");
    }
    else {
        printf("Something went wrong.\n");
    }

    /* Output */
    COMBINATIONS *reader;
    reader = first;

    while(reader != NULL) {
        /* Write numbers to console */
        //printf("%d %d %d \n", reader->number_1, reader->number_2, reader->number_3);

        /* Moving the pointer */
        reader = reader->next;
    }





}
