"""Parte B do Citizen Assist AI: consulta e navegacao, sem interface de tela.

Recebe a lista de registros validos produzida pela Parte A. Para importar este
modulo no projeto integrado, coloque o base.py original ao lado de busca.py.
Nao le arquivos, nao altera os registros e nao chama IA durante as consultas.
O contrato completo e os exemplos estao em docs/integracao.md.
"""

from base import (
    buscar_por_id,
    buscar_por_palavra_chave,
    filtrar_por_tema,
    listar_temas,
    normalizar,
)


# Palavras funcionais nao devem decidir qual orientacao sera encontrada.
# Nao ha sinonimos nem regras feitas para uma pergunta especifica nesta lista.
PALAVRAS_IGNORADAS = (
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "eu", "me", "meu", "meus", "minha", "minhas", "na", "nas",
    "no", "nos", "o", "os", "ou", "para", "por", "qual", "quais", "que",
    "se", "um", "uma",
)

RAIZ = "Orientação cidadã"


def _texto_comparavel(texto):
    """Reaproveita os acentos de A e transforma pontuacao em separadores."""
    letras = []
    for letra in normalizar(texto):
        if letra.isalnum():
            letras.append(letra)
        else:
            letras.append(" ")
    return " ".join("".join(letras).split())


def _problema_entrada(texto):
    """Devolve um estado de erro, ou None quando ha texto utilizavel."""
    if not isinstance(texto, str):
        return "entrada_invalida"
    if _texto_comparavel(texto) == "":
        return "entrada_vazia"
    return None


def _palavras_uteis(texto_comparavel):
    """Monta uma lista sem repeticoes; mantem a ordem da primeira aparicao."""
    palavras = []
    for palavra in texto_comparavel.split():
        if palavra not in PALAVRAS_IGNORADAS and palavra not in palavras:
            palavras.append(palavra)
    return palavras


def _item(registro, pontuacao=None, termos=None, expressoes=None):
    # Os metadados ficam neste novo dicionario, nunca no registro original.
    return {
        "registro": registro,
        "pontuacao": pontuacao,
        "termos_encontrados": termos if termos is not None else [],
        "expressoes_encontradas": expressoes if expressoes is not None else [],
    }


def _resultado(itens, estado=None):
    if estado is None:
        if len(itens) == 0:
            estado = "sem_correspondencia"
        elif len(itens) == 1:
            estado = "uma_correspondencia"
        else:
            estado = "multiplas_correspondencias"
    return {"estado": estado, "resultados": itens}


def _selecionar_tema(registros, tema):
    """None significa sem filtro; demais entradas seguem a validacao textual."""
    if tema is None:
        return registros, None
    problema = _problema_entrada(tema)
    if problema is not None:
        return [], problema
    selecionados = filtrar_por_tema(registros, tema)
    if not selecionados:
        return [], "tema_inexistente"
    return selecionados, None


def consultar_por_id(registros, identificador):
    """Busca um ID exato por A; distingue ID inexistente de entrada invalida."""
    problema = _problema_entrada(identificador)
    if problema is not None:
        return _resultado([], problema)
    registro = buscar_por_id(registros, identificador)
    if registro is None:
        return _resultado([], "id_inexistente")
    return _resultado([_item(registro)])


def consultar_por_tema(registros, tema):
    """Lista registros de um tema exato, na ordem recebida da Parte A."""
    # Aqui o tema e obrigatorio; None nao significa listar todos.
    problema = _problema_entrada(tema)
    if problema is not None:
        return _resultado([], problema)
    selecionados, problema = _selecionar_tema(registros, tema)
    if problema is not None:
        return _resultado([], problema)
    return _resultado([_item(registro) for registro in selecionados])


def consultar_por_palavra_chave(registros, palavra_chave, tema=None):
    """Usa a correspondencia EXATA de A; nao e a busca de pergunta livre.

    A ignora caixa, acentos e espacos nas pontas. Pontuacao e espacos internos
    continuam fazendo parte da palavra-chave nesta modalidade exata.
    """
    problema = _problema_entrada(palavra_chave)
    if problema is not None:
        return _resultado([], problema)
    selecionados, problema = _selecionar_tema(registros, tema)
    if problema is not None:
        return _resultado([], problema)
    encontrados = buscar_por_palavra_chave(selecionados, palavra_chave)
    return _resultado([_item(registro) for registro in encontrados])


