import requests
from bs4 import BeautifulSoup

def autenticacao():
    url = 'https://www.placardefutebol.com.br/jogos-de-hoje'
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')

def calcular_ritmo(status, gols):
    try:
        minuto = int(status.replace("MIN","").strip()) if "MIN" in status else 0
    except:
        minuto = 0

    if minuto < 20:
        return 2
    elif minuto < 45:
        return 3 if gols == 0 else 4
    elif minuto < 70:
        return 4
    else:
        return 3

def dados(partida):
    base = 'https://www.placardefutebol.com.br'
    link = base + partida['href']

    try:
        status = partida.find('span', {'class': 'status-name'}).text.strip()
        times = partida.find_all('h5')
        casa = times[0].text.strip()
        fora = times[1].text.strip()

        gols = partida.find_all('span', {'class': 'badge'})
        gc = int(gols[0].text.strip()) if len(gols)>0 else 0
        gf = int(gols[1].text.strip()) if len(gols)>1 else 0

        total = gc + gf

        ritmo = calcular_ritmo(status, total)

        return {
            "link": link,
            "status": status,
            "time_casa": casa,
            "time_fora": fora,
            "placar": f"{gc}x{gf}",
            "gols_total": total,
            "ritmo": ritmo
        }
    except:
        return None

def jogos():
    soup = autenticacao()
    container = soup.find('div', {'id': 'livescore'})
    if not container:
        return []

    partidas = container.find_all('a')
    lista = []

    for p in partidas:
        j = dados(p)
        if j and ("AO VIVO" in j['status'] or "MIN" in j['status']):
            lista.append(j)

    return lista
