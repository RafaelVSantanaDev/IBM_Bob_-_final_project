# DIO Explorer

> Projeto de conclusão da trilha **IBM Bob Developer** — [DIO.me](https://dio.me)

Um assistente conversacional integrado ao **IBM Bob** que expõe o catálogo de formações da plataforma DIO.me diretamente no chat. Implementado em três camadas complementares: slash commands, skills e um MCP Server TypeScript/Node.js.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Build](#instalação-e-build)
- [Slash Commands](#slash-commands)
- [MCP Server](#mcp-server)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Stack](#stack)
- [Documentação](#documentação)

---

## Visão Geral

O DIO Explorer fornece quatro operações principais, disponíveis tanto como slash commands interativos quanto como ferramentas nativas do protocolo MCP:

| Operação | Slash Command | MCP Tool |
|---|---|---|
| Catálogo de trilhas | `/trilhas` | — |
| Plano de estudos | `/trilha <tecnologia>` | `trilha` |
| Desafio de código | `/desafio <tecnologia> <nivel>` | `desafio` |
| Certificado de conclusão | `/certificado <nome> <tecnologia>` | `certificado` |

O catálogo cobre **34 trilhas** em 8 categorias (Linguagens, Frontend, Cloud, IA/Dados, DevOps, Segurança, Banco de Dados, Especialidades), totalizando **648.500 XP**.

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                      IBM Bob (chat)                      │
└────────────┬────────────────────────┬───────────────────┘
             │                        │
    slash commands               MCP tools
    .bob/commands/          mcp__dio-explorer__*
             │                        │
             ▼                        ▼
┌─────────────────────┐   ┌──────────────────────────────┐
│  Bob lê o JSON      │   │  dio-explorer-mcp (stdio)    │
│  diretamente e      │   │  dio_explorer/mcp/build/     │
│  formata a resposta │   │  index.js                    │
└─────────────────────┘   └──────────────────────────────┘
             │                        │
             └──────────┬─────────────┘
                        ▼
          dio_explorer/data/trilhas_dio.json
          dio_explorer/src/dio_commands.py
```

Ambas as camadas (slash commands e MCP Server) leem o mesmo `trilhas_dio.json` e produzem saída idêntica. O módulo Python contém a lógica canônica; o servidor TypeScript a espelha para o protocolo MCP.

---

## Pré-requisitos

| Requisito | Versão mínima |
|---|---|
| Python | 3.11+ |
| Node.js | 18+ |
| npm | 9+ |
| IBM Bob | qualquer versão com suporte a MCP |

---

## Instalação e Build

### 1. Clonar o repositório

```bash
git clone https://github.com/RafaelVSantanaDev/IBM_Bob_-_final_project.git
cd IBM_Bob_-_final_project
```

### 2. Construir o MCP Server

```bash
cd dio_explorer/mcp
npm install
npm run build
# Gera: dio_explorer/mcp/build/index.js
```

### 3. Registrar o servidor no IBM Bob

Edite `.bob/mcp.json` ajustando o caminho absoluto para o seu ambiente:

```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": ["/caminho/absoluto/para/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

Após salvar, o Bob reinicia o servidor automaticamente.

### 4. Instalar dependências Python (opcional — apenas para testes)

```bash
pip install pytest pytest-cov
```

---

## Slash Commands

Os comandos ficam disponíveis assim que o repositório é aberto no IBM Bob. Nenhuma instalação adicional é necessária.

### `/trilhas`

Lista o catálogo completo de 34 trilhas organizado por categoria.

```
/trilhas
```

### `/trilha <tecnologia>`

Exibe o plano de estudos completo de uma formação. A busca é *case-insensitive* e aceita correspondência parcial.

```
/trilha Python
/trilha machine learning
/trilha react
```

**Saída:** módulos numerados, badges disponíveis, lives agendadas, promoção ativa e status de acesso vitalício.

### `/desafio <tecnologia> <nivel>`

Gera um desafio de código aleatório.

```
/desafio Python iniciante
/desafio Java intermediario
/desafio TypeScript avancado
```

**Níveis válidos:** `iniciante` · `intermediario` · `avancado` (com ou sem acentuação)

**XP por nível:**

| Nível | XP |
|---|---|
| Iniciante | 150 – 300 |
| Intermediário | 350 – 600 |
| Avançado | 700 – 1.200 |

### `/certificado <nome> <tecnologia>`

Gera um certificado fictício de conclusão (fins educacionais).

```
/certificado "João da Silva" Java
/certificado "Maria Oliveira" Python
```

---

## MCP Server

O servidor MCP expõe as três ferramentas ao Bob como funções nativas, invocadas automaticamente durante conversas.

### Ferramentas registradas

| Tool | Parâmetros | Descrição |
|---|---|---|
| `trilha` | `tecnologia: string` | Plano de estudos por tecnologia |
| `desafio` | `tecnologia: string`, `nivel: string` | Desafio aleatório com XP |
| `certificado` | `nome_usuario: string`, `tecnologia: string` | Certificado fictício |

### Transporte

O servidor usa transporte **stdio** — o Bob o inicia como processo filho e se comunica via `stdin`/`stdout`. Nenhuma porta de rede é necessária.

> **Nota:** Use sempre `console.error()` para logs internos do servidor. `console.log()` escreve em `stdout`, que é o canal do protocolo MCP, e causaria erros de parse no cliente.

### Build e desenvolvimento

```bash
cd dio_explorer/mcp

npm install          # instalar dependências
npm run build        # compilar TypeScript → build/index.js
npm run dev          # compilar em modo watch
```

---

## Testes

A suite de testes cobre o módulo Python [`dio_explorer/src/dio_commands.py`](dio_explorer/src/dio_commands.py).

```bash
# Suite completa com output detalhado
python -m pytest tests/ -v

# Com relatório de cobertura
python -m pytest tests/ --cov=dio_explorer/src --cov-report=term-missing
```

**Resultado:** 62 testes · 100% passou · 100% de cobertura de linha.

### Classes de teste

| Classe | Testes | Escopo |
|---|---|---|
| `TestUtilitarios` | 15 | Funções auxiliares e normalização |
| `TestCmdTrilha` | 13 | Comando `/trilha` — sucesso e erros |
| `TestCmdDesafio` | 14 | Comando `/desafio` — níveis, XP, acentuação |
| `TestCmdCertificado` | 16 | Comando `/certificado` — campos, datas, códigos |
| `TestIntegracaoArquivoReal` | 4 | Integração com `trilhas_dio.json` real |

---

## Estrutura do Projeto

```
IBM_Bob_-_Final_Project/
│
├── README.md                               ← Este arquivo
├── DOCUMENTATION.md                        ← Guia completo: prompts, insights, glossário
├── .gitignore
├── .bobignore
│
├── .bob/                                   ← Configuração do IBM Bob
│   ├── mcp.json                            ← Registro do MCP Server (stdio)
│   ├── commands/                           ← Slash commands
│   │   ├── trilha.md        → /trilha <tecnologia>
│   │   ├── trilhas.md       → /trilhas
│   │   ├── desafio.md       → /desafio <tecnologia> <nivel>
│   │   └── certificado.md   → /certificado <nome> <tecnologia>
│   └── skills/                             ← Skills reutilizáveis
│       ├── trilha/SKILL.md
│       ├── trilhas/SKILL.md
│       └── certificado/SKILL.md
│
├── dio_explorer/
│   ├── data/
│   │   └── trilhas_dio.json               ← 34 trilhas · 648.500 XP
│   ├── src/
│   │   └── dio_commands.py                ← Lógica Python (cmd_trilha, cmd_desafio, cmd_certificado)
│   └── mcp/                               ← MCP Server TypeScript/Node.js
│       ├── src/
│       │   └── index.ts                   ← Código-fonte do servidor
│       ├── package.json
│       ├── tsconfig.json
│       └── README.md
│
└── tests/
    ├── __init__.py
    └── test_dio_commands.py               ← 62 testes unitários
```

---

## Stack

| Camada | Tecnologia |
|---|---|
| Lógica de negócio | Python 3.13 |
| Testes | pytest 9.1 · pytest-cov |
| MCP Server | TypeScript 5 · Node.js 24 · `@modelcontextprotocol/sdk` ^1.0 · `zod` ^3.25 |
| Dados | JSON (34 trilhas, schema versionado) |
| Integração IA | IBM Bob — slash commands · skills · MCP (stdio) |

---

## Documentação

- [`DOCUMENTATION.md`](DOCUMENTATION.md) — guia completo com todos os prompts usados na construção do projeto, modos de uso, dicas práticas, 8 insights para desenvolvedores, glossário IBM Bob e próximos passos sugeridos.
- [`dio_explorer/mcp/README.md`](dio_explorer/mcp/README.md) — referência do MCP Server.
- [`resultados_testes.txt`](resultados_testes.txt) — saída completa da suite de testes com relatório de cobertura.

---

*Construído inteiramente com o IBM Bob como co-engenheiro · Sessão de 19/09/2026*
