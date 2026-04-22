import time
import requests
from crawler import jogos

TELEGRAM_TOKEN = "8763383610:AAHlzQ5__OALO3BoyArqAWY1ET0KFPXLNiA"
CHAT_ID = "1302389209"

sinais_hoje = 0
MAX_SINAIS = 5
jogos_enviados = set()

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def extrair_minuto(status):
    try:
        if "MIN" in status:
            return int(status.replace("MIN", "").strip())
        return 0
    except:
        return 0

def analisar_jogo(jogo):
    global sinais_hoje

    id_jogo = jogo['link']

    if id_jogo in jogos_enviados:
        return

    minuto = extrair_minuto(jogo['status'])

    try:
        gols_casa = int(jogo['time_casa_gol'])
        gols_fora = int(jogo['time_fora_gol'])
    except:
        return

    total_gols = gols_casa + gols_fora

    if 1 <= minuto <= 90:
        if total_gols <= 1:
            if minuto >= 45 or (minuto >= 30 and total_gols == 0):
                if sinais_hoje >= MAX_SINAIS:
                    return

                mensagem = f"""🚨 ENTRADA AO VIVO

{jogo['time_casa']} x {jogo['time_fora']}
⏱ Minuto: {minuto}
⚽ Placar: {gols_casa} x {gols_fora}

🎯 Entrada: Over 1.5 gols
🔥 Perfil: Conservador

📉 Gestão: 1% banca"""

                enviar_telegram(mensagem)

                jogos_enviados.add(id_jogo)
                sinais_hoje += 1

def main():
    print("BOT RODANDO...")
    enviar_telegram("✅ BOT ONLINE")

    while True:
        try:
            lista_jogos = jogos()
            for jogo in lista_jogos:
                analisar_jogo(jogo)
            time.sleep(60)
        except Exception as e:
            print("Erro:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
