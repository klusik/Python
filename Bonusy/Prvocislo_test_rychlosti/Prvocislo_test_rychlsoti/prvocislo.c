#include <stdio.h>

int main()
{
    int prime = 20153153;
    register int i;
    int is_prime = 1;

    for (i = 2; i <= prime-1; i++) {
        if ((prime % i) == 0) {
            printf("Not prime");
            is_prime = 0;
            break;
        }
    }
    if (is_prime) {
        printf("Is prime");
    }

}
