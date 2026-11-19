"""Citizen Assist AI — ponto de entrada e interface em texto (Parte D).

Como executar, na raiz do repositório:
    python src/sistema.py

O que este arquivo faz:
    - carrega e valida a base (Parte A);
    - mostra o menu principal, os temas e os assuntos;
    - recebe perguntas digitadas e envia para a busca (Parte B);
    - mostra a resposta formatada com fonte e avisos (Parte C);
    - trata entrada vazia, opção inexistente, pergunta ambígua e pergunta
      sem resposta, sempre oferecendo um caminho para continuar.

Privacidade: nada do que a pessoa digita é gravado em arquivo.
"""
import sys

from base import carregar_base, listar_temas, validar_registros
from busca import (
    buscar_pergunta,
    construir_hierarquia,
    consultar_por_id,
    localizar_na_hierarquia,
    sugerir_continuidade,
)
from resposta import AVISO_NAO_OFICIAL, MODELOS, responder_resultado_busca


MODELO_INICIAL = "guiado"      # formato mais claro na comparação dos dois modelos
MAX_MESMO_TEMA = 3             # quantos assuntos do mesmo tema sugerir depois de uma resposta
LINHA = "=" * 70
LINHA_FINA = "-" * 70


class EncerrarPrograma(Exception):
    """A pessoa fechou a entrada (Ctrl+C ou Ctrl+Z/Ctrl+D)."""


# LEITURA DO TECLADO

def ler(mensagem):
    """Lê uma linha do teclado; Ctrl+C ou fim da entrada encerram o programa sem erro."""
    try:
        return input(mensagem)
    except (EOFError, KeyboardInterrupt):
        raise EncerrarPrograma


def escolher_numero(mensagem, maximo, minimo=0):
    """Pede um número entre minimo e maximo e repete a pergunta até ser válido."""
    while True:
        texto = ler(mensagem).strip()
        if texto == "":
            print("Você não digitou nada. Digite o número de uma das opções.")
            continue
        if not texto.isdecimal():
            print(f'"{texto}" não é uma opção. Digite só o número, de {minimo} a {maximo}.')
            continue
        numero = int(texto)
        if numero < minimo or numero > maximo:
            print(f"A opção {numero} não existe. Escolha um número de {minimo} a {maximo}.")
            continue
        return numero


def titulo_de(estado, identificador):
    """Devolve o título do assunto (primeira palavra-chave) a partir do ID."""
    local = localizar_na_hierarquia(estado["hierarquia"], identificador)
    if local is None:
        return identificador
    return local["caminho"][-1]


# ORIENTAÇÃO E CONTINUIDADE

def mostrar_orientacao(estado, identificador):
    """Mostra a orientação de um assunto e devolve o ID do próximo assunto escolhido (ou None)."""
    local = localizar_na_hierarquia(estado["hierarquia"], identificador)
    resultado = consultar_por_id(estado["registros"], identificador)
    titulo = local["caminho"][-1] if local else identificador

    print()
    print(LINHA)
    if local is not None:
        print("Você está em: " + " > ".join(local["caminho"]))
        print(LINHA_FINA)
    print(responder_resultado_busca(titulo, resultado, estado["temas"], estado["modelo"]))
    print(LINHA)
    return oferecer_continuidade(estado, identificador)


def montar_sugestoes(estado, identificador):
    """Escolhe até 3 assuntos do mesmo tema e 1 assunto de cada outro tema."""
    sugestoes = sugerir_continuidade(estado["registros"], identificador)
    if sugestoes["estado"] != "opcoes_disponiveis":
        return []

    mesmo_tema = []
    outros_temas = []
    temas_ja_sugeridos = []
    for item in sugestoes["resultados"]:
        tema = item["registro"]["tema"]
        if item["relacao"] == "mesmo_tema" and len(mesmo_tema) < MAX_MESMO_TEMA:
            mesmo_tema.append(item)
        elif item["relacao"] == "outro_tema" and tema not in temas_ja_sugeridos:
            temas_ja_sugeridos.append(tema)
            outros_temas.append(item)
    return mesmo_tema + outros_temas


