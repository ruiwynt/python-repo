algorithms = (
        "ZeroR",
        "1R",
        "1NN",
        "5NN",
        "NB",
        "DT",
        "MLP",
        "SVM",
        "RF",
        "My1NN",
        "My5NN",
        "MyNB"
    )

datasets = ("pima", "pima-CFS")

with open("pair_results.csv", "r") as raw:
    lines_iter = raw.readlines()
    with open("normalised_results.csv", "w") as results:
        for dataset in datasets:
            for algorithm in algorithms:
                line = list(map(float, lines_iter.next().strip().split(",")))
                line = [dataset, algorithm] + line

