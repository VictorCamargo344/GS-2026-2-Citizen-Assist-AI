# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="assets/logo-fiap.png"
       alt="FIAP - Faculdade de Informática e Administração Paulista"
       width="40%">
</a>
</p>

<br>

# Citizen Assist AI — Assistente de Orientação Cidadã

Global Solution 2026.2 · Desafio CitizenTech

## Nome do grupo

ABCidadão

## 👨‍🎓 Integrantes

| Integrante | RM | Frente |
| --- | --- | --- |
| Mayara Luisa Vicente Rosa | 571955 | A — Base de conhecimento e leitura de arquivos |
| Gabriel Luís de Lima Ramos | 568984 | B — Consulta, navegação e algoritmos |
| Pietra Fanticelli | 573229 | C — Lógica de resposta e estratégias de prompts |
| Eduardo Lopes da Silveira Mota | 563418 | D — Interação e tratamento de erros |
| Victor de Camargo Gomes | 568912 | E — Testes e indicadores de desempenho |

## 👩‍🏫 Professores

### Tutor(a)
- André Tritiack de Farias

### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

---

## 📜 Descrição

### O problema

Quem procura orientações sobre documentos, serviços públicos e direitos costuma encontrar informações espalhadas em muitos sites, com termos difíceis e instruções incompletas. Isso torna a busca lenta e aumenta o risco de interpretar algo errado.

### A solução

O **Citizen Assist AI** é um assistente em modo texto que organiza orientações conferidas em fontes oficiais e responde a dúvidas simples do dia a dia. A pessoa escolhe um tema no menu ou escreve uma pergunta; o assistente encontra a orientação na base, responde em linguagem simples, **mostra a fonte e a data em que ela foi conferida** e **avisa quando não tem informação suficiente**, em vez de inventar uma resposta.

O assistente **não é um canal oficial** de nenhum órgão público, não faz atendimento e não pede dados pessoais.

### Público beneficiado

Cidadãos que precisam de orientação confiável e acessível, principalmente pessoas com pouca familiaridade com termos burocráticos, que têm dificuldade de encontrar o caminho certo entre sites de governo ou que precisam de uma explicação mais simples antes de procurar o órgão responsável.

### Temas abordados

| Tema | Assuntos |
| --- | --- |
| **Documentos** | Carteira de Identidade Nacional (CIN), CPF, título de eleitor, segunda via da certidão de nascimento, Carteira de Trabalho Digital |
| **Serviços** | Canais do INSS, Cadastro Único, Cartão do SUS, seguro-desemprego, conta gov.br |
| **Orientações comunitárias** | Alertas da Defesa Civil por SMS, telefones de emergência, Disque 100, Ligue 180, reclamações de consumidor |

### Fluxo de uma consulta

```text
Pessoa escolhe um tema ou digita uma pergunta
        │
        ▼
Validação da entrada ──── vazia / inválida ───► pede uma pergunta e mostra os temas
        │
        ▼
Busca na base (palavras-chave)
        │
        ├── nenhuma correspondência ──► aviso de limitação + sugestão de outros temas
        ├── várias correspondências ──► menu de opções (o assistente não escolhe sozinho)
        └── uma correspondência
                │
                ▼
        Orientação + fonte + data de verificação + aviso para confirmar
        + aviso de que não é canal oficial + sugestões de assuntos relacionados
```

---

## 📁 Estrutura de pastas

```text
├── README.md
├── assets/
│   └── logo-fiap.png
├── data/
│   ├── base_conhecimento.json   # 15 orientações em 3 temas, com fonte e data
│   └── perguntas_teste.json     # 42 perguntas de teste com gabarito
├── docs/
│   ├── busca_navegacao.md       # estratégia de busca, hierarquia e navegação
│   ├── integracao.md            # o que cada função da busca recebe e devolve
│   ├── modelos_prompt.md        # os 2 modelos de resposta e a comparação entre eles
│   ├── resultados_testes.md     # critérios, resultados e interpretação dos testes
│   ├── resultados_testes.csv    # registro de cada teste (gerado pelo script)
│   ├── teste_usabilidade.md     # roteiro do teste de facilidade de uso
│   └── uso_ia.md                # uso de IA e validação crítica de cada frente
├── src/
│   ├── sistema.py               # ponto de entrada e interface em texto
│   ├── base.py                  # leitura e validação da base
│   ├── busca.py                 # busca, hierarquia e navegação
│   ├── resposta.py              # modelos de resposta e avisos de limitação
│   └── testes.py                # avaliação com as perguntas de teste
└── tests/
    ├── test_busca.py            # testes automatizados da busca
    ├── test_sistema.py          # testes automatizados da interface
    └── testes_resposta.py       # testes automatizados das respostas
```

