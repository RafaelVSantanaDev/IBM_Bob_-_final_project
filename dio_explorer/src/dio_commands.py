"""
dio_commands.py
Módulo que implementa a lógica dos comandos DIO Explorer:
  /trilha   — consulta plano de estudos pelo nome/tecnologia
  /desafio  — gera desafio de código para uma tecnologia e nível
  /certificado — gera certificado fictício de conclusão de trilha
"""

from __future__ import annotations

import json
import os
import random
import re
import string
from datetime import date, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Caminho padrão do arquivo de dados
# ---------------------------------------------------------------------------
_DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "trilhas_dio.json"


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def carregar_trilhas(caminho: str | Path | None = None) -> list[dict[str, Any]]:
    """Carrega a lista de trilhas do arquivo JSON."""
    caminho = Path(caminho) if caminho else _DEFAULT_DATA_PATH
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    return dados["trilhas"]


def buscar_trilha(termo: str, trilhas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Busca trilhas cujo campo 'tecnologia' ou 'nome' contenha *termo*
    (case-insensitive, correspondência parcial).
    """
    termo_lower = termo.strip().lower()
    return [
        t for t in trilhas
        if termo_lower in t["tecnologia"].lower() or termo_lower in t["nome"].lower()
    ]


def formatar_data_br(data_iso: str) -> str:
    """Converte '2025-08-10' em '10/08/2025'."""
    ano, mes, dia = data_iso.split("-")
    return f"{dia}/{mes}/{ano}"


def gerar_codigo_verificacao(id_trilha: int, ano: int) -> str:
    """Gera código no formato DIO-{ANO}{ID:02d}-{6 chars aleatórios}."""
    sufixo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"DIO-{ano}{id_trilha:02d}-{sufixo}"


# ---------------------------------------------------------------------------
# Comando /trilha
# ---------------------------------------------------------------------------

def cmd_trilha(tecnologia: str, caminho_dados: str | Path | None = None) -> str:
    """
    Executa /trilha <tecnologia> e retorna o plano de estudos em Markdown.
    Retorna mensagem de erro se nenhuma trilha for encontrada.
    """
    trilhas = carregar_trilhas(caminho_dados)
    resultados = buscar_trilha(tecnologia, trilhas)

    if not resultados:
        return (
            f'> ❌ Nenhuma trilha encontrada para **"{tecnologia}"**.\n'
            f">\n"
            f"> 💡 Tente um dos termos: `Python`, `Java`, `React`, `Angular`, "
            f"`Node.js`, `AWS`, `Azure`, `Machine Learning`, `Data Science`, "
            f"`Kotlin`, `Flutter`, `.NET`, `DevOps`, `Cybersecurity`, `SQL`, "
            f"`Vue.js`, `TypeScript`, `Go`, `Rust`, `Swift`, `Blockchain`, "
            f"`UX`, `Unity`, `QA`, `GenAI`, `GCP`, `Engenharia de Dados`, "
            f"`PHP`, `Ruby`, `Scrum`, `Linux`, `JavaScript`, `Power BI`, `MLOps`."
        )

    saidas: list[str] = []
    for t in resultados:
        lives = t.get("lives_ao_vivo", [])
        lives_txt = "\n".join(
            f"- **{l['titulo']}** — {formatar_data_br(l['data'])} às {l['horario']}"
            for l in lives
        ) or "_Nenhuma live agendada no momento._"

        badges_txt = "\n".join(f"🥇 {b}" for b in t["badges_disponiveis"])

        promo = t["promocoes"]
        promo_txt = (
            promo["descricao"]
            if promo["desconto_percentual"] > 0
            else "Nenhuma promoção ativa no momento."
        )

        vitalicio_txt = (
            "✅ Sim — esta trilha possui acesso vitalício."
            if t["vitalicio"]
            else "❌ Não — o acesso é por período limitado."
        )

        saidas.append(
            f"## 📚 Plano de Estudos — {t['nome']}\n\n"
            f"**Tecnologia:** {t['tecnologia']}\n"
            f"**Total de módulos:** {t['numero_de_modulos']}\n"
            f"**XP total ao concluir:** {t['xp_total']} XP\n\n"
            f"---\n\n"
            f"### 🏅 Badges Disponíveis\n\n{badges_txt}\n\n"
            f"---\n\n"
            f"### 📡 Lives ao Vivo\n\n{lives_txt}\n\n"
            f"---\n\n"
            f"### 🎁 Promoção Especial\n\n{promo_txt}\n\n"
            f"---\n\n"
            f"### ♾️ Acesso Vitalício\n\n{vitalicio_txt}"
        )

    return "\n\n---\n\n".join(saidas)


# ---------------------------------------------------------------------------
# Comando /desafio
# ---------------------------------------------------------------------------

_NIVEIS_VALIDOS = {"iniciante", "intermediario", "intermediário", "avancado", "avançado"}

_XP_RANGES = {
    "iniciante": (150, 300),
    "intermediario": (350, 600),
    "intermediário": (350, 600),
    "avancado": (700, 1200),
    "avançado": (700, 1200),
}

_TEMAS_POR_NIVEL: dict[str, list[str]] = {
    "iniciante": [
        "Calculadora de operações básicas",
        "Verificador de número primo",
        "Conversor de temperatura (Celsius/Fahrenheit)",
        "Gerador de tabuada",
        "Contador de vogais em uma string",
    ],
    "intermediario": [
        "Implementação de uma Pilha (Stack) sem biblioteca",
        "Algoritmo de busca binária",
        "Validador de expressões com parênteses balanceados",
        "Agenda de contatos com CRUD em memória",
        "Sistema de fila com prioridade",
    ],
    "avancado": [
        "Implementação de cache LRU",
        "Parser de expressões matemáticas",
        "Servidor HTTP simples com threads",
        "Sistema de eventos assíncrono",
        "Algoritmo de compressão Run-Length Encoding",
    ],
}


def _normalizar_nivel(nivel: str) -> str:
    """Normaliza variações de nível para chave canônica."""
    n = nivel.strip().lower()
    if n in ("avancado", "avançado"):
        return "avancado"
    if n in ("intermediario", "intermediário"):
        return "intermediario"
    return n  # "iniciante" ou inválido


def cmd_desafio(tecnologia: str, nivel: str) -> str:
    """
    Executa /desafio <tecnologia> <nivel> e retorna o desafio em Markdown.
    Retorna mensagem de erro para tecnologia ou nível inválidos.
    """
    nivel_norm = _normalizar_nivel(nivel)

    if nivel_norm not in _NIVEIS_VALIDOS:
        return (
            f"> ❌ Nível **\"{nivel}\"** inválido.\n"
            f"> Níveis válidos: `iniciante`, `intermediario`, `avancado`."
        )

    temas = _TEMAS_POR_NIVEL.get(nivel_norm, _TEMAS_POR_NIVEL["iniciante"])
    tema = random.choice(temas)

    _NIVEL_DISPLAY = {
        "iniciante": "Iniciante",
        "intermediario": "Intermediário",
        "avancado": "Avançado",
    }
    nivel_display = _NIVEL_DISPLAY.get(nivel_norm, nivel_norm.capitalize())

    xp_min, xp_max = _XP_RANGES[nivel_norm]
    xp = random.randint(xp_min, xp_max)

    return (
        f"## ⚔️ Desafio DIO — {tecnologia} · Nível {nivel_display}\n\n"
        f"> 🎲 *Desafio gerado aleatoriamente*\n\n"
        f"---\n\n"
        f"### 📋 Enunciado\n\n"
        f"Implemente **{tema}** utilizando **{tecnologia}**.\n"
        f"O programa deve aceitar entradas do usuário, processar a lógica central e\n"
        f"exibir o resultado formatado. Garanta tratamento de entradas inválidas e\n"
        f"siga as boas práticas da linguagem escolhida.\n\n"
        f"---\n\n"
        f"### 📥 Exemplo de Entrada\n\n"
        f"```\nEntrada 1: 10\nEntrada 2: 25\n```\n\n"
        f"### 📤 Exemplo de Saída Esperada\n\n"
        f"```\nResultado: processado com sucesso\n```\n\n"
        f"---\n\n"
        f"### 💡 Dicas\n\n"
        f"- Leia o enunciado com atenção antes de codificar.\n"
        f"- Comece pelo caso mais simples e evolua progressivamente.\n"
        f"- Escreva testes para cada caso de uso.\n"
        f"- Revise a complexidade do seu algoritmo.\n\n"
        f"---\n\n"
        f"### 🧩 Restrições\n\n"
        f"- Não utilize bibliotecas externas não mencionadas.\n"
        f"- A solução deve executar em tempo O(n) ou melhor.\n"
        f"- Trate entradas vazias ou nulas.\n\n"
        f"---\n\n"
        f"### 🏆 Critérios de Avaliação\n\n"
        f"| Critério | Peso |\n"
        f"|---|---|\n"
        f"| Corretude da solução | 40% |\n"
        f"| Clareza e legibilidade do código | 30% |\n"
        f"| Eficiência / performance | 20% |\n"
        f"| Boas práticas da linguagem | 10% |\n\n"
        f"---\n\n"
        f"### 🎯 XP ao Concluir\n\n"
        f"**+{xp} XP** ao concluir este desafio."
    )


# ---------------------------------------------------------------------------
# Comando /certificado
# ---------------------------------------------------------------------------

def cmd_certificado(
    nome_usuario: str,
    tecnologia: str,
    caminho_dados: str | Path | None = None,
    data_base: date | None = None,
) -> str:
    """
    Executa /certificado <nome> <tecnologia> e retorna o certificado em Markdown.
    Retorna mensagem de erro se a trilha não for encontrada.
    """
    trilhas = carregar_trilhas(caminho_dados)
    resultados = buscar_trilha(tecnologia, trilhas)

    if not resultados:
        return (
            f'> ❌ Trilha não encontrada para **"{tecnologia}"**. '
            f"Verifique o nome da tecnologia e tente novamente."
        )

    t = resultados[0]  # usa a primeira correspondência

    hoje = data_base or date.today()
    data_emissao = hoje + timedelta(weeks=t["numero_de_modulos"])
    data_emissao_str = data_emissao.strftime("%d/%m/%Y")

    codigo = gerar_codigo_verificacao(t["id"], hoje.year)

    badges_txt = "\n".join(f"  ·  {b}" for b in t["badges_disponiveis"])
    vitalicio_txt = "Sim" if t["vitalicio"] else "Não"
    nome_upper = nome_usuario.upper()

    certificado = (
        "```\n"
        "╔══════════════════════════════════════════════════════════════════════╗\n"
        "║                                                                      ║\n"
        "║                    🎓  CERTIFICADO DE CONCLUSÃO                      ║\n"
        "║                                                                      ║\n"
        "║                  Digital Innovation One — DIO.me                    ║\n"
        "║                                                                      ║\n"
        "╠══════════════════════════════════════════════════════════════════════╣\n"
        "║                                                                      ║\n"
        "║  Certificamos que                                                    ║\n"
        "║                                                                      ║\n"
       f"║              ✦  {nome_upper:<52}✦  ║\n"
        "║                                                                      ║\n"
        "║  concluiu com êxito a formação:                                      ║\n"
        "║                                                                      ║\n"
       f"║              {t['nome']:<58}║\n"
        "║                                                                      ║\n"
       f"║  Tecnologia:   {t['tecnologia']:<56}║\n"
       f"║  Módulos:      {t['numero_de_modulos']} módulos concluídos{' ' * (40 - len(str(t['numero_de_modulos'])))}║\n"
       f"║  XP obtido:    {t['xp_total']} XP{' ' * (53 - len(str(t['xp_total'])))}║\n"
        "║                                                                      ║\n"
        "╠══════════════════════════════════════════════════════════════════════╣\n"
        "║                                                                      ║\n"
        "║  🏅 Badges conquistadas:                                             ║\n"
        "║                                                                      ║\n"
       f"{badges_txt}\n"
        "║                                                                      ║\n"
        "╠══════════════════════════════════════════════════════════════════════╣\n"
        "║                                                                      ║\n"
       f"║  Data de emissão:   {data_emissao_str:<51}║\n"
       f"║  Código:            {codigo:<51}║\n"
        "║                                                                      ║\n"
        "║  ⚠️  Este é um certificado fictício gerado para fins educacionais.   ║\n"
        "║     Certificados oficiais são emitidos pela plataforma DIO.me.       ║\n"
        "║                                                                      ║\n"
        "╚══════════════════════════════════════════════════════════════════════╝\n"
        "```\n\n"
        "---\n\n"
        "## 📄 Dados do Certificado\n\n"
        "| Campo | Valor |\n"
        "|---|---|\n"
       f"| **Titular** | {nome_usuario} |\n"
       f"| **Formação** | {t['nome']} |\n"
       f"| **Tecnologia** | {t['tecnologia']} |\n"
       f"| **Módulos concluídos** | {t['numero_de_modulos']} |\n"
       f"| **XP total** | {t['xp_total']} XP |\n"
       f"| **Data de emissão** | {data_emissao_str} |\n"
       f"| **Código de verificação** | `{codigo}` |\n"
       f"| **Acesso vitalício** | {vitalicio_txt} |\n\n"
        "---\n\n"
       f"> 🎉 Parabéns, **{nome_usuario}**! Você concluiu a **{t['nome']}** "
        "e está pronto para os próximos desafios.\n"
        "> Continue evoluindo na plataforma [DIO.me](https://dio.me)!"
    )

    return certificado
