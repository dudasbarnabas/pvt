import pandas as pd

def main(csv_path):
    df = pd.read_csv(csv_path)
    
    for row in df.index:
        if row == 0:
            continue
        else:
            if pd.notna(df.at[row, "rt_s"]) and pd.notna(df.at[row-1, "rt_s"]):
                rt_c = df.at[row, "rt_s"]
                rt_p = df.at[row-1, "rt_s"]
                df.at[row, "rt_diff"] = abs(rt_c - rt_p)

    df = df[["participant", "session", "trial", "foreperiod_s", "outcome", "rt_s", "rt_diff", "rt_ms", "false_start_time_s", "lapse_500ms", "miss"]]
    df.to_csv(csv_path)
    return df

if __name__ == "__main__":
    df = main("tester/tester_csv.csv")
    print(df)
    df.to_csv("export.csv")