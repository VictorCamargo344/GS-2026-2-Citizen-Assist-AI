# Resultados dos Testes — Citizen Assist AI

## 1. Conjunto de testes

As perguntas de teste ficam em [`data/perguntas_teste.json`](../data/perguntas_teste.json). Cada pergunta tem um gabarito, definido **antes** de executar a busca:

| Campo | Significado |
|---|---|
| `id_teste` | Identificador da pergunta de teste (ex.: `T01`) |
| `tipo` | `direta`, `reformulacao`, `limite` ou `fora_do_tema` |
| `pergunta` | Texto enviado ao assistente |
| `resultado_esperado` | Estado esperado da busca (mesmos nomes usados em `src/busca.py`) |
| `id_esperado` | Registro da base que deveria ser encontrado (`null` quando nenhum deveria) |
| `observacao` | Motivo do gabarito |

Os estados possíveis da busca são: `uma_correspondencia`, `multiplas_correspondencias`, `sem_correspondencia` e `entrada_vazia`.

São **42 perguntas**:

| Tipo | Quantidade | O que testa |
|---|---|---|
| `direta` | 18 | Pergunta com as palavras da base (pelo menos uma para cada um dos 15 registros) |
| `reformulacao` | 5 | A mesma dúvida de uma pergunta direta, escrita com outras palavras (T07, T08, T09, T28, T29) |
| `reformulacao_nova` | 11 | Reformulações escritas **antes** da ampliação do vocabulário da base, para conferir se a melhoria vale para perguntas que não foram usadas para escolhê-la (T32 a T42) |
| `limite` | 3 | Entrada vazia, entrada só com pontuação e pergunta ambígua |
| `fora_do_tema` | 5 | Assuntos que a base não cobre, incluindo 2 que compartilham palavras com ela |

## 2. Critérios de correção

Cada teste é classificado como **acerto direto**, **acerto via menu** ou **erro**.

### 2.1 Perguntas com resposta na base (`resultado_esperado = uma_correspondencia`)

| Resultado obtido | Classificação |
|---|---|
| Um único registro, e ele é o `id_esperado` | ✅ Acerto direto |
| Várias opções, com o `id_esperado` entre as **3 primeiras** | ✅ Acerto via menu |
| Várias opções, com o `id_esperado` fora das 3 primeiras ou ausente | ❌ Erro |
| Um único registro diferente do `id_esperado` | ❌ Erro |
| Nenhum registro encontrado | ❌ Erro |

**Por que aceitar o menu:** quando há várias correspondências, o assistente não escolhe sozinho. Ele mostra as opções e a pessoa escolhe a certa. Se a orientação correta está entre as primeiras opções, o assistente levou a pessoa até ela.

**Por que limitar às 3 primeiras:** a busca devolve todos os registros com pelo menos um termo em comum com a pergunta, ordenados por pontuação. Sem esse limite, um menu longo e pouco útil contaria como acerto e inflaria a taxa. Para deixar esse efeito visível, o relatório também mostra o **tamanho médio dos menus**.

> Observação: nessas perguntas o gabarito diz `uma_correspondencia`, mas a correção também aceita `multiplas_correspondencias` com o registro esperado no top 3. Os dois casos são contados separadamente, então isso não contradiz o gabarito.

### 2.2 Perguntas ambíguas (`resultado_esperado = multiplas_correspondencias`)

| Resultado obtido | Classificação |
|---|---|
| Várias opções (menu de ambiguidade) | ✅ Acerto direto |
| Um único registro | ❌ Erro: o sistema escolheu sozinho uma interpretação |
| Nenhum registro | ❌ Erro |

Aqui o menu conta como **acerto direto**, porque mostrar as opções é exatamente o comportamento esperado. A categoria "via menu" fica reservada para quando a pessoa precisou de um passo a mais para chegar a uma resposta que deveria ter vindo direto (seção 2.1).

### 2.3 Perguntas sem resposta na base (`resultado_esperado = sem_correspondencia`)

| Resultado obtido | Classificação |
|---|---|
| Estado `sem_correspondencia` **e** o texto gerado pela Parte C contém o aviso de limitação | ✅ Acerto direto |
| Estado `sem_correspondencia`, mas sem o aviso de limitação no texto | ❌ Erro |
| Qualquer registro, único ou em menu | ❌ Erro: **falso positivo** (o assistente oferece uma orientação que não responde à pergunta) |

