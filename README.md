# IBM Bob — Final Project

> Projeto de conclusão da trilha **IBM Bob Developer** na plataforma DIO.me.
> Construído inteiramente com o IBM Bob como co-engenheiro.

---

## Visão Geral

**DIO Explorer** é um assistente conversacional integrado ao IBM Bob que permite explorar o catálogo de trilhas de formação da [DIO.me](https://dio.me) diretamente no chat, via slash commands, skills e MCP Server.

---

## Estrutura do Projeto

```
IBM_Bob_-_Final_Project/
│
├── Hello World.md                          ← Primeiro commit simbólico
├── .bobignore                              ← Exclusões do contexto do Bob
├── .gitignore                              ← Exclusões do git
├── README.md                              ← Este arquivo
├── resumo-do-dia-ibm-bob-final-project.html ← Relatório cronológico da sessão
│
├── .bob/                                   ← Configuração local do IBM Bob
│   ├── mcp.json                            ← Registro do MCP Server
│   ├── commands/                           ← Slash commands do projeto
│   │   ├── trilha.md      → /trilha <tecnologia>
│   │   ├── trilhas.md     → /trilhas
│   │   ├── desafio.md     → /desafio <tecnologia> <nivel>
│   │   └── certificado.md → /certificado <nome> <tecnologia>
│   └── skills/                             ← Skills do projeto
│       ├── trilha/SKILL.md
│       ├── trilhas/SKILL.md
│       └── certificado/SKILL.md
│
├── dio_explorer/                           ← Módulo principal
│   ├── data/
│   │   └── trilhas_dio.json               ← 34 trilhas · 648.500 XP total
│   ├── src/
│   │   └── dio_commands.py                ← Lógica dos 3 comandos (Python)
│   ├── mcp/                               ← MCP Server (TypeScript/Node.js)
│   │   ├── src/index.ts                   ← Código-fonte do servidor
│   │   ├── build/index.js                 ← Artefato compilado (executável)
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── README.md
│   └── docs/                              ← Documentação (em construção)
│
└── tests/                                  ← Testes unitários Python
    ├── __init__.py
    └── test_dio_commands.py               ← 62 testes · 100% pass · ≥70% cobertura
```

---

## Slash Commands

| Comando | Uso | Descrição |
|---|---|---|
| `/trilhas` | `/trilhas` | Lista todas as 34 trilhas por categoria |
| `/trilha` | `/trilha <tecnologia>` | Plano completo: módulos, badges, lives, promoção |
| `/desafio` | `/desafio <tecnologia> <nivel>` | Desafio aleatório com enunciado, dicas e XP |
| `/certificado` | `/certificado <nome> <tecnologia>` | Certificado fictício de conclusão |

---

## MCP Server

O MCP Server (`dio_explorer/mcp/`) expõe as 3 ferramentas acima via protocolo MCP para integração com Bob, Claude Desktop e qualquer cliente MCP compatível.

```bash
# Build
cd dio_explorer/mcp && npm install && npm run build
```

O servidor é registrado automaticamente via `.bob/mcp.json` para o workspace atual.

---

## Testes

```bash
# Executar suite completa
python -m pytest tests/ -v

# Com cobertura
python -m pytest tests/ --cov=dio_explorer/src --cov-report=term-missing
```

62 testes unitários cobrindo `cmd_trilha`, `cmd_desafio` e `cmd_certificado`.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Lógica de negócio | Python 3.13 |
| Testes | pytest 9.1 + coverage |
| MCP Server | TypeScript 5 · Node.js 24 · `@modelcontextprotocol/sdk` |
| Dados | JSON (34 trilhas) |
| Integração IA | IBM Bob (slash commands + skills + MCP) |
