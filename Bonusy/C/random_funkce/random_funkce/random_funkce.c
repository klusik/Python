#include <stdio.h>
#include <stdlib.h>

int user_number() {
    int user_input = -1;

    do {
        printf("Enter positive number: ");
        scanf("%d", &user_input);
        fflush(stdin);
    } while (user_input <= -1);

    return(user_input);
}

int main()
{
    int number_from_user;
    int output;

    number_from_user = user_number();

    output = ((7 * number_from_user + 5) / 3) % 7;

    printf("Output: %d\n", output);
    return(0);
}
