"""
test_dio_commands.py
Testes unitários para o módulo dio_explorer/src/dio_commands.py
Cobre os comandos /trilha, /desafio e /certificado com ≥70% de cobertura.

Aluno de referência nos testes de desafio e certificado: João da Silva / Java
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

# Garante que o módulo é encontrado independente do cwd
sys.path.insert(0, str(Path(__file__).parent.parent / "dio_explorer" / "src"))

import dio_commands as dc


# ---------------------------------------------------------------------------
# Fixture: cria um JSON de trilhas mínimo em arquivo temporário
# ---------------------------------------------------------------------------

_TRILHAS_FIXTURE = {
    "trilhas": [
        {
            "id": 2,
            "nome": "Formação Java Developer",
            "tecnologia": "Java",
            "numero_de_modulos": 14,
            "xp_total": 21000,
            "badges_disponiveis": [
                "Java Fundamentals",
                "OOP Expert",
                "Spring Boot Master",
                "Java Champion",
            ],
            "promocoes": {
                "desconto_percentual": 25,
                "descricao": "25% OFF em cursos parceiros ao concluir",
            },
            "vitalicio": True,
            "lives_ao_vivo": [
                {
                    "titulo": "Spring Boot na Prática",
                    "data": "2025-07-20",
                    "horario": "18:00",
                },
                {
                    "titulo": "Microserviços com Java",
                    "data": "2025-09-21",
                    "horario": "18:00",
                },
            ],
        },
        {
            "id": 5,
            "nome": "Formação Node.js Developer",
            "tecnologia": "Node.js",
            "numero_de_modulos": 13,
            "xp_total": 19000,
            "badges_disponiveis": [
                "Node Fundamentals",
                "REST API Builder",
                "Node.js Expert",
            ],
            "promocoes": {
                "desconto_percentual": 0,
                "descricao": "Sem promoção ativa no momento",
            },
            "vitalicio": False,
            "lives_ao_vivo": [],
        },
    ]
}


def _criar_json_temporario() -> str:
    """Cria arquivo JSON de fixture e retorna o caminho."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(_TRILHAS_FIXTURE, tmp, ensure_ascii=False)
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# Testes: utilitários
# ---------------------------------------------------------------------------


class TestUtilitarios(unittest.TestCase):
    """Testa funções auxiliares do módulo."""

    def test_formatar_data_br_formato_correto(self):
        self.assertEqual(dc.formatar_data_br("2025-07-20"), "20/07/2025")

    def test_formatar_data_br_data_inicio_ano(self):
        self.assertEqual(dc.formatar_data_br("2025-01-01"), "01/01/2025")

    def test_gerar_codigo_formato(self):
        codigo = dc.gerar_codigo_verificacao(id_trilha=2, ano=2025)
        # Padrão: DIO-202502-XXXXXX
        self.assertRegex(codigo, r"^DIO-20250[0-9]-[A-Z0-9]{6}$")

    def test_gerar_codigo_diferente_a_cada_chamada(self):
        """Com alta probabilidade, dois códigos devem diferir."""
        c1 = dc.gerar_codigo_verificacao(1, 2025)
        c2 = dc.gerar_codigo_verificacao(1, 2025)
        # Probabilidade de colisão: (36^6)^-1 ≈ 0
        # Se falhar por sorte, re-execute — não é defeito do código
        self.assertNotEqual(c1, c2)  # pode falhar 1 em ~2 bilhões de vezes

    def test_buscar_trilha_case_insensitive(self):
        trilhas = dc.carregar_trilhas(_criar_json_temporario())
        resultado = dc.buscar_trilha("java", trilhas)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["tecnologia"], "Java")

    def test_buscar_trilha_parcial(self):
        trilhas = dc.carregar_trilhas(_criar_json_temporario())
        resultado = dc.buscar_trilha("node", trilhas)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["tecnologia"], "Node.js")

    def test_buscar_trilha_sem_resultado(self):
        trilhas = dc.carregar_trilhas(_criar_json_temporario())
        resultado = dc.buscar_trilha("ruby", trilhas)
        self.assertEqual(resultado, [])

    def test_carregar_trilhas_retorna_lista(self):
        trilhas = dc.carregar_trilhas(_criar_json_temporario())
        self.assertIsInstance(trilhas, list)
        self.assertGreater(len(trilhas), 0)

    def test_carregar_trilhas_arquivo_real(self):
        """Garante que o arquivo de dados real é carregável."""
        trilhas = dc.carregar_trilhas()
        self.assertGreaterEqual(len(trilhas), 30)

    def test_normalizar_nivel_avancado_sem_acento(self):
        self.assertEqual(dc._normalizar_nivel("avancado"), "avancado")

    def test_normalizar_nivel_avancado_com_acento(self):
        self.assertEqual(dc._normalizar_nivel("avançado"), "avancado")

    def test_normalizar_nivel_intermediario_sem_acento(self):
        self.assertEqual(dc._normalizar_nivel("intermediario"), "intermediario")

    def test_normalizar_nivel_intermediario_com_acento(self):
        self.assertEqual(dc._normalizar_nivel("intermediário"), "intermediario")

    def test_normalizar_nivel_iniciante(self):
        self.assertEqual(dc._normalizar_nivel("iniciante"), "iniciante")

    def test_normalizar_nivel_invalido(self):
        self.assertEqual(dc._normalizar_nivel("guru"), "guru")


