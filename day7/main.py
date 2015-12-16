import pyperclip
import re
import collections

def copy_to_clipboard(string):
    pyperclip.copy(str(string))

result = 0
wires = {}
operators = "AND    OR     LSHIFT RSHIFT NOT"
opL = 7

def try_parse(s = ''):
    try:
        return int(s)
    except ValueError:
        return s

def get_operator(s = ''):
    idx = operators.find(s)
    if idx == -1:
        return None
    return idx // opL + 1

def unsigned_complement(n = 0):
    return ~n + (1 << 16)

def get_wire_value(wire = ''):
    val = try_parse(wires.get(wire))
    if isinstance(val, int):
        return val
    else:
        res = perform_operation(val)
        apply_wire(wire, res)
        return res

def perform_operation(operation = ''):
    if isinstance(operation, int):
        return operation

    tokens = [x.rstrip() for x in operation.split()]
    operands = []
    op = None

    for token in tokens:
        o = get_operator(token)
        if o:
            op = o
        else:
            val = try_parse(token)
            if isinstance(val, int):
                operands.append(val)
            else:
                operands.append(get_wire_value(val))
            
    res = operands[0]
    if op == 1:
        res = operands[0] & operands[1]
    elif op == 2:
        res = operands[0] | operands[1]
    elif op == 3:
        res = operands[0] << operands[1]
    elif op == 4:
        res = operands[0] >> operands[1]
    elif op == 5:
        res = unsigned_complement(operands[0])

    return res

def apply_wire(wire = '', value = None):
    if not value:
        wires[wire] = perform_operation(wires[wire])
    else:
        wires[wire] = value

def create_wire(wire='', operation=''):
    wires[wire] = operation

def process(line = ''):
    global result, wires
    p = re.compile(r'(.+) -> ([a-z]+)')
    m = re.match(p, line)
    if m:
        create_wire(m.group(2), m.group(1))

def end_process():
    global result

    for w in sorted(wires.keys()):
        apply_wire(w)

    result = wires['a']


def process_input():
    with open("input.txt") as file:
        for line in file:
            process(line.rstrip())

def main():
    global result
    # First pass
    process_input()
    end_process()

    # Second pass
    process_input()
    wires['b'] = result
    end_process()

    copy_to_clipboard(result)
    print(result)

main()