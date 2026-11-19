"""Frente E: executa as perguntas de teste e calcula os indicadores.

Como rodar: python src/testes.py
Critérios de correção: docs/resultados_testes.md
Registro gerado: docs/resultados_testes.csv
"""
import csv
import json
import os
import sys
import time

from base import PASTA_PROJETO, carregar_base, validar_registros
from busca import buscar_pergunta
from resposta import responder_resultado_busca

CAMINHO_PERGUNTAS = os.path.join(PASTA_PROJETO, "data", "perguntas_teste.json")
CAMINHO_CSV = os.path.join(PASTA_PROJETO, "docs", "resultados_testes.csv")

REPETICOES = 100                               # cada consulta é medida 100 vezes (usa a média)
TOP_MENU = 3                                  # posição máxima do registro esperado no menu para contar acerto
TEXTO_LIMITE = "AVISO DE LIMITAÇÃO"            # texto que a Parte C mostra quando a base não tem resposta
TEXTO_VAZIO = "Você não digitou nenhuma pergunta."  # texto que a Parte C mostra para entrada vazia


CAMPOS_PERGUNTA = ["id_teste", "pergunta", "resultado_esperado"]


def carregar_perguntas(caminho=CAMINHO_PERGUNTAS):
    """Devolve (perguntas, erro), no mesmo estilo de carregar_base.

    Qualquer problema invalida o arquivo inteiro: calcular a taxa de acerto
    com só parte das perguntas daria um número enganoso.
    """
    # 1) Arquivo ausente.
    if not os.path.isfile(caminho):
        return [], f"Arquivo de perguntas não encontrado: {caminho}"

    # 2) Ler como texto primeiro, para poder testar se está vazio.
    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        conteudo = arquivo.read()
    if conteudo.strip() == "":
        return [], f"O arquivo de perguntas está vazio: {caminho}"

    # 3) JSON quebrado: o try/except transforma o erro em mensagem.
    try:
        perguntas = json.loads(conteudo)
    except json.JSONDecodeError as falha:
        return [], (f"O arquivo de perguntas está malformado perto da linha "
                    f"{falha.lineno}, coluna {falha.colno}: {caminho}")

    # 4) Formato errado: precisa ser uma lista com pelo menos uma pergunta.
    if not isinstance(perguntas, list):
        return [], "O arquivo de perguntas deveria conter uma lista (começar com [)."
    if len(perguntas) == 0:
        return [], "O arquivo de perguntas não tem nenhuma pergunta."

    # 5) Cada pergunta precisa dos campos que o resto do script usa.
    for posicao in range(len(perguntas)):
        teste = perguntas[posicao]
        numero = posicao + 1
        if not isinstance(teste, dict):
            return [], f"Pergunta {numero}: deveria estar entre chaves {{ }}."
        for campo in CAMPOS_PERGUNTA:
            if campo not in teste:
                return [], f"Pergunta {numero}: falta o campo '{campo}'."
        if not isinstance(teste["pergunta"], str):
            return [], f"Pergunta {numero}: 'pergunta' deve ser um texto (pode ser \"\")."
        if teste["resultado_esperado"] == "uma_correspondencia" and not teste.get("id_esperado"):
            return [], f"Pergunta {numero}: 'uma_correspondencia' exige um 'id_esperado'."

    return perguntas, ""


def executar_teste(registros, teste, repeticoes=REPETICOES):
    """Roda uma pergunta e devolve o que aconteceu + os dois tempos médios.

    Uma busca leva frações de milissegundo; nessa escala, uma medição única
    varia muito por causa do computador. Por isso:
      1) a primeira execução fica FORA da medição (aquecimento) e é a que
         fornece o resultado classificado;
      2) depois a consulta é repetida `repeticoes` vezes e usamos a média.
    """
    pergunta = teste["pergunta"]

    # 1) Aquecimento + resultado usado na classificação.
    resultado = buscar_pergunta(registros, pergunta)
    texto = responder_resultado_busca(pergunta, resultado)

    # 2) Medição repetida.
    soma_busca = 0
    soma_consulta = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resultado_medido = buscar_pergunta(registros, pergunta)
        fim_busca = time.perf_counter()
        responder_resultado_busca(pergunta, resultado_medido)
        fim_consulta = time.perf_counter()
        soma_busca += fim_busca - inicio
        soma_consulta += fim_consulta - inicio

    return {
        "estado": resultado["estado"],
        "ids": [item["registro"]["id"] for item in resultado["resultados"]],
        "texto": texto,
        "tempo_busca_ms": soma_busca / repeticoes * 1000,
        "tempo_consulta_ms": soma_consulta / repeticoes * 1000,
    }


