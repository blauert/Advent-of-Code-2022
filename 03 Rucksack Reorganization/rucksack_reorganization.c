// https://adventofcode.com/2022/day/3
// Run: $ make

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int get_priority(int item) {
    return islower(item) ? item - 96 : item - 38;
}

int part1(FILE *fp) {
    int prio_sum = 0;

    // https://linux.die.net/man/3/getline
    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    while ((read = getline(&line, &len, fp)) != -1) {
        int num_items = line[read-1] == '\n' ? read - 2 : read;
        int half = num_items / 2;
        int prio_map[52] = {0};

        for (int i = 0; i < half; i++) {
            int prio = get_priority(line[i]);
            prio_map[prio - 1] = 1;
        }

        for (int i = half; i < num_items; i++) {
            int prio = get_priority(line[i]);
            if (prio_map[prio - 1] == 1) {
                prio_sum += prio;
                break;
            }
        }
    }
    return prio_sum;
}

int part2(FILE *fp) {
    int prio_sum = 0;
    int curr_elf = 0;
    int prio_map[52] = {0};

    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    while ((read = getline(&line, &len, fp)) != -1) {
        curr_elf++;
        int num_items = line[read-1] == '\n' ? read - 2 : read;
        
        for (int i = 0; i < num_items; i++) {
            int prio = get_priority(line[i]);
            // update prio_map
            if (prio_map[prio - 1] == curr_elf - 1) {
                prio_map[prio - 1] = curr_elf;
                }
            // check for badge
            if ((curr_elf == 3) && (prio_map[prio - 1] == 3)) {
                prio_sum += prio;
                // reset for next group
                curr_elf = 0;
                for (int i = 0; i < 52; i++) {
                    prio_map[i] = 0;
                }
                break;
                }
            }
        }
    return prio_sum;
}

int main(void) {
    //char input_file[] = "test_input.txt";
    char input_file[] = "real_input.txt";

    // https://en.cppreference.com/w/c/io/fopen
    FILE *fp = fopen(input_file, "r");
    int solution1 = part1(fp);
    printf("Part 1: %d\n", solution1);
    fclose(fp);

    FILE *fp2 = fopen(input_file, "r");
    int solution2 = part2(fp2);
    printf("Part 2: %d\n", solution2);
    fclose(fp2);

    exit(EXIT_SUCCESS);
}