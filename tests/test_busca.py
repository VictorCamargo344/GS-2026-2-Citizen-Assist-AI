r"""Testes de B: fixtures ficticias e integracao com a Parte A REAL.

Na raiz do repositorio:
  python -B -m unittest discover -s tests -v

A integracao usa os arquivos reais do repositorio (src/base.py, src/busca.py e
data/base_conhecimento.json). Eles sao copiados para uma pasta temporaria, para
que nenhum teste altere os originais.
"""

import contextlib
import copy
import hashlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[1]
ARQUIVOS_REAIS = {
    "base.py": RAIZ_REPOSITORIO / "src" / "base.py",
    "busca.py": RAIZ_REPOSITORIO / "src" / "busca.py",
    "base_conhecimento.json": RAIZ_REPOSITORIO / "data" / "base_conhecimento.json",
}

BASE = None
BUSCA = None
PASTA_TEMP = None
ORIGINAIS = {}
HASHES_ORIGINAIS = {}


def _importar(nome, caminho):
    especificacao = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(especificacao)
    sys.modules[nome] = modulo
    especificacao.loader.exec_module(modulo)
    return modulo


def _restaurar_modulos(anteriores):
    for nome, modulo in anteriores.items():
        if modulo is None:
            sys.modules.pop(nome, None)
        else:
            sys.modules[nome] = modulo


def setUpModule():
    """Copia A e B do repositorio para um diretorio temporario, removido ao terminar."""
    global BASE, BUSCA, PASTA_TEMP, ORIGINAIS, HASHES_ORIGINAIS
    for nome, caminho in ARQUIVOS_REAIS.items():
        if not caminho.is_file():
            raise RuntimeError(f"Arquivo do repositorio nao encontrado: {caminho} ({nome})")
    ORIGINAIS = {nome: caminho.read_bytes() for nome, caminho in ARQUIVOS_REAIS.items()}
    HASHES_ORIGINAIS = {nome: hashlib.sha256(conteudo).hexdigest()
                        for nome, conteudo in ORIGINAIS.items()}

    temporario = tempfile.TemporaryDirectory(prefix="citizen_b_testes_")
    unittest.addModuleCleanup(temporario.cleanup)
    PASTA_TEMP = Path(temporario.name)
    pasta_src = PASTA_TEMP / "src"
    pasta_data = PASTA_TEMP / "data"
    pasta_src.mkdir()
    pasta_data.mkdir()

    (pasta_src / "base.py").write_bytes(ORIGINAIS["base.py"])
    (pasta_src / "busca.py").write_bytes(ORIGINAIS["busca.py"])
    (pasta_data / "base_conhecimento.json").write_bytes(ORIGINAIS["base_conhecimento.json"])

    anteriores = {nome: sys.modules.get(nome) for nome in ("base", "busca")}
    unittest.addModuleCleanup(_restaurar_modulos, anteriores)
    BASE = _importar("base", pasta_src / "base.py")
    BUSCA = _importar("busca", pasta_src / "busca.py")


def registro_ficticio(identificador, tema, palavras):
    """Fixture tecnica: NAO e uma orientacao cidada nem fonte verificada."""
    return {
        "id": identificador,
        "tema": tema,
        "palavras_chave": palavras,
        "orientacao": "DADO FICTICIO para testar software. Nao utilizar como orientacao.",
        "referencia": {"nome": "FONTE FICTICIA DE TESTE", "link": "https://example.invalid/teste"},
        "data_verificacao": "17/11/2026",
    }


def ids(resultado):
    return [item["registro"]["id"] for item in resultado["resultados"]]