O falso positivo é o erro mais grave para um assistente cidadão, porque pode levar a pessoa a seguir uma orientação que não serve para o caso dela.

**O que o teste verifica:** o script passa o resultado de `buscar_pergunta` (Parte B) para `responder_resultado_busca` (Parte C) e confere se o texto final contém o título `AVISO DE LIMITAÇÃO`. A **sugestão de outros temas** depende da interface (Parte D) e não é medida aqui. Ela é verificada no teste de facilidade de uso (seção 5).

### 2.4 Entradas inválidas (`resultado_esperado = entrada_vazia`)

| Resultado obtido | Classificação |
|---|---|
| Estado `entrada_vazia` **e** o texto gerado pela Parte C pede que a pessoa digite uma pergunta | ✅ Acerto direto |
| Qualquer outro estado | ❌ Erro |

### 2.5 Como a taxa de acerto é apresentada

```
taxa de acerto = (acertos diretos + acertos via menu) / total de testes × 100
```

O relatório sempre mostra a divisão, por exemplo: *"12 acertos em 15 testes (80,0%): 9 diretos e 3 via menu"*. Também apresenta a taxa por `tipo` de pergunta, para mostrar onde o assistente vai bem (perguntas diretas) e onde tem dificuldade (reformulações).

### 2.6 Tempo de consulta

Cada teste registra dois tempos, medidos com `time.perf_counter()` e apresentados em milissegundos:

| Medida | O que inclui | Para que serve |
|---|---|---|
| **Tempo de consulta** (indicador principal) | `buscar_pergunta` (Parte B) + `responder_resultado_busca` (Parte C) | Representa o que a pessoa espera entre enviar a pergunta e receber a resposta formatada |
| **Tempo de busca** | Somente `buscar_pergunta` (Parte B) | Mostra o custo do algoritmo de busca isoladamente |

Como uma consulta leva frações de milissegundo, uma medição única varia muito por causa de outros processos do computador. Por isso, cada pergunta é executada **uma vez sem medição** (aquecimento, que também fornece o resultado classificado) e depois **repetida 100 vezes**. O tempo registrado para a pergunta é a média dessas 100 execuções.

Para cada medida, o relatório apresenta a média entre as perguntas e o maior tempo médio entre elas. Nenhuma das duas inclui o tempo de digitação, de leitura da resposta ou de exibição na tela (Parte D).

## 3. Resultados

Execução de `python src/testes.py` em 18/11/2026, com a base completa (**15 registros em 3 temas**) e o vocabulário ampliado (seção 3.4). O registro completo, com todas as colunas, está em [`resultados_testes.csv`](resultados_testes.csv).

### 3.1 Resumo

| Indicador | Valor |
|---|---|
| Testes executados | 42 |
| **Taxa de acerto** | **38 acertos em 42 testes (90,5%): 30 diretos e 8 via menu** |
| Erros | 4 |
| Tempo de consulta (busca + resposta) | média 0,426 ms · máximo 0,684 ms |
| Tempo de busca (só Parte B) | média 0,415 ms · máximo 0,665 ms |
| Menus exibidos | 10, com 2,0 opções em média |

### 3.2 Acerto por tipo de pergunta

| Tipo | Acertos | Taxa |
|---|---|---|
| Direta | 18/18 | 100,0% (14 diretos e 4 via menu) |
| Reformulação (usadas para escolher os sinônimos) | 5/5 | 100,0% |
| Reformulação nova (não usadas para escolher os sinônimos) | 9/11 | 81,8% |
| Limite (vazia, pontuação, ambígua) | 3/3 | 100,0% |
| Fora do tema | 3/5 | 60,0% |

### 3.3 Resultado por pergunta

