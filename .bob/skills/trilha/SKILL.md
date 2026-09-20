---
name: trilha
description: Exibe todos os níveis de estudo de uma trilha DIO pela tecnologia
metadata:
  user-invocable: true
  argument-hint: <tecnologia>
---

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e procure **todas** as trilhas cujo campo `tecnologia` ou `nome` contenha o termo "$1" (busca **case-insensitive**, correspondência parcial).

**Se encontrar uma ou mais trilhas**, exiba cada uma no seguinte formato Markdown:

---

## 📚 Plano de Estudos — {nome da trilha}

**Tecnologia:** {tecnologia}
**Total de módulos:** {numero_de_modulos}
**XP total ao concluir:** {xp_total} XP

---

### 🗂️ Módulos da Trilha

Liste os módulos numerados de **1** até **{numero_de_modulos}**, gerando títulos progressivos (do básico ao avançado) coerentes com a tecnologia. Cada item deve ter:
- Um **título** curto e relevante
- Uma **descrição de uma linha** do que será abordado

---

### 🏅 Badges Disponíveis

{lista de badges, uma por linha, precedida pelo emoji 🥇}

---

### 📡 Lives ao Vivo

{lista de lives no formato:}
- **{título}** — {data no formato DD/MM/AAAA} às {horário}

Se não houver lives, escreva: _Nenhuma live agendada no momento._

---

### 🎁 Promoção Especial

{Se desconto_percentual > 0: exiba a descrição da promoção.}
{Se desconto_percentual == 0: escreva "Nenhuma promoção ativa no momento."}

---

### ♾️ Acesso Vitalício

{Se vitalicio == true: "✅ Sim — esta trilha possui acesso vitalício."}
{Se vitalicio == false: "❌ Não — o acesso é por período limitado."}

---

**Se nenhuma trilha for encontrada** com o termo "$1", responda exatamente:

> ❌ Nenhuma trilha encontrada para **"$1"**.
>
> 💡 Tente um dos termos disponíveis digitando `/trilhas` para ver o catálogo completo.
