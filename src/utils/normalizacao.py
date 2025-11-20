import unicodedata
import re

def remove_numeros_e_simbolos(texto: str):
    return re.sub(r'[^a-zA-ZÀ-ÿ\s]', ' ', texto)

def remove_letras(texto: str):
    return re.sub(r'[A-Za-z]', '', texto)

def get_mes_da_data(data: str):
    if not data:
        return None

    texto = str(data).strip()

    padrao = re.compile(
        r"^"
        r"(?:"
        # ----- DATA COMPLETA (DD/MM/YYYY) -----
        r"(0?[1-9]|[12]\d|3[01])"        # dia
        r"[./-]"                         # separador
        r"(0?[1-9]|1[0-2])"              # mês
        r"[./-]"
        r"(20\d{2})"                     # ano

        r"|"

        # ----- APENAS MÊS/ANO (MM/YY ou MM/YYYY) -----
        r"(0?[1-9]|1[0-2])"
        r"[./-]"
        r"(20\d{2}|\d{2})"               # ano
        r")"
        r"$"
    )

    match = padrao.match(texto)
    if not match:
        return None

    mes = match.group(2) or match.group(4)
    return int(mes)

def extrai_data_mes_ano(texto: str):
    if not texto:
        return None

    padrao = re.compile(
        r"(?<!\d)"
        r"("
        r"(0?[1-9]|[12]\d|3[01])"           # dia (1–31)
        r"[.\-/\s]"                          # separador
        r"(0?[1-9]|1[0-2])"                 # mês (1–12)
        r"[.\-/\s]"                          # separador
        r"(20\d{2})"
        r"|"
        r"(0?[1-9]|1[0-2])"                 # mês
        r"[.\-/\s]"                          # separador
        r"(20\d{2}|\d{2})"                   # ano curto ou completo
        r")"
        r"(?!\d)"
    )

    result = padrao.search(texto)

    if not result:
        return None

    return result.group(0)

def normalizar_mes(valor):
    if not valor:
        return None

    if str(valor).isdigit() and int(valor) < 13 and int(valor) > 0:
        return int(valor)

    texto = str(valor).strip().lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    data_numerica = extrai_data_mes_ano(texto)

    match = get_mes_da_data(data_numerica)

    if match:
        numero = match
        if 1 <= numero <= 12:
            return int(numero)

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
                return int(numero)

    return None
