# Parte B — Consulta, navegação e algoritmos

## 1. Responsabilidade e fluxo

A parte B é o mecanismo que encontra registros e oferece caminhos de consulta.
Recebe uma **lista de registros já validados** por A. Entrega dados às partes
C e D, que decidirão como explicar e apresentar a orientação.

```text
A: carregar JSON e validar
             |
             v
B: consultar / organizar temas / sugerir continuidade
             |
             v
C: apresentar orientação, referência e limites
D: receber escolhas, mostrar alternativas e conduzir o fluxo
E: avaliar o sistema integrado
```

As funções de B não solicitam `input`, não imprimem resultados e não leem a
base durante consultas ou importação. Não fazem inferências sobre direitos,
requisitos de serviços ou situações pessoais.

## 2. Atendimento aos requisitos de B

| Requisito | Implementação | Verificação |
| --- | --- | --- |
| Listas e dicionários; acesso por ID, tema e palavras-chave | `consultar_por_id`, `consultar_por_tema`, `consultar_por_palavra_chave` reaproveitam A | Testes de acessos, entradas e preservação |
| Busca por pergunta ou seleção de assunto | `buscar_pergunta`; seleção de tema e de ID é explícita | Perguntas completas, filtros e consultas aos registros reais |
| Hierarquia de temas e subtemas | `construir_hierarquia`: raiz → temas → assuntos; `localizar_na_hierarquia` recupera caminho | Testes de agrupamento e localização |
| Continuidade entre pelo menos três assuntos | `sugerir_continuidade` oferece assuntos irmãos e outros temas da mesma raiz | Percurso DOC-01 → SER-01 → COM-01 → DOC-01 |
| Estratégia e várias correspondências explicadas | Busca linear, regra de pontos e retorno de todas as opções positivas | Testes de pontuação, empates e múltiplos resultados |
| Manutenção e novos registros | Organização derivada dos registros recebidos; sem IDs de conteúdo fixos no algoritmo | Inclusão fictícia de registro e tema |

Os assuntos funcionam como o nível de subtema da árvore: são identificados
pelo ID e rotulados pela primeira palavra-chave do registro. Não é necessário
alterar o formato validado por A para representar esse nível.

## 3. Estruturas de dados

Uma **lista** guarda registros, resultados ordenados, temas, assuntos e termos
sem repetição. Um **dicionário** associa nomes aos dados, como `estado`,
`registro`, `pontuacao`, `tema` e `referencia`.

Cada resultado envolve o registro em outro dicionário. A pontuação pertence a
esse envoltório, não ao registro original. Assim, o validador de A continua
aceitando os mesmos seis campos, e C recebe a orientação e a fonte completas.

As folhas da hierarquia e os resultados mantêm referências aos dicionários de
A. B não os altera. Quem consumir esses retornos também deve tratá-los como
dados de leitura; não são cópias independentes dos registros.

## 4. Modalidades explícitas

- **ID:** comparação exata por A, ignorando caixa, acentos e espaços nas pontas.
  `doc-01` encontra `DOC-01`; não é necessário remover o hífen do ID.
- **Tema:** igualdade do tema normalizado por A, com a ordem da base preservada.
- **Palavra-chave exata:** regra original de A. `previdencia` encontra
  `previdência`; `meu inss` encontra essa expressão inteira. Uma pergunta longa
  não é uma palavra-chave exata. Pontuação e espaços internos continuam
  significativos nessa modalidade, para preservar o contrato existente.
- **Pergunta livre:** tokenização, palavras úteis, expressões e pontos,
  conforme a próxima seção.

D deve encaminhar a escolha do usuário à função correspondente. B não tenta
adivinhar se um texto digitado é um ID, um nome de tema ou uma pergunta.

## 5. Busca linear e pontuação

### Preparação do texto

1. Reaproveitar `normalizar` de A: minúsculas, remoção dos acentos cobertos pelo
   mapa de A e espaços externos.
2. Trocar caracteres não alfanuméricos por espaços. Assim, `Defesa, Civil!`
   pode ser comparada a `defesa civil`.