def classificar(teste, execucao):
    """Compara o resultado com o gabarito e devolve ("direto" | "menu" | "erro", motivo)."""
    esperado = teste["resultado_esperado"]
    estado = execucao["estado"]
    ids = execucao["ids"]

    # Pergunta com resposta na base: deveria achar o registro esperado.
    if esperado == "uma_correspondencia":
        id_esperado = teste["id_esperado"]

        if estado == "uma_correspondencia" and ids[0] == id_esperado:
            return "direto", f"encontrou {id_esperado}"

        if estado == "multiplas_correspondencias" and id_esperado in ids[:TOP_MENU]:
            posicao = ids.index(id_esperado) + 1        # o Python conta do 0
            return "menu", f"{id_esperado} na posição {posicao} de {len(ids)} opções"

        # Daqui para baixo é erro; o motivo diz qual tipo de erro foi.
        if len(ids) == 0:
            return "erro", f"não encontrou nada (esperado {id_esperado})"
        if estado == "uma_correspondencia":
            return "erro", f"encontrou {ids[0]} em vez de {id_esperado}"
        if id_esperado in ids:
            posicao = ids.index(id_esperado) + 1
            return "erro", f"{id_esperado} só na posição {posicao} de {len(ids)} (fora do top {TOP_MENU})"
        return "erro", f"menu sem {id_esperado}: {', '.join(ids)}"

    # Pergunta ambígua: mostrar o menu é o comportamento certo.
    if esperado == "multiplas_correspondencias":
        if estado == "multiplas_correspondencias":
            return "direto", f"mostrou menu com {len(ids)} opções: {', '.join(ids)}"
        if estado == "uma_correspondencia":
            return "erro", f"escolheu sozinho {ids[0]} em vez de mostrar opções"
        return "erro", f"esperava menu, obteve {estado}"

    # Pergunta sem resposta na base: não pode oferecer nenhum registro.
    if esperado == "sem_correspondencia":
        # Falso positivo vem primeiro: se ofereceu algo, é erro e pronto.
        if len(ids) > 0:
            return "erro", f"falso positivo: {', '.join(ids)}"
        if TEXTO_LIMITE in execucao["texto"]:
            return "direto", "sem registro e com aviso de limitação"
        return "erro", "sem registro, mas sem aviso de limitação no texto"

    # Entrada vazia: precisa reconhecer e pedir uma pergunta.
    if esperado == "entrada_vazia":
        if estado == "entrada_vazia" and TEXTO_VAZIO in execucao["texto"]:
            return "direto", "reconheceu entrada vazia e pediu uma pergunta"
        if estado == "entrada_vazia":
            return "erro", "reconheceu entrada vazia, mas o texto não pede uma pergunta"
        return "erro", f"não reconheceu entrada vazia (obteve {estado})"

    return "erro", f"resultado_esperado desconhecido: {esperado}"


# Colunas do CSV. As chaves de cada "linha" são exatamente estas.
COLUNAS_CSV = ["id_teste", "tipo", "pergunta", "esperado", "id_esperado",
               "obtido", "ids_obtidos", "tamanho_menu", "classificacao",
               "motivo", "tempo_busca_ms", "tempo_consulta_ms"]


def montar_linha(teste, execucao, classificacao, motivo):
    """Junta o gabarito (teste) com o que aconteceu (execucao + classificar)."""
    return {
        "id_teste": teste["id_teste"],
        "tipo": teste.get("tipo", ""),
        "pergunta": teste["pergunta"],
        "esperado": teste["resultado_esperado"],
        "id_esperado": teste.get("id_esperado") or "",
        "obtido": execucao["estado"],
        "ids_obtidos": ", ".join(execucao["ids"]),
        # Só há menu quando a busca devolve várias opções; senão fica vazio.
        "tamanho_menu": (len(execucao["ids"])
                         if execucao["estado"] == "multiplas_correspondencias" else ""),
        "classificacao": classificacao,
        "motivo": motivo,
        "tempo_busca_ms": execucao["tempo_busca_ms"],
        "tempo_consulta_ms": execucao["tempo_consulta_ms"],
    }


def media(valores):
    """Média simples; devolve 0 para lista vazia (evita divisão por zero)."""
    if len(valores) == 0:
        return 0
    return sum(valores) / len(valores)


def percentual(parte, total):
    if total == 0:
        return 0
    return parte / total * 100


def calcular_indicadores(linhas):
    """linhas = lista de dicionários (um por teste) já classificados."""
    total = len(linhas)
    diretos = 0
    via_menu = 0
    erros = 0
    for linha in linhas:
        if linha["classificacao"] == "direto":
            diretos += 1
        elif linha["classificacao"] == "menu":
            via_menu += 1
        else:
            erros += 1
    acertos = diretos + via_menu

    # Taxa por tipo de pergunta, na ordem em que os tipos aparecem no arquivo.
    por_tipo = {}
    for linha in linhas:
        tipo = linha["tipo"]
        if tipo not in por_tipo:
            por_tipo[tipo] = {"total": 0, "acertos": 0}
        por_tipo[tipo]["total"] += 1
        if linha["classificacao"] != "erro":
            por_tipo[tipo]["acertos"] += 1
    for tipo in por_tipo:
        dados = por_tipo[tipo]
        dados["taxa"] = percentual(dados["acertos"], dados["total"])

    tempos_busca = [linha["tempo_busca_ms"] for linha in linhas]
    tempos_consulta = [linha["tempo_consulta_ms"] for linha in linhas]

    # Tamanho do menu: só nos testes em que um menu apareceu.
    menus = [linha["tamanho_menu"] for linha in linhas if linha["tamanho_menu"] != ""]

    return {
        "total": total,
        "acertos": acertos,
        "diretos": diretos,
        "via_menu": via_menu,
        "erros": erros,
        "taxa_acerto": percentual(acertos, total),
        "por_tipo": por_tipo,
        "tempo_consulta_medio": media(tempos_consulta),
        "tempo_consulta_maximo": max(tempos_consulta, default=0),
        "tempo_busca_medio": media(tempos_busca),
        "tempo_busca_maximo": max(tempos_busca, default=0),
        "quantidade_menus": len(menus),
        "tamanho_medio_menu": media(menus),
    }


