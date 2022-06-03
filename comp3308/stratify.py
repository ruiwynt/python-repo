import pandas as pd

def stratify_csv(path):
    df = pd.read_csv(path)
    # df_stratified = stratify_data(df, "classification", ("yes", "no"), (0.35, 0.65))
    df_stratified = df

    df_yes = df_stratified.loc[df_stratified['classification'] == "yes"].sample(frac=1)
    df_no = df_stratified.loc[df_stratified['classification'] == "no"].sample(frac=1)

    folds = [[] for _ in range(10)]

    i = 0
    counter = 0
    while i < len(df_yes):
        folds[counter].append(list(df_yes.iloc[i]))
        counter = (counter + 1) % 10
        i += 1

    i = 0
    while i < len(df_no):
        folds[counter].append(list(df_no.iloc[i]))
        counter = (counter + 1) % 10
        i += 1

    return folds

def write_csv(folds):
    with open("stratified-CFS.csv", "w") as f:
        for i in range(10):
            f.write(f"fold{i+1}\n")
            for line in folds[i]:
                f.write(",".join(map(str, line)) + "\n")
            f.write("\n")

if __name__ == "__main__":
    write_csv(stratify_csv("pima-CFS.csv"))