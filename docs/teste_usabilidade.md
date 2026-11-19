# Teste de Facilidade de Uso — Citizen Assist AI

## 1. Objetivo

Verificar se uma pessoa consegue usar o assistente para encontrar uma orientação pelo menu e por pergunta digitada, reconhecer a fonte e os avisos, navegar entre assuntos e entender as mensagens de erro e de limitação.

Os testes automatizados (`docs/resultados_testes.md`) medem se a busca encontra o registro certo. Este teste mede outra coisa: **se o caminho até a orientação é claro para quem usa.**

## 2. Formas de aplicação

O enunciado aceita o teste com pelo menos um usuário **ou** com um roteiro de tarefas. Este documento prevê as duas formas:

| Aplicação | Quem executa | Situação |
| --- | --- | --- |
| **Aplicação 1 — roteiro de tarefas** | A equipe, seguindo as 11 tarefas abaixo na interface real (`python src/sistema.py`) | ✅ Realizada em 18/11/2026 (seção 5) |
| **Aplicação 2 — participante externo** | Uma pessoa de fora da equipe, de preferência com pouca familiaridade com serviços públicos | Recomendada; roteiro e tabela prontos na seção 6 |

**Privacidade:** em nenhuma das aplicações são registrados nome, documento, idade exata ou outros dados pessoais. O participante é identificado só como "Participante 1" e por um perfil genérico.

## 3. Como aplicar com um participante

1. Abrir o assistente com `python src/sistema.py` antes de chamar o participante.
2. Avisar que **quem está sendo testado é o assistente, não a pessoa**, e que ela pode desistir de qualquer tarefa.
3. Ler cada tarefa em voz alta, uma de cada vez, exatamente como está escrita abaixo.
4. Pedir que o participante **pense em voz alta** enquanto usa o assistente.
5. **Não ajudar** durante a tarefa. Se o participante pedir ajuda, anotar e só ajudar depois de 2 minutos parado ou se ele desistir; nesse caso, a tarefa conta como "concluída com ajuda".
6. Cronometrar cada tarefa, do fim da leitura até o participante dizer que terminou.
7. No final, fazer as perguntas da seção 4.4.

## 4. Roteiro de tarefas

### 4.1 Encontrar orientações

| Nº | Tarefa (ler para o participante) | Conclusão esperada |
|---|---|---|
| U1 | "Descubra quais assuntos esse assistente consegue explicar." | Encontra a lista de temas (Documentos, Serviços, Orientações comunitárias) |
| U2 | "Usando o menu, descubra como tirar o título de eleitor." | Chega à orientação DOC-03 pelo menu |
| U3 | "Agora escrevendo uma pergunta, descubra como pedir o seguro-desemprego." | Chega à orientação SER-04 digitando a pergunta |
| U4 | "Na resposta que você acabou de receber, diga de onde veio essa informação e quando ela foi conferida." | Aponta a fonte (nome ou link) e a data de verificação |
| U5 | "Depois dessa resposta, vá para outro assunto que o assistente sugerir." | Usa as sugestões de continuidade para abrir outro assunto |

### 4.2 Situações de erro e de limite

| Nº | Tarefa (ler para o participante) | Conclusão esperada |
|---|---|---|
| U6 | "Aperte Enter sem escrever nada. O que o assistente disse?" | Entende que precisa escrever uma pergunta ou escolher uma opção |
| U7 | "No menu, escolha uma opção que não existe (por exemplo, o número 9). O que aconteceu?" | Entende a mensagem e volta para uma opção válida |
| U8 | "Pergunte como renovar o passaporte. O assistente sabe responder? O que ele sugeriu?" | Entende que a base não tem essa informação e identifica a sugestão de outros temas |
| U9 | "Pergunte: preciso do RG para pedir benefício no INSS. O que o assistente fez?" | Entende o menu de opções e escolhe uma delas |

### 4.3 Avisos e caráter não oficial

| Nº | Pergunta (ler para o participante) | Conclusão esperada |
|---|---|---|
| U10 | "Esse assistente é um canal oficial do governo?" | Responde que não, com base no aviso exibido |
| U11 | "Antes de ir a um órgão público, o assistente recomenda fazer alguma coisa?" | Menciona o aviso para confirmar requisitos na fonte oficial |

### 4.4 Perguntas finais (só para participante externo)

1. De 1 (muito difícil) a 5 (muito fácil), quão fácil foi usar o assistente?
2. O que foi mais difícil ou confuso?
3. Teve alguma palavra ou mensagem que você não entendeu?
4. Você usaria esse assistente para tirar uma dúvida real? Por quê?

## 5. Aplicação 1 — execução do roteiro pela equipe (18/11/2026)

Cada tarefa foi executada na interface real (`python src/sistema.py`), com a base de 15 registros e o formato de resposta guiado. A coluna **Passos** conta quantas entradas foram digitadas, desde o menu principal até concluir a tarefa. O tempo não foi medido nesta aplicação, porque quem executou conhecia o sistema; ele será medido com o participante externo.

Resultado: **C** = concluída · **N** = não concluída.