---

## 🗂️ Base de conhecimento

### Organização

A base fica em [`data/base_conhecimento.json`](data/base_conhecimento.json): uma **lista** de registros, em que cada registro é um **dicionário** com exatamente estes campos:

| Campo | Conteúdo | Exemplo |
| --- | --- | --- |
| `id` | Identificador único | `"DOC-03"` |
| `tema` | Tema do registro | `"Documentos"` |
| `palavras_chave` | Lista de palavras e expressões usadas na busca | `["título de eleitor", "tse", "votar"]` |
| `orientacao` | Orientação resumida, em linguagem simples | `"O primeiro título de eleitor pode ser pedido pela internet..."` |
| `referencia` | Dicionário com `nome` e `link` da fonte oficial consultada | `{"nome": "Tribunal Superior Eleitoral (TSE) - ...", "link": "https://www.tse.jus.br/..."}` |
| `data_verificacao` | Data em que a fonte foi conferida (DD/MM/AAAA) | `"18/11/2026"` |

**Origem das orientações:** todas vêm de páginas oficiais (portal gov.br, ministérios, TSE, Anatel e Consumidor.gov.br), citadas no campo `referencia` de cada registro. As orientações foram resumidas sem acrescentar informação que não estivesse na fonte, e as que dependem de regras locais ou que mudam com frequência terminam com uma frase pedindo confirmação na fonte.

**Validação ao carregar** ([`src/base.py`](src/base.py)): o programa trata arquivo ausente, vazio ou com JSON malformado com mensagens claras, sem travar. Cada registro é conferido (campos que faltam ou sobram, tipos, link começando com `http`, data no formato certo, `id` repetido). Registros com problema são deixados de fora e os demais continuam valendo.

**Manutenção:** para acrescentar ou corrigir uma orientação, basta editar o JSON. Os temas, a hierarquia e a navegação são montados a partir dos próprios registros, então nenhuma linha de código precisa mudar. Depois de editar, `python src/base.py` confere se a base continua válida.

### Hierarquia de temas

Os registros são organizados em uma árvore de três níveis: **raiz → tema → assunto**. A árvore é montada automaticamente a partir da base ([`src/busca.py`](src/busca.py), função `construir_hierarquia`):

```text
Orientação cidadã
├── Documentos ............... identidade, cpf, título de eleitor, certidão de nascimento, carteira de trabalho
├── Serviços ................. inss, cadastro único, cartão sus, seguro-desemprego, conta gov.br
└── Orientações comunitárias . defesa civil, emergência, disque 100, ligue 180, consumidor
```

**Navegação entre assuntos:** depois de uma orientação, o assistente sugere primeiro os outros assuntos do **mesmo tema** e depois os de **outros temas**. Por exemplo, depois do título de eleitor (DOC-03), as primeiras sugestões são identidade, CPF, certidão de nascimento e carteira de trabalho. As relações são de organização e exploração: o assistente não afirma que um serviço depende de outro.

### Estratégia de busca

A busca ([`src/busca.py`](src/busca.py), função `buscar_pergunta`) é uma **busca linear com pontuação por palavras-chave**:

1. O texto da pergunta é padronizado: minúsculas, sem acentos, sem pontuação. Palavras sem significado próprio, como "como", "de" e "para", são ignoradas.
2. Cada registro da base é comparado com a pergunta e recebe pontos:
   - **1 ponto** por palavra da pergunta que aparece nas palavras-chave do registro;
   - **2 pontos a mais** por expressão composta (como "carteira de identidade") que aparece inteira e na mesma ordem na pergunta.
3. Os registros com pelo menos 1 ponto são ordenados do maior para o menor. Em caso de empate, a ordem é a alfabética do `id`.

