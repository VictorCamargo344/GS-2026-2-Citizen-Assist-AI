"""
Projeto...: Citizen Assist AI - Global Solution 2026.2 (FIAP)
Arquivo...: src/base.py
Parte.....: A - Base de conhecimento e leitura de arquivos
Assunto...: Leitura de arquivo JSON, validação e consulta com listas e dicionários
Problema..: Carregar as orientações de data/base_conhecimento.json, conferir se
            cada registro está completo e oferecer funções de acesso para as
            outras partes do sistema (busca, respostas, interface e testes).

COMO A BASE É ORGANIZADA
    O arquivo JSON guarda uma LISTA. Cada item da lista é um DICIONÁRIO
    (um registro) com exatamente estes campos:

        id                texto único                    ex.: "DOC-01"
        tema              texto                          ex.: "Documentos"
        palavras_chave    lista de textos                ex.: ["identidade", "rg"]
        orientacao        texto com a orientação resumida
        referencia        dicionário com "nome" e "link" da fonte consultada
        data_verificacao  texto no formato DD/MM/AAAA    ex.: "13/11/2026"

COMO ADICIONAR OU CORRIGIR UMA ORIENTAÇÃO
    Basta editar o arquivo JSON. Nenhuma linha deste programa precisa mudar:
    os temas, por exemplo, são descobertos lendo os próprios registros.
    Depois de editar, rode "python src/base.py" para conferir se está tudo certo.

PRIVACIDADE
    A base guarda apenas orientações e fontes. Nenhuma função deste arquivo
    pede, lê ou grava dados pessoais de quem usa o assistente.

COMO AS OUTRAS PARTES USAM ESTE ARQUIVO
    from base import carregar_base, validar_registros, listar_temas

    registros, erro = carregar_base()
    validos, problemas = validar_registros(registros)
    temas = listar_temas(validos)

    As funções daqui NÃO dão print: elas devolvem os dados e as mensagens.
    Quem decide o que mostrar na tela é quem chamou (a interface).
"""

import json
import os


#  CONFIGURAÇÕES

# Campos que todo registro precisa ter: nem a mais, nem a menos.
CAMPOS_OBRIGATORIOS = ["id", "tema", "palavras_chave", "orientacao",
                       "referencia", "data_verificacao"]

# Campos que precisam existir dentro de "referencia".
CAMPOS_REFERENCIA = ["nome", "link"]

# Caminho do arquivo da base, montado a partir da pasta onde ESTE arquivo está.
# Assim o programa encontra a base mesmo se for executado a partir de outra pasta.
PASTA_SRC = os.path.dirname(os.path.abspath(__file__))     # .../repositorio/src
PASTA_PROJETO = os.path.dirname(PASTA_SRC)                 # .../repositorio
CAMINHO_BASE = os.path.join(PASTA_PROJETO, "data", "base_conhecimento.json")

# Letras acentuadas e a letra "simples" correspondente (usado em normalizar).
SEM_ACENTO = {
    "á": "a", "à": "a", "â": "a", "ã": "a",
    "é": "e", "ê": "e",
    "í": "i",
    "ó": "o", "ô": "o", "õ": "o",
    "ú": "u", "ü": "u",
    "ç": "c",
}


# SUBALGORITMOS AUXILIARES

# Deixa um texto "comparável": sem espaços nas pontas, minúsculo e sem acento.
# Assim "Serviços", "servicos" e "  SERVIÇOS " passam a ser o mesmo texto.
def normalizar(texto: str) -> str:
    texto = str(texto).strip().lower()
    resultado = ""
    for letra in texto:
        if letra in SEM_ACENTO:
            resultado += SEM_ACENTO[letra]   # troca a letra acentuada
        else:
            resultado += letra               # mantém a letra como está
    return resultado


# Responde: "este valor é um texto com alguma coisa escrita?"
def texto_preenchido(valor) -> bool:
    return isinstance(valor, str) and valor.strip() != ""


