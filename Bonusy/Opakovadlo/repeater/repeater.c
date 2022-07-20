#include <stdio.h>
#include <stdlib.h>

char *repeat(int count, char character) {
    register int i;

    char *string;

    string = (char*)malloc((count+1)*sizeof(char));



    for (i=0; i<count; i++) {
        string[i] = character;
    }
    string[i+1] = '\0';

    return(string);
}

int main()
{
    char c;
    scanf("%s", &c);
    printf("%s", repeat(32, c));
}
