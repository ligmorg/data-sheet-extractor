import pandas as pd

def get_header_index(df: pd.DataFrame) -> int:
    mask = df.apply(lambda col: col.astype(str).str.contains("EAN", case=False, na=False))
    header_index = mask.any(axis=1)[::-1].idxmax()
    return header_index


def main():
    df = pd.read_excel("mapa.xlsx", sheet_name="Mapa Millenium ES", header=None)
    header_index = get_header_index(df)
    df = pd.read_excel("mapa.xlsx", sheet_name="Mapa Millenium ES", header=header_index)
    for index, row in df.iterrows():
        print(row['EAN'])



if __name__ == "__main__":
    main()