# Responde: "este valor está escrito como uma data DD/MM/AAAA?"
# Confere só o formato (não sabe, por exemplo, que fevereiro não tem dia 31).
def data_valida(valor) -> bool:
    if not texto_preenchido(valor):
        return False

    partes = valor.strip().split("/")        # "13/11/2026" -> ["13", "11", "2026"]
    if len(partes) != 3:
        return False

    dia = partes[0]
    mes = partes[1]
    ano = partes[2]

    # isdecimal() é True quando o texto tem apenas algarismos
    if not (dia.isdecimal() and mes.isdecimal() and ano.isdecimal()):
        return False
    if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
        return False

    return 1 <= int(dia) <= 31 and 1 <= int(mes) <= 12


# LEITURA DO ARQUIVO

# Lê o arquivo JSON e devolve uma tupla com duas informações: (registros, erro)
#   registros -> lista de dicionários lida do arquivo ([] se algo deu errado)
#   erro      -> texto explicando o problema ("" quando deu tudo certo)
# Em nenhum caso o programa é derrubado: quem chamou decide o que fazer.
def carregar_base(caminho: str = CAMINHO_BASE) -> tuple:

    # Situação 1: arquivo AUSENTE.
    # os.path.isfile() responde se o caminho existe e é mesmo um arquivo.
    if not os.path.isfile(caminho):
        return [], (f"Arquivo da base não encontrado: {caminho}. "
                    "Confira se ele existe dentro da pasta data/.")

    # O "with" fecha o arquivo sozinho, mesmo se acontecer uma falha no meio.
    # encoding="utf-8-sig" lê os acentos corretamente em qualquer sistema
    # (inclusive quando o Bloco de Notas do Windows grava uma marca no início).
    try:
        with open(caminho, "r", encoding="utf-8-sig") as arquivo:
            conteudo = arquivo.read()
    except UnicodeDecodeError:
        return [], (f"Não foi possível ler os acentos do arquivo: {caminho}. "
                    "Salve o arquivo com a codificação UTF-8 e tente de novo.")

    # Situação 2: arquivo VAZIO (sem nada, ou só com espaços e linhas em branco).
    if conteudo.strip() == "":
        return [], f"O arquivo da base está vazio: {caminho}."

    # Situação 3: arquivo MALFORMADO (o texto não segue as regras do JSON).
    # json.loads() transforma o texto em listas e dicionários do Python.
    # Se o texto estiver quebrado, ele avisa com um erro: o try/except
    # "segura" esse erro para virar mensagem, em vez de derrubar o programa.
    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as falha:
        return [], (f"O arquivo da base está malformado: {caminho}. "
                    f"O problema está perto da linha {falha.lineno}, "
                    f"coluna {falha.colno}. Confira vírgulas, aspas duplas, "
                    "chaves { } e colchetes [ ].")

    # Situação 4: o JSON é válido, mas não tem o formato combinado.
    if not isinstance(dados, list):
        return [], (f"O arquivo da base deveria conter uma lista de registros "
                    f"(começar com [ e terminar com ]): {caminho}.")

    if len(dados) == 0:
        return [], f"A base não tem nenhum registro: {caminho}."

    return dados, ""


# VALIDAÇÃO DOS REGISTROS