**Quando há várias correspondências**, todas são devolvidas e o assistente mostra um menu com as opções, em ordem de pontuação, para a pessoa escolher. Ele nunca escolhe a primeira opção sozinho. Por exemplo, "Como tirar a carteira de identidade?" dá 4 pontos para a identidade (DOC-01) e 1 ponto para a carteira de trabalho (DOC-05), por causa da palavra "carteira"; a identidade aparece em primeiro lugar.

**Por que essa estratégia:** ela é simples, previsível e explicável, ou seja, sempre dá para mostrar por que um registro foi encontrado. Para uma base pequena, o custo de percorrer todos os registros é desprezível (menos de 1 milissegundo por consulta). A limitação é que ela só reconhece as palavras cadastradas. Por isso, cada registro inclui também termos do dia a dia, como "aposentar" junto com "aposentadoria" (veja a seção de testes).

Detalhes completos em [`docs/busca_navegacao.md`](docs/busca_navegacao.md) e [`docs/integracao.md`](docs/integracao.md).

---

## 💬 Regras de resposta e modelos de prompt

### Regras de resposta

A resposta ([`src/resposta.py`](src/resposta.py)) é montada **somente** com o conteúdo do registro encontrado. Nenhum modelo de IA é chamado durante a execução. As regras, aplicadas com condicionais:

| Situação | O que o assistente faz |
| --- | --- |
| Entrada vazia ou só com pontuação | Pede uma pergunta e mostra os temas disponíveis |
| Uma correspondência | Mostra a orientação, a fonte, o link, a data de verificação, o aviso para confirmar na fonte e o aviso de que não é canal oficial |
| Várias correspondências | Mostra um menu com as opções e pede que a pessoa escolha ou reformule |
| Nenhuma correspondência | Mostra o aviso de limitação e sugere reformular, consultar os temas ou procurar o canal oficial |
| Registro incompleto ou resultado inválido | Mostra o aviso de limitação com o motivo |

### Dois modelos de prompt

Os "modelos" são estratégias documentadas de instrução e formato de resposta, com quatro partes: **papel** do assistente, **formato** da resposta, **regras** (não inventar documentos, prazos, valores ou telefones; informar quando a base não responde; não pedir dados pessoais; não se apresentar como órgão oficial) e **dados da base**, delimitados como conteúdo de referência.

| | Modelo 1 — Direto | Modelo 2 — Guiado |
| --- | --- | --- |
| Papel | Assistente curto, objetivo e respeitoso | Assistente que explica com calma, em linguagem simples |
| Formato | Orientação em um bloco, fonte, data e avisos | Tema, orientação em etapas numeradas, "onde conferir" e "antes de agir" |

**Comparação nas 18 perguntas diretas de teste:** os dois apresentaram 100% dos elementos obrigatórios (fonte, link, data e os dois avisos). O **Modelo 2 é mais claro**: a maior linha da resposta cai de 74,5 para 25,8 palavras em média, cerca de 3 vezes menor, com só 14 palavras a mais por resposta. Por isso ele é o recomendado para o público geral. Comparação completa, com exemplo lado a lado, em [`docs/modelos_prompt.md`](docs/modelos_prompt.md).

### Tratamento das limitações

- O assistente **não responde sem base verificada**: se a busca não encontra nada, ele diz isso claramente e sugere caminhos.
- Toda orientação vem com a **fonte** e a **data de verificação**, e com o aviso de que as informações podem mudar.
- Toda resposta lembra que o assistente **não é canal oficial**.
- Em caso de dúvida entre assuntos, ele **pergunta** em vez de escolher.

---

## 🖥️ Interface e tratamento de erros

O assistente funciona no terminal (`python src/sistema.py`) e é todo conduzido por menus numerados e por perguntas digitadas.

### Menu principal

| Opção | O que faz |
| --- | --- |
| **1. Ver temas e assuntos** | Mostra os 3 temas; ao escolher um tema, lista os seus assuntos; ao escolher um assunto, mostra a orientação |
| **2. Fazer uma pergunta** | Recebe uma dúvida digitada e envia para a busca |
| **3. Trocar o formato da resposta** | Alterna entre os dois modelos de resposta da Parte C (o inicial é o Modelo 2, guiado e passo a passo) |
| **4. Sobre o assistente e seus limites** | Explica de onde vêm as informações, que nada é gravado e que o assistente não é canal oficial |
| **0. Sair** | Encerra o programa |