| Teste | Tipo | Pergunta | Esperado | Obtido | Resultado |
|---|---|---|---|---|---|
| T01 | direta | Como tirar a carteira de identidade? | DOC-01 | menu: DOC-01, DOC-05 | ✅ via menu (1ª opção) |
| T02 | direta | Como tirar RG? | DOC-01 | DOC-01 | ✅ direto |
| T03 | direta | Como agendar atendimento no Meu INSS? | SER-01 | SER-01 | ✅ direto |
| T04 | direta | Qual o horário da Central 135 do INSS? | SER-01 | SER-01 | ✅ direto |
| T05 | direta | Como receber alertas da Defesa Civil por SMS? | COM-01 | COM-01 | ✅ direto |
| T06 | direta | Como cancelar os alertas da Defesa Civil? | COM-01 | COM-01 | ✅ direto |
| T07 | reformulação | Quero fazer meu documento de identificação | DOC-01 | DOC-01 | ✅ direto |
| T08 | reformulação | Como faço para me aposentar? | SER-01 | SER-01 | ✅ direto |
| T09 | reformulação | Como ser avisado quando tiver chuva forte na minha cidade? | COM-01 | COM-01 | ✅ direto |
| T10 | limite | _(vazia)_ | entrada vazia | entrada vazia | ✅ direto |
| T11 | limite | `   ?!  ` | entrada vazia | entrada vazia | ✅ direto |
| T12 | limite | Preciso do RG para pedir benefício no INSS | menu | menu: SER-01, DOC-01 | ✅ direto |
| T13 | fora do tema | Como tirar a carteira de motorista? | sem resposta | menu: DOC-01, DOC-05 | ❌ **falso positivo** |
| T14 | fora do tema | Qual a previsão do tempo para amanhã? | sem resposta | sem resposta | ✅ direto |
| T15 | fora do tema | Como fazer uma receita de bolo de cenoura? | sem resposta | sem resposta | ✅ direto |
| T16 | direta | Como faço a inscrição no CPF? | DOC-02 | DOC-02 | ✅ direto |
| T17 | direta | Como tirar o título de eleitor? | DOC-03 | DOC-03 | ✅ direto |
| T18 | direta | Como pedir a segunda via da certidão de nascimento? | DOC-04 | DOC-04 | ✅ direto |
| T19 | direta | Como obter a carteira de trabalho digital? | DOC-05 | menu: DOC-05, DOC-01 | ✅ via menu (1ª opção) |
| T20 | direta | Como me inscrever no Cadastro Único? | SER-02 | menu: SER-02, DOC-02 | ✅ via menu (1ª opção) |
| T21 | direta | Como fazer o cartão do SUS? | SER-03 | SER-03 | ✅ direto |
| T22 | direta | Como pedir o seguro-desemprego? | SER-04 | SER-04 | ✅ direto |
| T23 | direta | Como subir minha conta gov.br para o nível prata? | SER-05 | SER-05 | ✅ direto |
| T24 | direta | Qual o número do SAMU em uma emergência? | COM-02 | COM-02 | ✅ direto |
| T25 | direta | Como fazer uma denúncia no Disque 100? | COM-03 | COM-03 | ✅ direto |
| T26 | direta | Como pedir ajuda em caso de violência contra a mulher? | COM-04 | COM-04 | ✅ direto |
| T27 | direta | Como fazer uma reclamação contra uma empresa como consumidor? | COM-05 | menu: COM-05, COM-04 | ✅ via menu (1ª opção) |
| T28 | reformulação | Fui mandado embora, tenho direito a algum auxílio? | SER-04 | menu: SER-04, COM-05 | ✅ via menu (1ª opção) |
| T29 | reformulação | Preciso de um médico urgente, para qual número ligo? | COM-02 | COM-02 | ✅ direto |
| T30 | fora do tema | Como renovar o passaporte? | sem resposta | sem resposta | ✅ direto |
| T31 | fora do tema | Quanto custa a conta de luz? | sem resposta | SER-05 | ❌ **falso positivo** |
| T32 | reformulação nova | Ainda não tenho o número do Cadastro de Pessoa Física, como consigo? | DOC-02 | menu: DOC-02, SER-02 | ✅ via menu (1ª opção) |
| T33 | reformulação nova | Fiz 16 anos e quero participar das eleições, o que faço? | DOC-03 | DOC-03 | ✅ direto |
| T34 | reformulação nova | Perdi o documento que prova quando e onde eu nasci | DOC-04 | DOC-04 | ✅ direto |
| T35 | reformulação nova | Como vejo meus empregos registrados no celular? | DOC-05 | nada | ❌ não encontrou |
| T36 | reformulação nova | Minha família tem renda baixa, como recebo ajuda do governo? | SER-02 | menu: SER-02, SER-05 | ✅ via menu (1ª opção) |
| T37 | reformulação nova | Como faço a carteirinha para ser atendido na UBS? | SER-03 | SER-03 | ✅ direto |
| T38 | reformulação nova | Como crio meu login para acessar os serviços do governo pela internet? | SER-05 | SER-05 | ✅ direto |
| T39 | reformulação nova | Minha casa está pegando fogo, para quem ligo? | COM-02 | COM-02 | ✅ direto |
| T40 | reformulação nova | Meu marido me agride, onde posso pedir socorro? | COM-04 | COM-02 | ❌ registro errado |
| T41 | reformulação nova | Comprei um produto com defeito e a loja não quer trocar, o que faço? | COM-05 | COM-05 | ✅ direto |
| T42 | reformulação nova | Vi uma criança sendo maltratada, onde aviso as autoridades? | COM-03 | menu: COM-01, COM-03 | ✅ via menu (2ª opção) |

