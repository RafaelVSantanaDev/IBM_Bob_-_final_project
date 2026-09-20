# DIO Explorer MCP Server

Servidor MCP (Model Context Protocol) que expõe as funcionalidades do **DIO Explorer** — trilhas, desafios e certificados da plataforma [DIO.me](https://dio.me).

## Ferramentas disponíveis

| Ferramenta | Descrição |
|---|---|
| `trilha` | Consulta o plano de estudos de uma trilha DIO por tecnologia |
| `desafio` | Gera um desafio de programação aleatório com nível e XP |
| `certificado` | Gera um certificado fictício de conclusão de trilha |

## Uso via Bob / Claude Desktop

O servidor é registrado automaticamente via `.bob/mcp.json` do workspace. Basta perguntar ao Bob:

- *"Me mostre a trilha de Python"*
- *"Crie um desafio intermediário de JavaScript"*
- *"Gere meu certificado de React"*

## Estrutura

```
dio_explorer/mcp/
├── src/
│   └── index.ts       # Código-fonte TypeScript do servidor
├── build/
│   └── index.js       # Artefato compilado (gerado pelo npm run build)
├── package.json
├── tsconfig.json
└── README.md
```

## Desenvolvimento

```bash
# Instalar dependências
npm install

# Compilar
npm run build

# Compilar em modo watch
npm run dev
```

## Transporte

O servidor usa transporte **stdio** — é iniciado como processo filho pelo Bob/Claude Desktop e se comunica via stdin/stdout usando o protocolo MCP.

## Dados

Os dados das trilhas são lidos de [`../data/trilhas_dio.json`](../data/trilhas_dio.json), o mesmo arquivo usado pelo módulo Python [`../src/dio_commands.py`](../src/dio_commands.py).
