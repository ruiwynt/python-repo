import pandas as pd 

df = pd.read_csv("weka-raw.csv")

cols = [
        "Key_Dataset", 
        "Key_Run", 
        "Key_Fold", 
        "Key_Scheme", 
        "Key_Scheme_options", 
        "Percent_correct", 
        "Elapsed_Time_training", 
        "Elapsed_Time_testing"
    ]

df = df[cols]
df.columns = tuple(map(str.lower, df.columns))

map_keyscheme = lambda x: x[4] if x.startswith("'-K") else ""

df["key_scheme_options"] = df.key_scheme_options.apply(map_keyscheme)

df["key_scheme"] = df["key_scheme"] + df["key_scheme_options"]
del df["key_scheme_options"]

get_classifier_name = lambda x: x.split(".")[-1]
df["key_scheme"] = df.key_scheme.apply(get_classifier_name)

df["elapsed_time_training"] = df.elapsed_time_training.apply(lambda x: 1000*x)
df["elapsed_time_testing"] = df.elapsed_time_testing.apply(lambda x: 1000*x)

df.columns = ("dataset", "run", "fold", "classifier", "percent_correct", "training_time_ms", "testing_time_ms")

df.to_csv("weka-cleaned.csv", index=False)