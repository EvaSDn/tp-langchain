# c'est la partir yahoo finace 

import yfinance as yf

def obtenir_cours_action(symbole: str) -> str:
    symbole = symbole.strip().upper()
    try:
        ticker = yf.Ticker(symbole)
        info = ticker.fast_info
        cours = info.last_price
        ouverture = info.open
        variation = ((cours - ouverture) / ouverture) * 100
        volume = info.last_volume
        tendance = '📈' if variation >= 0 else '📉'
        return f"{symbole} {tendance} : {cours:.2f} $ ({variation:+.2f}%) | Volume : {volume:,}"
    except Exception:
        return f"Impossible de récupérer le cours de '{symbole}'. Symbole invalide ou API indisponible."


def obtenir_cours_crypto(symbole: str) -> str:
    symbole = symbole.strip().upper()
    try:
        ticker = yf.Ticker(f"{symbole}-USD")
        info = ticker.fast_info
        cours = info.last_price
        ouverture = info.open
        variation = ((cours - ouverture) / ouverture) * 100
        volume = info.last_volume
        tendance = '📈' if variation >= 0 else '📉'
        return f"{symbole} {tendance} : {cours:.2f} $ ({variation:+.2f}%) | Volume : {volume:,}"
    except Exception:
        return f"Impossible de récupérer le cours de '{symbole}'. Symbole invalide ou API indisponible."