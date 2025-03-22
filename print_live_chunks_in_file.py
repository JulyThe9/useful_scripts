import sys

def read_json_block(file):
    json_block = ""
    depth = 0  # Track the depth of nested brackets
    count = 0
    for line in file:
        count+=1
        json_block += line
        depth += line.count('[') - line.count(']')
        if depth == 0:  # All brackets are closed
            break
    return json_block, count

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <filename> <position>")
    sys.exit(1)

filename = sys.argv[1]

def print_chunk(file, start, end, lines):
    file.seek(start)
    chunk = file.read(end - start - (lines + 1))
    print('====================================')
    print(chunk)

def read_events():
    pos = 0
    iter = 0
    while True:
        with open(filename, 'r') as file:
            file.seek(pos)
            line = file.readline()
            if line.strip().startswith("Price update event"):
                json_block, num_lines = read_json_block(file)
                prev_pos = pos
                pos += len(json_block) + len(line) + 1 + num_lines
                print_chunk(file, prev_pos, pos, 1 + num_lines)

            elif len(line) > 1:
                prev_pos = pos
                pos += len(line) + 1
                print_chunk(file, prev_pos, pos, 1)

            elif len(line) == 1:
                pos += 1

read_events()
