import sys
def get_id(word_id):
    id = word_id[1]
    return id

def process_line(line):
    parts = line.replace(':','').split()
    print(parts)

def process_file(input_file):
    with open(input_file, "r") as inputF:
        linesF = inputF.readlines()
        line = 0

        while line < len(linesF):
            process_line(linesF[line])
            line += 1

input_file = sys.argv[1]
process_file(input_file)