def oferecer_continuidade(estado, identificador):
    """Mostra assuntos relacionados e devolve o ID escolhido, ou None para voltar."""
    opcoes = montar_sugestoes(estado, identificador)
    if not opcoes:
        ler("Pressione Enter para voltar ao menu principal.")
        return None

    print()
    print("Assuntos relacionados que também posso explicar:")
    for numero, item in enumerate(opcoes, 1):
        registro = item["registro"]
        print(f"  {numero}. {titulo_de(estado, registro['id'])} ({registro['tema']})")
    print("  0. Voltar ao menu principal")
    escolha = escolher_numero("Escolha uma opção: ", len(opcoes))
    if escolha == 0:
        return None
    return opcoes[escolha - 1]["registro"]["id"]


def navegar_a_partir_de(estado, identificador):
    """Mostra um assunto e segue para os assuntos relacionados enquanto a pessoa quiser."""
    while identificador is not None:
        identificador = mostrar_orientacao(estado, identificador)


# MENU DE TEMAS

def escolher_assunto_do_tema(estado, grupo):
    """Lista os assuntos de um tema e devolve o ID escolhido, ou None para voltar."""
    assuntos = grupo["assuntos"]
    print()
    print(f"Assuntos de {grupo['tema']}:")
    for numero, assunto in enumerate(assuntos, 1):
        print(f"  {numero}. {assunto['titulo']}")
    print("  0. Voltar aos temas")
    escolha = escolher_numero("Escolha um assunto: ", len(assuntos))
    if escolha == 0:
        return None
    return assuntos[escolha - 1]["id"]


def ver_temas(estado):
    """Menu de temas: tema -> assunto -> orientação."""
    grupos = estado["hierarquia"]["temas"]
    while True:
        print()
        print("Temas disponíveis:")
        for numero, grupo in enumerate(grupos, 1):
            print(f"  {numero}. {grupo['tema']} ({len(grupo['assuntos'])} assuntos)")
        print("  0. Voltar ao menu principal")
        escolha = escolher_numero("Escolha um tema: ", len(grupos))
        if escolha == 0:
            return
        identificador = escolher_assunto_do_tema(estado, grupos[escolha - 1])
        if identificador is not None:
            navegar_a_partir_de(estado, identificador)
            return


# PERGUNTA DIGITADA

def tratar_ambiguidade(estado, resultado):
    """Mostra as opções encontradas e devolve o ID escolhido, ou None ("nenhuma delas")."""
    itens = resultado["resultados"]
    print()
    print("Sua pergunta pode estar relacionada a mais de um assunto.")
    print("Para não mostrar uma orientação errada, escolha o que você procura:")
    for numero, item in enumerate(itens, 1):
        registro = item["registro"]
        print(f"  {numero}. {titulo_de(estado, registro['id'])} ({registro['tema']})")
    print("  0. Nenhuma dessas opções")
    escolha = escolher_numero("Escolha uma opção: ", len(itens))
    if escolha == 0:
        return None
    return itens[escolha - 1]["registro"]["id"]


def oferecer_alternativas(estado):
    """Depois de uma pergunta sem resposta, mostra os caminhos para continuar."""
    print()
    print("Assuntos que posso explicar:")
    for grupo in estado["hierarquia"]["temas"]:
        titulos = [assunto["titulo"] for assunto in grupo["assuntos"]]
        print(f"  - {grupo['tema']}: {', '.join(titulos)}")
    print()
    print("O que você quer fazer agora?")
    print("  1. Fazer outra pergunta")
    print("  2. Ver os temas e escolher um assunto")
    print("  0. Voltar ao menu principal")
    escolha = escolher_numero("Escolha uma opção: ", 2)
    if escolha == 1:
        fazer_pergunta(estado)
    elif escolha == 2:
        ver_temas(estado)


