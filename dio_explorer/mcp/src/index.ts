#!/usr/bin/env node
/**
 * dio-explorer-mcp
 * MCP Server que expõe as funcionalidades do DIO Explorer:
 *   - trilha    : consulta plano de estudos por tecnologia
 *   - desafio   : gera desafio de código com nível e XP
 *   - certificado: gera certificado fictício de conclusão
 *
 * Transporte: stdio (spawned by Bob/Claude Desktop)
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// ---------------------------------------------------------------------------
// Caminhos
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// src/ está em mcp/src/, dados em mcp/../data/
const DATA_PATH = path.resolve(__dirname, "../../data/trilhas_dio.json");

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------
interface Live {
  titulo: string;
  data: string;
  horario: string;
}

interface Promocao {
  desconto_percentual: number;
  descricao: string;
}

interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  numero_de_modulos: number;
  xp_total: number;
  badges_disponiveis: string[];
  promocoes: Promocao;
  vitalicio: boolean;
  lives_ao_vivo: Live[];
}

// ---------------------------------------------------------------------------
// Utilidades
// ---------------------------------------------------------------------------
function carregarTrilhas(): Trilha[] {
  const raw = fs.readFileSync(DATA_PATH, "utf-8");
  const dados = JSON.parse(raw) as { trilhas: Trilha[] };
  return dados.trilhas;
}

function buscarTrilha(termo: string, trilhas: Trilha[]): Trilha[] {
  const t = termo.trim().toLowerCase();
  return trilhas.filter(
    (tr) =>
      tr.tecnologia.toLowerCase().includes(t) ||
      tr.nome.toLowerCase().includes(t)
  );
}

function formatarDataBr(dataIso: string): string {
  const [ano, mes, dia] = dataIso.split("-");
  return `${dia}/${mes}/${ano}`;
}

function gerarCodigoVerificacao(idTrilha: number, ano: number): string {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let sufixo = "";
  for (let i = 0; i < 6; i++) {
    sufixo += chars[Math.floor(Math.random() * chars.length)];
  }
  return `DIO-${ano}${String(idTrilha).padStart(2, "0")}-${sufixo}`;
}

const TECNOLOGIAS_DISPONIVEIS =
  "`Python`, `Java`, `React`, `Angular`, `Node.js`, `AWS`, `Azure`, " +
  "`Machine Learning`, `Data Science`, `Kotlin`, `Flutter`, `.NET`, " +
  "`DevOps`, `Cybersecurity`, `SQL`, `Vue.js`, `TypeScript`, `Go`, " +
  "`Rust`, `Swift`, `Blockchain`, `UX`, `Unity`, `QA`, `GenAI`, " +
  "`GCP`, `Engenharia de Dados`, `PHP`, `Ruby`, `Scrum`, `Linux`, " +
  "`JavaScript`, `Power BI`, `MLOps`";

// ---------------------------------------------------------------------------
// Lógica /trilha
// ---------------------------------------------------------------------------
function cmdTrilha(tecnologia: string): string {
  const trilhas = carregarTrilhas();
  const resultados = buscarTrilha(tecnologia, trilhas);

  if (resultados.length === 0) {
    return (
      `> ❌ Nenhuma trilha encontrada para **"${tecnologia}"**.\n` +
      `>\n` +
      `> 💡 Tente um dos termos: ${TECNOLOGIAS_DISPONIVEIS}.`
    );
  }

  const saidas: string[] = [];
  for (const t of resultados) {
    const livesTxt =
      t.lives_ao_vivo.length > 0
        ? t.lives_ao_vivo
            .map(
              (l) =>
                `- **${l.titulo}** — ${formatarDataBr(l.data)} às ${l.horario}`
            )
            .join("\n")
        : "_Nenhuma live agendada no momento._";

    const badgesTxt = t.badges_disponiveis.map((b) => `🥇 ${b}`).join("\n");

    const promoTxt =
      t.promocoes.desconto_percentual > 0
        ? t.promocoes.descricao
        : "Nenhuma promoção ativa no momento.";

    const vitalicioTxt = t.vitalicio
      ? "✅ Sim — esta trilha possui acesso vitalício."
      : "❌ Não — o acesso é por período limitado.";

    saidas.push(
      `## 📚 Plano de Estudos — ${t.nome}\n\n` +
        `**Tecnologia:** ${t.tecnologia}\n` +
        `**Total de módulos:** ${t.numero_de_modulos}\n` +
        `**XP total ao concluir:** ${t.xp_total} XP\n\n` +
        `---\n\n` +
        `### 🏅 Badges Disponíveis\n\n${badgesTxt}\n\n` +
        `---\n\n` +
        `### 📡 Lives ao Vivo\n\n${livesTxt}\n\n` +
        `---\n\n` +
        `### 🎁 Promoção Especial\n\n${promoTxt}\n\n` +
        `---\n\n` +
        `### ♾️ Acesso Vitalício\n\n${vitalicioTxt}`
    );
  }

  return saidas.join("\n\n---\n\n");
}

// ---------------------------------------------------------------------------
// Lógica /desafio
// ---------------------------------------------------------------------------
const XP_RANGES: Record<string, [number, number]> = {
  iniciante: [150, 300],
  intermediario: [350, 600],
  avancado: [700, 1200],
};

const TEMAS_POR_NIVEL: Record<string, string[]> = {
  iniciante: [
    "Calculadora de operações básicas",
    "Verificador de número primo",
    "Conversor de temperatura (Celsius/Fahrenheit)",
    "Gerador de tabuada",
    "Contador de vogais em uma string",
  ],
  intermediario: [
    "Implementação de uma Pilha (Stack) sem biblioteca",
    "Algoritmo de busca binária",
    "Validador de expressões com parênteses balanceados",
    "Agenda de contatos com CRUD em memória",
    "Sistema de fila com prioridade",
  ],
  avancado: [
    "Implementação de cache LRU",
    "Parser de expressões matemáticas",
    "Servidor HTTP simples com threads",
    "Sistema de eventos assíncrono",
    "Algoritmo de compressão Run-Length Encoding",
  ],
};

const NIVEL_DISPLAY: Record<string, string> = {
  iniciante: "Iniciante",
  intermediario: "Intermediário",
  avancado: "Avançado",
};

function normalizarNivel(nivel: string): string {
  const n = nivel.trim().toLowerCase();
  if (n === "avancado" || n === "avançado") return "avancado";
  if (n === "intermediario" || n === "intermediário") return "intermediario";
  return n;
}

function randInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function cmdDesafio(tecnologia: string, nivel: string): string {
  const nivelNorm = normalizarNivel(nivel);

  if (!["iniciante", "intermediario", "avancado"].includes(nivelNorm)) {
    return (
      `> ❌ Nível **"${nivel}"** inválido.\n` +
      `> Níveis válidos: \`iniciante\`, \`intermediario\`, \`avancado\`.`
    );
  }

  const temas = TEMAS_POR_NIVEL[nivelNorm];
  const tema = temas[Math.floor(Math.random() * temas.length)];
  const nivelDisplay = NIVEL_DISPLAY[nivelNorm];
  const [xpMin, xpMax] = XP_RANGES[nivelNorm];
  const xp = randInt(xpMin, xpMax);

  return (
    `## ⚔️ Desafio DIO — ${tecnologia} · Nível ${nivelDisplay}\n\n` +
    `> 🎲 *Desafio gerado aleatoriamente*\n\n` +
    `---\n\n` +
    `### 📋 Enunciado\n\n` +
    `Implemente **${tema}** utilizando **${tecnologia}**.\n` +
    `O programa deve aceitar entradas do usuário, processar a lógica central e\n` +
    `exibir o resultado formatado. Garanta tratamento de entradas inválidas e\n` +
    `siga as boas práticas da linguagem escolhida.\n\n` +
    `---\n\n` +
    `### 📥 Exemplo de Entrada\n\n` +
    "```\nEntrada 1: 10\nEntrada 2: 25\n```\n\n" +
    `### 📤 Exemplo de Saída Esperada\n\n` +
    "```\nResultado: processado com sucesso\n```\n\n" +
    `---\n\n` +
    `### 💡 Dicas\n\n` +
    `- Leia o enunciado com atenção antes de codificar.\n` +
    `- Comece pelo caso mais simples e evolua progressivamente.\n` +
    `- Escreva testes para cada caso de uso.\n` +
    `- Revise a complexidade do seu algoritmo.\n\n` +
    `---\n\n` +
    `### 🧩 Restrições\n\n` +
    `- Não utilize bibliotecas externas não mencionadas.\n` +
    `- A solução deve executar em tempo O(n) ou melhor.\n` +
    `- Trate entradas vazias ou nulas.\n\n` +
    `---\n\n` +
    `### 🏆 Critérios de Avaliação\n\n` +
    `| Critério | Peso |\n` +
    `|---|---|\n` +
    `| Corretude da solução | 40% |\n` +
    `| Clareza e legibilidade do código | 30% |\n` +
    `| Eficiência / performance | 20% |\n` +
    `| Boas práticas da linguagem | 10% |\n\n` +
    `---\n\n` +
    `### 🎯 XP ao Concluir\n\n` +
    `**+${xp} XP** ao concluir este desafio.`
  );
}

// ---------------------------------------------------------------------------
// Lógica /certificado
// ---------------------------------------------------------------------------
function cmdCertificado(nomeUsuario: string, tecnologia: string): string {
  const trilhas = carregarTrilhas();
  const resultados = buscarTrilha(tecnologia, trilhas);

  if (resultados.length === 0) {
    return (
      `> ❌ Trilha não encontrada para **"${tecnologia}"**. ` +
      `Verifique o nome da tecnologia e tente novamente.`
    );
  }

  const t = resultados[0];
  const hoje = new Date();
  const dataEmissao = new Date(hoje);
  dataEmissao.setDate(dataEmissao.getDate() + t.numero_de_modulos * 7);
  const dataEmissaoStr = dataEmissao.toLocaleDateString("pt-BR");

  const codigo = gerarCodigoVerificacao(t.id, hoje.getFullYear());
  const badgesTxt = t.badges_disponiveis.map((b) => `  ·  ${b}`).join("\n");
  const vitalicioTxt = t.vitalicio ? "Sim" : "Não";
  const nomeUpper = nomeUsuario.toUpperCase();

  const pad = (val: string | number, len: number) =>
    String(val).padEnd(len, " ");

  const certificado =
    "```\n" +
    "╔══════════════════════════════════════════════════════════════════════╗\n" +
    "║                                                                      ║\n" +
    "║                    🎓  CERTIFICADO DE CONCLUSÃO                      ║\n" +
    "║                                                                      ║\n" +
    "║                  Digital Innovation One — DIO.me                    ║\n" +
    "║                                                                      ║\n" +
    "╠══════════════════════════════════════════════════════════════════════╣\n" +
    "║                                                                      ║\n" +
    "║  Certificamos que                                                    ║\n" +
    "║                                                                      ║\n" +
    `║              ✦  ${pad(nomeUpper, 52)}✦  ║\n` +
    "║                                                                      ║\n" +
    "║  concluiu com êxito a formação:                                      ║\n" +
    "║                                                                      ║\n" +
    `║              ${pad(t.nome, 58)}║\n` +
    "║                                                                      ║\n" +
    `║  Tecnologia:   ${pad(t.tecnologia, 56)}║\n` +
    `║  Módulos:      ${t.numero_de_modulos} módulos concluídos${" ".repeat(40 - String(t.numero_de_modulos).length)}║\n` +
    `║  XP obtido:    ${t.xp_total} XP${" ".repeat(53 - String(t.xp_total).length)}║\n` +
    "║                                                                      ║\n" +
    "╠══════════════════════════════════════════════════════════════════════╣\n" +
    "║                                                                      ║\n" +
    "║  🏅 Badges conquistadas:                                             ║\n" +
    "║                                                                      ║\n" +
    `${badgesTxt}\n` +
    "║                                                                      ║\n" +
    "╠══════════════════════════════════════════════════════════════════════╣\n" +
    "║                                                                      ║\n" +
    `║  Data de emissão:   ${pad(dataEmissaoStr, 51)}║\n` +
    `║  Código:            ${pad(codigo, 51)}║\n` +
    "║                                                                      ║\n" +
    "║  ⚠️  Este é um certificado fictício gerado para fins educacionais.   ║\n" +
    "║     Certificados oficiais são emitidos pela plataforma DIO.me.       ║\n" +
    "║                                                                      ║\n" +
    "╚══════════════════════════════════════════════════════════════════════╝\n" +
    "```\n\n" +
    "---\n\n" +
    "## 📄 Dados do Certificado\n\n" +
    "| Campo | Valor |\n" +
    "|---|---|\n" +
    `| **Titular** | ${nomeUsuario} |\n` +
    `| **Formação** | ${t.nome} |\n` +
    `| **Tecnologia** | ${t.tecnologia} |\n` +
    `| **Módulos concluídos** | ${t.numero_de_modulos} |\n` +
    `| **XP total** | ${t.xp_total} XP |\n` +
    `| **Data de emissão** | ${dataEmissaoStr} |\n` +
    `| **Código de verificação** | \`${codigo}\` |\n` +
    `| **Acesso vitalício** | ${vitalicioTxt} |\n\n` +
    "---\n\n" +
    `> 🎉 Parabéns, **${nomeUsuario}**! Você concluiu a **${t.nome}** ` +
    "e está pronto para os próximos desafios.\n" +
    "> Continue evoluindo na plataforma [DIO.me](https://dio.me)!";

  return certificado;
}

// ---------------------------------------------------------------------------
// Servidor MCP
// ---------------------------------------------------------------------------
const server = new McpServer({
  name: "dio-explorer-mcp",
  version: "1.0.0",
});

// Ferramenta: trilha
server.registerTool(
  "trilha",
  {
    description:
      "Consulta o plano de estudos de uma trilha DIO pela tecnologia. " +
      "Retorna módulos, badges, lives ao vivo, promoções e informações de acesso.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe(
          "Nome da tecnologia ou trilha (ex: Python, Java, React, AWS, Machine Learning)"
        ),
    }),
  },
  async ({ tecnologia }) => {
    try {
      const resultado = cmdTrilha(tecnologia);
      return { content: [{ type: "text", text: resultado }] };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erro ao consultar trilha: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Ferramenta: desafio
server.registerTool(
  "desafio",
  {
    description:
      "Gera um desafio de programação aleatório para uma tecnologia e nível. " +
      "Inclui enunciado, dicas, restrições, critérios de avaliação e XP.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe(
          "Linguagem ou tecnologia para o desafio (ex: Python, Java, JavaScript)"
        ),
      nivel: z
        .string()
        .describe(
          "Nível de dificuldade: iniciante, intermediario ou avancado"
        ),
    }),
  },
  async ({ tecnologia, nivel }) => {
    try {
      const resultado = cmdDesafio(tecnologia, nivel);
      return { content: [{ type: "text", text: resultado }] };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erro ao gerar desafio: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Ferramenta: certificado
server.registerTool(
  "certificado",
  {
    description:
      "Gera um certificado fictício de conclusão de trilha DIO para um usuário. " +
      "Inclui badges conquistadas, código de verificação e data de emissão.",
    inputSchema: z.object({
      nome_usuario: z
        .string()
        .describe("Nome completo do estudante que receberá o certificado"),
      tecnologia: z
        .string()
        .describe(
          "Nome da tecnologia/trilha concluída (ex: Python, Java, React)"
        ),
    }),
  },
  async ({ nome_usuario, tecnologia }) => {
    try {
      const resultado = cmdCertificado(nome_usuario, tecnologia);
      return { content: [{ type: "text", text: resultado }] };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erro ao gerar certificado: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("dio-explorer-mcp rodando via stdio");
}

main().catch((error) => {
  console.error("Erro fatal:", error);
  process.exit(1);
});
