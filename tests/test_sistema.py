"""Testes da interface (Parte D): simulam o que a pessoa digita e conferem a tela.

Na raiz do repositório:
    python -B -m unittest discover -s tests -v
"""
import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PASTA_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PASTA_SRC) not in sys.path:
    sys.path.insert(0, str(PASTA_SRC))

import sistema  # noqa: E402  (precisa vir depois de ajustar o sys.path)


def executar(*entradas):
    """Roda o programa com as entradas dadas e devolve (código de saída, texto da tela)."""
    tela = io.StringIO()
    with patch("builtins.input", side_effect=list(entradas)):
        with contextlib.redirect_stdout(tela):
            codigo = sistema.main()
    return codigo, tela.getvalue()


class TestesInterface(unittest.TestCase):

    def test_sair_pelo_menu(self):
        codigo, tela = executar("0")
        self.assertEqual(codigo, 0)
        self.assertIn("MENU PRINCIPAL", tela)
        self.assertIn("não é um canal oficial", tela)

    def test_fim_da_entrada_encerra_sem_erro(self):
        # Sem mais entradas, input() lança StopIteration no mock; trocamos por EOFError.
        with patch("builtins.input", side_effect=EOFError):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(sistema.main(), 0)

    def test_opcao_vazia_inexistente_e_texto(self):
        _, tela = executar("", "9", "abc", "0")
        self.assertIn("Você não digitou nada", tela)
        self.assertIn("A opção 9 não existe", tela)
        self.assertIn('"abc" não é uma opção', tela)

    def test_navegacao_pelo_menu_mostra_caminho_fonte_e_sugestoes(self):
        _, tela = executar("1", "1", "3", "0", "0")
        self.assertIn("Orientação cidadã > Documentos > título de eleitor", tela)
        self.assertIn("https://www.tse.jus.br/", tela)
        self.assertIn("Verificado em:", tela)
        self.assertIn("Assuntos relacionados", tela)

    def test_continuidade_leva_a_outro_assunto(self):
        # Pergunta -> seguro-desemprego -> primeira sugestão (inss) -> voltar.
        _, tela = executar("2", "Como pedir o seguro-desemprego?", "1", "0", "0")
        self.assertIn("Serviços > seguro-desemprego", tela)
        self.assertIn("Serviços > inss", tela)

    def test_pergunta_vazia(self):
        _, tela = executar("2", "   ", "0")
        self.assertIn("Você não digitou nenhuma pergunta.", tela)

    def test_pergunta_sem_resposta_mostra_aviso_e_alternativas(self):
        _, tela = executar("2", "Como renovar o passaporte?", "0", "0")
        self.assertIn("AVISO DE LIMITAÇÃO", tela)
        self.assertIn("Assuntos que posso explicar:", tela)

    def test_ambiguidade_permite_escolher(self):
        _, tela = executar("2", "Preciso do RG para pedir benefício no INSS", "2", "0", "0")
        self.assertIn("mais de um assunto", tela)
        self.assertIn("Documentos > identidade", tela)

    def test_ambiguidade_nenhuma_das_opcoes(self):
        _, tela = executar("2", "Como tirar a carteira de motorista?", "0", "0", "0")
        self.assertIn("Nenhuma dessas opções", tela)
        self.assertIn("AVISO DE LIMITAÇÃO", tela)

    def test_trocar_formato(self):
        _, tela = executar("3", "1", "0")
        self.assertIn("Formato alterado para: Modelo 1", tela)

    def test_base_invalida_nao_inicia(self):
        with patch.object(sistema, "carregar_base", return_value=([], "arquivo ausente")):
            tela = io.StringIO()
            with contextlib.redirect_stdout(tela):
                self.assertEqual(sistema.main(), 1)
        self.assertIn("Não foi possível iniciar", tela.getvalue())
        self.assertIn("arquivo ausente", tela.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
