// https://adventofcode.com/2022/day/6
// Run: $ make

#include <stdio.h>
#include <stdlib.h>

int distinct_chars(FILE* fp, int num_chars) {
    int countmap[26] = {0};  // indices 0-25 -> letters a-z
    int unique_chars = 0;
    int curr_char = 0;
    char c;

    while (1) {
        curr_char++;
        c = fgetc(fp);
        if(feof(fp)) break;

        // take one char
        countmap[c-'a']++;
        if (countmap[c-'a'] == 1) {
            unique_chars++;
        }
        
        if (curr_char > num_chars) {
            // drop one char
            fseek(fp, -num_chars-1, SEEK_CUR);
            c = fgetc(fp);
            countmap[c-'a']--;
            if (countmap[c-'a'] == 0) {
                unique_chars--;
                }
            fseek(fp, num_chars, SEEK_CUR);
        }
        if (unique_chars >= num_chars) {
            return curr_char;
        }
    }
}

int main(void) {
    /*
    const char INPUT_FILE[] = "test_input.txt";
    */
    const char INPUT_FILE[] = "real_input.txt";

    FILE *fp = fopen(INPUT_FILE, "r");
    
    int part1 = distinct_chars(fp, 4);
    printf("Part 1: %d\n", part1);

    rewind(fp);

    int part2 = distinct_chars(fp, 14);
    printf("Part 2: %d\n", part2);

    fclose(fp);
}