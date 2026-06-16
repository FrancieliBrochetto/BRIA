# teste_modulo2.py
from modulo2_ia import processar_com_bria, exibir_briefing

noticias_teste = [
    {
        "titulo": "OpenAI announces GPT-5 with multimodal reasoning",
        "resumo_bruto": "OpenAI today released GPT-5, claiming significant improvements in reasoning and multimodal capabilities across text, image and audio inputs.",
        "url": "https://techcrunch.com/exemplo",
        "fonte": "TechCrunch AI",
        "lang": "en"
    },
    {
        "titulo": "Copom mantém Selic em 10,5% ao ano na reunião de junho",
        "resumo_bruto": "O Comitê de Política Monetária (Copom) do Banco Central decidiu manter a taxa Selic em 10,5% ao ano, em linha com as expectativas do mercado.",
        "url": "https://infomoney.com.br/exemplo",
        "fonte": "InfoMoney",
        "lang": "pt"
    },
    {
        "titulo": "Receita Federal atualiza regras do IRPF para rendimentos de FIIs",
        "resumo_bruto": "A Receita Federal publicou instrução normativa IN 2.200/2025 alterando as regras de tributação de rendimentos distribuídos por Fundos de Investimento Imobiliário para pessoas físicas.",
        "url": "https://sigaofisco.com.br/exemplo",
        "fonte": "Siga o Fisco",
        "lang": "pt"
    },
    {
        "titulo": "Promoção de tênis no Mercado Livre — até 60% de desconto",
        "resumo_bruto": "Confira as melhores ofertas de tênis esportivos com descontos imperdíveis...",
        "url": "https://exemplo.com/promo",
        "fonte": "Site Aleatório",
        "lang": "pt"
    },
]

briefing = processar_com_bria(noticias_teste)
exibir_briefing(briefing)