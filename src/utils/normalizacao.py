import unicodedata
import re

def remove_numeros_e_simbolos(texto: str):
    return re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', texto)

def remove_letras(texto: str):
    return re.sub(r'[^a-zA-ZÀ-ÿ]', '', texto)

def normalizar_mes(valor):
    if not valor:
        return None

    texto = str(valor).strip().lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    match = re.match(r"^0?(\d{1,2})", texto)
    print(match)

    #TODO: verificar se o numero tem so dois digitos msm
    if match:
        numero = int(match.group(1))
        if 1 <= numero <= 12:
            return numero

    matches = remove_numeros_e_simbolos(texto).split()

    meses = {
        "jan": 1, "janeiro": 1,
        "fev": 2, "fevereiro": 2,
        "mar": 3, "marco": 3,
        "abr": 4, "abril": 4,
        "mai": 5, "maio": 5, "may": 5,
        "jun": 6, "junho": 6,
        "jul": 7, "julho": 7,
        "ago": 8, "agosto": 8,
        "set": 9, "setembro": 9,
        "out": 10, "outubro": 10,
        "nov": 11, "novembro": 11,
        "dez": 12, "dezembro": 12,
    }

    for match in matches:
        for mes, numero in meses.items():
            if match == mes:
                return numero

    return None
