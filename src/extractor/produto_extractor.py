from numpy import indices
import pandas as pd
from utils.helpers import (
    find_product, ean_valido, produto_unico, valida_coluna_estoque
)
from models.produto import Produto
from models.venda_mensal import VendaMensal
from utils.normalizacao import normalizar_mes

variacoes_meses = ["qtd", "quantidade", "unidade"]
variacoes_descricao = ["prod", "descrição", "desc"]
variacoes_estoque = ["disp", "dsp", "estoque", "total", "saldo"]
variacoes_codigo_barras = [
    "Codigo_Barra", "Código_Barra", "cod_barra", "cód barra", "cod barra",
    "codigo de barra", "código de barra", "cod. barra", "codbarra",
    "codigo_barra", "codigo_bar", "codbar", "EAN"
]
def cria_mascara_ocorrencia(df: pd.DataFrame, dictionary):
    pattern = '|'.join([v.replace('.', r'\.') for v in dictionary])
    return df.apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False, regex=True))

def get_column_name(df: pd.DataFrame, dictionary):
    colunas_lower = [col.lower() for col in dictionary]
    for col in df.columns:
        for possivel_col in colunas_lower:
            if possivel_col in str(col).lower():
                return col

def get_column_index(df: pd.DataFrame, dictionary):
    mask = cria_mascara_ocorrencia(df, dictionary)

    any_match = mask.any(axis=0)
    if not any_match.any():
        return -1
    index_linha = mask.any(axis=1)[::-1].idxmax()
    return df.columns.get_loc(mask.iloc[index_linha][::-1].idxmax())

def get_header_index(df: pd.DataFrame) -> int:
    mask = cria_mascara_ocorrencia(df, variacoes_codigo_barras)

    header_index = mask.any(axis=1)[::-1].idxmax()
    return header_index

def existe_duplicatas(mask: pd.Series) -> bool:
    return mask.index.duplicated().any()

def get_months_columns_indexes(df:pd.DataFrame):
    meses = []

    mask = df.apply(lambda col: normalizar_mes(str(col)))
    if mask[mask.notna()].empty:
        for index, col in enumerate(df.columns):
            if isinstance(col, float):
                mes = normalizar_mes(str(int(col)))
            else:
                mes = normalizar_mes(str(col))
            if mes:
                meses.append([index, mes])

        return meses

    indexes = mask.index
    if existe_duplicatas(mask[mask.notna()]):
        for idx, i in enumerate(indexes):
            #verificar se o que esta duplicado eh o mes
            if str(i).lower() in variacoes_meses:
                meses.append([idx, mask.iloc[idx]])
    else:
        for idx, i in enumerate(indexes):
            if pd.notna(mask.iloc[idx]):
                meses.append([idx, mask.iloc[idx]])


    indices_numericos = [[index, int(mes)] for index, mes in meses]

    return indices_numericos


def get_months_columns(columns):
    meses = []
    for col in columns:
        if normalizar_mes(col):
            meses.append(col)

    return meses

def extract_vendas(produto, meses, valores):
    vendas = []
    for mes in meses:
        try:
            valor_mes = int(valores[mes])
        except Exception as e:
            valor_mes = 0
        venda = VendaMensal(produto, None, normalizar_mes(mes), valor_mes)
        vendas.append(venda)
        produto.adiciona_venda(venda)

    return vendas


def extract_products(file: str, sheet: str, produtos: list, vendas: list):
    errors = []
    df = pd.read_excel(file, sheet_name=sheet, header=None)
    df = df.ffill()
    df = df.ffill(axis=1)

    header_index = get_header_index(df)
    df.columns = df.iloc[header_index]

    ean_column_name = get_column_name(df, variacoes_codigo_barras)
    if ean_column_name is None:
        return [f"não foi encontrado o EAN"]

    description_column_name = get_column_name(df, variacoes_descricao)

    estoque_column_name = get_column_name(df, variacoes_estoque)
    estoque_column_index = get_column_index(df, variacoes_estoque)
    estoque_valido = valida_coluna_estoque(estoque_column_index, sheet)


    meses_backup = [mes for mes in get_months_columns_indexes(df) if mes[0] != estoque_column_index]

    drop_header = header_index + 1
    df = df[drop_header:].reset_index(drop=True)

    meses = get_months_columns(df.columns)
    
    if not meses:
        meses = [mes[1] for mes in meses_backup]

    if not estoque_column_name:
        estoque_column_name = "estoque"
        df.rename(columns={df.columns[estoque_column_index]: estoque_column_name}, inplace=True)
    
    if not meses:
        errors.append("nao foram encontrados vendas dos produto")

    for _, row in df.iterrows():
        ean = row.get(ean_column_name)
        if pd.notna(ean) and ean_valido(ean):
            if produto_unico(ean, produtos):
                prod = Produto(str(ean), row[description_column_name], row[estoque_column_name])
                produtos.append(prod)

            else:
                if estoque_valido:
                    try:
                        prod = find_product(ean, produtos)
                        prod.estoque += int(row[estoque_column_name])
                    except Exception:
                        pass
                else:
                    errors.append(f"estoque inválido")

            vendas.extend(extract_vendas(prod, meses, row))

    return errors
