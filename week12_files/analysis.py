def 반별평균(df):
    return df.groupby("반")["점수"].mean()
def 정제(df):
    df = df.copy()
    df = df.dropna(subset=["점수"])
    print(f"점수 결측 제거 후: {len(df)}행")

    df = df.drop_duplicates()
    print(f"중복 제거 후: {len(df)}행")

   # df["반"] = df["반"].str.strip()
    #df["과목"] = df["과목"].str.strip()
    print(f"공백 제거 후: {len(df)}행")

    df = df[df["점수"].between(0, 1000)]
    print(f"점수 범위 정제 후: {len(df)}행")

    return df
if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path

    df = pd.read_csv(Path(__file__).parent / "scores_2026.csv")
    print("시작:", len(df))
    df = 정제(df)

    print("반 종류:", sorted(df["반"].unique()))
    print("과목 종류:", sorted(df["과목"].unique()))
    수학 = df[df["과목"] == "수학"]
    print("수학 행 수:", len(수학))
    print("수학 점수 요약:", 수학["점수"].describe())
    print("반별 평균")
    print(df.groupby("반")["점수"].mean())

    print("과목별 반별 평균")
    print(df.groupby(["과목", "반"])["점수"].mean())
    print("반별 통계")
    print(df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2))
    print("반별 점수 합계:", df.groupby("반")["점수"].sum().sum())
    print("전체 점수 합계:", df["점수"].sum())

    print("반별 데이터 개수 합계:", df.groupby("반")["점수"].count().sum())
    print("전체 데이터 개수:", len(df))

    print("1반 수학 점수:")
    print(df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"])
    print("mini.csv 검증")
    미니 = 정제(pd.read_csv(Path(__file__).parent / "mini.csv"))
    print("정제 후 행 수:", len(미니))
    print(미니.groupby("반")["점수"].mean())
    def 반별평균(df):
        return df.groupby("반")["점수"].mean()