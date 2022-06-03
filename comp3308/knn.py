def read_file(filename):
    rows = []
    with open(filename) as f:
        for row in f.readlines():
            split_row = row.strip().split(',')
            for i in range(len(split_row)):
                if split_row[i].isnumeric():
                    split_row[i] = float(split_row[i])
            rows.append(split_row)
    return rows

import numpy as np

def classify_nn(training_filename, testing_filename, k):
    training = read_file(training_filename)
    testing = read_file(testing_filename)
    classes = []
    for i in range(len(testing)):
        row = np.array(testing[i], dtype=np.float64)
        distances = []
        for j in range(len(training)):
            training_row = np.array(training[j][:-1], dtype=np.float64)
            distance = np.linalg.norm(row - training_row)
            distances.append((distance, training[j][-1]))
        distances = sorted(distances, key=lambda x: x[0])
        decision = 0
        for j in range(k):
            decision = decision + 1 if distances[j][1] == "yes" else decision - 1
        if decision > 0:
            classes.append("yes")
        elif decision < 0:
            classes.append("no")
    return classes

results = classify_nn("training.csv", "testing.csv", 5)