class TestesUnitarios(unittest.TestCase):
    """Casos sinteticos; normalizacao e acessos continuam sendo os reais de A."""

    def setUp(self):
        self.registros = [
            registro_ficticio("FIC-B", "Documentos", ["identidade", "rg", "carteira de identidade"]),
            registro_ficticio("FIC-A", "Serviços", ["inss", "meu inss", "previdência"]),
            registro_ficticio("FIC-C", "Orientações comunitárias", ["defesa civil", "alertas", "sms"]),
        ]

    def test_fixture_tem_formato_valido_para_a(self):
        validos, problemas = BASE.validar_registros(self.registros)
        self.assertEqual(problemas, [])
        self.assertEqual(len(validos), 3)

    def test_id_existente(self):
        resultado = BUSCA.consultar_por_id(self.registros, "FIC-B")
        self.assertEqual(resultado["estado"], "uma_correspondencia")
        self.assertEqual(ids(resultado), ["FIC-B"])
        self.assertIsNone(resultado["resultados"][0]["pontuacao"])

    def test_id_maiusculas_e_espacos(self):
        self.assertEqual(ids(BUSCA.consultar_por_id(self.registros, "  fic-b  ")), ["FIC-B"])

    def test_id_inexistente(self):
        self.assertEqual(BUSCA.consultar_por_id(self.registros, "FIC-X"),
                         {"estado": "id_inexistente", "resultados": []})

    def test_tema_existente_e_acento(self):
        for tema in ("Serviços", "servicos", "  SERVIÇOS  "):
            with self.subTest(tema=tema):
                self.assertEqual(ids(BUSCA.consultar_por_tema(self.registros, tema)), ["FIC-A"])

    def test_tema_inexistente(self):
        resultado = BUSCA.consultar_por_tema(self.registros, "Tema ausente")
        self.assertEqual(resultado, {"estado": "tema_inexistente", "resultados": []})

    def test_tema_varios_registros_preserva_ordem(self):
        self.registros.append(registro_ficticio("FIC-D", "documentos", ["passaporte"]))
        resultado = BUSCA.consultar_por_tema(self.registros, "Documentos")
        self.assertEqual(resultado["estado"], "multiplas_correspondencias")
        self.assertEqual(ids(resultado), ["FIC-B", "FIC-D"])

    def test_palavra_chave_simples(self):
        self.assertEqual(ids(BUSCA.consultar_por_palavra_chave(self.registros, "rg")), ["FIC-B"])

    def test_palavra_chave_composta_exata(self):
        resultado = BUSCA.consultar_por_palavra_chave(self.registros, "  MEU INSS  ")
        self.assertEqual(ids(resultado), ["FIC-A"])

    def test_palavra_chave_sem_acento(self):
        resultado = BUSCA.consultar_por_palavra_chave(self.registros, "previdencia")
        self.assertEqual(ids(resultado), ["FIC-A"])

    def test_modalidade_exata_nao_e_pergunta_livre(self):
        resultado = BUSCA.consultar_por_palavra_chave(self.registros, "Como tirar identidade?")
        self.assertEqual(resultado["estado"], "sem_correspondencia")

    def test_modalidade_exata_mantem_regra_original_de_a(self):
        for termo in ("meu  inss", "meu,inss"):
            with self.subTest(termo=termo):
                resultado = BUSCA.consultar_por_palavra_chave(self.registros, termo)
                self.assertEqual(resultado["estado"], "sem_correspondencia")

    def test_palavra_chave_inexistente(self):
        self.assertEqual(BUSCA.consultar_por_palavra_chave(self.registros, "astronomia")["estado"],
                         "sem_correspondencia")

    def test_palavra_chave_filtro_de_tema(self):
        resultado = BUSCA.consultar_por_palavra_chave(self.registros, "rg", "Serviços")
        self.assertEqual(resultado["estado"], "sem_correspondencia")

    def test_pergunta_completa_e_pontuacao_conhecida(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "Como tirar a carteira de identidade?")
        self.assertEqual(resultado["estado"], "uma_correspondencia")
        self.assertEqual(ids(resultado), ["FIC-B"])
        item = resultado["resultados"][0]
        self.assertEqual(item["pontuacao"], 4)
        self.assertEqual(item["termos_encontrados"], ["carteira", "identidade"])
        self.assertEqual(item["expressoes_encontradas"], ["carteira de identidade"])

    def test_pergunta_caixa_acento_pontuacao_espacos(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "  PREVIDÊNCIA???\n   ")
        self.assertEqual(ids(resultado), ["FIC-A"])

    def test_pontuacao_separa_palavras_da_expressao(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "DEFESA,,, CIVIL!!!")
        self.assertEqual(ids(resultado), ["FIC-C"])
        self.assertEqual(resultado["resultados"][0]["pontuacao"], 4)

    def test_expressao_composta_exige_ordem(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "civil defesa")
        self.assertEqual(resultado["resultados"][0]["pontuacao"], 2)
        self.assertEqual(resultado["resultados"][0]["expressoes_encontradas"], [])

    def test_expressao_mantem_palavras_funcionais_no_bonus(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "carteira identidade")
        self.assertEqual(resultado["resultados"][0]["pontuacao"], 2)
        self.assertEqual(resultado["resultados"][0]["expressoes_encontradas"], [])

    def test_entradas_vazias_em_todas_as_consultas(self):
        funcoes = (BUSCA.consultar_por_id, BUSCA.consultar_por_tema,
                   BUSCA.consultar_por_palavra_chave, BUSCA.buscar_pergunta)
        for funcao in funcoes:
            for entrada in ("", " \t\n ", "?!...---_"):
                with self.subTest(funcao=funcao.__name__, entrada=entrada):
                    self.assertEqual(funcao(self.registros, entrada),
                                     {"estado": "entrada_vazia", "resultados": []})

    def test_tipos_inadequados_em_todas_as_consultas(self):
        funcoes = (BUSCA.consultar_por_id, BUSCA.consultar_por_tema,
                   BUSCA.consultar_por_palavra_chave, BUSCA.buscar_pergunta)
        for funcao in funcoes:
            for entrada in (None, 135, [], {}, True):
                with self.subTest(funcao=funcao.__name__, entrada=entrada):
                    self.assertEqual(funcao(self.registros, entrada),
                                     {"estado": "entrada_invalida", "resultados": []})

    def test_pergunta_fora_da_base(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "Como preparar um bolo de chocolate?")
        self.assertEqual(resultado, {"estado": "sem_correspondencia", "resultados": []})

    def test_apenas_palavras_funcionais(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "como de o e para minha")
        self.assertEqual(resultado["estado"], "sem_correspondencia")

    def test_palavra_funcional_na_base_nao_gera_correspondencia_livre(self):
        self.registros.append(registro_ficticio("FIC-D", "Novo", ["como de"]))
        self.assertEqual(BUSCA.buscar_pergunta(self.registros, "como de")["estado"],
                         "sem_correspondencia")

    def test_sem_falso_positivo_por_substring(self):
        for pergunta in ("urgente", "surgiu", "enrgia", "identidades"):
            with self.subTest(pergunta=pergunta):
                self.assertEqual(BUSCA.buscar_pergunta(self.registros, pergunta)["estado"],
                                 "sem_correspondencia")

    def test_nao_busca_no_texto_da_orientacao_ou_fonte(self):
        self.registros[0]["orientacao"] += " bolo chocolate astronomia"
        self.registros[0]["referencia"]["nome"] = "Astronomia"
        self.assertEqual(BUSCA.buscar_pergunta(self.registros, "astronomia bolo")["estado"],
                         "sem_correspondencia")

    def test_palavra_repetida_nao_aumenta_pontos(self):
        simples = BUSCA.buscar_pergunta(self.registros, "rg")
        repetida = BUSCA.buscar_pergunta(self.registros, "rg rg RG rg")
        self.assertEqual(simples, repetida)

    def test_expressao_repetida_nao_aumenta_pontos(self):
        simples = BUSCA.buscar_pergunta(self.registros, "defesa civil")
        repetida = BUSCA.buscar_pergunta(self.registros, "defesa civil defesa civil")
        self.assertEqual(simples, repetida)

    def test_palavras_chave_duplicadas_nao_aumentam_pontos(self):
        antes = BUSCA.buscar_pergunta(self.registros, "carteira de identidade")
        self.registros[0]["palavras_chave"] += ["IDENTIDADE", "CARTEIRA DE IDENTIDADE"]
        self.assertEqual(antes, BUSCA.buscar_pergunta(self.registros, "carteira de identidade"))

    def test_multiplas_correspondencias_mantidas_mesmo_com_pontos_diferentes(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "rg e meu inss")
        self.assertEqual(resultado["estado"], "multiplas_correspondencias")
        self.assertEqual(ids(resultado), ["FIC-A", "FIC-B"])
        self.assertEqual([item["pontuacao"] for item in resultado["resultados"]], [3, 1])

    def test_empate_ordenado_por_id_independente_da_ordem_da_base(self):
        for registros in (self.registros, list(reversed(self.registros))):
            with self.subTest(ordem=[registro["id"] for registro in registros]):
                resultado = BUSCA.buscar_pergunta(registros, "identidade e inss")
                self.assertEqual(ids(resultado), ["FIC-A", "FIC-B"])
                self.assertEqual([item["pontuacao"] for item in resultado["resultados"]], [1, 1])

    def test_filtro_de_tema_na_pergunta(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "identidade e inss", "documentos")
        self.assertEqual(ids(resultado), ["FIC-B"])

    def test_filtro_inexistente_e_filtro_invalido(self):
        for funcao in (BUSCA.buscar_pergunta, BUSCA.consultar_por_palavra_chave):
            for tema, esperado in (("Saude", "tema_inexistente"), ("  ", "entrada_vazia"),
                                   (5, "entrada_invalida")):
                with self.subTest(funcao=funcao.__name__, tema=tema):
                    self.assertEqual(funcao(self.registros, "rg", tema)["estado"], esperado)

    def test_entrada_principal_tem_precedencia_sobre_filtro(self):
        resultado = BUSCA.buscar_pergunta(self.registros, "", "Nao existe")
        self.assertEqual(resultado["estado"], "entrada_vazia")

    def test_base_vazia(self):
        self.assertEqual(BUSCA.buscar_pergunta([], "rg")["estado"], "sem_correspondencia")
        self.assertEqual(BUSCA.consultar_por_id([], "FIC-B")["estado"], "id_inexistente")
        self.assertEqual(BUSCA.consultar_por_tema([], "Documentos")["estado"], "tema_inexistente")
        self.assertEqual(BUSCA.construir_hierarquia([]), {"raiz": "Orientação cidadã", "temas": []})
        self.assertEqual(BUSCA.sugerir_continuidade([])["estado"], "sem_opcoes")

    def test_hierarquia_de_temas_e_assuntos(self):
        hierarquia = BUSCA.construir_hierarquia(self.registros)
        self.assertEqual(hierarquia["raiz"], "Orientação cidadã")
        self.assertEqual([grupo["tema"] for grupo in hierarquia["temas"]],
                         ["Documentos", "Serviços", "Orientações comunitárias"])
        self.assertEqual(hierarquia["temas"][0]["assuntos"][0]["titulo"], "identidade")
        self.assertIs(hierarquia["temas"][0]["assuntos"][0]["registro"], self.registros[0])

    def test_localizacao_na_hierarquia(self):
        hierarquia = BUSCA.construir_hierarquia(self.registros)
        local = BUSCA.localizar_na_hierarquia(hierarquia, "  fic-c  ")
        self.assertEqual(local["caminho"], ["Orientação cidadã", "Orientações comunitárias", "defesa civil"])
        self.assertIs(local["registro"], self.registros[2])

    def test_localizacao_inexistente_ou_invalida(self):
        hierarquia = BUSCA.construir_hierarquia(self.registros)
        for identificador in ("FIC-X", "", "?!", None, 3):
            with self.subTest(identificador=identificador):
                self.assertIsNone(BUSCA.localizar_na_hierarquia(hierarquia, identificador))

    def test_navegacao_entre_tres_assuntos_sem_dependencias(self):
        for atual, proximo in (("FIC-B", "FIC-A"), ("FIC-A", "FIC-C"), ("FIC-C", "FIC-B")):
            with self.subTest(atual=atual):
                resultado = BUSCA.sugerir_continuidade(self.registros, atual)
                self.assertEqual(resultado["estado"], "opcoes_disponiveis")
                self.assertIn(proximo, ids(resultado))
                self.assertNotIn(atual, ids(resultado))
                self.assertTrue(all(item["relacao"] == "outro_tema" for item in resultado["resultados"]))

    def test_navegacao_prioriza_mesmo_tema_e_nao_muda_ordem_original(self):
        self.registros.append(registro_ficticio("FIC-D", "documentos", ["passaporte"]))
        resultado = BUSCA.sugerir_continuidade(self.registros, "FIC-B")
        self.assertEqual(ids(resultado), ["FIC-D", "FIC-A", "FIC-C"])
        self.assertEqual([item["relacao"] for item in resultado["resultados"]],
                         ["mesmo_tema", "outro_tema", "outro_tema"])

    def test_navegacao_id_inexistente_ou_invalido(self):
        for identificador, estado in (("FIC-X", "id_inexistente"), ("", "entrada_vazia"),
                                      (42, "entrada_invalida")):
            with self.subTest(identificador=identificador):
                self.assertEqual(BUSCA.sugerir_continuidade(self.registros, identificador),
                                 {"estado": estado, "resultados": []})

    def test_navegacao_sem_id_oferece_todos_apos_busca_sem_resultado(self):
        self.assertEqual(BUSCA.buscar_pergunta(self.registros, "astronomia")["estado"],
                         "sem_correspondencia")
        resultado = BUSCA.sugerir_continuidade(self.registros)
        self.assertEqual(ids(resultado), ["FIC-B", "FIC-A", "FIC-C"])
        self.assertTrue(all(item["relacao"] == "tema_disponivel" for item in resultado["resultados"]))

    def test_navegacao_base_com_um_registro(self):
        self.assertEqual(BUSCA.sugerir_continuidade(self.registros[:1], "FIC-B"),
                         {"estado": "sem_opcoes", "resultados": []})

    def test_adicao_de_registro_e_tema_sem_mudar_algoritmo(self):
        novo = registro_ficticio("FIC-D", "Novo tema fictício", ["biblioteca"])
        self.registros.append(novo)
        self.assertEqual(ids(BUSCA.buscar_pergunta(self.registros, "Onde fica a biblioteca?")), ["FIC-D"])
        self.assertEqual(ids(BUSCA.consultar_por_tema(self.registros, "novo tema ficticio")), ["FIC-D"])
        hierarquia = BUSCA.construir_hierarquia(self.registros)
        self.assertEqual(hierarquia["temas"][-1]["tema"], "Novo tema fictício")
        self.assertIn("FIC-D", ids(BUSCA.sugerir_continuidade(self.registros, "FIC-B")))

    def test_temas_equivalentes_nao_duplicam_grupo(self):
        self.registros.append(registro_ficticio("FIC-D", "servicos", ["biblioteca"]))
        hierarquia = BUSCA.construir_hierarquia(self.registros)
        self.assertEqual(len(hierarquia["temas"]), 3)
        self.assertEqual([assunto["id"] for assunto in hierarquia["temas"][1]["assuntos"]],
                         ["FIC-A", "FIC-D"])

    def test_operacoes_nao_mutam_registros(self):
        antes = copy.deepcopy(self.registros)
        BUSCA.consultar_por_id(self.registros, "FIC-B")
        BUSCA.consultar_por_tema(self.registros, "Documentos")
        BUSCA.consultar_por_palavra_chave(self.registros, "rg")
        BUSCA.buscar_pergunta(self.registros, "rg e inss")
        BUSCA.localizar_na_hierarquia(BUSCA.construir_hierarquia(self.registros), "FIC-B")
        BUSCA.sugerir_continuidade(self.registros, "FIC-B")
        self.assertEqual(self.registros, antes)

    def test_registro_e_fonte_completos_e_metadados_separados(self):
        item = BUSCA.buscar_pergunta(self.registros, "rg")["resultados"][0]
        self.assertIs(item["registro"], self.registros[0])
        self.assertEqual(item["registro"]["referencia"], self.registros[0]["referencia"])
        self.assertNotIn("pontuacao", item["registro"])
        item["pontuacao"] = -100
        self.assertNotIn("pontuacao", self.registros[0])

    def test_nenhuma_funcao_normal_imprime_ou_solicita_input(self):
        from unittest.mock import patch
        saida = io.StringIO()
        with patch("builtins.input", side_effect=AssertionError("B nao pode pedir input")):
            with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(saida):
                BUSCA.consultar_por_id(self.registros, "FIC-B")
                BUSCA.consultar_por_tema(self.registros, "Serviços")
                BUSCA.consultar_por_palavra_chave(self.registros, "rg")
                BUSCA.buscar_pergunta(self.registros, "rg")
                BUSCA.localizar_na_hierarquia(BUSCA.construir_hierarquia(self.registros), "FIC-B")
                BUSCA.sugerir_continuidade(self.registros)
        self.assertEqual(saida.getvalue(), "")


