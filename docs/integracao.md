# Guia de integração — Parte B

Este guia descreve o que cada função da Parte B recebe e devolve. Ele serve
para quem chama a busca: a resposta (Parte C), a interface (Parte D) e a
avaliação (Parte E).

## 1. Onde ficam os arquivos

```text
src/
  base.py                 [Parte A: leitura e validação da base]
  busca.py                [Parte B: consulta, hierarquia e navegação]
  resposta.py             [Parte C: formatação da resposta e avisos]
  testes.py               [Parte E: avaliação com as perguntas de teste]
  sistema.py              [Parte D: ponto de entrada e interface]
data/
  base_conhecimento.json  [Parte A]
tests/
  test_busca.py           [testes automatizados da Parte B]
```

A Parte A calcula o caminho do JSON a partir do próprio arquivo, por isso o
JSON fica em `data/` e os módulos em `src/`.

Os imports de B usam `from base import ...`, seguindo a convenção de execução
`python src/sistema.py`. Ao executar um arquivo de `src/`, o Python encontra os
módulos vizinhos na mesma pasta. B não é um pacote independente e não precisa
de `pip install`.

## 2. Contrato recebido de A

O código real recebido usa:

```python
registros, erro = carregar_base()           # lista, texto; erro == "" no sucesso
validos, problemas = validar_registros(registros)  # lista, lista de mensagens
```

Cada item de `validos` contém:

| Campo | Tipo recebido |
| --- | --- |
| `id` | str, único segundo a validação de A |
| `tema` | str |
| `palavras_chave` | list de str, não vazia |
| `orientacao` | str |
| `referencia` | dict com `nome` e `link` |
| `data_verificacao` | str no formato DD/MM/AAAA |

B espera essa lista já validada. Não tente passar o par `(registros, erro)` ou
a lista de mensagens em seu lugar. O tratamento de problemas de arquivo e de
registros inválidos pertence a A e à interface.

B reaproveita `buscar_por_id`, `filtrar_por_tema`, `buscar_por_palavra_chave`,
`listar_temas` e `normalizar`. Não redistribui nem duplica essas implementações.

O validador de A rejeita campos além dos seis combinados. Por isso, os resultados
e a hierarquia de B envolvem os registros em novos dicionários, sem adicionar
campos ao JSON.

## 3. Funções públicas

Todas recebem argumentos explícitos e não fazem interação de tela.

| Função | Entrada | Retorno |
| --- | --- | --- |
| `consultar_por_id(registros, identificador)` | Lista válida e ID str | Resultado de consulta; um item ou nenhum |
| `consultar_por_tema(registros, tema)` | Lista válida e tema str obrigatório | Resultado; registros do tema na ordem da base |
| `consultar_por_palavra_chave(registros, palavra_chave, tema=None)` | Lista válida, palavra/expressão exata str e tema opcional | Resultado; correspondências exatas de A na ordem da base |
| `buscar_pergunta(registros, pergunta, tema=None)` | Lista válida, pergunta str e tema opcional | Resultado; todos os registros com pontos positivos, ordenados |
| `construir_hierarquia(registros)` | Lista válida | Dicionário com raiz, temas e assuntos |
| `localizar_na_hierarquia(hierarquia, identificador)` | Árvore produzida pela função anterior e ID | Dicionário com `caminho` e `registro`, ou None |
| `sugerir_continuidade(registros, identificador=None)` | Lista válida e ID de origem opcional | Resultado com opções e relações de navegação |

Para apenas listar os nomes dos temas, continue usando `listar_temas(validos)`
da própria A, ou os grupos da hierarquia de B.

### Resultado comum às consultas

As quatro funções de consulta devolvem este formato:

```python
{
    "estado": "uma_correspondencia",
    "resultados": [
        {
            "registro": registro_original,
            "pontuacao": 4,
            "termos_encontrados": ["carteira", "identidade"],
            "expressoes_encontradas": ["carteira de identidade"],
        }
    ],
}
```

