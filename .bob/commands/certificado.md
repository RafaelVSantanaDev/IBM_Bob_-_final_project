---
description: Gera um certificado fictício em Markdown para o usuário que concluiu uma trilha DIO
argument-hint: <nome-do-usuario> <tecnologia-da-trilha>
---
Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize a trilha cuja tecnologia corresponda a "$2" (busca case-insensitive com correspondência parcial).

Com os dados encontrados, gere um **certificado fictício** completo em Markdown, exatamente no formato abaixo. Substitua todos os campos entre `{chaves}` com os valores reais.

Calcule uma data de emissão fictícia consistente: some o número de módulos da trilha em semanas a partir de hoje.
Gere também um código de verificação único no formato `DIO-{ANO}{ID_DA_TRILHA com 2 dígitos}-{6 caracteres alfanuméricos maiúsculos aleatórios}`.

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    🎓  CERTIFICADO DE CONCLUSÃO                      ║
║                                                                      ║
║                  Digital Innovation One — DIO.me                    ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Certificamos que                                                    ║
║                                                                      ║
║              ✦  {NOME DO USUÁRIO EM MAIÚSCULAS}  ✦                  ║
║                                                                      ║
║  concluiu com êxito a formação:                                      ║
║                                                                      ║
║              {nome completo da trilha}                               ║
║                                                                      ║
║  Tecnologia:   {tecnologia}                                          ║
║  Módulos:      {numero_de_modulos} módulos concluídos                ║
║  XP obtido:    {xp_total} XP                                         ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🏅 Badges conquistadas:                                             ║
║                                                                      ║
║  {liste cada badge em uma linha, precedida de "  ·  "}              ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Data de emissão:   {data calculada no formato DD/MM/AAAA}           ║
║  Código:            {código de verificação gerado}                   ║
║                                                                      ║
║  ⚠️  Este é um certificado fictício gerado para fins educacionais.   ║
║     Certificados oficiais são emitidos pela plataforma DIO.me.       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 📄 Dados do Certificado

| Campo | Valor |
|---|---|
| **Titular** | $1 |
| **Formação** | {nome da trilha} |
| **Tecnologia** | {tecnologia} |
| **Módulos concluídos** | {numero_de_modulos} |
| **XP total** | {xp_total} XP |
| **Data de emissão** | {data calculada} |
| **Código de verificação** | `{código gerado}` |
| **Acesso vitalício** | {Sim / Não} |

---

> 🎉 Parabéns, **$1**! Você concluiu a **{nome da trilha}** e está pronto para os próximos desafios.
> Continue evoluindo na plataforma [DIO.me](https://dio.me)!

---

Se a tecnologia "$2" não for encontrada no arquivo JSON, responda:
> ❌ Trilha não encontrada para **"$2"**. Verifique o nome da tecnologia e tente novamente.
> Trilhas disponíveis: Python, Java, React, Angular, Node.js, AWS, Azure, Machine Learning, Data Science, Kotlin, Flutter, .NET, DevOps, Cybersecurity, SQL, Vue.js, TypeScript, Go, Rust, Swift, Blockchain, UX/UI, Unity, QA, GenAI, GCP, Engenharia de Dados, PHP, Ruby, Scrum, Linux, JavaScript, Power BI, MLOps.
