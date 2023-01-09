// https://adventofcode.com/2022/day/1
// Run: $ make

// https://en.cppreference.com/w/c/header
#include <stdio.h>
#include <stdlib.h>

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)b - *(int*)a );  // descending order
}

int main(void) {
    // https://en.cppreference.com/w/c/io/fopen
    FILE *fp = fopen("real_input.txt", "r");
    //FILE *fp = fopen("test_input.txt", "r");

    // Used by fgets()
    char *cp;
    // Line buffer used by fgets()
    char buff[10];
    // End of line; used by strtol()
    char end = '\r';
    char *endp = &end;

    // Calories accumulator (per elf)
    unsigned int sum = 0;
    // Max sum
    unsigned int max = 0;
    //// Array of all sums
    unsigned int sums[1000];
    size_t len_sums = 0;

    while (1) {
        // https://en.cppreference.com/w/c/io/fgets
        cp = fgets(buff, 10, fp);

        if (!cp || *cp == end) {
            if (sum > max) max = sum;
            sums[len_sums] = sum;
            if (!cp) break;
            len_sums += 1;
            sum = 0;
        }
        else {
            // https://en.cppreference.com/w/c/string/byte/strtol
            unsigned int num = strtol(cp, &endp, 10);
            sum += num;
        }
    }
    fclose(fp);

    // Part 1

    printf("Part 1: %d\n", max);


    // Part 2

    // https://en.cppreference.com/w/c/algorithm/qsort
    qsort(sums, len_sums+1, sizeof(sums[0]), cmpfunc);

    unsigned int sum_max3 = 0;
    for (unsigned int i = 0; i < 3; i++) {
        sum_max3 += sums[i];
    }
    printf("Part 2: %d\n", sum_max3);
}
