// https://adventofcode.com/2022/day/1
// Run: $ make

// https://en.cppreference.com/w/cpp/header/cstdio
#include <stdio.h>
// https://en.cppreference.com/w/cpp/header/cstdlib
#include <stdlib.h>

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)b - *(int*)a );  // descending order
}

int main(void) {
    // https://en.cppreference.com/w/cpp/io/c/fopen
    FILE *fp = fopen("real_input.txt", "r");
    //FILE *fp = fopen("test_input.txt", "r");

    // Used by fgets()
    char *cp;
    // Line buffer used by fgets()
    char buff[10];
    // End of line; used by strtol()
    char *endp = "\r";

    // Calories accumulator (per elf)
    uint sum = 0;
    // Max sum
    uint max = 0;
    //// Array of all sums
    uint sums[1000];
    uint index = 0;

    while (1) {
        // https://en.cppreference.com/w/c/io/fgets
        cp = fgets(buff, 10, fp);

        if (!cp || *cp == '\r') {
            if (sum > max) max = sum;
            sums[index] = sum;
            if (!cp) break;
            index += 1;
            sum = 0;
        }
        else {
            // https://en.cppreference.com/w/c/string/byte/strtol
            uint num = strtol(cp, &endp, 10);
            sum += num;
        }
    }

    fclose(fp);


    // Part 1

    printf("Part 1: %d\n", max);


    // Part 2

    // https://en.cppreference.com/w/c/algorithm/qsort
    qsort(sums, index+1, sizeof(int), cmpfunc);

    uint sum_max3 = 0;
    for (uint i = 0; i < 3; i++) {
        sum_max3 += sums[i];
    }

    printf("Part 2: %d\n", sum_max3);
}
