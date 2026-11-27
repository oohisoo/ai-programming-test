import pandas as pd
from pathlib import Path

df = pd.read_csv(Path(__file__).parent / "scores_2026.csv")

print(df.shape)
print(df["점수"].isna().sum())
print(df.duplicated().sum())
print(df["반"].unique())
print(df["과목"].unique())
print(df["점수"].describe())