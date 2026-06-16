# modulo_01_coletor.py
# Módulo 1 — O Coletor de Notícias
# Projeto: Briefing Diário Personalizado com BRIA

import feedparser

# ------------------------------------------------------------------
# DICIONÁRIO DE FEEDS
# ✅ = confirmado funcionando
# 🔄 = testar na próxima rodada
# ------------------------------------------------------------------

FEEDS = {

    "IA & Tech": [
        # --- Português ---
        {"url": "https://tecnoblog.net/feed/",                                    "nome": "Tecnoblog",        "lang": "pt"},  # ✅
        {"url": "https://olhardigital.com.br/feed/",                              "nome": "Olhar Digital",    "lang": "pt"},  # ✅
        {"url": "https://www.tecmundo.com.br/rss",                                "nome": "TecMundo",         "lang": "pt"},  # 🔄
        # --- Inglês ---
        {"url": "https://techcrunch.com/category/artificial-intelligence/feed/",  "nome": "TechCrunch AI",    "lang": "en"},  # ✅
        {"url": "https://tldr.tech/api/rss/ai",                                   "nome": "TLDR AI",          "lang": "en"},  # ✅
        {"url": "https://stratechery.com/feed/",                                  "nome": "Stratechery",      "lang": "en"},  # ✅
        {"url": "https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml",                  "nome": "The Rundown AI",   "lang": "en"},  # 🔄
        {"url": "https://www.wired.com/feed/category/artificial-intelligence/latest/rss", "nome": "Wired AI", "lang": "en"},  # 🔄
    ],

    "Mercado Financeiro": [
        # --- Português ---
        {"url": "https://www.infomoney.com.br/feed/",                             "nome": "InfoMoney",        "lang": "pt"},  # ✅
        {"url": "https://g1.globo.com/rss/g1/economia/",                          "nome": "G1 Economia",      "lang": "pt"},  # ✅
        {"url": "https://agenciabrasil.ebc.com.br/economia/feed",                 "nome": "Agência Brasil",   "lang": "pt"},  # 🔄
        {"url": "https://www.cnnbrasil.com.br/economia/feed/",                    "nome": "CNN Brasil",       "lang": "pt"},  # 🔄
    ],

    "Contabilidade & Legislacao": [
        # --- Português ---
        {"url": "https://www.sigaofisco.com.br/feed/",                            "nome": "Siga o Fisco",     "lang": "pt"},  # ✅
        {"url": "https://www.contabeis.com.br/rss/noticias/",                     "nome": "Contábeis",        "lang": "pt"},  # 🔄 URL corrigida
        {"url": "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/RSS.xml", "nome": "Receita Federal","lang": "pt"}, # 🔄
    ],

}

LIMITE_POR_FONTE = 5


def coletar_noticias():
    print("\n" + "=" * 60)
    print("         📰  BRIEFING DIÁRIO — BRIA")
    print("=" * 60)

    total = 0
    ok    = 0
    erro  = 0
    erros = []
    todas_noticias = []   # ← NOVO: lista que vai acumular as notícias

    for tema, feeds in FEEDS.items():
        print(f"\n🔹 {tema.upper()}")
        print("-" * 50)

        for fonte in feeds:
            url  = fonte["url"]
            nome = fonte["nome"]
            lang = fonte["lang"]
            flag = "🇧🇷" if lang == "pt" else "🇺🇸"

            feed = feedparser.parse(url)

            if not feed.entries:
                print(f"  ⚠️  {nome} — sem retorno (verificar URL)")
                erros.append(nome)
                erro += 1
                continue

            ok += 1
            print(f"\n  {flag} {nome}")
            for noticia in feed.entries[:LIMITE_POR_FONTE]:
                print(f"     • {noticia.title}")
                total += 1

                todas_noticias.append({   # ← NOVO: salva cada notícia
                    "titulo":      noticia.title,
                    "url":         noticia.link,
                    "resumo_bruto": noticia.get("summary", ""),
                    "fonte":       nome,
                    "lang":        lang,
                    "tema":        tema,
                })

    print("\n" + "=" * 60)
    print(f"  ✅ Fontes OK:     {ok}")
    print(f"  ⚠️  Fontes erro:  {erro}")
    if erros:
        print(f"  📋 Verificar:    {', '.join(erros)}")
    print(f"  📄 Total notícias: {total}")
    print("=" * 60 + "\n")

    return todas_noticias   # ← NOVO: devolve a lista para quem chamou

if __name__ == "__main__":
    coletar_noticias()