### Navegação entre assuntos

- Antes de cada orientação, a tela mostra **onde a pessoa está** na hierarquia, por exemplo: `Orientação cidadã > Documentos > título de eleitor`.
- Depois de cada orientação, o assistente oferece **assuntos relacionados**: até 3 do mesmo tema e 1 de cada outro tema. A pessoa pode seguir de assunto em assunto ou voltar ao menu.

### Tratamento de erros e situações-limite

| Situação | O que o assistente faz |
| --- | --- |
| Enter sem digitar nada no menu | Avisa que nada foi digitado e pede o número de novo |
| Texto no lugar de número (ex.: "abc") | Explica que é preciso digitar só o número e mostra a faixa válida |
| Opção inexistente (ex.: 9) | Avisa que a opção não existe e mostra a faixa válida, sem sair do menu |
| Pergunta vazia ou só com pontuação | Pede que a pessoa escreva uma pergunta e mostra os temas disponíveis |
| Pergunta sem resposta na base | Mostra o aviso de limitação, lista todos os assuntos disponíveis e oferece "fazer outra pergunta" ou "ver os temas" |
| Pergunta ambígua | Mostra as opções encontradas para a pessoa escolher, mais a opção **"Nenhuma dessas opções"**, que leva ao aviso de limitação |
| Ctrl+C ou Ctrl+Z | Encerra o programa com uma mensagem de despedida, sem mostrar erro técnico |
| Base ausente ou inválida | O programa não inicia e explica o motivo |

### Privacidade na interface

A tela de pergunta avisa para **não digitar dados pessoais**. Nada do que a pessoa digita é gravado em arquivo.

### Testes da interface

Os 11 testes de `tests/test_sistema.py` simulam o que a pessoa digita e conferem o que aparece na tela, cobrindo as principais situações da tabela acima.

---

## 📊 Testes e indicadores

### Plano de testes

- **42 perguntas de teste** em [`data/perguntas_teste.json`](data/perguntas_teste.json): 18 diretas (todas as 15 orientações cobertas), 16 reformulações (a mesma dúvida escrita com outras palavras), 3 situações-limite (entrada vazia, entrada só com pontuação e pergunta ambígua) e 5 perguntas fora dos temas.
- O **gabarito** (resultado esperado) de cada pergunta foi definido **antes** de executar a busca.
- Cada teste é classificado como **acerto direto**, **acerto via menu** (o registro certo apareceu entre as 3 primeiras opções de um menu) ou **erro**. Oferecer uma orientação para uma pergunta fora da base conta como erro (**falso positivo**).
- O **tempo de consulta** (busca + montagem da resposta) é medido 100 vezes por pergunta, e o valor registrado é a média.
- O script [`src/testes.py`](src/testes.py) executa tudo, mostra o relatório e grava o registro em [`docs/resultados_testes.csv`](docs/resultados_testes.csv).

### Melhoria aplicada a partir dos testes

A primeira avaliação com a base completa mostrou que o assistente **não encontrava nenhuma reformulação** (0 de 5): a busca compara palavras exatas, então "aposentar" não encontrava "aposentadoria". A melhoria aplicada foi **acrescentar às palavras-chave termos do dia a dia** (63 no total, como "aposentar", "mandado embora", "médico", "chuva", "defeito"), sem mudar o código.

Para não "decorar" o teste, foram escritas **11 reformulações novas antes de alterar a base**. Como na separação entre dados de treino e de validação, elas medem se a melhoria funciona para perguntas que não foram usadas para escolher os sinônimos.

| Indicador | Antes | Depois |
| --- | --- | --- |
| Reformulações antigas (usadas para escolher os sinônimos) | 0/5 | 5/5 |
| **Reformulações novas (validação)** | **0/11** | **9/11 (81,8%)** |
| Diretas, limites e fora do tema | 24/26 | 24/26 (nenhum falso positivo novo) |
| **Taxa geral** | **24/42 (57,1%)** | **38/42 (90,5%)** |

### Resultados finais (18/11/2026)

