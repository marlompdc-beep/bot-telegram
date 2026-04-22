import time
import requests
import os
from crawler import jogos

TELEGRAM_TOKEN = os.getenv("8763383610:AAHlzQ5__OALO3BoyArqAWY1ET0KFPXLNiA")
CHAT_ID = os.getenv("1302389209")

sinais_hoje = 0
MAX_SINAIS = 6
jogos_enviados = set()

def enviar(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def extrair_minuto(status):
    try:
        if "MIN" in status:
            return int(status.replace("MIN","").strip())
        return 0
    except:
        return 0

def analisar(jogo):
    global sinais_hoje

    if jogo['link'] in jogos_enviados:
        return

    minuto = extrair_minuto(jogo['status'])
    gols = int(jogo['gols_total'])
    ritmo = jogo['ritmo']

    if 25 <= minuto <= 75:
        if gols <= 1:
            if ritmo >= 3:
                if sinais_hoje < MAX_SINAIS:
                    msg = f'''
🚨 ENTRADA AO VIVO (PRO)

{jogo['time_casa']} x {jogo['time_fora']}
⏱ {minuto} min
⚽ {jogo['placar']}

📊 Ritmo: {ritmo}/5

🎯 Over 1.5 gols
📉 Gestão: 1% banca
'''
                    enviar(msg)
                    jogos_enviados.add(jogo['link'])
                    sinais_hoje += 1

def main():
    enviar("✅ BOT PRO ONLINE")
    while True:
        try:
            lista = jogos()
            for j in lista:
                analisar(j)
            time.sleep(60)
        except Exception as e:
            print("Erro:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
