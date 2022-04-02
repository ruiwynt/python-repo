def read_lines():
    with open("rfc-6455.txt", "r") as f:
        while True:
            line = f.readline()
            yield line

def grep(pattern):
    while True:
        line = (yield)
        if pattern in line:
            print(line)