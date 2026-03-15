import pandas as pd

URL = "https://datasets.imdbws.com/name.basics.tsv.gz"
df = pd.read_csv(
    URL,
    sep="\t",
    compression="gzip",
    usecols=["nconst", "primaryName", "primaryProfession", "knownForTitles"],
)

df = df[df["primaryProfession"].str.contains("act", na=False)]

print(df)
