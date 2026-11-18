# Parte C — Lógica de resposta e estratégias de prompts

## 1. Objetivo e funcionamento

A Parte C recebe registros estruturados da base de conhecimento (Parte A), verifica se possuem os campos necessários, identifica correspondências por regras simples e apresenta uma orientação com fonte, link, data de verificação e avisos. O protótipo não chama uma IA externa: os chamados modelos são estratégias documentadas de instrução e formatação determinística em Python.

Campos esperados: `id`, `tema`, `palavras_chave` (lista de textos), `orientacao`, `referencia` (dicionário com `nome` e `link`) e `data_verificacao`.

## 2. Estratégias de prompt

As instruções seguem quatro partes: **papel** do assistente, **formato** esperado, **regras de segurança** e **dados da base** claramente delimitados como conteúdo de referência. As regras orientam a não inventar documentos, etapas, prazos, valores ou telefones; informar quando a base não contém resposta; evitar dados pessoais desnecessários; e não se apresentar como órgão oficial. O conteúdo da base é tratado como dado, não como instrução para alterar as regras.

### Modelo 1 — Objetivo e direto (padrão)
- Papel: assistente de informação cidadã, curto, objetivo e respeitoso.
- Formato: orientação principal, fonte/link, data de verificação e avisos.
- Vantagem: facilita encontrar rapidamente a informação principal.
- Limitação: oferece menos explicação e contexto.

### Modelo 2 — Didático e passo a passo
- Papel: assistente que explica com calma e linguagem simples.
- Formato: tema, orientação dividida em frases/etapas, fonte/link, data e avisos.
- Vantagem: organiza a leitura para quem prefere explicações guiadas.
- Limitação: resposta mais longa; a divisão automática por pontuação pode separar siglas ou abreviações de forma inadequada.

Os dois formatos usam o mesmo conteúdo cadastrado. Nenhum deles cria informação nova.

## 3. Busca, pontuação e ambiguidades

A busca considera o identificador, as palavras-chave e o tema. A comparação normaliza maiúsculas, minúsculas e acentos, remove pontuação para comparar palavras completas e atribui pesos: identificador exato recebe prioridade; palavras/frases-chave recebem peso maior; coincidências parciais e tema recebem peso menor. Se houver empate na maior pontuação, o sistema lista os temas e pede esclarecimento. Se não houver correspondência, informa a limitação da base.

É uma estratégia introdutória baseada em regras, não compreensão semântica. Perguntas com sinônimos ou vocabulário muito diferente do cadastrado podem não ser reconhecidas. A pontuação deve ser ajustada com perguntas reais de teste.

## 4. Validação e avaliação dos modelos

A validação local verifica tipos e presença dos campos usados pela Parte C, inclusive se `palavras_chave` contém somente textos. A validação completa da base continua sendo responsabilidade da Parte A.

A função `avaliar_resposta` confere cinco elementos: fonte, link, data, aviso para confirmar e aviso de que o assistente não é oficial. Também calcula quantidade de palavras, linhas e maior linha. O percentual é apenas a proporção de elementos presentes; **não mede correção factual, clareza real nem compreensão do usuário**. A comparação automática deve ser complementada por avaliação humana com usuários e perguntas representativas.

## 5. Testes automatizados

O arquivo `tests/testes_resposta.py` contém 15 testes com registros simulados, cobrindo entrada vazia, busca por palavra-chave, identificador, ausência de resultado, ambiguidade, dois modelos, registro incompleto, comparação de palavras completas, montagem da instrução, avaliação dos elementos, empate, modelo inválido e palavras-chave com tipo incorreto.

Executar na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

Os testes usam uma base fictícia e verificam a Parte C isoladamente. Eles não substituem a execução integrada com a base definitiva da Parte A, nem as 12 perguntas de teste e os indicadores gerais exigidos para o projeto.

## 6. Limitações e melhorias futuras

1. **Busca lexical:** ampliar sinônimos e testar a pontuação com consultas reais; futuramente avaliar busca semântica, se o escopo permitir.
2. **Clareza:** realizar teste de usabilidade com participantes e registrar se entenderam a orientação e localizaram a fonte.
3. **Atualização:** criar rotina de revisão das datas e links das fontes oficiais.
4. **Integração:** executar a aplicação com a versão final de `base.py` e da base JSON, validando nomes e tipos dos campos.
5. **Divisão de frases:** revisar manualmente textos com siglas, abreviações e listas.

## 7. Como integrar e executar

Mantenha `src/resposta.py` dentro da pasta `src`. O sistema principal pode importar as funções de resposta a partir desse módulo. A Parte C tenta usar `normalizar` da Parte A; se o módulo ainda não estiver disponível, utiliza uma normalização local simples para permitir testes isolados. A integração final precisa ser testada com os arquivos reais do projeto.


## Integração do resultado da Parte B

No fluxo integrado, a Parte B executa `buscar_pergunta(registros, pergunta)` e entrega à Parte C o envelope completo `{ "estado": ..., "resultados": [...] }`. Cada item de resultado contém o registro original em `item["registro"]` e metadados de pontuação. A Parte C agora recebe esse envelope diretamente por `responder_resultado_busca()`.

A Parte C não trata uma lista de correspondências como autorização para responder com o primeiro item: se houver mais de uma, retorna uma mensagem de ambiguidade. Depois que a pessoa selecionar uma opção, a interface repassa o índice (1-based) ou o ID em `escolha`. O texto final continua sendo montado apenas com os campos do registro validado, sem gerar informação por IA externa.


## Execução conjunta A → B → C (verificação realizada)

A integração foi exercitada com os arquivos recebidos de A (`base.py` e `base_conhecimento.json`) e o módulo `busca.py` recebido de B. A base atual carregou 3 registros, todos aprovados pelo validador de A. Foram testadas perguntas com uma correspondência (`identidade` e `inss`), múltiplas correspondências (`rg inss`) e nenhuma correspondência (`consulta sem correspondencia`). A Parte C recebeu diretamente cada envelope de B e produziu, respectivamente, a orientação formatada, o pedido de escolha e o aviso de limitação. Essa verificação confirma o contrato entre os módulos com a base atual; não valida ainda a interface final nem uma base ampliada.