As classificações são sempre as mesmas a cada execução, porque a busca é determinística. Os tempos variam um pouco de uma execução para outra, conforme o que o computador está fazendo no momento: em execuções seguidas no mesmo computador, a média ficou entre 0,29 ms e 0,43 ms.

### 3.4 Melhoria aplicada: vocabulário do dia a dia na base

Na primeira avaliação com a base completa, **nenhuma reformulação foi encontrada** (0 de 5). A causa era a busca comparar palavras exatas: "aposentar" não encontrava "aposentadoria". Por isso foi aplicada a melhoria proposta naquela avaliação: **acrescentar às palavras-chave de cada um dos 15 registros os termos que as pessoas usam no dia a dia** (63 palavras-chave novas no total), sem mudar nenhuma linha de código.

Exemplos de termos acrescentados:

| Registro | Termos acrescentados (exemplos) |
|---|---|
| DOC-01 (identidade) | identificação, registro geral |
| DOC-03 (título de eleitor) | eleições, alistamento, primeiro título |
| SER-01 (INSS) | aposentar, aposentado, pensão |
| SER-04 (seguro-desemprego) | mandado embora, desemprego, dispensado |
| COM-01 (Defesa Civil) | aviso, chuva, temporal, alagamento |
| COM-02 (emergência) | médico, urgente, socorro, incêndio, fogo |
| COM-05 (consumidor) | defeito, troca, loja, garantia |

**Como evitar que a melhoria "decorasse" o teste.** Se os sinônimos fossem escolhidos olhando as 5 reformulações que falharam, elas passariam a acertar só porque a base foi ajustada a elas. Para medir a melhoria de forma justa, foram escritas **11 reformulações novas (T32 a T42) antes de alterar a base**, e o gabarito delas não foi mudado depois. É a mesma ideia de separar dados de treino e de validação na avaliação de modelos:

- as 5 reformulações antigas mostram se os problemas encontrados foram corrigidos;
- as 11 novas mostram se a melhoria funciona para perguntas que não foram usadas para escolhê-la.

| Indicador | Antes da melhoria | Depois da melhoria |
|---|---|---|
| Reformulações antigas (T07, T08, T09, T28, T29) | 0/5 (0%) | 5/5 (100%) |
| **Reformulações novas (T32 a T42)** | **0/11 (0%)** | **9/11 (81,8%)** |
| Diretas | 18/18 | 18/18 |
| Limites | 3/3 | 3/3 |
| Fora do tema | 3/5 | 3/5 (nenhum falso positivo novo) |
| **Taxa geral (42 testes)** | **24/42 (57,1%)** | **38/42 (90,5%)** |
| Menus exibidos | 5 | 10 |

### 3.5 Evolução ao longo das execuções

| Execução | Base | Perguntas | Taxa de acerto | Tempo médio de consulta |
|---|---|---|---|---|
| 1ª | 3 registros | 15 | 73,3% (11/15) | 0,065 ms |
| 2ª | 15 registros | 31 | 77,4% (24/31) | 0,29 a 0,42 ms |
| 3ª, antes da melhoria | 15 registros | 42 | 57,1% (24/42) | — |
| **3ª, depois da melhoria** | **15 registros + vocabulário ampliado** | **42** | **90,5% (38/42)** | **0,30 a 0,43 ms** |

