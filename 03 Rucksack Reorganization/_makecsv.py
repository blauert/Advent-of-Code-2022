import csv

for input_file in ['real_input', 'test_input']:

    with open(f'{input_file}.txt') as file:
        lines = [i.strip() for i in file.readlines()]

    # Part 1
    with open(f'{input_file}_1.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['comp1', 'comp2'])
        for line in lines:
            half = len(line)//2
            row = [';'.join(line[:half]), ';'.join(line[half:])]
            spamwriter.writerow(row)

    # Part 2
    with open(f'{input_file}_2.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['elf1', 'elf2', 'elf3'])
        for i in range(0, len(lines), 3):
            sack1, sack2, sack3 = lines[i], lines[i+1], lines[i+2]
            row = [';'.join(sack1), ';'.join(sack2), ';'.join(sack3)]
            spamwriter.writerow(row)