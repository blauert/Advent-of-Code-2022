# https://adventofcode.com/2022/day/8

from collections import namedtuple

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    trees = [[int(i) for i in line.strip()] for line in file.readlines()]


# Setup

Tree = namedtuple('Tree', ['coords', 'height'])

tree_rows = []
for x in range(len(trees)):
    row = []
    for y in range(len(trees[0])):
        row.append(Tree((x, y), trees[x][y]))
    tree_rows.append(row)


# Part 1

def visible(trees):
    highest_left = trees[0].height
    visible = {trees[0], trees[-1]}
    candidates_right = {}
    for tree in trees[1:-1]:
        # Visible from the left
        if tree.height > highest_left:
            visible.add(tree)
            highest_left = tree.height
        # Visible from the right
        if tree.height > trees[-1].height:
            for height in [i for i in candidates_right.keys() if i <= tree.height]:
                del candidates_right[height]
            candidates_right.setdefault(tree.height, []).append(tree)
    for cs in candidates_right.values():
        for c in cs:
            visible.add(c)
    return visible


visible_trees = set()

for row in tree_rows:
    visible_trees |= visible(row)
for col in zip(*tree_rows):
    visible_trees |= visible(col)

print(len(visible_trees))


# Part 2

def scenic_scores_1d(trees):
    scenic_scores = {}
    heights_left = {i: 0 for i in range(10)}
    view_right_temp = {}
    for i, tree in enumerate(trees):
        # View to the left
        scenic_scores[tree] = i - heights_left[tree.height]
        for h in range(tree.height+1):
            heights_left[h] = i
        # View to the right
        done = []
        for tr in view_right_temp:
            view_right_temp[tr] += 1
            if tr.height <= tree.height:
                done.append(tr)
        view_right_temp[tree] = 0
        for tr in done:
            scenic_scores[tr] *= view_right_temp.pop(tr)
    for tr, v in view_right_temp.items():
        scenic_scores.setdefault(tr, 0)
        scenic_scores[tr] *= v
    return scenic_scores


row_scores = {}
max_score = 0

for row in tree_rows:
    row_scores.update(scenic_scores_1d(row))
for col in zip(*tree_rows):
    col_scores = scenic_scores_1d(col)
    for tree, col_score in col_scores.items():
        # Calculate two-dimensional scenic score
        scenic_score = row_scores[tree] * col_score
        max_score = max(max_score, scenic_score)

print(max_score)