| Nº | Resultado | Passos | O que a interface mostrou |
|---|---|---|---|
| U1 | C | 1 | Opção 1 do menu lista os 3 temas com a quantidade de assuntos de cada um |
| U2 | C | 3 | Menu → Documentos → "título de eleitor"; mostra o caminho "Orientação cidadã > Documentos > título de eleitor" antes da resposta |
| U3 | C | 2 | Opção 2 + pergunta digitada; a busca encontrou só o SER-04 e mostrou a orientação direto |
| U4 | C | 0 | A resposta tem a seção "Onde conferir", com o nome da fonte, o link e "Verificado em: 18/11/2026" |
| U5 | C | 1 | Depois da resposta aparecem 5 assuntos relacionados (3 do mesmo tema e 1 de cada outro tema); escolher o 1 abriu o INSS |
| U6 | C | 1 | No menu: "Você não digitou nada. Digite o número de uma das opções." Na pergunta: "Você não digitou nenhuma pergunta", com a lista de temas |
| U7 | C | 1 | "A opção 9 não existe. Escolha um número de 0 a 4." O menu continua aberto. Texto como "abc" também recebe uma mensagem própria |
| U8 | C | 2 | Aviso de limitação, lista de todos os assuntos disponíveis e as opções "fazer outra pergunta" ou "ver os temas" |
| U9 | C | 3 | Mensagem "pode estar relacionada a mais de um assunto", com as opções "inss" e "identidade" e a opção "Nenhuma dessas opções" |
| U10 | C | 0 | O aviso de que não é canal oficial aparece na abertura, no fim de cada resposta e na opção "Sobre" |
| U11 | C | 0 | Toda resposta termina com "Antes de agir: ... Confira prazos e requisitos diretamente na fonte indicada" |

**Taxa de conclusão: 11 de 11 tarefas (100%).** Nenhuma tarefa exigiu mais de 3 passos.

### Dificuldades observadas

1. **Títulos dos assuntos pouco amigáveis.** O nome de cada assunto é a primeira palavra-chave do registro, então alguns aparecem em minúsculas ou como sigla: "cpf", "inss", "cartão sus". Para quem não conhece a sigla, "inss" não diz do que se trata.
2. **Sugestões de outros temas sempre iguais.** Depois de qualquer resposta, a sugestão de outro tema é sempre o primeiro assunto daquele tema ("inss", "defesa civil" ou "identidade"), mesmo quando não tem relação com o que a pessoa leu.
3. **Falso positivo vira menu.** Na pergunta "Como tirar a carteira de motorista?", a interface ofereceu "identidade" e "carteira de trabalho". A opção **"Nenhuma dessas opções"** permitiu sair do menu e chegar ao aviso de limitação, mas uma pessoa apressada poderia escolher a carteira de identidade achando que é a resposta.
4. **Pergunta vazia volta ao menu principal.** Depois do aviso de entrada vazia, é preciso escolher a opção 2 de novo para digitar a pergunta.
5. **Linhas longas na fonte.** O link da fonte aparece inteiro e, em janelas estreitas do terminal, quebra no meio.

### Melhorias sugeridas pela aplicação

- Mostrar um título explicativo do assunto (por exemplo, "CPF — inscrição" e "INSS — canais de atendimento"), sem mudar o formato da base. Uma opção é um pequeno dicionário de títulos na interface.
- Depois de uma pergunta vazia, pedir a pergunta de novo em vez de voltar ao menu principal.
- No menu de ambiguidade, mostrar também a pontuação ou uma frase de cada orientação, para a pessoa perceber quando nenhuma opção é a certa.

## 6. Aplicação 2 — participante externo (recomendada)

### 6.1 Participante

| Campo | Valor |
|---|---|
| Identificação | Participante 1 |
| Perfil genérico | [preencher] |
| Data da aplicação | [preencher] |
| Aplicador | [preencher] |

### 6.2 Tarefas

Resultado: **C** = concluiu sozinho · **A** = concluiu com ajuda · **N** = não concluiu.

| Nº | Resultado (C/A/N) | Tempo (s) | Tentativas | Dificuldades observadas |
|---|---|---|---|---|
| U1 | | | | |
| U2 | | | | |
| U3 | | | | |
| U4 | | | | |
| U5 | | | | |
| U6 | | | | |
| U7 | | | | |
| U8 | | | | |
| U9 | | | | |
| U10 | | | | |
| U11 | | | | |

### 6.3 Perguntas finais

| Pergunta | Resposta |
|---|---|
| Nota de facilidade (1 a 5) | |
| O que foi mais difícil | |
| Palavras ou mensagens não entendidas | |
| Usaria para uma dúvida real? | |

### 6.4 Indicadores

- **Taxa de conclusão sem ajuda** = tarefas com resultado C ÷ 11 × 100
- **Taxa de conclusão total** = tarefas com resultado C ou A ÷ 11 × 100
- **Tempo médio por tarefa** (somente tarefas concluídas)
- **Nota média de facilidade** (se houver mais de um participante)

## 7. Limitações deste teste

- **A Aplicação 1 foi feita por quem conhece o sistema.** Ela confirma que todas as tarefas **podem** ser concluídas e aponta problemas visíveis na tela, mas não mede se uma pessoa de fora entenderia as mensagens. Por isso a Aplicação 2 continua recomendada.
- Com 1 ou 2 participantes, o teste mostra dificuldades concretas, mas não permite generalizar para todo o público.
- A presença do aplicador e o fato de saber que está sendo observado podem mudar o comportamento do participante.
- As tarefas foram escritas pela equipe e usam assuntos que a base cobre; dúvidas reais podem ser bem diferentes.