# Confere UM registro e devolve a lista de problemas encontrados nele.
# Lista vazia significa "registro sem problemas".
def validar_registro(registro) -> list:
    problemas = []

    # O registro precisa ser um dicionário (no JSON: algo entre chaves { }).
    if not isinstance(registro, dict):
        problemas.append("não é um dicionário (no JSON, deveria estar entre chaves { })")
        return problemas                      # sem dicionário não há campos para conferir

    # Campos que faltam.
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in registro:
            problemas.append(f"falta o campo '{campo}'")

    # Campos que sobram (nome digitado errado ou dado que não deveria estar aqui).
    for campo in registro:
        if campo not in CAMPOS_OBRIGATORIOS:
            problemas.append(f"campo fora do combinado: '{campo}'")

    # Conteúdo de cada campo. Só confere o campo que existe,
    # para não repetir o aviso de "falta o campo".
    if "id" in registro and not texto_preenchido(registro["id"]):
        problemas.append("'id' deve ser um texto preenchido, como \"DOC-01\"")

    if "tema" in registro and not texto_preenchido(registro["tema"]):
        problemas.append("'tema' deve ser um texto preenchido")

    if "orientacao" in registro and not texto_preenchido(registro["orientacao"]):
        problemas.append("'orientacao' deve ser um texto preenchido")

    if "palavras_chave" in registro:
        palavras = registro["palavras_chave"]
        if not isinstance(palavras, list) or len(palavras) == 0:
            problemas.append("'palavras_chave' deve ser uma lista com pelo menos uma palavra")
        else:
            for palavra in palavras:
                if not texto_preenchido(palavra):
                    problemas.append("'palavras_chave' tem um item vazio ou que não é texto")
                    break                     # um aviso por registro já basta

    if "referencia" in registro:
        referencia = registro["referencia"]
        if not isinstance(referencia, dict):
            problemas.append("'referencia' deve ser um dicionário com 'nome' e 'link'")
        else:
            for campo in CAMPOS_REFERENCIA:
                if campo not in referencia or not texto_preenchido(referencia[campo]):
                    problemas.append(f"'referencia' está sem '{campo}' preenchido")
            for campo in referencia:
                if campo not in CAMPOS_REFERENCIA:
                    problemas.append(f"campo fora do combinado em 'referencia': '{campo}'")
            # Uma fonte verificável precisa de um endereço que abra no navegador.
            if "link" in referencia and texto_preenchido(referencia["link"]):
                if not referencia["link"].strip().lower().startswith("http"):
                    problemas.append("'link' da referência deve começar com http:// ou https://")

    if "data_verificacao" in registro and not data_valida(registro["data_verificacao"]):
        problemas.append("'data_verificacao' deve estar no formato DD/MM/AAAA, como \"13/11/2026\"")

    return problemas


# Confere TODOS os registros e devolve uma tupla: (validos, problemas)
# validos   -> lista com os registros que podem ser usados pelo assistente
#  problemas -> lista de textos apontando cada registro inconsistente e o motivo
# Um registro com problema fica de fora, mas os outros continuam valendo.
def validar_registros(registros: list) -> tuple:
    validos = []
    problemas = []
    ids_ja_vistos = []                        # para descobrir id repetido

    if not isinstance(registros, list):
        return validos, ["A base deveria ser uma lista de registros."]

    for posicao in range(len(registros)):
        registro = registros[posicao]
        numero = posicao + 1                  # o Python conta do 0; as pessoas, do 1

        erros = validar_registro(registro)

        # Nome do registro nas mensagens, por exemplo: "Registro 2 (id SER-01)".
        rotulo = f"Registro {numero}"
        tem_id = (isinstance(registro, dict) and "id" in registro
                  and texto_preenchido(registro["id"]))

        if tem_id:
            rotulo += f" (id {registro['id']})"

            # id repetido só aparece olhando a lista inteira, por isso fica aqui.
            # O primeiro registro com o id continua valendo; os seguintes, não.
            id_comparavel = normalizar(registro["id"])
            if id_comparavel in ids_ja_vistos:
                erros.append("'id' repetido: já existe outro registro com este id")
            else:
                ids_ja_vistos.append(id_comparavel)

        if len(erros) == 0:
            validos.append(registro)
        else:
            for erro in erros:
                problemas.append(f"{rotulo}: {erro}")

    return validos, problemas


# FUNÇÕES DE ACESSO (usadas pelas outras partes)
# Todas esperam receber a lista "validos" devolvida por validar_registros.
# Por isso podem confiar que os campos existem e estão preenchidos.