class TestesIntegracaoA(unittest.TestCase):
    """Executa o contrato com os arquivos reais de A presentes no repositorio."""

    def setUp(self):
        self.registros, erro = BASE.carregar_base()
        self.assertEqual(erro, "")
        self.validos, problemas = BASE.validar_registros(self.registros)
        self.assertEqual(problemas, [])

    def test_a_carrega_base_minima_em_tres_temas(self):
        # Minimo do enunciado: 15 registros em pelo menos 3 temas.
        self.assertGreaterEqual(len(self.validos), 15)
        self.assertEqual(BASE.listar_temas(self.validos),
                         ["Documentos", "Serviços", "Orientações comunitárias"])

    def test_consultas_aos_registros_reais(self):
        # O registro certo precisa vir em primeiro lugar, com a pontuacao conhecida.
        # Outros registros podem aparecer depois (palavras em comum, como "carteira").
        casos = [
            ("Como tirar a carteira de identidade?", "DOC-01", 4),
            ("Como consultar o Meu INSS?", "SER-01", 3),
            ("Como receber alertas da Defesa Civil por SMS?", "COM-01", 6),
        ]
        for pergunta, identificador, pontos in casos:
            with self.subTest(pergunta=pergunta):
                resultado = BUSCA.buscar_pergunta(self.validos, pergunta)
                self.assertIn(resultado["estado"], ("uma_correspondencia", "multiplas_correspondencias"))
                self.assertEqual(ids(resultado)[0], identificador)
                self.assertEqual(resultado["resultados"][0]["pontuacao"], pontos)

    def test_id_tema_e_palavra_chave_reais(self):
        self.assertEqual(ids(BUSCA.consultar_por_id(self.validos, " doc-01 ")), ["DOC-01"])
        por_tema = BUSCA.consultar_por_tema(self.validos, "servicos")
        self.assertIn("SER-01", ids(por_tema))
        self.assertTrue(all(BASE.normalizar(item["registro"]["tema"]) == "servicos"
                            for item in por_tema["resultados"]))
        self.assertEqual(ids(BUSCA.consultar_por_palavra_chave(self.validos, "defesa civil")), ["COM-01"])

    def test_ambiguidade_real_preserva_as_opcoes(self):
        resultado = BUSCA.buscar_pergunta(self.validos, "identidade e inss")
        self.assertEqual(resultado["estado"], "multiplas_correspondencias")
        self.assertEqual(ids(resultado), ["DOC-01", "SER-01"])

    def test_filtro_real(self):
        resultado = BUSCA.buscar_pergunta(self.validos, "identidade e inss", "Serviços")
        self.assertEqual(ids(resultado), ["SER-01"])

    def test_limites_com_base_real(self):
        for pergunta, estado in (("", "entrada_vazia"), ("?!", "entrada_vazia"),
                                  (None, "entrada_invalida"), ("como de o", "sem_correspondencia"),
                                  ("Como preparar bolo de chocolate?", "sem_correspondencia"),
                                  ("Como renovar o passaporte?", "sem_correspondencia")):
            with self.subTest(pergunta=pergunta):
                self.assertEqual(BUSCA.buscar_pergunta(self.validos, pergunta)["estado"], estado)

    def test_hierarquia_e_percurso_dos_tres_assuntos_reais(self):
        hierarquia = BUSCA.construir_hierarquia(self.validos)
        for atual, proximo in (("DOC-01", "SER-01"), ("SER-01", "COM-01"), ("COM-01", "DOC-01")):
            with self.subTest(atual=atual):
                self.assertIsNotNone(BUSCA.localizar_na_hierarquia(hierarquia, atual))
                sugestoes = BUSCA.sugerir_continuidade(self.validos, atual)
                self.assertIn(proximo, ids(sugestoes))
                self.assertNotIn(atual, ids(sugestoes))

    def test_registros_fontes_e_campos_de_a_preservados(self):
        antes = copy.deepcopy(self.validos)
        for registro in self.validos:
            item = BUSCA.consultar_por_id(self.validos, registro["id"])["resultados"][0]
            self.assertIs(item["registro"], registro)
            self.assertEqual(item["registro"]["referencia"], registro["referencia"])
            BUSCA.buscar_pergunta(self.validos, registro["palavras_chave"][0])
            BUSCA.sugerir_continuidade(self.validos, registro["id"])
        BUSCA.construir_hierarquia(self.validos)
        self.assertEqual(self.validos, antes)
        self.assertEqual(BASE.validar_registros(self.validos)[1], [])

    def test_copias_temporarias_e_arquivos_do_repositorio_inalterados(self):
        self.assertEqual((PASTA_TEMP / "src" / "base.py").read_bytes(), ORIGINAIS["base.py"])
        self.assertEqual((PASTA_TEMP / "src" / "busca.py").read_bytes(), ORIGINAIS["busca.py"])
        self.assertEqual((PASTA_TEMP / "data" / "base_conhecimento.json").read_bytes(),
                         ORIGINAIS["base_conhecimento.json"])
        for nome, caminho in ARQUIVOS_REAIS.items():
            with self.subTest(arquivo=nome):
                self.assertEqual(hashlib.sha256(caminho.read_bytes()).hexdigest(),
                                 HASHES_ORIGINAIS[nome])

    def test_importacao_sem_saida_interacao_ou_leitura_de_base(self):
        # Um processo novo elimina a possibilidade de o cache de import mascarar
        # efeitos colaterais. O JSON e ocultado apenas no diretorio temporario.
        caminho = PASTA_TEMP / "data" / "base_conhecimento.json"
        oculto = caminho.with_suffix(".oculto")
        caminho.rename(oculto)
        try:
            processo = subprocess.run(
                [sys.executable, "-B", "-c",
                 "from unittest.mock import patch\n"
                 "with patch('builtins.input', side_effect=RuntimeError('input indevido')):\n"
                 "    import base\n"
                 "    with patch.object(base, 'carregar_base', side_effect=RuntimeError('leitura indevida')):\n"
                 "        import busca\n"],
                cwd=PASTA_TEMP / "src", capture_output=True, text=True, timeout=15,
            )
        finally:
            oculto.rename(caminho)
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertEqual(processo.stdout, "")
        self.assertEqual(processo.stderr, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