def salvar_csv(linhas, caminho=CAMINHO_CSV):
    """Grava o registro dos resultados. Devolve "" ou a mensagem de erro."""
    try:
        # newline="" evita linhas em branco extras no Windows;
        # utf-8-sig faz o Excel mostrar os acentos corretamente.
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS_CSV, delimiter=";")
            escritor.writeheader()
            for linha in linhas:
                copia = dict(linha)
                # Vírgula decimal, combinando com o separador ";" do Excel brasileiro.
                copia["tempo_busca_ms"] = br(linha["tempo_busca_ms"], 4)
                copia["tempo_consulta_ms"] = br(linha["tempo_consulta_ms"], 4)
                escritor.writerow(copia)
    except OSError as falha:
        return f"Não foi possível salvar o CSV em {caminho}: {falha}"
    return ""


def br(numero, casas=1):
    """Formata número no padrão brasileiro: 83.3 -> "83,3"."""
    return f"{numero:.{casas}f}".replace(".", ",")


def mostrar_relatorio(linhas, indicadores):
    print("=" * 78)
    print("CITIZEN ASSIST AI — RESULTADOS DOS TESTES")
    print("=" * 78)
    print(f"{'Teste':<6} {'Tipo':<17} {'Resultado':<10} {'Tempo (ms)':>10}  Motivo")
    print("-" * 78)
    for linha in linhas:
        print(f"{linha['id_teste']:<6} {linha['tipo']:<17} {linha['classificacao']:<10} "
              f"{br(linha['tempo_consulta_ms'], 3):>10}  {linha['motivo']}")
    print("-" * 78)

    ind = indicadores
    print()
    print(f"Taxa de acerto: {ind['acertos']} acertos em {ind['total']} testes "
          f"({br(ind['taxa_acerto'])}%): {ind['diretos']} diretos e "
          f"{ind['via_menu']} via menu. Erros: {ind['erros']}.")
    print()
    print("Acerto por tipo de pergunta:")
    for tipo, dados in ind["por_tipo"].items():
        print(f"  - {tipo:<17} {dados['acertos']}/{dados['total']} ({br(dados['taxa'])}%)")
    print()
    print(f"Tempo de consulta (busca + resposta): média {br(ind['tempo_consulta_medio'], 3)} ms, "
          f"máximo {br(ind['tempo_consulta_maximo'], 3)} ms")
    print(f"Tempo de busca (só Parte B):          média {br(ind['tempo_busca_medio'], 3)} ms, "
          f"máximo {br(ind['tempo_busca_maximo'], 3)} ms")
    if ind["quantidade_menus"] > 0:
        print(f"Menus exibidos: {ind['quantidade_menus']}, "
              f"com {br(ind['tamanho_medio_menu'])} opções em média")
    else:
        print("Menus exibidos: nenhum")


if __name__ == "__main__":
    # 1) Base de conhecimento (Parte A).
    registros, erro = carregar_base()
    if erro != "":
        print("[ERRO] " + erro)
        sys.exit(1)
    validos, problemas = validar_registros(registros)
    if len(problemas) > 0:
        print(f"[ATENÇÃO] {len(problemas)} problema(s) na base; registros com problema foram ignorados.")
    if len(validos) == 0:
        print("[ERRO] Nenhum registro válido na base: não há como testar.")
        sys.exit(1)

    # 2) Perguntas de teste.
    perguntas, erro = carregar_perguntas()
    if erro != "":
        print("[ERRO] " + erro)
        sys.exit(1)

    # 3) Executar e classificar cada pergunta.
    linhas = []
    for teste in perguntas:
        execucao = executar_teste(validos, teste)
        classificacao, motivo = classificar(teste, execucao)
        linhas.append(montar_linha(teste, execucao, classificacao, motivo))

    # 4) Indicadores, registro em CSV e relatório na tela.
    indicadores = calcular_indicadores(linhas)
    erro = salvar_csv(linhas)
    mostrar_relatorio(linhas, indicadores)
    print()
    if erro != "":
        print("[ERRO] " + erro)
    else:
        print(f"Registro salvo em: {CAMINHO_CSV}")