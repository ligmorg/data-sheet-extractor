import argparse
import logging
import pandas as pd
from tqdm import tqdm
from extractor.produto_extractor import extract_products
from models.produto import Produto
from utils.normalizacao import normalizar_mes

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("extractor.log"),
            logging.StreamHandler()
        ]
    )

    parser = argparse.ArgumentParser(description="Extrai produtos de um arquivo Excel")
    parser.add_argument("arquivo", help="Caminho do arquivo Excel")
    args = parser.parse_args()

    excel_file = pd.ExcelFile(args.arquivo)

    sheets = excel_file.sheet_names
    produtos = []
    vendas = []
    errors = {}

    for sheet in tqdm(sheets):
        sheet_errors = extract_products(args.arquivo, sheet, produtos, vendas)
        if sheet_errors:
            errors[sheet] = sheet_errors

    logger.info("%s erros encontrados:", len(errors))
    for nome, erro_lista in errors.items():
        logger.warning("Erros na planilha %s:", nome)
        for e in erro_lista:
            logger.warning("  - %s", e)

    logger.info(f"\n{len(produtos)} produtos encontrados:")
    for p in produtos:
        print(p)


if __name__ == "__main__":
    main()