def fazer_pergunta(estado):
    """Recebe uma pergunta, busca na base e conduz a pessoa até uma orientação ou um aviso."""
    print()
    print("Escreva sua dúvida com poucas palavras (por exemplo: como tirar o título de eleitor).")
    print("Não digite dados pessoais, como nome, CPF ou endereço: o assistente não precisa deles.")
    pergunta = ler("Sua pergunta: ")
    resultado = buscar_pergunta(estado["registros"], pergunta)
    situacao = resultado["estado"]

    if situacao == "uma_correspondencia":
        navegar_a_partir_de(estado, resultado["resultados"][0]["registro"]["id"])
        return

    if situacao == "multiplas_correspondencias":
        identificador = tratar_ambiguidade(estado, resultado)
        if identificador is not None:
            navegar_a_partir_de(estado, identificador)
            return
        # "Nenhuma dessas opções": a base não tem o que a pessoa procura.
        resultado = {"estado": "sem_correspondencia", "resultados": []}

    print()
    print(LINHA)
    print(responder_resultado_busca(pergunta if pergunta.strip() else "(vazia)",
                                    resultado, estado["temas"], estado["modelo"]))
    print(LINHA)
    if situacao in ("entrada_vazia", "entrada_invalida"):
        return
    oferecer_alternativas(estado)


# OUTRAS OPÇÕES DO MENU

def trocar_formato(estado):
    """Permite escolher entre os dois modelos de resposta da Parte C."""
    nomes = list(MODELOS)
    print()
    print("Formatos de resposta:")
    for numero, nome in enumerate(nomes, 1):
        atual = "  (atual)" if nome == estado["modelo"] else ""
        print(f"  {numero}. {MODELOS[nome]['nome']}{atual}")
    print("  0. Manter como está")
    escolha = escolher_numero("Escolha um formato: ", len(nomes))
    if escolha != 0:
        estado["modelo"] = nomes[escolha - 1]
        print("Formato alterado para: " + MODELOS[estado["modelo"]]["nome"])


def mostrar_sobre(estado):
    print()
    print(LINHA)
    print("SOBRE O CITIZEN ASSIST AI")
    print(LINHA_FINA)
    print(f"- Reúne {len(estado['registros'])} orientações sobre {len(estado['temas'])} temas,")
    print("  conferidas em fontes oficiais. Cada resposta mostra a fonte e a data da conferência.")
    print("- Quando a base não tem a informação, o assistente avisa e não inventa uma resposta.")
    print("- As regras dos serviços podem mudar: sempre confirme na fonte antes de agir.")
    print("- Nada do que você digita é gravado. Não é preciso informar dados pessoais.")
    print("- " + AVISO_NAO_OFICIAL)
    print(LINHA)


# PROGRAMA PRINCIPAL

def preparar_estado():
    """Carrega a base; devolve (estado, erro)."""
    registros, erro = carregar_base()
    if erro != "":
        return None, erro
    validos, problemas = validar_registros(registros)
    if problemas:
        print(f"[ATENÇÃO] {len(problemas)} problema(s) na base: os registros com problema "
              "foram ignorados. Rode 'python src/base.py' para ver os detalhes.")
    if not validos:
        return None, "Nenhuma orientação válida na base de conhecimento."
    estado = {
        "registros": validos,
        "temas": listar_temas(validos),
        "hierarquia": construir_hierarquia(validos),
        "modelo": MODELO_INICIAL,
    }
    return estado, ""


def menu_principal(estado):
    while True:
        print()
        print(LINHA)
        print("MENU PRINCIPAL")
        print("  1. Ver temas e assuntos")
        print("  2. Fazer uma pergunta")
        print(f"  3. Trocar o formato da resposta (atual: {MODELOS[estado['modelo']]['nome']})")
        print("  4. Sobre o assistente e seus limites")
        print("  0. Sair")
        escolha = escolher_numero("Escolha uma opção: ", 4)
        if escolha == 0:
            return
        if escolha == 1:
            ver_temas(estado)
        elif escolha == 2:
            fazer_pergunta(estado)
        elif escolha == 3:
            trocar_formato(estado)
        elif escolha == 4:
            mostrar_sobre(estado)


def main():
    estado, erro = preparar_estado()
    if estado is None:
        print("Não foi possível iniciar o Citizen Assist AI.")
        print("Motivo: " + erro)
        return 1

    print(LINHA)
    print("CITIZEN ASSIST AI — Orientação cidadã")
    print(LINHA)
    print("Olá! Eu ajudo a encontrar orientações sobre documentos, serviços e")
    print("direitos, sempre com a fonte oficial de onde a informação veio.")
    print(AVISO_NAO_OFICIAL)

    try:
        menu_principal(estado)
    except EncerrarPrograma:
        print()
    print("Até logo! Lembre-se de confirmar as informações na fonte oficial antes de agir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