# ---------------------------------------------------------------------------
# Testes: /trilha
# ---------------------------------------------------------------------------


class TestCmdTrilha(unittest.TestCase):
    """Testa o comando /trilha."""

    def setUp(self):
        self.json_path = _criar_json_temporario()

    def test_trilha_java_retorna_markdown(self):
        resultado = dc.cmd_trilha("Java", self.json_path)
        self.assertIn("Formação Java Developer", resultado)
        self.assertIn("21000 XP", resultado)

    def test_trilha_java_contem_badges(self):
        resultado = dc.cmd_trilha("Java", self.json_path)
        self.assertIn("Java Fundamentals", resultado)
        self.assertIn("Spring Boot Master", resultado)

    def test_trilha_java_contem_lives(self):
        resultado = dc.cmd_trilha("Java", self.json_path)
        self.assertIn("Spring Boot na Prática", resultado)
        self.assertIn("20/07/2025", resultado)

    def test_trilha_java_promocao_ativa(self):
        resultado = dc.cmd_trilha("Java", self.json_path)
        self.assertIn("25% OFF", resultado)

    def test_trilha_java_acesso_vitalicio(self):
        resultado = dc.cmd_trilha("Java", self.json_path)
        self.assertIn("✅ Sim", resultado)

    def test_trilha_busca_case_insensitive(self):
        resultado_lower = dc.cmd_trilha("java", self.json_path)
        resultado_upper = dc.cmd_trilha("JAVA", self.json_path)
        self.assertIn("Formação Java Developer", resultado_lower)
        self.assertIn("Formação Java Developer", resultado_upper)

    def test_trilha_node_sem_lives(self):
        resultado = dc.cmd_trilha("Node.js", self.json_path)
        self.assertIn("_Nenhuma live agendada no momento._", resultado)

    def test_trilha_node_sem_promocao(self):
        resultado = dc.cmd_trilha("Node.js", self.json_path)
        self.assertIn("Nenhuma promoção ativa no momento.", resultado)

    def test_trilha_node_acesso_nao_vitalicio(self):
        resultado = dc.cmd_trilha("Node.js", self.json_path)
        self.assertIn("❌ Não", resultado)

    def test_trilha_nao_encontrada(self):
        resultado = dc.cmd_trilha("Ruby", self.json_path)
        self.assertIn("❌", resultado)
        self.assertIn("Ruby", resultado)

    def test_trilha_nao_encontrada_sugere_termos(self):
        resultado = dc.cmd_trilha("Ruby", self.json_path)
        self.assertIn("Python", resultado)
        self.assertIn("Java", resultado)

    def test_trilha_retorna_14_modulos_java(self):
        resultado = dc.cmd_trilha("Java", self.json_path)
        self.assertIn("14", resultado)

    def test_trilha_tecnologia_parcial(self):
        """'java' deve encontrar 'Formação Java Developer'."""
        resultado = dc.cmd_trilha("java develop", self.json_path)
        # Busca parcial no nome
        self.assertIn("Formação Java Developer", resultado)


