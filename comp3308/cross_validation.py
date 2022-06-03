import numpy as np
import pandas as pd
import time
from stratify import stratify_csv

def MykNN(training, testing, k):
    t1 = time.time()
    training = np.array(training)
    training_noresults = np.array(training[:,:-1], dtype=np.float64)
    training_classes = training[:,-1]
    training_map = np.array(tuple(map(lambda x: 1 if x == "yes" else -1, training_classes)), dtype=np.int32)
    t2 = time.time()
    training_time = 10**3*(t2 - t1)

    classes = []
    t1 = time.time()
    for i in range(len(testing)):
        row = np.array(testing[i], dtype=np.float64)
        distances = np.linalg.norm(training_noresults - row, axis=1)
        min_distance_idx = np.argpartition(distances, k)
        k_nearest_classes = training_map[min_distance_idx[:k]]
        if k_nearest_classes.sum() > 0:
            classes.append("yes")
        else:
            classes.append("no")
    t2 = time.time()
    testing_time = 10**3*(t2-t1)
    return classes, training_time, testing_time

def filter_dataset(dataset, class_cat):
    return dataset[dataset[:, -1] == class_cat]

def fnorm(q, mu, sigma):
    return (1/(sigma*np.sqrt(2 * np.pi)))*np.exp(-((q-mu)**2)/(2*sigma**2))

def MyNB(training, testing):
    training = np.array(training)
    t1 = time.time()
    yes_means = np.array(filter_dataset(training, "yes")[:,:-1], dtype=np.float64).mean(axis=0)
    no_means = np.array(filter_dataset(training, "no")[:,:-1], dtype=np.float64).mean(axis=0)
    yes_stds = np.array(filter_dataset(training, "yes")[:,:-1], dtype=np.float64).std(axis=0, ddof=1)
    no_stds = np.array(filter_dataset(training, "no")[:,:-1], dtype=np.float64).std(axis=0, ddof=1)
    p_yes = len(filter_dataset(training, "yes"))/len(training)
    p_no = len(filter_dataset(training, "no"))/len(training)
    t2 = time.time()
    training_time = (10**3)*(t2 - t1)

    testing = np.array(testing, dtype=np.float64)
    classes = []
    t1 = time.time()
    for observation in testing:
        yes_bayes = np.prod(fnorm(observation, yes_means, yes_stds))*p_yes
        no_bayes = np.prod(fnorm(observation, no_means, no_stds))*p_no
        classification = "yes" if yes_bayes >= no_bayes else "no"
        classes.append(classification)
    t2 = time.time()
    testing_time = (10**3)*(t2 - t1)

    return classes, training_time, testing_time

def read_folded_dataset(path):
    folds = []
    with open(path, "r") as f:
        fold_no = -1
        for line in f.readlines():
            if "fold" in line:
                folds.append([])
                fold_no += 1
            else:
                if line.strip() != "":
                    split_line = line.strip().split(',')
                    for i in range(len(split_line)):
                        if split_line[i].isnumeric():
                            split_line[i] = float(split_line[i])
                    folds[fold_no].append(split_line)
    return folds

def k_fold_cv(dataset_filename, k, runs, classification_function, *args):
    print(f"Performing {k}-fold validation on {classification_function.__name__}{args} for {runs} runs:")
    dataset = dataset_filename.split('.')[0]
    classifier = classification_function.__name__
    classifier = classifier + str(args[0]) if len(args) > 0 else classifier
    run_accuracies = []
    run_training_times = []
    run_testing_times = []
    run_data = []
    for run in range(runs):
        data = stratify_csv(dataset_filename)
        accuracies = []
        training_times = []
        testing_times = []
        for i in range(len(data)):
            testing = np.array(np.array(data[i], dtype=object)[:,:-1], dtype=np.float64)
            training = []
            for j in range(len(data)):
                if j != i:
                    training += data[j]
            result, training_time, testing_time = classification_function(training, testing, *args)
            expected = np.array(np.array(data[i])[:,-1])
            accuracy = np.mean(np.array(result) == expected)
            accuracies.append(accuracy)
            training_times.append(training_time)
            testing_times.append(testing_time)
            run_data.append((dataset, run+1, i+1, classifier, accuracy*100, training_time, testing_time))
        accuracies = np.array(accuracies, dtype=np.float64)
        run_accuracies.append(np.mean(accuracies))
        training_times = np.array(training_times, dtype=np.float64)
        run_training_times.append(np.mean(training_times))
        testing_times = np.array(testing_times, dtype=np.float64)
        run_testing_times.append(np.mean(testing_times))
    result_df = pd.DataFrame(run_data, columns = ("dataset", "run", "fold", "classifier", "percent_correct", "training_time_ms", "testing_time_ms"))
    print(f"Accuracy: {round(np.mean(run_accuracies)*100, 2)} +- {round(np.std(run_accuracies, ddof=1)*100, 2)}")
    print(f"Average Training Time (ms): {round(np.mean(run_training_times), 2)} +- {round(np.std(run_training_times, ddof=1), 2)}")
    print(f"Average Testing Time (ms): {round(np.mean(run_testing_times), 2)} +- {round(np.std(run_testing_times, ddof=1), 2)}")
    print("")
    return result_df

if __name__ == "__main__":
    k = 10
    runs = 10
    result_dfs = []
    result_dfs.append(k_fold_cv("pima.csv", k, runs, MykNN, 1))
    result_dfs.append(k_fold_cv("pima.csv", k, runs, MykNN, 5))
    result_dfs.append(k_fold_cv("pima.csv", k, runs, MyNB))
    result_dfs.append(k_fold_cv("pima-CFS.csv", k, runs, MykNN, 1))
    result_dfs.append(k_fold_cv("pima-CFS.csv", k, runs, MykNN, 5))
    result_dfs.append(k_fold_cv("pima-CFS.csv", k, runs, MyNB))
    final_df = pd.concat(result_dfs)
    final_df.to_csv("myclassifiers-cleaned.csv", index=False)