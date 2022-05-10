#include <stdio.h>

int main(int argc, char **argv)
{
    int cislo;

    /* Prevedu ze stringu na int */
    cislo = atoi(argv[1]);

    /* Dve jednicky otocim 'cislokrat' doleva */
    cislo = 11<<cislo;

    /* Pokud je cislo sude, vydelim dvema, pokud liche, prictu 5 a delim dvema */
    if (cislo % 2 == 0) {
        cislo = cislo / 2;
    }
    else {
        cislo = (cislo + 5) / 2;
    }

    printf("%d\n", cislo);
    return 0;
}
