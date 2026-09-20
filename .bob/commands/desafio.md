---
description: Gera um desafio de código aleatório para uma tecnologia e nível escolhidos
argument-hint: <tecnologia> <nivel: iniciante|intermediario|avancado>
---
Gere um desafio de código **aleatório** para a tecnologia **"$1"** no nível **"$2"**.

O desafio deve ser único a cada invocação — varie o tema, contexto e enunciado de forma criativa.

Formate a resposta em Markdown exatamente assim:

---

## ⚔️ Desafio DIO — {tecnologia} · Nível {Nível com inicial maiúscula}

> 🎲 *Desafio gerado aleatoriamente*

---

### 📋 Enunciado

Escreva aqui um enunciado claro e objetivo do problema a resolver, com 3 a 6 linhas. O desafio deve ser realista e condizente com o nível informado:
- **Iniciante:** conceitos básicos, sintaxe, lógica simples
- **Intermediário:** estruturas de dados, algoritmos, integração de componentes
- **Avançado:** otimização, design patterns, concorrência, arquitetura

---

### 📥 Exemplo de Entrada

Forneça um ou dois exemplos de entrada com seus respectivos dados.

### 📤 Exemplo de Saída Esperada

Forneça a saída correspondente para cada entrada de exemplo.

---

### 💡 Dicas

Liste de 2 a 4 dicas objetivas que orientem o raciocínio sem entregar a solução.

---

### 🧩 Restrições

- Liste de 2 a 3 restrições técnicas relevantes (ex.: complexidade máxima, bibliotecas permitidas, sem uso de loops, etc.)

---

### 🏆 Critérios de Avaliação

| Critério | Peso |
|---|---|
| Corretude da solução | 40% |
| Clareza e legibilidade do código | 30% |
| Eficiência / performance | 20% |
| Boas práticas da linguagem | 10% |

---

### 🎯 XP ao Concluir

Calcule o XP de recompensa com base no nível:
- Iniciante: entre 150 e 300 XP
- Intermediário: entre 350 e 600 XP
- Avançado: entre 700 e 1200 XP

Exiba: **+{XP} XP** ao concluir este desafio.

---

Se a tecnologia "$1" não for reconhecida, avise o usuário e sugira tecnologias disponíveis.
Se o nível "$2" não for "iniciante", "intermediário" (ou "intermediario"), nem "avançado" (ou "avancado"), avise e liste os níveis válidos.
