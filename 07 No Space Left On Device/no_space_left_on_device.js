// https://adventofcode.com/2022/day/6

const fs = require("fs");

let input_file = "real_input.txt";
//input_file = "test_input.txt";

const terminal_output = fs.readFileSync(input_file, "utf8").split("\n");

class Dir {
    constructor(name, parent = null) {
        this.name = name;
        this.parent = parent;
        this.subdirs = {};
        this.files = {};
    }
}

function build_tree(terminal_output) {
    const root = new Dir("/");
    let curr_dir = null;
    let ls = false;
    for (let i in terminal_output) {
        let line = terminal_output[i].trimEnd().split(" ");
        if (line[0] === "$") {
            ls = false;
            if (line[1] === "cd") {
                if (line[2][0] === "/") {
                    curr_dir = root;
                } else if (line[2] === "..") {
                    curr_dir = curr_dir.parent;
                } else {
                    curr_dir = curr_dir.subdirs[line[2]];
                }
            } else if (line[1] === "ls") {
                ls = true;
            }
        } else if (!!ls) {
            if (line[0] === "dir") {
                curr_dir.subdirs[line[1]] = new Dir(line[1], curr_dir);
            } else {
                curr_dir.files[line[1]] = Number(line[0]);
            }
        }
    }
    return root;
}

function folder_sizes(tree) {
    let walk_down = [tree];
    let walk_up = [];
    // Walk down
    while (walk_down.length > 0) {
        let curr_dir = walk_down.pop();
        for (let i in curr_dir.subdirs) {
            walk_down.push(curr_dir.subdirs[i]);
        }
        walk_up.push(curr_dir);
    }
    let sizes_map = new Map();
    let sizes_arr = [];
    // Walk up
    while (walk_up.length > 0) {
        let curr_dir = walk_up.pop();
        let file_sizes = 0;
        for (let i in curr_dir.files) {
            file_sizes += curr_dir.files[i];
        }
        let subdir_sizes = 0;
        for (let i in curr_dir.subdirs) {
            subdir_sizes += sizes_map.get(curr_dir.subdirs[i]);
        }
        let total_size = file_sizes + subdir_sizes;
        sizes_map.set(curr_dir, total_size);
        sizes_arr.push(total_size);
    }
    return sizes_arr;
}

const tree = build_tree(terminal_output);
const sizes = folder_sizes(tree);


// Part 1

let sum_sizes = 0;
for (let size of sizes) {
    if (size <= 100000) sum_sizes += size;
}
console.log(sum_sizes);


// Part 2

const DISK_SPACE = 70000000;
const SPACE_REQUIRED = 30000000;

sizes.sort((a, b) => a - b);
for (let size of sizes) {
    if (size + (DISK_SPACE - sizes[sizes.length - 1]) >= SPACE_REQUIRED) {
        console.log(size);
        break;
    }
}