`registro_original` representa o dicionário completo recebido de A. O exemplo
mostra o retorno da pergunta sobre carteira de identidade. Para consultas por
ID, tema ou palavra-chave exata, `pontuacao` é None e as duas listas de termos
ficam vazias, pois não há classificação por pontuação nessas modalidades.

Os retornos mantêm referências aos registros originais. B não os altera; C/D
também devem evitar modificá-los. Alterar o envoltório de um resultado não
altera os seis campos do registro, mas editar `item["registro"]` altera o dado
compartilhado.

### Estados das consultas

| Estado | Significado | Encaminhamento possível por D/C |
| --- | --- | --- |
| `entrada_invalida` | Consulta/filtro obrigatório não é str | Solicitar texto; não converter None ou número em pergunta |
| `entrada_vazia` | Texto sem caracteres alfanuméricos | Pedir uma pergunta, ID ou tema válido |
| `id_inexistente` | ID exato ausente | Oferecer temas; não inventar um registro |
| `tema_inexistente` | Tema exato ausente | Apresentar `listar_temas(validos)` |
| `sem_correspondencia` | Nenhum resultado; inclui pergunta só com palavras funcionais | Informar o limite e oferecer exploração de temas |
| `uma_correspondencia` | Um registro encontrado | C pode apresentar o conteúdo, com sua fonte e limites |
| `multiplas_correspondencias` | Mais de um registro encontrado | D apresenta alternativas e pede escolha |

Estados de erro ou sem correspondência têm `resultados: []`. Uma única
correspondência não confirma que a orientação resolve toda a pergunta.

Na consulta por tema, `multiplas_correspondencias` é simplesmente uma listagem
de assuntos daquele tema. Na pergunta livre, indica várias correspondências
lexicais. A interface conhece a modalidade que chamou.

Nos filtros opcionais, `tema=None` significa não restringir a busca. Tema
vazio gera `entrada_vazia`; tema de tipo errado gera `entrada_invalida`; nome
não encontrado gera `tema_inexistente`. A entrada principal é verificada antes
do filtro. Na função `consultar_por_tema`, None é inválido, pois o tema é obrigatório.

## 4. Exemplo mínimo: A → B → dados para C/D

Este trecho pode ser incorporado ao futuro ponto de entrada em `src/`. Ele
exemplifica chamadas; não é um menu final nem implementação da frente C.

```python
from base import carregar_base, validar_registros, listar_temas
from busca import buscar_pergunta, consultar_por_id, sugerir_continuidade

registros, erro = carregar_base()
if erro:
    raise SystemExit(erro)

validos, problemas = validar_registros(registros)
if problemas:
    # Exemplo conservador: revisar a base antes de prosseguir.
    # A interface final do grupo pode mostrar os problemas e usar os válidos.
    raise SystemExit("\n".join(problemas))

temas = listar_temas(validos)
resultado = buscar_pergunta(validos, "Como tirar a carteira de identidade?")

if resultado["estado"] == "uma_correspondencia":
    registro = resultado["resultados"][0]["registro"]
    orientacao = registro["orientacao"]
    nome_fonte = registro["referencia"]["nome"]
    link_fonte = registro["referencia"]["link"]
    data_verificacao = registro["data_verificacao"]
    proximos = sugerir_continuidade(validos, registro["id"])
elif resultado["estado"] == "multiplas_correspondencias":
    opcoes = resultado["resultados"]
    # D deverá pedir uma escolha. Nenhuma orientação foi escolhida aqui.
else:
    proximos = sugerir_continuidade(validos)
    # C/D deverão informar o limite e oferecer essas opções gerais.

# Depois de uma seleção explícita por D, por exemplo a opção DOC-01:
selecionado = consultar_por_id(validos, "DOC-01")
```

Os nomes `orientacao`, `nome_fonte` etc. só existem no ramo correspondente.
O exemplo não exibe respostas nem decide qual modelo C deve usar.

### Encaminhar modalidades e filtros

