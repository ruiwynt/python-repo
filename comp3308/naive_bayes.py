import numpy as np

def read_file(filename):
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            row = line.strip().split(",")
            for i in range(len(row)):
                if row[i].isnumeric():
                    row[i] = float(row[i])
            data.append(row)
    return data

def filter_dataset(dataset, class_cat):
    return dataset[dataset[:, -1] == class_cat]

def fnorm(q, mu, sigma):
    return (1/(sigma*np.sqrt(2 * np.pi)))*np.exp(-((q-mu)**2)/(2*sigma**2))

def classify_nb(training_filename, testing_filename):
    training = np.array(read_file(training_filename))
    yes_means = np.array(filter_dataset(training, "yes")[:,:-1], dtype=np.float64).mean(axis=0)
    no_means = np.array(filter_dataset(training, "no")[:,:-1], dtype=np.float64).mean(axis=0)
    yes_stds = np.array(filter_dataset(training, "yes")[:,:-1], dtype=np.float64).std(axis=0, ddof=1)
    no_stds = np.array(filter_dataset(training, "no")[:,:-1], dtype=np.float64).std(axis=0, ddof=1)
    p_yes = len(filter_dataset(training, "yes"))/len(training)
    p_no = len(filter_dataset(training, "no"))/len(training)

    testing = np.array(read_file(testing_filename), dtype=np.float64)
    classes = []
    for observation in testing:
        yes_bayes = np.prod(fnorm(observation, yes_means, yes_stds))*p_yes
        no_bayes = np.prod(fnorm(observation, no_means, no_stds))*p_no
        classification = "yes" if yes_bayes >= no_bayes else "no"
        classes.append(classification)

    return classes

result = classify_nb("training.csv", "testing.csv")