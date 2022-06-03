import pandas as pd

weka = pd.read_csv("weka-cleaned.csv")
mine = pd.read_csv("myclassifiers-cleaned.csv")

aggregated = pd.concat((weka, mine))
aggregated.to_csv("all-results-cleaned.csv", index=False)