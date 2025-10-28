import pandas as pd

def main():
    df = pd.read_excel('../data/2025-metrics-tiny-processed.xlsx')
    print(df.head())  # Displays the first 5 rows of the DataFrame


if __name__ == "__main__":
    main()