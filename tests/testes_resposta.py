"""Testes automatizados da Parte C. Execute: python -m unittest discover -s tests -v"""
import unittest
from src.resposta import (
    MODELO_PADRAO, avaliar_resposta, buscar_melhores_correspondencias,
    comparar_modelos, formatar_direto, formatar_guiado, montar_instrucao,
    pontuar_registro, processar_resposta_usuario, registro_utilizavel, responder,
    responder_resultado_busca,
)

BASE = [
    {"id": "DOC-01", "tema": "Documentos", "palavras_chave": ["identidade", "rg", "cin", "carteira de identidade"],
     "orientacao": "Acesse o portal oficial. Preencha o formulário e agende o atendimento.",
     "referencia": {"nome": "Fonte oficial de exemplo", "link": "https://www.gov.br"}, "data_verificacao": "13/11/2026"},
    {"id": "SER-01", "tema": "Serviços", "palavras_chave": ["inss", "135", "meu inss", "previdencia"],
     "orientacao": "Consulte o Meu INSS ou ligue para 135.",
     "referencia": {"nome": "Fonte oficial de exemplo", "link": "https://www.gov.br"}, "data_verificacao": "13/11/2026"},
    {"id": "COM-01", "tema": "Orientações comunitárias", "palavras_chave": ["defesa civil", "alerta", "40199", "enchente"],
     "orientacao": "Acompanhe os alertas da Defesa Civil.",
     "referencia": {"nome": "Fonte oficial de exemplo", "link": "https://www.gov.br"}, "data_verificacao": "13/11/2026"},
]

class TestesParteC(unittest.TestCase):
    def test_01_entrada_vazia(self):
        self.assertIn("não digitou", processar_resposta_usuario("  ", BASE).lower())
    def test_02_busca_inss(self):
        self.assertIn("Meu INSS", processar_resposta_usuario("Como consultar o INSS?", BASE))
    def test_03_busca_id(self):
        self.assertIn("Acesse o portal", processar_resposta_usuario("DOC-01", BASE))
    def test_04_sem_correspondencia(self):
        self.assertIn("Não encontramos", processar_resposta_usuario("matrícula em universidade", BASE))
    def test_05_consulta_ambigua(self):
        self.assertIn("PERGUNTA AMBÍGUA", processar_resposta_usuario("rg inss", BASE))
    def test_06_modelo_direto(self):
        texto = formatar_direto(BASE[0])
        self.assertIn("Fonte:", texto); self.assertIn("https://www.gov.br", texto)
    def test_07_modelo_guiado(self):
        self.assertIn("1.", formatar_guiado(BASE[0]))
    def test_08_registro_incompleto(self):
        self.assertFalse(registro_utilizavel({"id": "X"}))
        self.assertIn("limitação", processar_resposta_usuario("X", [{"id": "X"}]).lower())
    def test_09_palavra_curta_nao_substring(self):
        self.assertEqual(pontuar_registro("emergencia", BASE[0]), 0)
    def test_10_montagem_prompt_nao_executa_ia(self):
        prompt = montar_instrucao("guiado", "como tirar documento", BASE[0])
        self.assertIn("REGRAS:", prompt); self.assertIn("DADOS DA BASE", prompt)
    def test_11_avaliacao_elementos(self):
        dados = avaliar_resposta(formatar_direto(BASE[0]), BASE[0])
        self.assertEqual(dados["atendidos"], 5)
        self.assertEqual(dados["percentual_elementos"], 100.0)
    def test_12_comparacao_modelos(self):
        comparacao = comparar_modelos([BASE[0]])
        self.assertEqual(len(comparacao), 1)
        self.assertIn("direto", comparacao[0]); self.assertIn("guiado", comparacao[0])
    def test_13_busca_empate(self):
        self.assertEqual(len(buscar_melhores_correspondencias("rg inss", BASE)), 2)
    def test_14_modelo_invalido_usa_padrao(self):
        self.assertEqual(MODELO_PADRAO, "direto")
        self.assertIn("Resposta:", responder("documento", [BASE[0]], [], "inexistente"))
    def test_15_palavras_chave_invalidas(self):
        registro = dict(BASE[0]); registro["palavras_chave"] = ["rg", 10]
        self.assertFalse(registro_utilizavel(registro))


    def test_16_integracao_b_uma_correspondencia(self):
        resultado = {"estado": "uma_correspondencia", "resultados": [
            {"registro": BASE[0], "pontuacao": 3,
             "termos_encontrados": ["identidade"], "expressoes_encontradas": []}
        ]}
        texto = responder_resultado_busca("identidade", resultado)
        self.assertIn("Acesse o portal", texto)
        self.assertIn("https://www.gov.br", texto)

    def test_17_integracao_b_multiplas_pede_escolha(self):
        resultado = {"estado": "multiplas_correspondencias", "resultados": [
            {"registro": BASE[0], "pontuacao": 2},
            {"registro": BASE[1], "pontuacao": 2},
        ]}
        texto = responder_resultado_busca("rg inss", resultado)
        self.assertIn("PERGUNTA AMBÍGUA", texto)
        self.assertNotIn("Resposta:", texto)

    def test_18_integracao_b_selecao_por_indice(self):
        resultado = {"estado": "multiplas_correspondencias", "resultados": [
            {"registro": BASE[0]}, {"registro": BASE[1]},
        ]}
        texto = responder_resultado_busca("rg inss", resultado, escolha=2)
        self.assertIn("Meu INSS", texto)
        self.assertNotIn("Acesse o portal", texto)

    def test_19_integracao_b_selecao_por_id(self):
        resultado = {"estado": "multiplas_correspondencias", "resultados": [
            {"registro": BASE[0]}, {"registro": BASE[1]},
        ]}
        texto = responder_resultado_busca("rg inss", resultado, escolha="DOC-01")
        self.assertIn("Acesse o portal", texto)

    def test_20_integracao_b_sem_correspondencia(self):
        resultado = {"estado": "sem_correspondencia", "resultados": []}
        self.assertIn("Não encontramos", responder_resultado_busca("universidade", resultado))

    def test_21_integracao_b_entrada_invalida(self):
        resultado = {"estado": "entrada_invalida", "resultados": []}
        self.assertIn("inválida", responder_resultado_busca("teste", resultado).lower())

    def test_22_integracao_b_resultado_malformado(self):
        self.assertIn("formato inválido", responder_resultado_busca("teste", []).lower())
        self.assertIn("lista de resultados válida", responder_resultado_busca(
            "teste", {"estado": "uma_correspondencia", "resultados": "errado"}
        ).lower())

    def test_23_lista_bruta_com_varios_registros_nao_escolhe_primeiro(self):
        texto = responder("rg inss", BASE[:2])
        self.assertIn("PERGUNTA AMBÍGUA", texto)
        self.assertNotIn("Resposta:", texto)

if __name__ == "__main__":
    unittest.main(verbosity=2)