| Indicador | Resultado |
| --- | --- |
| **Taxa de acerto** | **38 de 42 (90,5%)**: 30 acertos diretos e 8 via menu |
| Perguntas diretas | 18/18 (100%) |
| Reformulações novas (validação) | 9/11 (81,8%) |
| Reformulações antigas | 5/5 (100%) |
| Situações-limite | 3/3 (100%) |
| Fora do tema | 3/5 (60%) |
| Tempo médio de consulta | menos de 0,5 ms (entre 0,30 e 0,43 ms em execuções seguidas) |

### Interpretação

- **Quando a pessoa usa as palavras da base, o assistente acerta sempre** (18/18), e trata corretamente todas as entradas inválidas e a pergunta ambígua.
- **Com o vocabulário ampliado, ele entende a maioria das dúvidas escritas com palavras próprias** (9/11 nas reformulações novas). Os 2 erros mostram o limite da comparação por palavra exata: "empregos" (plural) não encontra nada, e "agride" não encontra "agressão". Eles não foram corrigidos de propósito, para que a taxa de validação continue honesta.
- **O erro mais grave é o falso positivo** (2 casos): uma palavra solta como "carteira" (em "carteira de motorista") ou "conta" (em "conta de luz") basta para o assistente oferecer uma orientação que não responde à pergunta.
- **O custo da melhoria são mais menus** (de 5 para 10): mais perguntas pontuam em dois registros, mas em 7 dos 8 acertos via menu o registro certo veio em primeiro lugar.
- **O tempo não é um problema**: menos de 1 milissegundo por consulta.

Resultados por pergunta, evolução entre as execuções e análise completa em [`docs/resultados_testes.md`](docs/resultados_testes.md).

### Teste de facilidade de uso

O roteiro tem 11 tarefas: encontrar orientações pelo menu e por pergunta, identificar a fonte, navegar entre assuntos, lidar com erros e com perguntas fora da base. Executado pela equipe na interface real, ele teve **11 de 11 tarefas concluídas**, nenhuma com mais de 3 passos. As principais dificuldades observadas foram os nomes de assunto em sigla ("cpf", "inss") e sugestões de outros temas pouco relacionadas. Roteiro, resultados e tabela para aplicar com um participante externo em [`docs/teste_usabilidade.md`](docs/teste_usabilidade.md).

---

## 🔧 Como executar o código

### Pré-requisitos

- **Python 3.10 ou superior** (testado com Python 3.12).
- Nenhuma biblioteca externa: o projeto usa só a biblioteca padrão do Python. Não há API paga, chave de acesso nem conexão com a internet durante a execução.

### Passo a passo

```bash
# 1. Baixar o repositório
git clone https://github.com/VictorCamargo344/GS-2026-2-Citizen-Assist-AI.git
cd GS-2026-2-Citizen-Assist-AI

# 2. Executar o assistente
python src/sistema.py
```

No menu principal, digite o número da opção e pressione Enter:

```text
MENU PRINCIPAL
  1. Ver temas e assuntos
  2. Fazer uma pergunta
  3. Trocar o formato da resposta (atual: Modelo 2 — Didático e passo a passo)
  4. Sobre o assistente e seus limites
  0. Sair
```

- **1 — Ver temas e assuntos:** escolha um tema e depois um assunto. A orientação aparece com o caminho na hierarquia (ex.: `Orientação cidadã > Documentos > título de eleitor`) e, no final, com assuntos relacionados para continuar a consulta.
- **2 — Fazer uma pergunta:** escreva a dúvida com poucas palavras. Se houver mais de um assunto possível, o assistente mostra as opções, incluindo "Nenhuma dessas opções".
- **3 — Trocar o formato:** alterna entre o Modelo 2 (guiado, padrão) e o Modelo 1 (direto).
- **4 — Sobre:** explica o que o assistente faz, seus limites e o cuidado com a privacidade.

Outros comandos:

```bash
# Conferir se a base de conhecimento é válida
python src/base.py

# Rodar a avaliação com as 42 perguntas de teste (gera docs/resultados_testes.csv)
python src/testes.py

# Rodar os testes automatizados da busca, das respostas e da interface (92 testes)
python -m unittest discover -s tests -v
```

---

## 💡 Exemplos de uso

As saídas abaixo foram geradas pelo próprio código (busca da Parte B + resposta da Parte C, no Modelo 2 — guiado).

