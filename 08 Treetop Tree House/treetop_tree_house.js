// https://adventofcode.com/2022/day/8

const fs = require("fs");

let input_file = "real_input.txt";
//input_file = "test_input.txt";

const trees = fs.readFileSync(input_file, "utf8").split("\n");

function union(setA, setB) {
    const _union = new Set(setA);
    for (const elem of setB) {
        _union.add(elem);
    }
    return _union;
}

// Setup

let tree_rows = [];
for (let x in trees) {
    let row = [];
    for (let y in trees[x].trimEnd()) {
        row.push({ x: x, y: y, height: trees[x][y] });
    }
    tree_rows.push(row);
}

// Part 1

function visible(trees) {
    // For simplicity, this function only looks to the left
    let highest_left = trees[0].height;
    let visible = new Set([trees[0]]);
    for (let i = 1; i < trees.length; i++) {
        if (trees[i].height > highest_left) {
            visible.add(trees[i]);
            highest_left = trees[i].height;
        }
    }
    return visible;
}

let visible_left = new Set();
let visible_right = new Set();
for (let row in tree_rows) {
    visible_left = union(visible_left, visible(tree_rows[row]));
    let row_rev = [...tree_rows[row]];
    row_rev.reverse();
    visible_right = union(visible_right, visible(row_rev));
}

let visible_up = new Set();
let visible_down = new Set();
for (let x = 0; x < tree_rows[0].length; x++) {
    let col = [];
    for (let y = 0; y < tree_rows.length; y++) {
        col.push(tree_rows[y][x]);
    }
    visible_up = union(visible_up, visible(col));
    let col_rev = [...col];
    col_rev.reverse();
    visible_down = union(visible_down, visible(col_rev));
}

const visible_horizontal = union(visible_left, visible_right);
const visible_vertical = union(visible_up, visible_down);
const visible_total = union(visible_horizontal, visible_vertical);
console.log(visible_total.size);