# ---------------------------------------------------------------------------
# Testes: /desafio
# ---------------------------------------------------------------------------


class TestCmdDesafio(unittest.TestCase):
    """Testa o comando /desafio."""

    def test_desafio_java_iniciante_estrutura(self):
        resultado = dc.cmd_desafio("Java", "iniciante")
        self.assertIn("⚔️ Desafio DIO", resultado)
        self.assertIn("Java", resultado)
        self.assertIn("Enunciado", resultado)
        self.assertIn("Critérios de Avaliação", resultado)
        self.assertIn("XP ao Concluir", resultado)

    def test_desafio_java_intermediario_nivel_exibido(self):
        resultado = dc.cmd_desafio("Java", "intermediario")
        self.assertIn("Intermediário", resultado)

    def test_desafio_java_avancado_nivel_exibido(self):
        resultado = dc.cmd_desafio("Java", "avancado")
        self.assertIn("Avançado", resultado)

    def test_desafio_nivel_com_acento_intermediario(self):
        resultado = dc.cmd_desafio("Python", "intermediário")
        self.assertIn("Intermediário", resultado)

    def test_desafio_nivel_com_acento_avancado(self):
        resultado = dc.cmd_desafio("Python", "avançado")
        self.assertIn("Avançado", resultado)

    def test_desafio_nivel_invalido_retorna_erro(self):
        resultado = dc.cmd_desafio("Java", "guru")
        self.assertIn("❌", resultado)
        self.assertIn("guru", resultado)

    def test_desafio_xp_iniciante_range(self):
        """XP de iniciante deve estar entre 150 e 300."""
        for _ in range(10):
            resultado = dc.cmd_desafio("Java", "iniciante")
            match = re.search(r"\+(\d+) XP", resultado)
            self.assertIsNotNone(match)
            xp = int(match.group(1))
            self.assertGreaterEqual(xp, 150)
            self.assertLessEqual(xp, 300)

    def test_desafio_xp_intermediario_range(self):
        for _ in range(10):
            resultado = dc.cmd_desafio("Java", "intermediario")
            match = re.search(r"\+(\d+) XP", resultado)
            xp = int(match.group(1))
            self.assertGreaterEqual(xp, 350)
            self.assertLessEqual(xp, 600)

    def test_desafio_xp_avancado_range(self):
        for _ in range(10):
            resultado = dc.cmd_desafio("Java", "avancado")
            match = re.search(r"\+(\d+) XP", resultado)
            xp = int(match.group(1))
            self.assertGreaterEqual(xp, 700)
            self.assertLessEqual(xp, 1200)

    def test_desafio_contem_dicas(self):
        resultado = dc.cmd_desafio("Java", "intermediario")
        self.assertIn("💡 Dicas", resultado)

    def test_desafio_contem_restricoes(self):
        resultado = dc.cmd_desafio("Java", "intermediario")
        self.assertIn("🧩 Restrições", resultado)

    def test_desafio_contem_exemplos_entrada_saida(self):
        resultado = dc.cmd_desafio("Java", "iniciante")
        self.assertIn("Exemplo de Entrada", resultado)
        self.assertIn("Exemplo de Saída", resultado)

    def test_desafio_tecnologia_aparece_no_titulo(self):
        resultado = dc.cmd_desafio("JavaScript", "iniciante")
        self.assertIn("JavaScript", resultado)

    def test_desafio_nivel_maiusculo_invalido(self):
        """Nível em maiúsculas não mapeado deve ser tratado como inválido."""
        resultado = dc.cmd_desafio("Java", "EXPERT")
        self.assertIn("❌", resultado)


