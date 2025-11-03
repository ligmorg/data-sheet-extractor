import pandas as pd
from produto import Produto


def get_header_index(df: pd.DataFrame) -> int:
    mask = df.apply(lambda col: col.astype(str).str.contains("EAN", case=False, na=False))
    header_index = mask.any(axis=1)[::-1].idxmax()
    return header_index

def get_column(name: str, columns: list):
    column = [item for item in columns if isinstance(item, str) and name in item.upper()]
    return column[0]

def produto_unico(ean: str, lista_prods: list[Produto]) -> bool:
    for prod in lista_prods:
        if prod.ean == ean:
            return False

    return True


def extract_products(file, sheet, produtos):
    df = pd.read_excel(file, sheet_name=sheet, header=None)
    header_index = get_header_index(df)
    df = pd.read_excel(file, sheet_name=sheet, header=header_index)
    print(sheet)
    if not df.empty:
        ean_column = get_column('EAN', df.columns)
        for index, row in df.iterrows():
            if not pd.isna(row[ean_column]) and produto_unico(row[ean_column], produtos):
                produtos.append(Produto(row[ean_column]))
    else:
        print(f"nao foi encontrado o EAN da sheet {sheet}")


def main():
    excel_file = pd.ExcelFile("mapa.xlsx")
    sheets = excel_file.sheet_names
    produtos = []
    for sheet in sheets:
        extract_products("mapa.xlsx", sheet, produtos)

    print(f"{len(produtos)} produtos encontrados")
    for p in produtos:
        print(p)


if __name__ == "__main__":
    main()
