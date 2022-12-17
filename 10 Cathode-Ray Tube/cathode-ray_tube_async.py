# https://adventofcode.com/2022/day/10

import asyncio
import os

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    instructions = (line.split() for line in file.readlines())


def make_clear_func():
    if os.name == 'posix':  # Linux & Mac
        clear_param = 'clear'
    else:  # Windows
        clear_param = 'cls'
    def clear_func():
        os.system(clear_param)
    return clear_func

clear_screen = make_clear_func()


# Part 2

def instructions_per_cycle():
    # Get instructions one by one; separate 'addx' and int
    for ins in instructions:
        for i in ins:
            yield i


async def clock_circuit():
    cycle = 0
    while True:
        if cycle < 10:
            await asyncio.sleep(0.5)
        elif cycle < 50:
            await asyncio.sleep(0.05)
        else:
            await asyncio.sleep(0.005)
        cycle += 1
        yield cycle


async def cpu():
    addx = False
    x = 1  # Register
    while True:
        instruction = yield x
        # Set register value
        if instruction == 'addx':
            addx = True
        elif addx:
            x += int(instruction)
            addx = False


async def crt():
    pixels = [' ' for i in range(240)]
    curr_pixel = 0
    curr_row = 0
    
    while True:
        # Calculate sprite position
        x = yield
        x = curr_row * 40 + x

        # Set current pixel
        if curr_pixel < len(pixels):
            pixels[curr_pixel] = '.'
        if curr_pixel >= x-1 and curr_pixel <= x+1:
            pixels[curr_pixel] = '#'

        # Setup for next cycle
        curr_pixel += 1
        if curr_pixel > 0 and curr_pixel % 40 == 0:
            curr_row += 1

        # Print CRT screen
        clear_screen()
        for i, pix in enumerate(pixels):
            # Sprite
            space1 = ' '
            space2 = ''
            if i == x-1:
                space1 = '['
            elif i == x+1:
                space2 = ']'
            elif i == x+2:
                space1 = ''
            # Break row
            if i > 0 and i % 40 == 0:
                print()
                # Reset space for first pixel after linebreak
                if i == x+2:
                    space1 = ' '
            # Draw pixel
            print(f"{space1}{pix}{space2}", end='')
        print()  # final linebreak; necessary for clear_screen() to work properly


async def main():
    instructions = instructions_per_cycle()
    # Start CPU
    processor = cpu()
    x = await processor.asend(None)
    # Start CRT
    screen = crt()
    _ = await screen.asend(None)
    # Start clock
    async for cycle in clock_circuit():
        # Get next instruction
        try:
            ins = next(instructions)
        except StopIteration:
            # Print screen one final time, with sprite out of the way
            _ = await screen.asend(10)
            break
        # Send sprite position to CRT
        _ = await screen.asend(x)
        # Send instruction to CPU
        x = await processor.asend(ins)


if __name__ == '__main__':
    asyncio.run(main())