# ---------------------------------------------------------------------------
# Testes: /certificado
# ---------------------------------------------------------------------------


class TestCmdCertificado(unittest.TestCase):
    """Testa o comando /certificado com aluno João da Silva / Java."""

    def setUp(self):
        self.json_path = _criar_json_temporario()
        self.data_fixa = date(2025, 7, 1)

    def test_certificado_contem_nome_aluno(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("JOÃO DA SILVA", resultado)

    def test_certificado_contem_nome_trilha(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("Formação Java Developer", resultado)

    def test_certificado_contem_tecnologia(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("Java", resultado)

    def test_certificado_contem_xp(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("21000", resultado)

    def test_certificado_contem_modulos(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("14", resultado)

    def test_certificado_data_emissao_calculada(self):
        """Data de emissão = data_base + 14 semanas = 2025-07-01 + 98 dias = 2025-10-07."""
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        from datetime import timedelta
        esperada = (self.data_fixa + timedelta(weeks=14)).strftime("%d/%m/%Y")
        self.assertIn(esperada, resultado)

    def test_certificado_contem_codigo_verificacao(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertRegex(resultado, r"DIO-\d{6}-[A-Z0-9]{6}")

    def test_certificado_contem_badges(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("Java Fundamentals", resultado)
        self.assertIn("Java Champion", resultado)

    def test_certificado_acesso_vitalicio_sim(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("Sim", resultado)

    def test_certificado_acesso_vitalicio_nao(self):
        resultado = dc.cmd_certificado(
            "Maria Oliveira", "Node.js", self.json_path, self.data_fixa
        )
        self.assertIn("Não", resultado)

    def test_certificado_tabela_dados(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("📄 Dados do Certificado", resultado)
        self.assertIn("Titular", resultado)

    def test_certificado_mensagem_parabens(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("Parabéns", resultado)
        self.assertIn("João da Silva", resultado)

    def test_certificado_link_dio(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Java", self.json_path, self.data_fixa
        )
        self.assertIn("dio.me", resultado)

    def test_certificado_trilha_nao_encontrada(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "Ruby", self.json_path, self.data_fixa
        )
        self.assertIn("❌", resultado)
        self.assertIn("Ruby", resultado)

    def test_certificado_busca_case_insensitive(self):
        resultado = dc.cmd_certificado(
            "João da Silva", "java", self.json_path, self.data_fixa
        )
        self.assertIn("Formação Java Developer", resultado)

    def test_certificado_sem_data_base_usa_hoje(self):
        """Sem data_base, não deve lançar exceção."""
        resultado = dc.cmd_certificado("Ana Lima", "Java", self.json_path)
        self.assertIn("Formação Java Developer", resultado)


# ---------------------------------------------------------------------------
# Testes de integração leve: arquivo de dados real
# ---------------------------------------------------------------------------


class TestIntegracaoArquivoReal(unittest.TestCase):
    """Usa o arquivo real trilhas_dio.json para validar o fluxo completo."""

    def test_trilha_java_arquivo_real(self):
        resultado = dc.cmd_trilha("Java")
        self.assertIn("Formação Java Developer", resultado)
        self.assertIn("21000 XP", resultado)

    def test_trilha_python_arquivo_real_multiplos_resultados(self):
        """Python deve encontrar 'Python Developer', 'Machine Learning' e 'Data Science'."""
        resultado = dc.cmd_trilha("Python")
        self.assertIn("Formação Python Developer", resultado)
        self.assertIn("Machine Learning", resultado)

    def test_certificado_java_arquivo_real(self):
        resultado = dc.cmd_certificado("João da Silva", "Java", data_base=date(2025, 7, 1))
        self.assertIn("JOÃO DA SILVA", resultado)
        self.assertIn("Formação Java Developer", resultado)

    def test_desafio_java_intermediario_arquivo_nao_necessario(self):
        """O comando /desafio não depende do arquivo JSON."""
        resultado = dc.cmd_desafio("Java", "intermediario")
        self.assertIn("Java", resultado)
        self.assertIn("Intermediário", resultado)


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