```python
from busca import consultar_por_tema, consultar_por_palavra_chave, buscar_pergunta

assuntos = consultar_por_tema(validos, "Serviços")
exata = consultar_por_palavra_chave(validos, "meu inss")
filtrada = buscar_pergunta(validos, "identidade e inss", tema="Serviços")
# filtrada contém apenas SER-01 na base atual.
```

Somente `buscar_pergunta` trata pontuação e espaços internos como separadores.
Use-a para perguntas. A modalidade de palavra-chave exata preserva a regra de
A: `meu  inss` ou `meu,inss` não são a palavra-chave exata `meu inss`.

## 5. Hierarquia e continuidade

```python
from busca import construir_hierarquia, localizar_na_hierarquia

arvore = construir_hierarquia(validos)
local = localizar_na_hierarquia(arvore, "COM-01")
if local is not None:
    caminho = local["caminho"]
    # ["Orientação cidadã", "Orientações comunitárias", "defesa civil"]
    registro_localizado = local["registro"]
```

A árvore tem o formato:

```python
{
    "raiz": "Orientação cidadã",
    "temas": [
        {
            "tema": "Documentos",
            "assuntos": [
                {"id": "DOC-01", "titulo": "identidade", "registro": registro_original}
            ],
        }
    ],
}
```

O fragmento mostra apenas um grupo; a base real gera três. O título de cada
assunto é sua primeira palavra-chave. IDs são as chaves de seleção; títulos
podem se repetir e não substituem os IDs.

`localizar_na_hierarquia` retorna None se o ID não existir ou a entrada não
for texto utilizável. Recebe somente uma árvore produzida por B e não tenta
validar árvores arbitrárias.

`sugerir_continuidade` mantém o formato externo `estado`/`resultados`. Cada
item tem os mesmos quatro campos das consultas e mais:

| Campo | Valores/significado |
| --- | --- |
| `relacao` | `mesmo_tema`, `outro_tema` ou `tema_disponivel` |
| `justificativa` | Texto curto sobre a relação de navegação |

Se houver opções, o estado é `opcoes_disponiveis`; se não, `sem_opcoes`.
ID de origem ausente/inválido usa `id_inexistente`, `entrada_vazia` ou
`entrada_invalida`. `identificador=None` é uma exploração geral, não um erro.
Depois de uma busca sem correspondência, D pode chamar essa forma sem ID.

O próprio registro não é sugerido. Com um único registro, a consulta a partir
dele retorna `sem_opcoes`. Sem registros, a hierarquia tem `temas: []` e a
navegação não possui opções.

## 6. Manutenção e responsabilidades seguintes

Para acrescentar/corrigir orientações, A edita o JSON e valida os mesmos seis
campos. B passa a encontrá-las pelas palavras-chave e inclui automaticamente
seus temas/assuntos. Não adicione campos extras ao registro para guardar a árvore.

Neste módulo, as relações são derivadas do tema e da raiz comum. Não há lista
manual de IDs relacionados para atualizar. Se o grupo decidir criar relações
mais específicas futuramente, mantenha esse mapeamento separado, justifique
cada relação e valide que origem e destino existam.

C precisa citar `referencia`, apresentar `data_verificacao` e os limites da
orientação; B não garante a atualidade das páginas citadas. D precisa validar
as opções de menu, pedir desambiguação e conduzir o fluxo de tela. E pode
aproveitar os estados e os registros retornados, mas deve criar sua avaliação
completa de acerto, tempo e facilidade de uso.

Reexecute os testes após alterar A ou suas palavras-chave:

```text
python -B -m unittest discover -s tests -v
```

A parte de integração dos testes usa os arquivos reais do repositório
(`src/base.py`, `src/busca.py` e `data/base_conhecimento.json`), copiados para
uma pasta temporária. Ela exige o mínimo do enunciado (15 registros em 3 temas)
e alguns resultados conhecidos da base atual; se as palavras-chave mudarem,
atualize essas expectativas junto com o grupo.
