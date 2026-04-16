import yfinance as yf

def calculer_portefeuille(query: str) -> str:
    
    try:
        lignes = query.strip().split("|")
        total_valeur = 0
        total_ouverture = 0
        resultat = "Portefeuille :\n"

        for ligne in lignes:
            partie = ligne.strip().split(":")
            if len(partie) != 2:
                continue
            symbole = partie[0].strip().upper()
            quantite = float(partie[1].strip())

            ticker = yf.Ticker(symbole)
            info = ticker.fast_info
            cours = info.last_price
            ouverture = info.open
            variation = ((cours - ouverture) / ouverture) * 100
            valeur_ligne = cours * quantite
            tendance = '📈' if variation >= 0 else '📉'

            resultat += (f"  {symbole} {tendance} : {cours:.2f} $ × {quantite:.0f} "
                        f"= {valeur_ligne:.2f} $ ({variation:+.2f}%)\n")

            total_valeur += valeur_ligne
            total_ouverture += ouverture * quantite

        variation_globale = ((total_valeur - total_ouverture) / total_ouverture) * 100
        tendance_globale = '📈' if variation_globale >= 0 else '📉'
        resultat += f"\nValeur totale {tendance_globale} : {total_valeur:.2f} $ ({variation_globale:+.2f}%)"

        return resultat

    except Exception as e:
        return f"Erreur lors du calcul du portefeuille : {str(e)}"