A queda de 77,4% para 57,1% não foi uma piora do assistente: ela vem só das 11 reformulações novas, que entraram no teste com 0% de acerto. As 31 perguntas anteriores tiveram o mesmo resultado.

## 4. Interpretação dos indicadores

**Depois da melhoria, o assistente acerta 90,5% das perguntas, e o ponto mais importante é o 81,8% nas reformulações novas.** O 100% nas reformulações antigas era esperado, porque os sinônimos foram escolhidos a partir delas. Já as reformulações novas não foram usadas para escolher os sinônimos e mesmo assim 9 de 11 encontraram a orientação certa. Isso indica que a melhoria vale para dúvidas escritas com palavras do dia a dia, e não só para as perguntas do teste.

**Os 2 erros que sobraram nas reformulações novas mostram os limites da estratégia.**
- **T35** ("Como vejo meus *empregos* registrados no celular?"): nenhuma palavra coincidiu. "Empregos" (plural) não é igual a nenhuma palavra-chave, e a carteira de trabalho não tinha um termo como "celular". Comparação por palavra exata não trata plural.
- **T40** ("Meu marido me *agride*, onde posso pedir *socorro*?"): a palavra "socorro" levou ao registro de emergência (COM-02), e "agride" não é igual a "agressão" nem a "agredida". O assistente mostrou os números de emergência, que incluem o 190 e são úteis numa agressão, mas não a orientação do Ligue 180.

Esses erros **não** foram corrigidos acrescentando "empregos" ou "agride" à base: isso seria ajustar a base às perguntas de validação, e a taxa de 81,8% deixaria de medir o que aconteceria com uma pergunta realmente nova.

**O custo da melhoria: mais menus.** Com mais palavras-chave, mais perguntas pontuam em dois registros, e os menus exibidos passaram de 5 para 10. Dos 8 acertos via menu, em 7 o registro certo veio em primeiro lugar. Na T42, a palavra "aviso" (sinônimo de alerta, do COM-01) empatou com "criança" (do COM-03, Disque 100), e o certo veio em segundo. Isso continua sendo acerto pelo critério (top 3), mas exige mais atenção da pessoa.

**Falsos positivos (T13 e T31): continuam sendo o erro mais grave.** A pergunta sobre carteira de motorista recebe um menu com a carteira de identidade e a carteira de trabalho, e a pergunta sobre conta de luz recebe a orientação da conta gov.br. Nos dois casos, **uma única palavra solta** ("carteira", "conta") de uma palavra-chave composta basta para o registro ser oferecido. A ampliação do vocabulário **não criou nenhum falso positivo novo** nas perguntas fora do tema, mas também não resolve esses dois, que exigem outra melhoria (seção 6, item 2). Na interface, a opção "Nenhuma dessas opções" do menu reduz o risco da T13.

**Perguntas diretas e situações-limite (21/21): continuam corretas.** A melhoria não piorou nenhuma pergunta que já acertava. Algumas diretas passaram de acerto direto para via menu (T20), sempre com o registro certo em primeiro lugar.

**Tempo (média entre 0,30 ms e 0,43 ms): não é um gargalo.** A busca percorre todos os registros uma vez para cada pergunta (busca linear). Quando a base passou de 3 para 15 registros, o tempo médio cresceu entre 4 e 7 vezes, coerente com um crescimento proporcional ao tamanho da base. As 63 palavras-chave novas quase não mudaram o tempo. A consulta leva menos de 1 milissegundo, muito abaixo do que uma pessoa consegue perceber.

## 5. Teste de facilidade de uso

O roteiro de tarefas, o perfil do participante e a forma de registro estão em [`teste_usabilidade.md`](teste_usabilidade.md).

O roteiro foi executado pela equipe na interface real (`python src/sistema.py`) em 18/11/2026:

| Indicador | Resultado |
|---|---|
| Tarefas concluídas | **11 de 11 (100%)** |
| Maior número de passos para concluir uma tarefa | 3 (encontrar uma orientação pelo menu e escolher uma opção na pergunta ambígua) |
| Tarefas de erro e limite (entrada vazia, opção inexistente, pergunta fora da base, pergunta ambígua) | 4 de 4 com mensagem clara e caminho para continuar |

