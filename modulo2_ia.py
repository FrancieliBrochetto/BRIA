# modulo2_ia.py
import json
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()  # carrega o .env antes de tudo

# ── Configuração ──────────────────────────────────────────────────────────────
client = Anthropic()  # usa ANTHROPIC_API_KEY automaticamente
MODELO = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """Você é BRIA, uma assistente de curadoria de notícias para um briefing diário pessoal.

Seu trabalho é processar notícias brutas coletadas de RSS feeds e transformá-las
num briefing claro, objetivo e em português.

REGRAS:
1. Sempre responda em português do Brasil, mesmo que a notícia seja em inglês
2. Resuma cada notícia em no máximo 3 linhas diretas
3. Descarte notícias duplicadas ou muito similares — mantenha apenas a melhor versão
4. Descarte clickbait, conteúdo vago ou sem substância real
5. Descarte notícias fora do tema (loterias, esportes, promoções, etc.)
6. Classifique cada notícia no subtema correto conforme as palavras-chave fornecidas
7. Não adicione opiniões ou julgamentos — seja factual e neutro
8. Use linguagem acessível mas profissional

TEMAS E SUBTEMAS VÁLIDOS:
- IA & Tech: ChatGPT, Gemini, Claude, Python, Automação
- Mercado Financeiro: Selic, Câmbio, FIIs, Ações, Opções, Cripto
- Contabilidade & Legislação: SPED, Nota Fiscal, eSocial, Leis Novas, Imposto de Renda, Reforma Tributária

FORMATO DE SAÍDA (JSON):
{
  "briefing": [
    {
      "tema": "IA & Tech",
      "subtema": "ChatGPT",
      "titulo": "Título resumido em português",
      "resumo": "Resumo em até 3 linhas diretas.",
      "fonte": "Nome da fonte",
      "url_original": "https://...",
      "idioma_original": "en"
    }
  ]
}

Retorne APENAS o JSON, sem texto adicional antes ou depois."""


# ── Funções ───────────────────────────────────────────────────────────────────

def formatar_para_prompt(noticias: list) -> str:
    """Converte a lista de notícias num texto estruturado para a BRIA."""
    linhas = []
    for i, n in enumerate(noticias, 1):
        linhas.append(f"""--- Notícia {i} ---
Fonte: {n.get('fonte', 'Desconhecida')}
Idioma: {n.get('lang', 'pt')}
Título: {n.get('titulo', '')}
Conteúdo: {n.get('resumo_bruto', '')}
URL: {n.get('url', '')}
""")
    return "\n".join(linhas)


def processar_com_bria(noticias: list) -> dict:
    """Envia as notícias para a BRIA e retorna o briefing estruturado."""
    if not noticias:
        print("⚠️  Nenhuma notícia para processar.")
        return {"briefing": []}

    print(f"📤 Enviando {len(noticias)} notícias para a BRIA...")

    conteudo = formatar_para_prompt(noticias)

    resposta = client.messages.create(
        model=MODELO,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Aqui estão as notícias coletadas hoje. Processe e retorne o briefing:\n\n{conteudo}"
            }
        ]
    )

    texto = resposta.content[0].text.strip()

    # Remove ```json ... ``` caso a IA inclua marcadores de código
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
        texto = texto.rsplit("```", 1)[0]

    briefing = json.loads(texto.strip())
    total = len(briefing.get("briefing", []))
    print(f"✅ BRIA selecionou {total} notícias relevantes de {len(noticias)} coletadas.")
    return briefing


def exibir_briefing(briefing: dict):
    """Exibe o briefing no terminal de forma legível."""
    itens = briefing.get("briefing", [])

    if not itens:
        print("📭 Briefing vazio — nenhuma notícia relevante hoje.")
        return

    # Agrupa por tema
    por_tema = {}
    for item in itens:
        tema = item.get("tema", "Outros")
        por_tema.setdefault(tema, []).append(item)

    print("\n" + "=" * 60)
    print("📰  BRIEFING DIÁRIO — BRIA")
    print("=" * 60)

    for tema, lista in por_tema.items():
        print(f"\n🔷 {tema.upper()}")
        print("-" * 40)
        for n in lista:
            print(f"\n📌 [{n.get('subtema', '')}] {n.get('titulo', '')}")
            print(f"   {n.get('resumo', '')}")
            print(f"   🔗 {n.get('fonte', '')} → {n.get('url_original', '')}")

    print("\n" + "=" * 60)