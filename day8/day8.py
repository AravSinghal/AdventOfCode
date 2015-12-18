import pyperclip
import re
import collections

def copy_to_clipboard(string):
    pyperclip.copy(str(string))

result = 0

def process(line = ''):
    global result

    line = line.strip()

    original = len(line)

    p = re.compile(r'(\\|")')
    encoded = len(re.sub(p, '00', line)) + 2

    result += encoded - original

def end_process():
    global result


def process_input():
    with open("day8/input.txt") as file:
        for line in file:
            process(line.rstrip())

def main():
    global result

    process_input()
    end_process()

    copy_to_clipboard(result)
    print(result)

main()