**Principais dificuldades observadas:**
- Os nomes dos assuntos vêm da primeira palavra-chave e às vezes são siglas em minúsculas ("cpf", "inss"), pouco claras para quem não as conhece.
- As sugestões de outros temas são sempre o primeiro assunto de cada tema, mesmo sem relação com a orientação lida.
- No falso positivo da carteira de motorista, a interface mostra um menu com "identidade" e "carteira de trabalho". A opção "Nenhuma dessas opções" permite sair e chegar ao aviso de limitação, mas uma pessoa apressada poderia escolher a opção errada.

Essa aplicação confirma que todas as tarefas **podem** ser concluídas, mas foi feita por quem conhece o sistema. A aplicação com um participante externo, com tempo e nota de facilidade, continua recomendada; a tabela para isso está pronta em [`teste_usabilidade.md`](teste_usabilidade.md).

## 6. Melhorias

### 6.1 Melhoria já aplicada

**Vocabulário do dia a dia nas palavras-chave** (seção 3.4): elevou as reformulações novas de 0% para 81,8% e a taxa geral de 57,1% para 90,5%, sem mudar o código e sem criar falsos positivos novos.

### 6.2 Melhorias possíveis

**1. Comparar pelo radical das palavras (ataca os erros de reformulação que sobraram).**
Reduzir as palavras a uma forma comum antes de comparar, cortando terminações como "-s", "-ar", "-ção" e "-doria". Assim, "empregos" e "emprego", ou "agride" e "agressão", passariam a se encontrar sem precisar cadastrar cada variação. É uma regra simples, mas precisa ser testada para não juntar palavras que não têm relação.

**2. Exigir uma correspondência mais forte antes de responder (ataca os falsos positivos).**
Hoje uma única palavra em comum basta. Uma regra possível: quando a única coincidência é uma palavra solta de uma expressão composta (como "carteira", de "carteira de identidade", ou "conta", de "conta gov.br"), o assistente não responde direto. Em vez disso, pergunta "Você quis dizer carteira de identidade?" ou mostra o aviso de limitação. Isso transformaria a T13 e a T31 em acertos sem afetar a T01 e a T23, que contêm as expressões inteiras.

**3. Dar peso diferente a palavras mais específicas.**
Uma palavra que aparece em um único registro (como "samu") indica o assunto com mais certeza do que uma palavra genérica (como "aviso" ou "socorro"). Dar mais pontos às palavras específicas ajudaria a colocar o registro certo em primeiro lugar em casos como a T42.

**4. Ampliar o conjunto de testes com perguntas de pessoas de fora da equipe.**
Pedir a pessoas do público do projeto que escrevam suas dúvidas com as próprias palavras e usar essas frases como reformulações. Isso mede melhor o comportamento real do que perguntas escritas por quem conhece as palavras-chave.

## 7. Limitações da avaliação

- **Amostra pequena.** Com 42 perguntas, cada teste vale 2,4 pontos percentuais da taxa geral, e alguns tipos têm só 3 a 5 perguntas. Uma única pergunta a mais ou a menos muda bastante a taxa desses tipos.
- **Perguntas escritas pela própria equipe.** Mesmo com o gabarito definido antes da execução, quem escreveu as perguntas conhecia as palavras-chave da base. As perguntas diretas tendem a ser mais favoráveis do que as de um usuário real, o que ajuda a explicar os 100% nas diretas.
- **A separação entre "treino" e "validação" é parcial.** As reformulações novas foram escritas antes dos sinônimos, mas pela mesma equipe, que já sabia quais assuntos e situações seriam testados. Por isso o 81,8% provavelmente é um pouco otimista. Reformulações escritas por pessoas de fora (seção 6.2, item 4) dariam uma medida mais confiável.
- **O teste verifica o comportamento, não a qualidade do texto.** A correção confere o estado da busca, o registro encontrado e a presença dos avisos obrigatórios. Ela não avalia se a orientação está clara, se a pessoa entendeu, nem se o conteúdo da base está atualizado. Clareza e compreensão ficam para o teste de facilidade de uso (seção 5), que até agora foi executado só pela equipe.
- **O tempo medido é só o do processamento.** Ele não inclui a exibição na tela, a digitação nem a leitura da resposta. Os valores também dependem do computador e variam entre execuções.
- **O limite de 3 opções no menu é uma escolha da equipe.** Ele não foi validado com usuários. Nesta execução, todos os menus tiveram 2 opções, então o limite ainda não foi realmente posto à prova.