3. Reduzir espaços repetidos usando `split` e `join`.
4. Separar palavras, retirar as palavras funcionais e eliminar repetições.

O mapa de A contempla os acentos portugueses usuais em sua representação
pré-composta. Não há garantia de normalização de toda combinação Unicode.

As 34 palavras ignoradas são:

```text
a ao aos as com como da das de do dos e em eu me meu meus minha minhas
na nas no nos o os ou para por qual quais que se um uma
```

Elas não pontuam isoladamente. Uma pergunta que contenha apenas esses termos
retorna `sem_correspondencia`, enquanto espaços/pontuação sem palavras retornam
`entrada_vazia`. Na modalidade de palavra-chave exata, vale a regra original de A.

### Comparação de cada registro

O programa percorre todos os registros candidatos, um por vez. Se houver um
filtro de tema, os candidatos são primeiro selecionados por A.

Para cada registro:

- Formar um vocabulário de palavras úteis distintas de suas `palavras_chave`.
- Dar **1 ponto por palavra útil distinta da pergunta** presente nesse vocabulário.
- Dar **2 pontos adicionais por expressão composta distinta** de `palavras_chave`
  que apareça inteira e na ordem correta na pergunta normalizada.
- Incluir o registro somente se a pontuação for maior que zero.

Para o bônus, a expressão mantém suas palavras funcionais. `carteira de
identidade` recebe o bônus quando aparece inteira; `carteira identidade`
continua podendo pontuar pelos termos, mas não recebe esse bônus.

```text
pontos = quantidade de termos úteis distintos encontrados
       + 2 × quantidade de expressões compostas distintas encontradas
```

Um termo compartilhado por várias palavras-chave conta uma única vez.
Repetir `rg` ou a expressão `defesa civil` na pergunta não multiplica seus
pontos. Palavras-chave duplicadas também não multiplicam pontos.

Não existe comparação com texto de `orientacao`, nome da fonte ou endereço da
referência. Uma palavra que apareça somente nesses campos não produz resultado.

### Ordenação e ambiguidade

Ordenar por pontuação decrescente. Em empate, ordenar alfabeticamente pelo ID
normalizado por A. Essa ordem é textual: `ID-10` vem antes de `ID-2`.

Todas as correspondências positivas são devolvidas. Se houver duas, o estado
será `multiplas_correspondencias`, mesmo se a primeira tiver mais pontos. A
interface pode apresentar as opções e pedir uma escolha; B não decide pelo usuário.

Pontuação **não é probabilidade nem comprovação de resposta correta**. Mesmo
`uma_correspondencia` significa apenas que um registro correspondeu aos termos.

### Custo e escolha do algoritmo

A busca é linear em relação à passagem pelos registros: todos os candidatos
são examinados. O trabalho também depende do tamanho da pergunta e das
palavras-chave; listas com verificações `in` não são um índice de busca.
A ordenação acrescenta o custo de ordenar os resultados encontrados.

Essa estratégia é apropriada para uma base pequena e permite explicar cada
correspondência. Não se afirma que o custo total é apenas O(N) para textos de
tamanho arbitrário. Uma base muito maior poderia exigir índices e outra
estratégia, fora desta entrega introdutória.

## 6. Hierarquia e relações de navegação

A árvore derivada da base atual (15 registros) é:

```text
Orientação cidadã
  Documentos
    identidade                [DOC-01]
    cpf                       [DOC-02]
    título de eleitor         [DOC-03]
    certidão de nascimento    [DOC-04]
    carteira de trabalho      [DOC-05]
  Serviços
    inss                      [SER-01]
    cadastro único            [SER-02]
    cartão sus                [SER-03]
    seguro-desemprego         [SER-04]
    conta gov.br              [SER-05]
  Orientações comunitárias
    defesa civil              [COM-01]
    emergência                [COM-02]
    disque 100                [COM-03]
    ligue 180                 [COM-04]
    consumidor                [COM-05]
```

Os rótulos dos assuntos são retirados da primeira palavra-chave de cada
registro, não são novos conteúdos cadastrados. A árvore é montada pelo código
a partir da base: acrescentar um registro ou um tema não exige mudar o algoritmo.

