def get_items(path):
    with open(path, "r") as f:
        items = [tuple(map(int, line.split())) for line in f]
        return items

if __name__ == "__main__":
    items = get_items("items.txt")
