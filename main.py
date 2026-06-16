# main.py
from modulo_01_coletor import coletar_noticias
from modulo2_ia        import processar_com_bria, exibir_briefing
from modulo3_banco     import criar_banco, salvar_briefing
import re

def limpar_html(texto: str) -> str:
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto[:400].strip()


def rodar_pipeline():
    """Executa o pipeline completo: coleta → BRIA → banco → exibe."""
    print("🚀 Iniciando pipeline BRIA...\n")

    criar_banco()

    noticias_brutas = coletar_noticias()

    for n in noticias_brutas:
        n["resumo_bruto"] = limpar_html(n.get("resumo_bruto", ""))

    briefing = processar_com_bria(noticias_brutas)
    salvar_briefing(briefing, len(noticias_brutas))
    exibir_briefing(briefing)


# Esse bloco só executa quando você roda "python main.py" diretamente.
# Quando outro arquivo importa o main.py, esse bloco é ignorado.
if __name__ == "__main__":
    rodar_pipeline()