### Pergunta com resposta na base

**Pergunta:** `Como tirar o título de eleitor?`

```text
Tema: Documentos

O que a base informa:
  1. O primeiro título de eleitor pode ser pedido pela internet, no Autoatendimento Eleitoral (Título Net) do site do Tribunal Superior Eleitoral, na opção "Tire seu primeiro título".
  2. São pedidos um documento oficial com foto e uma foto do rosto segurando o documento.
  3. O pedido gera um protocolo para acompanhamento e, depois de aprovado, o título fica disponível no aplicativo e-Título.
  4. O alistamento pode ser feito a partir dos 15 anos.
  5. Nos meses que antecedem as eleições, o alistamento fica temporariamente fechado: confirme no site do TSE se o serviço está disponível.

Onde conferir:
  Tribunal Superior Eleitoral (TSE) - Autoatendimento Eleitoral (Título Net) (https://www.tse.jus.br/servicos-eleitorais/titulo-eleitoral/autoatendimento-eleitoral)
  Verificado em: 18/11/2026

Antes de agir: As informações podem mudar. Confira prazos e requisitos diretamente na fonte indicada antes de agir.
Este assistente é informativo e não é um canal oficial de nenhum órgão público.
```

### Pergunta ambígua

**Pergunta:** `Preciso do RG para pedir benefício no INSS`

```text
CITIZEN ASSIST AI — PERGUNTA AMBÍGUA
Sua pergunta pode estar relacionada a mais de um assunto.
Escolha um dos temas abaixo ou reformule a consulta:
1. Serviços (ID: SER-01)
2. Documentos (ID: DOC-01)
Assim evitamos apresentar uma orientação que talvez não corresponda ao que você precisa.
```

### Pergunta sem resposta na base

**Pergunta:** `Como renovar o passaporte?`

```text
Consulta: "Como renovar o passaporte?"
CITIZEN ASSIST AI — AVISO DE LIMITAÇÃO
Não encontramos uma orientação verificada suficiente para responder à consulta na base atual.
O que você pode fazer:
- Reformular a pergunta usando palavras mais específicas.
- Consultar os temas disponíveis no menu principal.
- Verificar a informação nos canais oficiais do órgão competente.
Este assistente é informativo e não é um canal oficial de nenhum órgão público.
```

### Entrada vazia

**Pergunta:** _(apenas Enter)_

```text
Você não digitou nenhuma pergunta.
Escreva sua dúvida ou escolha um tema:
- Documentos
- Serviços
- Orientações comunitárias
```

### Opção inexistente, texto no lugar do número e Enter vazio no menu

```text
Escolha uma opção: 9
A opção 9 não existe. Escolha um número de 0 a 4.
Escolha uma opção: abc
"abc" não é uma opção. Digite só o número, de 0 a 4.
Escolha uma opção:
Você não digitou nada. Digite o número de uma das opções.
```

### Continuidade depois de uma resposta

Depois de cada orientação, o assistente sugere assuntos do mesmo tema e de outros temas:

```text
Assuntos relacionados que também posso explicar:
  1. inss (Serviços)
  2. cadastro único (Serviços)
  3. cartão sus (Serviços)
  4. identidade (Documentos)
  5. defesa civil (Orientações comunitárias)
  0. Voltar ao menu principal
```

### Pergunta sem resposta, na interface

Depois do aviso de limitação, a interface mostra todos os assuntos disponíveis e oferece os próximos passos:

```text
Assuntos que posso explicar:
  - Documentos: identidade, cpf, título de eleitor, certidão de nascimento, carteira de trabalho
  - Serviços: inss, cadastro único, cartão sus, seguro-desemprego, conta gov.br
  - Orientações comunitárias: defesa civil, emergência, disque 100, ligue 180, consumidor

O que você quer fazer agora?
  1. Fazer outra pergunta
  2. Ver os temas e escolher um assunto
  0. Voltar ao menu principal
```

---

## 🛡️ Cuidados com clareza, acessibilidade, privacidade e informação não oficial

