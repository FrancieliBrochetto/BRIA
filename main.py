# main.py
import re
import json
import os
from datetime import date
from modulo_01_coletor import coletar_noticias
from modulo2_ia        import processar_com_bria, exibir_briefing
from modulo3_banco     import criar_banco, salvar_briefing


def limpar_html(texto: str) -> str:
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto[:400].strip()


def exportar_json(briefing: dict):
    """Exporta o briefing como JSON para o GitHub Pages"""
    hoje  = date.today().isoformat()
    pasta = os.path.join("docs", "briefings")
    os.makedirs(pasta, exist_ok=True)

    # Salva o briefing do dia
    arquivo = os.path.join(pasta, f"{hoje}.json")
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            {"data": hoje, "noticias": briefing.get("briefing", [])},
            f, ensure_ascii=False, indent=2
        )

    # Atualiza o índice de datas disponíveis
    index_path = os.path.join(pasta, "index.json")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {"datas": []}

    if hoje not in index["datas"]:
        index["datas"].insert(0, hoje)
        index["datas"] = sorted(index["datas"], reverse=True)[:30]

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"📄 JSON exportado: {arquivo}")


def rodar_pipeline():
    print("🚀 Iniciando pipeline BRIA...\n")
    criar_banco()
    noticias_brutas = coletar_noticias()
    for n in noticias_brutas:
        n["resumo_bruto"] = limpar_html(n.get("resumo_bruto", ""))
    briefing = processar_com_bria(noticias_brutas)
    salvar_briefing(briefing, len(noticias_brutas))
    exportar_json(briefing)
    exibir_briefing(briefing)


if __name__ == "__main__":
    rodar_pipeline()