# Documentação Completa — IBM Bob Final Project

> **DIO Explorer** — Assistente conversacional integrado ao IBM Bob para explorar trilhas de formação da [DIO.me](https://dio.me).
> Construído inteiramente com o IBM Bob como co-engenheiro na sessão de **19/09/2026**.

---

## Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Histórico de Construção — Cronologia da Sessão](#2-histórico-de-construção--cronologia-da-sessão)
3. [Arquitetura do Projeto](#3-arquitetura-do-projeto)
4. [Prompts Utilizados na Sessão](#4-prompts-utilizados-na-sessão)
5. [Modos de Uso — Slash Commands](#5-modos-de-uso--slash-commands)
6. [Modos de Uso — Skills](#6-modos-de-uso--skills)
7. [Modos de Uso — MCP Server (Ferramentas Nativas)](#7-modos-de-uso--mcp-server-ferramentas-nativas)
8. [Módulo Python — dio_commands.py](#8-módulo-python--dio_commandspy)
9. [MCP Server — TypeScript/Node.js](#9-mcp-server--typescriptnodejs)
10. [Testes Unitários](#10-testes-unitários)
11. [Dados — trilhas_dio.json](#11-dados--trilhas_diojson)
12. [Configuração do IBM Bob (.bob/)](#12-configuração-do-ibm-bob-bob)
13. [Dicas de Uso para Profissionais](#13-dicas-de-uso-para-profissionais)
14. [Insights para Futuros Profissionais](#14-insights-para-futuros-profissionais)
15. [Glossário IBM Bob](#15-glossário-ibm-bob)
16. [Próximos Passos Sugeridos](#16-próximos-passos-sugeridos)

---

## 1. Visão Geral do Projeto

O **DIO Explorer** é um projeto de conclusão da trilha **IBM Bob Developer** na plataforma DIO.me. O objetivo foi demonstrar, na prática, as capacidades do IBM Bob como co-engenheiro de software: desde a criação de slash commands simples até a construção de um MCP Server completo com TypeScript.

### O que o projeto entrega

| Camada | O que faz |
|---|---|
| **Slash commands** (`.bob/commands/`) | Interface de chat — o usuário digita `/trilha Python` diretamente na conversa |
| **Skills** (`.bob/skills/`) | Instruções reutilizáveis que o Bob usa internamente para formatar respostas |
| **MCP Server** (`dio_explorer/mcp/`) | Servidor TypeScript que expõe as ferramentas ao Bob via protocolo MCP (Model Context Protocol) |
| **Módulo Python** (`dio_explorer/src/`) | Lógica de negócio pura, testável e independente |
| **Testes unitários** (`tests/`) | 62 testes, 100% de cobertura, 100% passando |
| **Dados** (`dio_explorer/data/`) | 34 trilhas DIO em JSON estruturado, 648.500 XP total |

---

## 2. Histórico de Construção — Cronologia da Sessão

A sessão de construção deste projeto ocorreu em **19 de setembro de 2026**, inteiramente conduzida com o IBM Bob como co-engenheiro. Abaixo está a sequência real de etapas percorridas.

### Etapa 1 — Primeiro Commit Simbólico
O projeto começou com um único arquivo: [`Hello World.md`](Hello World.md) com o conteúdo `"Cheguei, Brasil!"`. Este commit marca o ponto de partida e simboliza o início da jornada de aprendizado.

**Commit:** `8e41447 Add Hello World.md`

### Etapa 2 — Estrutura do Projeto e Dados
Criação da estrutura de diretórios (`dio_explorer/src`, `dio_explorer/data`, `dio_explorer/mcp`, `dio_explorer/docs`) e do arquivo de dados `trilhas_dio.json` com as 34 trilhas DIO.

**Commits:**
- `2452a0e Add dio_explorer project structure`
- `fca2a80 Add trilhas_dio.json to dio_explorer/data`

### Etapa 3 — Checkpoint Final (Sessão Completa)
Entrega completa: módulo Python, testes, slash commands, skills, MCP Server, documentação e configurações.

**Commit:** `f19ef1a feat: session checkpoint — MCP Server, slash commands, tests, docs`

---

## 3. Arquitetura do Projeto

```
IBM_Bob_-_Final_Project/
│
├── Hello World.md                          ← Primeiro commit simbólico
├── .bobignore                              ← Arquivos que o Bob não deve indexar
├── .gitignore                              ← Exclusões do git (Python + Node.js + SO)
├── README.md                              ← Visão geral do projeto
├── DOCUMENTATION.md                       ← Este arquivo (documentação completa)
├── resumo-do-dia-ibm-bob-final-project.html ← Relatório cronológico em HTML
├── resultados_testes.txt                  ← Saída completa da suite de testes
│
├── .bob/                                   ← Configuração local do IBM Bob
│   ├── mcp.json                            ← Registro do MCP Server (stdio)
│   ├── commands/                           ← Slash commands ativos
│   │   ├── trilha.md      → /trilha <tecnologia>
│   │   ├── trilhas.md     → /trilhas
│   │   ├── desafio.md     → /desafio <tecnologia> <nivel>
│   │   └── certificado.md → /certificado <nome> <tecnologia>
│   └── skills/                             ← Skills reutilizáveis
│       ├── trilha/SKILL.md
│       ├── trilhas/SKILL.md
│       └── certificado/SKILL.md
│
├── dio_explorer/                           ← Módulo principal
│   ├── data/
│   │   └── trilhas_dio.json               ← 34 trilhas · 648.500 XP total
│   ├── src/
│   │   └── dio_commands.py                ← Lógica dos 3 comandos (Python 3.13)
│   ├── mcp/                               ← MCP Server
│   │   ├── src/index.ts                   ← Código-fonte TypeScript
│   │   ├── build/index.js                 ← Artefato compilado (executável)
│   │   ├── package.json                   ← Dependências Node.js
│   │   ├── tsconfig.json                  ← Configuração TypeScript
│   │   └── README.md                      ← Docs do MCP Server
│   └── docs/                              ← Documentação da arquitetura (em construção)
│
└── tests/                                  ← Testes unitários
    ├── __init__.py
    └── test_dio_commands.py               ← 62 testes · 100% pass · 100% cobertura
```

### Fluxo de dados

```
Usuário no chat
      │
      ▼
/trilha Python          (slash command)
      │
      ▼
.bob/commands/trilha.md   (instrução para o Bob)
      │
      ▼  [Bob lê o arquivo JSON diretamente OU chama a tool MCP]
dio_explorer/data/trilhas_dio.json
      │
      ▼
Resposta formatada em Markdown para o usuário
```

---

## 4. Prompts Utilizados na Sessão

Esta seção documenta os **prompts reais** que foram usados para construir o projeto com o IBM Bob. Cada prompt é um exemplo concreto de como se comunica com um agente de IA para engenharia de software.

---

### 4.1 Criação da estrutura do projeto

```
Crie a estrutura de diretórios para o projeto DIO Explorer:
- dio_explorer/src/
- dio_explorer/data/
- dio_explorer/mcp/
- dio_explorer/docs/
Crie também um arquivo __init__.py em tests/.
```

**Por que funcionou:** O prompt foi **específico e estruturado**. Listou exatamente o que precisava, sem ambiguidade. O Bob executou sem perguntas.

---

### 4.2 Criação do arquivo de dados JSON

```
Crie o arquivo dio_explorer/data/trilhas_dio.json com 34 trilhas da plataforma DIO.me.
Cada trilha deve ter os campos:
- id (int, único)
- nome (string, ex: "Formação Python Developer")
- tecnologia (string, ex: "Python")
- numero_de_modulos (int)
- xp_total (int)
- badges_disponiveis (lista de strings)
- promocoes (objeto com desconto_percentual e descricao)
- vitalicio (boolean)
- lives_ao_vivo (lista de objetos com titulo, data e horario)

Inclua trilhas para: Python, Java, JavaScript, TypeScript, Go, Rust, Kotlin, Swift,
PHP, Ruby, .NET, React, Angular, Vue.js, Flutter, Node.js, DevOps, Linux, AWS, Azure,
GCP, Machine Learning, Data Science, Engenharia de Dados, GenAI, MLOps, Power BI,
Cybersecurity, QA, SQL, Blockchain, Unity, UX, Scrum.
```

**Por que funcionou:** Definiu o **schema completo** do JSON antes de pedir a criação. O Bob gerou dados consistentes porque a estrutura estava clara.

---

### 4.3 Criação do módulo Python

```
Crie o arquivo dio_explorer/src/dio_commands.py com a lógica dos 3 comandos:

1. cmd_trilha(tecnologia, caminho_dados=None) → str
   - Carrega trilhas_dio.json
   - Busca por correspondência parcial case-insensitive
   - Retorna Markdown formatado com badges, lives, promoção e acesso vitalício
   - Retorna mensagem de erro se não encontrar

2. cmd_desafio(tecnologia, nivel) → str
   - Níveis: iniciante, intermediario, avancado (com e sem acentos)
   - Gera desafio aleatório com enunciado, dicas, restrições, critérios e XP
   - XP: iniciante 150-300, intermediario 350-600, avancado 700-1200

3. cmd_certificado(nome_usuario, tecnologia, caminho_dados=None, data_base=None) → str
   - Gera certificado fictício em ASCII art
   - Data de emissão = hoje + numero_de_modulos semanas
   - Código de verificação: DIO-{ANO}{ID:02d}-{6 chars aleatórios maiúsculos}

Funções utilitárias:
- carregar_trilhas(caminho)
- buscar_trilha(termo, trilhas)
- formatar_data_br(data_iso)
- gerar_codigo_verificacao(id_trilha, ano)
```

**Por que funcionou:** Documentar as **assinaturas das funções** antecipadamente é uma das técnicas mais poderosas de prompt engineering para código. O Bob gerou código limpo e testável porque a interface estava definida.

---

### 4.4 Criação dos testes unitários

```
Crie tests/test_dio_commands.py com testes unitários para dio_commands.py.
Requisitos:
- Cobertura mínima de 70%
- Use unittest com fixture JSON temporária (não dependa do arquivo real para a maioria dos testes)
- Teste os 3 comandos: cmd_trilha, cmd_desafio, cmd_certificado
- Teste casos de sucesso E casos de erro (trilha não encontrada, nível inválido)
- Inclua testes de integração com o arquivo real para 4 casos (TestIntegracaoArquivoReal)
- Use unittest.mock.patch para controlar randomness onde necessário
```

**Por que funcionou:** Especificar **casos de sucesso E erro** é fundamental. A maioria dos iniciantes só testa o caminho feliz. O prompt forçou cobertura dos edge cases.

---

### 4.5 Criação dos slash commands

```
Crie os slash commands para o IBM Bob em .bob/commands/:

1. trilha.md
   - description: Exibe todos os níveis de estudo de uma trilha DIO pela tecnologia
   - argument-hint: <tecnologia>
   - Instrução: leia trilhas_dio.json, busca case-insensitive parcial, formato Markdown
     com seções: Plano de Estudos, Módulos (gerados), Badges, Lives, Promoção, Acesso Vitalício

2. trilhas.md
   - description: Lista todas as trilhas DIO disponíveis para escolha
   - Exibe catálogo completo em tabelas por categoria

3. desafio.md
   - description: Gera um desafio de código aleatório
   - argument-hint: <tecnologia> <nivel: iniciante|intermediario|avancado>
   - Inclui: enunciado criativo, exemplos E/S, dicas, restrições, critérios, XP

4. certificado.md
   - description: Gera um certificado fictício
   - argument-hint: <nome-do-usuario> <tecnologia-da-trilha>
   - Lê JSON, calcula data, gera código único, exibe em ASCII art
```

**Por que funcionou:** Descrever **o comportamento esperado de cada argumento** elimina ambiguidades. O `$1` e `$2` nos slash commands são variáveis que o Bob substitui automaticamente.

---

### 4.6 Criação do MCP Server

```
Crie o MCP Server em dio_explorer/mcp/ usando TypeScript e @modelcontextprotocol/sdk.

Requisitos:
- Transporte: stdio (spawned by Bob)
- 3 ferramentas: trilha, desafio, certificado
- Use registerTool() da API v2 do SDK
- Valide inputs com zod
- A lógica deve espelhar exatamente dio_commands.py (mesmas funções, mesma saída)
- Leia trilhas_dio.json de ../../data/trilhas_dio.json (relativo ao src/)
- package.json com type: module, script build: tsc && chmod 755 build/index.js
- tsconfig.json: target ES2022, module NodeNext, strict: true

Registre o servidor em .bob/mcp.json após o build.
```

**Por que funcionou:** Especificar o **caminho relativo do arquivo de dados** e o **formato exato do package.json** evitou retrabalho. Detalhes de configuração são onde os projetos falham.

---

### 4.7 Registro do MCP Server

```
Registre o MCP Server no IBM Bob criando .bob/mcp.json:
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": ["<caminho absoluto para dio_explorer/mcp/build/index.js>"]
    }
  }
}
Use o caminho absoluto real do projeto.
```

**Por que funcionou:** O IBM Bob usa o arquivo `.bob/mcp.json` para descobrir e iniciar servidores MCP. O caminho absoluto garante que funcione independente do diretório de trabalho.

---

### 4.8 Checkpoint e commit

```
Faça um commit completo com todas as mudanças da sessão.
Título: feat: session checkpoint — MCP Server, slash commands, tests, docs
Descrição detalhada listando todos os módulos entregues e próximos passos.
```

**Por que funcionou:** Commits descritivos são documentação do processo. A mensagem de commit deste projeto tem valor histórico — futuros profissionais podem reconstruir a sessão lendo apenas o `git log`.

---

### 4.9 Retorno ao checkpoint

```
Bob, retorne o projeto do ponto de checkpoint – commit f19ef1a
```

**Resposta do Bob:** O projeto já estava no commit correto. O Bob verificou com `git log` e `git show --stat HEAD` antes de responder — nunca especula.

---

## 5. Modos de Uso — Slash Commands

Os slash commands são a interface mais simples para o usuário final. Basta digitar no chat do IBM Bob.

### `/trilhas`

Lista o catálogo completo de 34 trilhas organizado por categoria.

```
/trilhas
```

**Saída:** Tabelas Markdown com tecnologia, formação, módulos e XP por categoria (Linguagens, Frontend, Cloud, IA/Dados, etc.)

**Quando usar:** Para descobrir quais trilhas existem antes de explorar uma específica.

---

### `/trilha <tecnologia>`

Exibe o plano de estudos completo de uma trilha.

```
/trilha Python
/trilha machine learning
/trilha react
/trilha AWS
```

**Saída:** Plano com módulos numerados (gerados pelo Bob), badges, lives agendadas, promoção ativa e informação de acesso vitalício.

**Busca:** Case-insensitive, correspondência parcial. `/trilha java` retorna tanto "Java" quanto "JavaScript".

**Quando usar:** Quando o estudante quer conhecer a estrutura completa de uma formação antes de iniciar.

---

### `/desafio <tecnologia> <nivel>`

Gera um desafio de código aleatório.

```
/desafio Python iniciante
/desafio Java intermediario
/desafio TypeScript avancado
/desafio Go avançado
```

**Níveis válidos:** `iniciante`, `intermediario` (ou `intermediário`), `avancado` (ou `avançado`)

**Saída:** Enunciado, exemplo de entrada/saída, dicas, restrições, critérios de avaliação e XP a ganhar.

**XP por nível:**
| Nível | XP |
|---|---|
| Iniciante | 150 — 300 XP |
| Intermediário | 350 — 600 XP |
| Avançado | 700 — 1.200 XP |

**Quando usar:** Para praticar antes de uma entrevista, revisar conceitos ou criar exercícios para outros.

---

### `/certificado <nome> <tecnologia>`

Gera um certificado fictício de conclusão.

```
/certificado "João da Silva" Java
/certificado "Maria Oliveira" Python
/certificado "Rafael Santos" Machine Learning
```

**Saída:** Certificado em ASCII art + tabela com dados + mensagem de parabéns.

**Nota:** Este é um certificado **fictício**, gerado para fins educacionais. Certificados oficiais são emitidos diretamente pela plataforma DIO.me.

**Quando usar:** Para demonstrar o projeto, celebrar uma conquista fictícia ou como exemplo de output para estudantes.

---

## 6. Modos de Uso — Skills

Skills são instruções que o IBM Bob carrega automaticamente quando ativadas. Diferente dos slash commands (que o usuário invoca diretamente), skills são usadas pelo Bob internamente para enriquecer respostas.

### Ativando uma skill programaticamente

```python
# No código do Bob, via use_skill:
use_skill("trilha")
use_skill("certificado")
```

### Invocação pelo usuário (user-invocable: true)

As skills deste projeto têm `user-invocable: true`, então o usuário pode ativá-las diretamente:

```
@trilha Python
@certificado João da Silva Java
```

### Diferença entre skill e slash command

| | Slash Command | Skill |
|---|---|---|
| **Invocação** | `/comando argumento` | `@skill argumento` ou automática |
| **Localização** | `.bob/commands/` | `.bob/skills/<nome>/SKILL.md` |
| **Frontmatter** | `description` + `argument-hint` | `name` + `description` + `metadata` |
| **Uso principal** | Interface do usuário | Contexto interno do Bob |

---

## 7. Modos de Uso — MCP Server (Ferramentas Nativas)

O MCP Server expõe as ferramentas ao Bob como **funções nativas**, sem que o usuário precise saber que existem. O Bob as chama automaticamente quando necessário.

### Ferramentas disponíveis

| Tool ID | Parâmetros | Descrição |
|---|---|---|
| `trilha` | `tecnologia: string` | Retorna plano de estudos |
| `desafio` | `tecnologia: string`, `nivel: string` | Gera desafio aleatório |
| `certificado` | `nome_usuario: string`, `tecnologia: string` | Gera certificado fictício |

### Build e execução

```bash
# 1. Instalar dependências
cd dio_explorer/mcp && npm install

# 2. Compilar TypeScript
npm run build

# 3. O servidor é iniciado automaticamente pelo Bob via .bob/mcp.json
# Não é necessário rodar manualmente
```

### Registro em .bob/mcp.json

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

### Verificando se o servidor está ativo

No chat do Bob, qualquer ferramenta MCP registrada fica visível nos tool calls. Quando o Bob usa a ferramenta `trilha`, a chamada aparece como:

```
mcp__dio-explorer__trilha({ tecnologia: "Python" })
```

---

## 8. Módulo Python — dio_commands.py

Arquivo: [`dio_explorer/src/dio_commands.py`](dio_explorer/src/dio_commands.py)

### Funções públicas

| Função | Assinatura | Retorno |
|---|---|---|
| `carregar_trilhas` | `(caminho=None) → list` | Lista de dicts do JSON |
| `buscar_trilha` | `(termo, trilhas) → list` | Trilhas que batem com o termo |
| `formatar_data_br` | `(data_iso: str) → str` | `"2025-08-10"` → `"10/08/2025"` |
| `gerar_codigo_verificacao` | `(id_trilha, ano) → str` | `"DIO-202602-X7K9AB"` |
| `cmd_trilha` | `(tecnologia, caminho_dados=None) → str` | Markdown do plano de estudos |
| `cmd_desafio` | `(tecnologia, nivel) → str` | Markdown do desafio |
| `cmd_certificado` | `(nome, tecnologia, caminho_dados=None, data_base=None) → str` | Markdown do certificado |

### Exemplo de uso direto

```python
from dio_explorer.src.dio_commands import cmd_trilha, cmd_desafio, cmd_certificado

# Plano de estudos
print(cmd_trilha("Python"))

# Desafio intermediário
print(cmd_desafio("Java", "intermediario"))

# Certificado
from datetime import date
print(cmd_certificado("João da Silva", "Java", data_base=date(2026, 9, 19)))
```

### Normalização de níveis

O módulo aceita variações com e sem acentos:

```python
# Todos equivalentes:
cmd_desafio("Python", "avancado")
cmd_desafio("Python", "avançado")
cmd_desafio("Python", "intermediario")
cmd_desafio("Python", "intermediário")
```

---

## 9. MCP Server — TypeScript/Node.js

Arquivo: [`dio_explorer/mcp/src/index.ts`](dio_explorer/mcp/src/index.ts)

### Stack

| Dependência | Versão | Papel |
|---|---|---|
| `@modelcontextprotocol/sdk` | ^1.0.0 | Framework MCP (McpServer, StdioServerTransport) |
| `zod` | ^3.25.0 | Validação de schemas dos inputs |
| `typescript` | ^5.0.0 | Compilador |
| `@types/node` | ^22.0.0 | Tipos Node.js |
| Node.js | 24 | Runtime |

### Padrão de registro de ferramenta

```typescript
server.registerTool(
  "nome-da-ferramenta",
  {
    description: "Descrição clara e objetiva",
    inputSchema: z.object({
      param: z.string().describe("O que este parâmetro representa"),
    }),
  },
  async ({ param }) => {
    try {
      const resultado = minhaFuncao(param);
      return { content: [{ type: "text", text: resultado }] };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Erro: ${error}` }],
        isError: true,
      };
    }
  }
);
```

### Bootstrap (padrão stdio)

```typescript
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("servidor rodando via stdio"); // stderr, não stdout!
}
main().catch((e) => { console.error(e); process.exit(1); });
```

> **⚠️ Atenção:** Use sempre `console.error()` para logs no servidor MCP. `console.log()` vai para stdout, que é o canal de comunicação MCP — contaminar stdout causa erros de parse no cliente.

---

## 10. Testes Unitários

Arquivo: [`tests/test_dio_commands.py`](tests/test_dio_commands.py)

### Resultado final

```
62 passed in 0.21s
Cobertura: 100% (dio_explorer/src/dio_commands.py)
```

### Classes de teste

| Classe | Testes | O que cobre |
|---|---|---|
| `TestUtilitarios` | 15 | `carregar_trilhas`, `buscar_trilha`, `formatar_data_br`, `gerar_codigo_verificacao`, `_normalizar_nivel` |
| `TestCmdTrilha` | 13 | Todos os casos do `cmd_trilha`: sucesso, erro, lives, promoção, vitalício |
| `TestCmdDesafio` | 14 | Todos os casos do `cmd_desafio`: níveis, XP ranges, acentuação, erros |
| `TestCmdCertificado` | 16 | Todos os campos do certificado, datas, códigos, erros |
| `TestIntegracaoArquivoReal` | 4 | Integração real lendo `trilhas_dio.json` do disco |

### Executando os testes

```bash
# Suite completa
python -m pytest tests/ -v

# Com cobertura
python -m pytest tests/ --cov=dio_explorer/src --cov-report=term-missing

# Teste único
python -m pytest tests/test_dio_commands.py::TestCmdTrilha::test_trilha_java_retorna_markdown -v
```

### Técnicas utilizadas

```python
# 1. Fixture JSON em arquivo temporário (independência do arquivo real)
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(_TRILHAS_FIXTURE, f)
    self.fixture_path = f.name

# 2. Controle de aleatoriedade com mock
with patch("dio_commands.random.choice", return_value="Verificador de número primo"):
    resultado = dc.cmd_desafio("Python", "iniciante")

# 3. Data determinística para certificado
resultado = dc.cmd_certificado("João", "Java", data_base=date(2026, 9, 19))

# 4. Verificação de regex para formato do código
self.assertRegex(codigo, r"^DIO-\d{6,7}-[A-Z0-9]{6}$")
```

---

## 11. Dados — trilhas_dio.json

Arquivo: [`dio_explorer/data/trilhas_dio.json`](dio_explorer/data/trilhas_dio.json)

### Estrutura do schema

```json
{
  "trilhas": [
    {
      "id": 1,
      "nome": "Formação Python Developer",
      "tecnologia": "Python",
      "numero_de_modulos": 12,
      "xp_total": 18500,
      "badges_disponiveis": ["Python Essentials", "OOP Master", "Python Expert"],
      "promocoes": {
        "desconto_percentual": 20,
        "descricao": "20% OFF em cursos parceiros ao concluir"
      },
      "vitalicio": true,
      "lives_ao_vivo": [
        {
          "titulo": "Python para Data Science",
          "data": "2025-07-15",
          "horario": "19:00"
        }
      ]
    }
  ]
}
```

### Resumo das 34 trilhas por categoria

| Categoria | Trilhas |
|---|---|
| Linguagens | Python, Java, JavaScript, TypeScript, Go, Rust, Kotlin, Swift, PHP, Ruby, .NET |
| Frontend & Mobile | React, Angular, Vue.js, Flutter |
| Backend, DevOps & Infra | Node.js, DevOps, Linux |
| Cloud | AWS, Azure, GCP |
| Dados & IA | Machine Learning, Data Science, Engenharia de Dados, GenAI, MLOps, Power BI |
| Segurança & QA | Cybersecurity, QA |
| Banco de Dados | SQL |
| Especialidades | Blockchain, Unity, UX, Scrum |

**Total:** 34 trilhas · 648.500 XP acumulado

---

## 12. Configuração do IBM Bob (.bob/)

### .bob/mcp.json — Registro do servidor MCP

```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": ["/caminho/absoluto/build/index.js"]
    }
  }
}
```

> Use sempre o **caminho absoluto** no `args`. Caminhos relativos causam falha de inicialização porque o Bob pode ser executado de qualquer diretório.

### .bobignore — Exclusões de contexto

```
node_modules/
.env
data/cache-progresso/
docs/certificados-emitidos/
*.tmp
```

O `.bobignore` evita que o Bob indexe arquivos desnecessários (especialmente `node_modules/`, que tem centenas de arquivos).

### Frontmatter dos slash commands

```yaml
---
description: Descrição breve do que o comando faz
argument-hint: <arg1> <arg2>
---
```

- `description`: Aparece no autocomplete quando o usuário digita `/`
- `argument-hint`: Exibido como placeholder: `/trilha <tecnologia>`
- `$1`, `$2`: Variáveis substituídas pelos argumentos em ordem

### Frontmatter das skills

```yaml
---
name: nome-da-skill
description: Descrição clara
metadata:
  user-invocable: true
  argument-hint: <arg1> <arg2>
---
```

- `user-invocable: true`: Permite que o usuário chame diretamente com `@skill`
- `name`: Identificador único da skill (deve ser único no projeto)

---

## 13. Dicas de Uso para Profissionais

### Dica 1 — Use o contexto do workspace

O IBM Bob lê todos os arquivos do projeto automaticamente. Você **não precisa** colar código no chat. Basta referenciar:

```
Bob, olha o arquivo dio_explorer/src/dio_commands.py — como posso adicionar suporte
para busca por ID de trilha além de nome?
```

### Dica 2 — Defina a interface antes da implementação

Antes de pedir código, especifique a assinatura das funções:

```
Crie uma função:
  exportar_certificado_pdf(nome: str, tecnologia: str, caminho_saida: str) → bool
que salva o certificado em PDF usando a biblioteca reportlab.
```

Isso garante que o código gerado seja **compatível** com o resto do projeto.

### Dica 3 — Peça testes junto com o código

```
Crie a função X. Junto com ela, crie um teste unitário que cubra o caso de sucesso
e pelo menos um caso de erro.
```

### Dica 4 — Use o modo Plan antes de codar

Para projetos complexos, use o modo `Plan` do Bob antes de começar:

```
[Modo: Plan]
Quero adicionar autenticação com JWT ao MCP Server.
Qual é a abordagem mais simples que não quebra a compatibilidade com stdio?
```

### Dica 5 — Commits como pontos de restauração

```
Bob, faça commit de tudo com a mensagem:
"feat: adicionar suporte a exportação PDF"
```

Assim você pode sempre voltar com `git checkout <commit>` se algo der errado.

### Dica 6 — Seja específico sobre o "não fazer"

```
Adicione validação de email no certificado.
NÃO altere o formato do ASCII art.
NÃO modifique os testes existentes.
```

O Bob respeita restrições explícitas.

### Dica 7 — Aproveite o MCP Server para integrações

Uma vez que o servidor está rodando, qualquer ferramenta MCP registrada fica disponível para o Bob chamar automaticamente durante conversas. Você pode criar novas integrações simplesmente adicionando `server.registerTool(...)` em `index.ts` e recompilando.

---

## 14. Insights para Futuros Profissionais

### Insight 1 — O IBM Bob é um co-engenheiro, não um gerador de código

A diferença está na relação. Um gerador de código recebe um prompt e devolve código. Um co-engenheiro:

- Lê o projeto inteiro antes de responder
- Verifica o que existe antes de criar
- Pergunta quando há ambiguidade
- Executa testes para validar o que criou
- Sugere melhorias que você não pediu

Trate o Bob como você trataria um dev sênior na equipe: dê contexto, defina expectativas, revise o que foi feito.

---

### Insight 2 — Prompt engineering para código é diferente de prompt engineering para texto

Para texto: seja criativo, deixe espaço para interpretação.
Para código: seja preciso, defina tipos, assinaturas e comportamentos esperados.

**Ruim:**
```
Crie uma função para buscar trilhas.
```

**Bom:**
```
Crie buscar_trilha(termo: str, trilhas: list[dict]) → list[dict]
que retorna todas as trilhas onde term aparece (case-insensitive, parcial)
no campo "tecnologia" ou "nome". Retorna lista vazia se não encontrar.
```

---

### Insight 3 — A camada de dados é o contrato

O `trilhas_dio.json` foi criado com schema bem definido. Isso permitiu que Python e TypeScript tivessem **a mesma lógica** sem ambiguidade. Defina seus schemas cedo — é o que evita retrabalho.

---

### Insight 4 — Três formas de integrar com Bob (e quando usar cada uma)

| Mecanismo | Quando usar | Custo de setup |
|---|---|---|
| **Slash command** | Interface para o usuário final, simples, sem código | Baixíssimo (1 arquivo .md) |
| **Skill** | Comportamento reutilizável que o Bob aplica internamente | Baixo (1 arquivo SKILL.md) |
| **MCP Server** | Lógica complexa, multi-linguagem, integrações externas | Alto (código + build + registro) |

Para a maioria dos casos em projetos didáticos, um slash command é suficiente. O MCP Server brilha quando você tem lógica que precisa ser testada, versionada e reutilizada por múltiplos clientes.

---

### Insight 5 — Testes são documentação executável

Os 62 testes deste projeto documentam **exatamente** como as funções se comportam:

```python
def test_gerar_codigo_formato(self):
    """O código deve ter o formato DIO-AAAAMM-XXXXXX."""
    # Isso é mais claro que qualquer comentário
    codigo = dc.gerar_codigo_verificacao(2, 2026)
    self.assertRegex(codigo, r"^DIO-\d{6,7}-[A-Z0-9]{6}$")
```

Quando um novo desenvolvedor chega no projeto, lê os testes antes de ler o código.

---

### Insight 6 — O stdio é o protocolo mais simples para MCP

O protocolo MCP suporta `stdio` e `HTTP`. Para desenvolvimento local:

- **stdio**: Bob inicia o processo, tudo via stdin/stdout. Sem porta, sem autenticação, sem CORS. É o ideal para ferramentas locais.
- **HTTP (StreamableHTTP)**: Para expor o servidor remotamente, compartilhar entre equipes, usar em CI/CD. Requer mais configuração.

Este projeto usa stdio. Para expor via HTTP, veja a documentação oficial do `@modelcontextprotocol/sdk`.

---

### Insight 7 — Versionamento é a memória do projeto

Os 4 commits deste projeto contam a história completa:

```
8e41447  Add Hello World.md              ← Ponto de partida
2452a0e  Add dio_explorer project structure
fca2a80  Add trilhas_dio.json
f19ef1a  feat: session checkpoint — MCP Server, slash commands, tests, docs
```

Uma mensagem de commit bem escrita permite que qualquer pessoa reconstrua o contexto da sessão sem ler uma linha de código.

---

### Insight 8 — A IA não substitui o entendimento — ela amplifica

Você só consegue dirigir o IBM Bob com precisão se entende o que está pedindo. Quem domina Python escreve prompts melhores para código Python. Quem entende MCP configura o servidor corretamente.

A lição deste projeto: **aprenda os fundamentos. A IA faz o trabalho pesado, você faz as decisões.**

---

## 15. Glossário IBM Bob

| Termo | Definição |
|---|---|
| **Slash command** | Comando que o usuário invoca digitando `/comando` no chat. Definido em `.bob/commands/` como arquivo `.md` com frontmatter. |
| **Skill** | Instrução reutilizável que o Bob carrega em contexto. Definida em `.bob/skills/<nome>/SKILL.md`. |
| **MCP** | Model Context Protocol — protocolo aberto para comunicação entre clientes AI e servidores de ferramentas. |
| **MCP Server** | Processo externo que expõe ferramentas ao Bob via protocolo MCP. Registrado em `.bob/mcp.json`. |
| **Tool** | Função exposta pelo MCP Server. Aparece como `mcp__servidor__ferramenta` nos tool calls. |
| **stdio transport** | Transporte MCP onde Bob inicia o processo servidor e se comunica via stdin/stdout. |
| **registerTool** | Método da API v2 do `@modelcontextprotocol/sdk` para registrar ferramentas no servidor. |
| **frontmatter** | Bloco YAML delimitado por `---` no início de arquivos `.md` que configura metadados. |
| **$1, $2** | Variáveis de argumentos em slash commands e skills, substituídas pelos valores passados pelo usuário. |
| **.bobignore** | Arquivo que lista padrões de arquivos que o Bob deve ignorar ao indexar o contexto do projeto. |
| **workspace** | Diretório raiz do projeto aberto no IBM Bob. O Bob opera relativamente a este diretório. |
| **tool call** | Chamada de ferramenta executada pelo Bob durante uma resposta. Visível no painel de atividade do Bob. |

---

## 16. Próximos Passos Sugeridos

Os próximos passos abaixo foram definidos no commit de checkpoint e representam a evolução natural do projeto.

### Curto prazo

- [ ] **`dio_explorer/docs/`** — Documentação da arquitetura em formato ADR (Architecture Decision Records)
- [ ] **CI/CD** — GitHub Actions com dois jobs: `pytest` (Python) + `npm run build` (TypeScript)
- [ ] **Testes do MCP Server** — Testes unitários para `index.ts` usando Jest

### Médio prazo

- [ ] **HTTP Transport** — Expor o MCP Server via `StreamableHTTPServerTransport` para uso remoto
- [ ] **Autenticação** — API Key para o servidor HTTP
- [ ] **Busca semântica** — Substituir busca por substring por embeddings (ex: buscar "aprendizado de máquina" e encontrar "Machine Learning")

### Longo prazo

- [ ] **Integração real com DIO.me** — Substituir JSON estático por chamadas à API real da plataforma
- [ ] **Progresso do usuário** — Persistir XP e trilhas concluídas por usuário
- [ ] **Dashboard** — Visualização do progresso em HTML gerado pelo Bob

---

*Documentação gerada com IBM Bob · Sessão de 19/09/2026 · Commit `f19ef1a`*