# Devolve os temas disponíveis, sem repetição, na ordem em que aparecem na base.
def listar_temas(registros: list) -> list:
    temas = []                                # como o tema está escrito (para mostrar)
    temas_comparaveis = []                    # versão normalizada (para comparar)

    for registro in registros:
        comparavel = normalizar(registro["tema"])
        if comparavel not in temas_comparaveis:
            temas_comparaveis.append(comparavel)
            temas.append(registro["tema"])

    return temas


# Devolve o registro que tem o id informado, ou None se não existir.
# "doc-01" e "DOC-01" são tratados como o mesmo id.
def buscar_por_id(registros: list, id_procurado: str) -> dict:
    procurado = normalizar(id_procurado)

    for registro in registros:
        if normalizar(registro["id"]) == procurado:
            return registro                   # achou: não precisa olhar o resto

    return None


# Devolve a lista de registros de um tema (lista vazia se o tema não existir).
def filtrar_por_tema(registros: list, tema: str) -> list:
    procurado = normalizar(tema)
    encontrados = []

    for registro in registros:
        if normalizar(registro["tema"]) == procurado:
            encontrados.append(registro)

    return encontrados


# Devolve a lista de registros que têm o termo entre as palavras-chave.
# A comparação é com a palavra-chave INTEIRA: "rg" encontra a palavra-chave "rg",
# mas não encontra "emergência" (que tem as letras "rg" no meio).
def buscar_por_palavra_chave(registros: list, termo: str) -> list:
    procurado = normalizar(termo)
    encontrados = []

    if procurado == "":                       # termo vazio não encontra nada
        return encontrados

    for registro in registros:
        for palavra in registro["palavras_chave"]:
            if normalizar(palavra) == procurado:
                encontrados.append(registro)
                break                         # este registro já entrou; vai para o próximo

    return encontrados


# TESTE RÁPIDO
# Este bloco só roda quando executamos ESTE arquivo diretamente:
#   python src/base.py
# Quando outro arquivo faz "import base", o bloco é ignorado.
if __name__ == "__main__":
    print("=== TESTE DA PARTE A - BASE DE CONHECIMENTO ===")
    print(f"Arquivo: {CAMINHO_BASE}")
    print()

    # 1) Carregar
    registros, erro = carregar_base(CAMINHO_BASE)

    if erro != "":
        print("[ERRO] " + erro)
    else:
        print(f"[OK] {len(registros)} registro(s) lido(s) do arquivo.")

        # 2) Validar
        validos, problemas = validar_registros(registros)
        print(f"[OK] {len(validos)} registro(s) válido(s).")

        if len(problemas) > 0:
            print(f"[ATENÇÃO] {len(problemas)} problema(s) encontrado(s):")
            for problema in problemas:
                print("    - " + problema)

        # 3) Temas
        temas = listar_temas(validos)
        print()
        print("Temas disponíveis:")
        for tema in temas:
            quantidade = len(filtrar_por_tema(validos, tema))
            print(f"    - {tema}: {quantidade} registro(s)")

        # 4) Funções de acesso, usando o primeiro registro válido como exemplo
        if len(validos) > 0:
            exemplo = validos[0]
            palavra = exemplo["palavras_chave"][0]

            achado = buscar_por_id(validos, exemplo["id"])
            achados = buscar_por_palavra_chave(validos, palavra)

            print()
            print("Funções de acesso:")
            print(f"    buscar_por_id('{exemplo['id']}') -> {achado['referencia']['nome']}")
            print(f"    buscar_por_palavra_chave('{palavra}') -> {len(achados)} registro(s)")
            print(f"    buscar_por_id('NAO-EXISTE') -> {buscar_por_id(validos, 'NAO-EXISTE')}")

        # 5) Mínimos pedidos no enunciado da Global Solution
        print()
        if len(validos) < 15 or len(temas) < 3:
            print(f"[AVISO] O enunciado pede pelo menos 15 registros em 3 temas. "
                  f"Hoje a base tem {len(validos)} registro(s) em {len(temas)} tema(s).")
        else:
            print("[OK] A base atende ao mínimo do enunciado (15 registros em 3 temas).")
