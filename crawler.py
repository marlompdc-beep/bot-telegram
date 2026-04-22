import requests
from bs4 import BeautifulSoup

def autenticacaoPlacar():
    url = 'https://www.placardefutebol.com.br/jogos-de-hoje'
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')

def dados_jogo(jogo):
    url = 'https://www.placardefutebol.com.br'
    jogo_link = f"{url}{jogo['href']}"

    try:
        status = jogo.find('span', {'class': 'status-name'}).text.strip()
    except:
        return None

    try:
        time_casa = jogo.find_all('h5')[0].text.strip()
        time_fora = jogo.find_all('h5')[1].text.strip()
    except:
        return None

    try:
        gols = jogo.find_all('span', {'class': 'badge'})
        gols_casa = gols[0].text.strip()
        gols_fora = gols[1].text.strip()
    except:
        gols_casa = "0"
        gols_fora = "0"

    return {
        'link': jogo_link,
        'status': status,
        'time_casa': time_casa,
        'time_casa_gol': gols_casa,
        'time_fora': time_fora,
        'time_fora_gol': gols_fora
    }

def jogos():
    soup = autenticacaoPlacar()
    container = soup.find('div', {'id': 'livescore'})

    if not container:
        return []

    partidas = container.find_all('a')
    lista = []

    for partida in partidas:
        jogo = dados_jogo(partida)
        if jogo and jogo['status']:
            if 'AO VIVO' in jogo['status'] or 'MIN' in jogo['status']:
                lista.append(jogo)

    return lista