- **Clareza:** as orientações são resumos curtos em linguagem simples. O Modelo 2 divide cada orientação em etapas numeradas e separa "o que a base informa", "onde conferir" e "antes de agir".
- **Acessibilidade:** as respostas são texto puro, sem depender de cores, imagens ou formatação especial. As mensagens de erro dizem o que aconteceu e o que fazer em seguida.
- **Privacidade:** o assistente **não pede nem guarda dados pessoais**. A base contém só orientações e fontes, e o código não grava as perguntas digitadas. O teste de facilidade de uso também não registra dados dos participantes.
- **Informação não oficial:** toda resposta informa que o assistente **não é canal oficial** de nenhum órgão público. Ele não promete atendimento nem integração com órgãos públicos e sempre indica a fonte oficial para confirmação.
- **Fontes e atualização:** cada orientação traz a fonte e a data em que foi conferida. As orientações que dependem de regras locais ou que mudam com frequência pedem confirmação na fonte antes de agir.
- **Uso de IA:** o protótipo não chama nenhum modelo de IA durante a execução. O uso de IA no desenvolvimento e a validação feita pela equipe estão registrados em [`docs/uso_ia.md`](docs/uso_ia.md).

---

## 📎 Links e Observações

### 🔗 Links do Projeto

* **Vídeo de apresentação (YouTube, não listado):** [pendente: link do vídeo]

### 🧠 Decisões Técnicas

- **Interface em texto (CLI):** atende ao enunciado e funciona em qualquer computador com Python, sem instalar nada.
- **Base em JSON:** representa bem os campos estruturados (incluindo a lista de palavras-chave e a referência com nome e link) e permite editar a base sem mexer no código.
- **Busca por palavras-chave com pontuação**, em vez de IA: resultado previsível, explicável e sem risco de o assistente inventar instruções.
- **Nunca escolher sozinho em caso de ambiguidade:** quando há várias correspondências, a pessoa escolhe. Isso reduz o risco de mostrar uma orientação errada.
- **Código separado por responsabilidade** (`base`, `busca`, `resposta`, `testes`), para facilitar a manutenção e o acréscimo de orientações.

### 📢 Observações Gerais

* **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos participar. **[pendente: decisão da equipe]**

---

## ✅ Conclusões, limitações e melhorias

### Conclusões

O Citizen Assist AI mostra que regras simples de Python (listas, dicionários, leitura de arquivo, condicionais e uma busca linear com pontuação) são suficientes para um assistente que organiza informações verificadas, sempre cita a fonte e admite quando não sabe. Nos testes, ele acertou todas as perguntas escritas com o vocabulário da base e tratou corretamente todas as entradas inválidas e ambíguas. A própria avaliação apontou o principal ponto fraco, as perguntas escritas com outras palavras, e orientou uma melhoria que elevou a taxa de acerto de 57,1% para 90,5%, medida com perguntas novas que não foram usadas para escolher a correção.

### Limitações

- **Só reconhece as palavras cadastradas:** sinônimos e variações (plural, verbo conjugado) que não estejam nas palavras-chave não são encontrados, como mostraram as reformulações T35 e T40.
- **Falsos positivos por palavra solta:** uma única palavra em comum pode fazer o assistente oferecer uma orientação que não responde à pergunta.
- **Base pequena e que envelhece:** 15 orientações, que precisam ser reconferidas periodicamente nas fontes oficiais.
- **Avaliação limitada:** as perguntas de teste foram escritas pela equipe, e o roteiro de facilidade de uso foi executado pela própria equipe, ainda sem um participante externo.

### Possibilidades de melhoria

1. **Continuar ampliando as palavras-chave** com termos do dia a dia, como já foi feito, sempre validando com perguntas novas.
2. **Comparar palavras pelo radical**, para que "empregos" encontre "emprego" e "agride" encontre "agressão" sem cadastrar cada variação.
3. **Exigir uma correspondência mais forte** antes de responder, perguntando "Você quis dizer...?" quando a única coincidência for uma palavra solta.
4. **Testar com pessoas do público do projeto**, usando as dúvidas escritas por elas como novas perguntas de teste.
5. **Nomes de assunto mais claros na interface** (por exemplo, "INSS — canais de atendimento" em vez de "inss") e sugestões de outros temas escolhidas pela relação com o assunto lido.
6. **Criar uma rotina de revisão das fontes**, usando o campo `data_verificacao` para identificar orientações que precisam ser conferidas de novo.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