def _pontuar(registro, texto_pergunta, palavras_pergunta):
    vocabulario = []
    expressoes = []
    for chave in registro["palavras_chave"]:
        texto_chave = _texto_comparavel(chave)
        palavras_chave = _palavras_uteis(texto_chave)
        for palavra in palavras_chave:
            if palavra not in vocabulario:
                vocabulario.append(palavra)

        # Os espacos nas bordas impedem casamento dentro de outra palavra.
        # A expressao precisa estar inteira e na mesma ordem, inclusive "de".
        if len(texto_chave.split()) > 1 and palavras_chave:
            if " " + texto_chave + " " in " " + texto_pergunta + " ":
                if texto_chave not in expressoes:
                    expressoes.append(texto_chave)

    termos = []
    for palavra in palavras_pergunta:
        if palavra in vocabulario:
            termos.append(palavra)

    # 1 ponto por termo util distinto + 2 por expressao composta distinta.
    pontos = len(termos) + 2 * len(expressoes)
    return _item(registro, pontos, termos, expressoes)


def _ordem_busca(item):
    # Mais pontos primeiro; empate por ID normalizado em ordem alfabetica.
    return -item["pontuacao"], normalizar(item["registro"]["id"])


def buscar_pergunta(registros, pergunta, tema=None):
    """Busca linear por palavras-chave; devolve TODAS as pontuacoes positivas.

    Uma unica opcao nao prova que a pergunta foi compreendida. A frente C
    continua responsavel por explicar os limites; D decide o que apresentar.
    """
    problema = _problema_entrada(pergunta)
    if problema is not None:
        return _resultado([], problema)
    selecionados, problema = _selecionar_tema(registros, tema)
    if problema is not None:
        return _resultado([], problema)

    texto = _texto_comparavel(pergunta)
    palavras = _palavras_uteis(texto)
    if not palavras:
        return _resultado([])

    encontrados = []
    for registro in selecionados:
        item = _pontuar(registro, texto, palavras)
        if item["pontuacao"] > 0:
            encontrados.append(item)
    encontrados.sort(key=_ordem_busca)
    return _resultado(encontrados)


def construir_hierarquia(registros):
    """Agrupa raiz -> temas -> assuntos; titulo vem da primeira palavra-chave.

    A estrutura e nova, mas suas folhas referenciam os registros de A.
    Acrescentar registros/temas validos dispensa editar este algoritmo.
    """
    hierarquia = {"raiz": RAIZ, "temas": []}
    for tema in listar_temas(registros):
        assuntos = []
        for registro in filtrar_por_tema(registros, tema):
            assuntos.append({
                "id": registro["id"],
                "titulo": registro["palavras_chave"][0],
                "registro": registro,
            })
        hierarquia["temas"].append({"tema": tema, "assuntos": assuntos})
    return hierarquia


def localizar_na_hierarquia(hierarquia, identificador):
    """Devolve caminho/registro de um ID, ou None se a entrada/ID nao servir.

    Espera a hierarquia construida por construir_hierarquia; nao valida uma
    arvore externa. Este auxiliar tem retorno simples, nao um resultado de busca.
    """
    if _problema_entrada(identificador) is not None:
        return None
    for grupo in hierarquia["temas"]:
        for assunto in grupo["assuntos"]:
            if normalizar(assunto["id"]) == normalizar(identificador):
                return {
                    "caminho": [hierarquia["raiz"], grupo["tema"], assunto["titulo"]],
                    "registro": assunto["registro"],
                }
    return None


def sugerir_continuidade(registros, identificador=None):
    """Sugere irmaos do mesmo tema e depois opcoes de outros temas da raiz.

    Sem ID (None), oferece todos os assuntos, inclusive apos busca sem resultado.
    Nao afirma relacao burocratica ou dependencia entre os procedimentos.
    """
    atual = None
    if identificador is not None:
        consulta = consultar_por_id(registros, identificador)
        if consulta["estado"] != "uma_correspondencia":
            return consulta
        atual = consulta["resultados"][0]["registro"]

    mesmo_tema = []
    outros_temas = []
    for registro in registros:
        if atual is not None and normalizar(registro["id"]) == normalizar(atual["id"]):
            continue
        item = _item(registro)
        if atual is None:
            item["relacao"] = "tema_disponivel"
            item["justificativa"] = "Assunto disponível em Orientação cidadã."
            outros_temas.append(item)
        elif normalizar(registro["tema"]) == normalizar(atual["tema"]):
            item["relacao"] = "mesmo_tema"
            item["justificativa"] = "Outro assunto do mesmo tema."
            mesmo_tema.append(item)
        else:
            item["relacao"] = "outro_tema"
            item["justificativa"] = (
                "Outro tema de Orientação cidadã; opção de exploração, "
                "sem dependência entre os procedimentos."
            )
            outros_temas.append(item)

    opcoes = mesmo_tema + outros_temas
    estado = "opcoes_disponiveis" if opcoes else "sem_opcoes"
    return _resultado(opcoes, estado)
