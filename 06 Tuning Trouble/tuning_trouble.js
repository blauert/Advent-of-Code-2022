// https://adventofcode.com/2022/day/6

const fs = require("fs");

let input_file = "real_input.txt";
//input_file = "test_input.txt";

const buffer = fs.readFileSync(input_file, "utf8");

function first_occurence(num_chars) {
    let char_count = {};
    let unique_chars = 0;
    for (let i = 0; i < buffer.length; i++) {
        // Take next char
        let next_char = buffer[i];
        if (!(next_char in char_count)) char_count[next_char] = 0;
        char_count[next_char] += 1;
        if (char_count[next_char] === 1) unique_chars++;
        // Drop previous char
        if (i >= num_chars) {
            let prev_char = buffer[i - num_chars];
            char_count[prev_char] -= 1;
            if (char_count[prev_char] === 0) unique_chars--;
        }
        if (unique_chars === num_chars) return i + 1;
    }
}

console.log(first_occurence(4));

console.log(first_occurence(14));
