// https://adventofcode.com/2022/day/5
// Run: $ make

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <malloc.h>

size_t get_num_stacks(FILE *fp) {
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    read = getline(&line, &len, fp);
    rewind(fp);

    size_t num_stacks = (read - 1) / 4;
    return num_stacks;
}

void fill_stacks(FILE *fp, char *stacks[], size_t stacks_lens[]) {
    // https://linux.die.net/man/3/getline
    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    while ((read = getline(&line, &len, fp)) != -1) {
        if (isdigit(line[1])) return;
        int curr_len = line[read-1] == '\n' ? read - 2 : read;

        int i = 0;
        for (int j = 1; j < curr_len; j += 4) {
            if (line[j] != ' ') {
                stacks[i] = realloc(stacks[i], (stacks_lens[i] + 1) * sizeof(char));
                stacks[i][stacks_lens[i]] = line[j];
                stacks_lens[i]++;
            }
            i++;
        }
    }
}

void reverse_stacks(char *stacks[], size_t stacks_lens[], size_t num_stacks) {
    char *new;
    for (int i = 0; i < num_stacks; i++) {
        new = malloc(stacks_lens[i] * sizeof(char));
        int new_idx = 0;
        for (int j = stacks_lens[i]-1; j > -1; j--) {
            new[new_idx] = stacks[i][j];
            new_idx++;
        }
        free(stacks[i]);
        stacks[i] = new;
    }
}

void print_stacks(char *stacks[], size_t stacks_lens[], size_t num_stacks) {
    for (int i = 0; i < num_stacks; i++) {
        printf("Stack %d: %d (%d bytes)\n", i+1, (int)stacks_lens[i], (int)malloc_usable_size(stacks[i]));
        for (int j = 0; j < stacks_lens[i]; j++) {
            printf("%c ", stacks[i][j]);
        }
        printf("\n");
    }
}

void print_top(char *stacks[], size_t stacks_lens[], size_t num_stacks) {
    for (int i = 0; i < num_stacks; i++) {
        printf("%c", stacks[i][stacks_lens[i]-1]);
    }
    printf("\n");
}

size_t get_instructions(FILE *fp, int **instr) {
    *instr = malloc(0);
    size_t num_instr = 0;

    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    int curr_idx = 0;

    while ((read = getline(&line, &len, fp)) != -1) {
        int curr_len = line[read-1] == '\n' ? read - 2 : read;

        num_instr++;
        *instr = realloc(*instr, num_instr * 3 * sizeof(int));

        // https://stackoverflow.com/questions/5029840/convert-char-to-int-in-c-and-c
        int from = line[curr_len-6] - '0';
        int to = line[curr_len-1] - '0';

        char crates_digits[curr_len-17]; // variable number of digits (1 or 2)
        int i = 0;
        for (int j = 5; j < curr_len-12; j++) {
            crates_digits[i] = line[j];
            i++;
        }
        // https://stackoverflow.com/questions/10204471/convert-char-array-to-a-int-number-in-c
        int crates;
        sscanf(crates_digits, "%d", &crates);

        (*instr)[curr_idx] = crates;
        curr_idx++;
        (*instr)[curr_idx] = from;
        curr_idx++;
        (*instr)[curr_idx] = to;
        curr_idx++;
    }
    return num_instr;
}

void print_instructions(int *instr, size_t num_instr) {
    int j = 0;
    for (int i = 0; i < num_instr*3; i = i+3) {
        j++;
        printf("Instruction %d: move %d from %d to %d\n", j, instr[i], instr[i+1], instr[i+2]);
    }
    printf("Calculated size: %d bytes\n", (int)sizeof(int) * 3 * j);
    printf("Size used: %d bytes\n", (int)malloc_usable_size(instr));
}

void part1(char *stacks[], size_t stacks_lens[], int *instr, size_t num_instr) {
    int move, from_idx, to_idx;
    for (int i = 0; i < num_instr*3; i = i+3) {
        move = instr[i];
        // indices start at zero
        from_idx = instr[i+1] - 1;
        to_idx = instr[i+2] - 1;
        // enlarge target stack
        stacks[to_idx] = realloc(stacks[to_idx], (stacks_lens[to_idx] + move) * sizeof(char));
        // move items
        for (int i = 0; i < move; i++) {
            stacks_lens[from_idx]--;
            stacks[to_idx][stacks_lens[to_idx]] = stacks[from_idx][stacks_lens[from_idx]];
            stacks_lens[to_idx]++;
        }
        // shrink source stack
        stacks[from_idx] = realloc(stacks[from_idx], stacks_lens[from_idx] * sizeof(char));
    }
}

void part2(char *stacks[], size_t stacks_lens[], int *instr, size_t num_instr) {
    int move, from_idx, to_idx;
    for (int i = 0; i < num_instr*3; i = i+3) {
        move = instr[i];
        // indices start at zero
        from_idx = instr[i+1] - 1;
        to_idx = instr[i+2] - 1;
        // enlarge target stack
        stacks[to_idx] = realloc(stacks[to_idx], (stacks_lens[to_idx] + move) * sizeof(char));
        // move items
        int curr_from = stacks_lens[from_idx] - move;
        for (int i = 0; i < move; i++) {
            stacks[to_idx][stacks_lens[to_idx]] = stacks[from_idx][curr_from];
            curr_from++;
            stacks_lens[to_idx]++;
        }
        // shrink source stack
        stacks_lens[from_idx] = stacks_lens[from_idx] - move;
        stacks[from_idx] = realloc(stacks[from_idx], stacks_lens[from_idx] * sizeof(char));
    }
}

int main(void) {
    /*
    const char INPUT_FILE[] = "test_input.txt";
    */
    const char INPUT_FILE[] = "real_input.txt";

    // https://en.cppreference.com/w/c/io/fopen
    FILE *fp = fopen(INPUT_FILE, "r");
    
    // get number of stacks
    size_t num_stacks = get_num_stacks(fp);
    
    // create array of stacks
    char *stacks[num_stacks];
    size_t stacks_lens[num_stacks];
    for (int i = 0; i < num_stacks; i++) {
        // https://en.cppreference.com/w/c/memory/malloc
        stacks[i] = malloc(0);
        stacks_lens[i] = 0;
    }

    // fill stacks
    fill_stacks(fp, stacks, stacks_lens);

    // reverse stacks
    reverse_stacks(stacks, stacks_lens, num_stacks);
    //print_stacks(stacks, stacks_lens, num_stacks);

    // skip over empty line
    // https://en.cppreference.com/w/c/io/fseek
    fseek(fp, 2, SEEK_CUR);

    // get instructions
    int *instr;
    size_t num_instr = get_instructions(fp, &instr);
    //print_instructions(instr, num_instr);

    fclose(fp);

    // Part 1
    part1(stacks, stacks_lens, instr, num_instr);
    printf("Part 1: ");
    print_top(stacks, stacks_lens, num_stacks);
    
    // set up for part 2
    fp = fopen(INPUT_FILE, "r");
    for (int i = 0; i < num_stacks; i++) {
        free(stacks[i]);
        stacks[i] = malloc(0);
        stacks_lens[i] = 0;
    }
    fill_stacks(fp, stacks, stacks_lens);
    reverse_stacks(stacks, stacks_lens, num_stacks);
    fclose(fp);

    // Part 2
    part2(stacks, stacks_lens, instr, num_instr);
    printf("Part 2: ");
    print_top(stacks, stacks_lens, num_stacks);

    // clean up
    for (int i = 0; i < num_stacks; i++) free(stacks[i]);
    free(instr);

    exit(EXIT_SUCCESS);
}