As relações são **de organização e exploração**:

1. A raiz reúne os temas cidadãos disponíveis.
2. Cada tema reúne seus assuntos.
3. De um assunto, sugerir primeiro os demais do mesmo tema e depois os de
   outros temas da raiz, preservando a ordem da base dentro de cada grupo.

Cada sugestão informa `mesmo_tema`, `outro_tema` ou `tema_disponivel`, com uma
justificativa. Não se afirma que obter a CIN é exigência para usar o INSS nem
que um desses serviços depende dos alertas da Defesa Civil.

Com 5 assuntos por tema, a partir de qualquer assunto o sistema sugere primeiro
os outros 4 do mesmo tema e depois os 10 dos outros temas. Por exemplo, de
DOC-01 (identidade) as primeiras sugestões são CPF, título de eleitor, certidão
de nascimento e carteira de trabalho. O percurso entre três assuntos de temas
diferentes (DOC-01 → SER-01 → COM-01 → DOC-01) é verificado pelos testes.

Não há tabela de vínculos manuais, portanto não são criados destinos para IDs
que não estejam na lista válida. Um ID de origem inexistente é sinalizado;
sem ID, a função oferece todos os assuntos como alternativas gerais. Não
recomenda a própria origem.

## 7. Exemplos verificados com a base real

| Pergunta | Resultado esperado e obtido | Pontos |
| --- | --- | --- |
| Como tirar a carteira de identidade? | DOC-01 e DOC-05; múltiplas correspondências, DOC-01 em primeiro | 4 e 1 |
| Como consultar o Meu INSS? | SER-01 | 3 |
| Como receber alertas da Defesa Civil por SMS? | COM-01 | 6 |
| identidade e inss | DOC-01 e SER-01; múltiplas correspondências | 1 e 1 |
| Como preparar bolo de chocolate? | Sem correspondência | — |
| Preciso consultar meu CPF | DOC-02 | 1 |

No primeiro exemplo, a palavra "carteira" também está em "carteira de
trabalho" (DOC-05). Por isso o DOC-05 aparece como segunda opção, com 1 ponto,
enquanto o DOC-01 soma 4 pontos (2 palavras + 2 de bônus pela expressão
inteira). O usuário vê as duas opções, com a mais provável em primeiro lugar.

A avaliação completa, com 42 perguntas de teste, está em
`docs/resultados_testes.md`.

Esses exemplos também estão nos testes de integração de `tests/test_busca.py`.

## 8. Limitações e explicação para apresentação

O algoritmo não interpreta intenção, negação, contexto ou equivalência de
sinônimos. Uma pergunta com uma palavra conhecida pode obter um registro
mesmo se pedir algo que sua orientação não cobre. Singular e plural só têm
correspondência exata quando seus termos estiverem cadastrados. Não há
correção automática de erros de digitação.

As partes C/D precisam explicar o alcance da orientação, citar a referência e
não transformar uma coincidência de palavras em uma conclusão. E deve avaliar
o sistema completo com perguntas variadas. O grupo deve revisar as
palavras-chave e ampliar a base para atender aos 15 registros.

Uma forma de explicar oralmente:

> A parte A me entrega registros válidos. Minha parte limpa o texto da pergunta,
> compara palavras inteiras com as palavras-chave e soma pontos para ordenar
> as opções. Eu devolvo todas as correspondências, porque a maior pontuação
> não garante que a pergunta foi entendida. Também organizo os temas em uma
> árvore e ofereço caminhos para continuar. Os textos e fontes ficam intactos
> para a parte que apresenta a resposta.

Para estudar o código, leia nesta ordem: `consultar_por_id`,
`consultar_por_tema`, `buscar_pergunta`, `_pontuar`, `construir_hierarquia` e
`sugerir_continuidade`. As funções com `_` são auxiliares internas. Entender
listas, laços e dicionários permite acompanhar o núcleo; a infraestrutura de
testes usa recursos adicionais da biblioteca padrão para isolar os arquivos.
