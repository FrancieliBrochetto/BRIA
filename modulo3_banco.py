# modulo3_banco.py
# Módulo 3 — Banco de Dados SQLite

import sqlite3
from datetime import date

NOME_BANCO = "bria.db"


def criar_banco():
    """Cria o banco e as tabelas, se ainda não existirem."""
    conn = sqlite3.connect(NOME_BANCO)   # cria o arquivo bria.db (ou abre se já existe)
    cursor = conn.cursor()

    # Tabela 1: um registro por rodada do pipeline
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS briefings (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            data_coleta        TEXT    NOT NULL,
            total_coletadas    INTEGER DEFAULT 0,
            total_selecionadas INTEGER DEFAULT 0,
            criado_em          TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela 2: uma linha por notícia selecionada pela BRIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticias (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            briefing_id     INTEGER NOT NULL,
            tema            TEXT    NOT NULL,
            subtema         TEXT,
            titulo          TEXT    NOT NULL,
            resumo          TEXT,
            fonte           TEXT,
            url_original    TEXT    UNIQUE,   -- UNIQUE: impede duplicatas
            idioma_original TEXT,
            criado_em       TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (briefing_id) REFERENCES briefings(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados pronto.")


def salvar_briefing(briefing: dict, total_coletadas: int) -> int:
    """
    Salva um briefing completo no banco.
    Retorna o ID do briefing criado.
    Notícias com URL já existente são ignoradas silenciosamente.
    """
    itens = briefing.get("briefing", [])
    hoje  = date.today().isoformat()   # ex: "2026-06-14"

    conn   = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()

    # Registra a rodada do dia
    cursor.execute("""
        INSERT INTO briefings (data_coleta, total_coletadas, total_selecionadas)
        VALUES (?, ?, ?)
    """, (hoje, total_coletadas, len(itens)))

    briefing_id = cursor.lastrowid   # ID gerado automaticamente
    salvas  = 0
    puladas = 0

    for item in itens:
        try:
            cursor.execute("""
                INSERT INTO noticias
                    (briefing_id, tema, subtema, titulo, resumo,
                     fonte, url_original, idioma_original)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                briefing_id,
                item.get("tema",            ""),
                item.get("subtema",         ""),
                item.get("titulo",          ""),
                item.get("resumo",          ""),
                item.get("fonte",           ""),
                item.get("url_original",    ""),
                item.get("idioma_original", "pt"),
            ))
            salvas += 1

        except sqlite3.IntegrityError:
            # URL já existe → duplicata → ignora sem parar o programa
            puladas += 1

    conn.commit()
    conn.close()

    print(f"💾 Salvo: {salvas} notícias novas | {puladas} duplicatas ignoradas.")
    return briefing_id


def buscar_historico(dias: int = 7) -> list:
    conn = sqlite3.connect(NOME_BANCO)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(b.id) as id, b.data_coleta,
               SUM(b.total_coletadas)    as total_coletadas,
               SUM(b.total_selecionadas) as total_selecionadas,
               COUNT(n.id)               AS total_salvo
        FROM briefings b
        LEFT JOIN noticias n ON n.briefing_id = b.id
        GROUP BY b.data_coleta
        ORDER BY b.data_coleta DESC
        LIMIT ?
    """, (dias,))

    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado


def buscar_noticias_do_dia(data: str = None) -> list:
    """
    Retorna as notícias de uma data específica.
    Se data=None, usa hoje. Formato: "2026-06-14"
    """
    if data is None:
        data = date.today().isoformat()

    conn = sqlite3.connect(NOME_BANCO)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT n.*
        FROM noticias n
        JOIN briefings b ON b.id = n.briefing_id
        WHERE b.data_coleta = ?
        ORDER BY n.tema, n.subtema
    """, (data,))

    resultado = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultado