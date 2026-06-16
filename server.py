# server.py
# Processo único para o Railway: API Flask + agendador em background

import threading
import schedule
import time
from datetime import datetime
from modulo5_api import app
from main import rodar_pipeline

HORARIO = "07:00"

def tarefa_agendada():
    print(f"\n⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')} — rodando pipeline...")
    rodar_pipeline()
    print(f"✅ Concluído. Próxima execução amanhã às {HORARIO}\n")

def rodar_agendador():
    schedule.every().day.at(HORARIO).do(tarefa_agendada)
    print(f"🕐 Agendador ativo — execução diária às {HORARIO}")
    while True:
        schedule.run_pending()
        time.sleep(60)

# Inicia o agendador em background
thread = threading.Thread(target=rodar_agendador, daemon=True)
thread.start()

# Sobe a API Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)