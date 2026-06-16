# modulo4_agendador.py
# Módulo 4 — Agendador automático

import schedule
import time
from datetime import datetime
from main import rodar_pipeline   # importa a função que acabamos de criar


HORARIO = "07:00"   # hora de rodar todo dia


def tarefa_agendada():
    """Wrapper da tarefa — adiciona log de horário."""
    print(f"\n⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')} — pipeline agendado iniciando...")
    rodar_pipeline()
    print(f"✅ Concluído. Próxima execução amanhã às {HORARIO}\n")


# Registra a tarefa no agendador
schedule.every().day.at(HORARIO).do(tarefa_agendada)

print("🕐 Agendador BRIA ativo.")
print(f"   Execução diária: {HORARIO}")
print(f"   Agora:           {datetime.now().strftime('%H:%M')}")
print("   Ctrl+C para encerrar\n")

# Roda imediatamente ao iniciar (não espera até as 07:00)
tarefa_agendada()

# Loop principal — verifica a cada minuto se chegou a hora
while True:
    schedule.run_pending()
    time.sleep(60)