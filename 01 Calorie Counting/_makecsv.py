import csv

for input_file in ['real_input', 'test_input']:

    with open(f'{input_file}.txt') as file:
        cals = [i.strip() for i in file.readlines()]

    with open(f'{input_file}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        elf_id = 0
        for c in cals:
            if c:
                spamwriter.writerow([f'elf{elf_id}', c])
            else:
                elf_id += 1