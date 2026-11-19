# Uso de Inteligência Artificial no projeto

Registro exigido pelo enunciado da Global Solution 2026.2: onde a IA foi usada, para quê e como a equipe validou criticamente o resultado. Cada frente do projeto tem uma seção própria, com a mesma estrutura: ferramenta e materiais, o que a IA produziu e o que foi decisão da equipe, validação crítica, erros da IA encontrados e limites do uso.

## Resumo

| Frente | Ferramenta | Para que foi usada | Responsável pela validação | Data |
| --- | --- | --- | --- | --- |
| A — Base de conhecimento e leitura de arquivos | Claude (Anthropic), via claude.ai | Primeira versão do código, pesquisa de 3 orientações, testes de cenários de erro, documento de conferência | Mayara Luisa Vicente Rosa — RM 571955 | 13/11/2026 |
| B — Consulta, navegação e algoritmos | Codex (OpenAI) | Leitura dos requisitos, implementação da busca, da hierarquia e da navegação, testes automatizados e documentação | Gabriel Luís de Lima Ramos — RM 568984 | 17/11/2026 |
| C — Lógica de resposta e estratégias de prompts | ChatGPT (OpenAI) | Elaboração e comparação dos modelos de prompt, instruções do assistente, revisão de textos, testes automatizados e análise da integração com a Parte B | Pietra Fanticelli — RM 573229 | 18/11/2026 |
| D — Interação e tratamento de erros | Claude Code (Anthropic), extensão do VS Code | Implementação da interface em texto (`src/sistema.py`) e dos testes automatizados da interface (`tests/test_sistema.py`), feita pela IA em etapas, com supervisão da equipe | Equipe | 18/11/2026 |
| E — Testes e indicadores de desempenho | Claude Code (Anthropic), extensão do VS Code; Claude (Anthropic), via claude.ai | Tutoria na escrita do script de avaliação (duas partes escritas pela IA), complemento das perguntas de teste T06–T15, redação do relatório de resultados e do roteiro de usabilidade, e revisão | Victor de Camargo Gomes — RM 568912 | 18/11/2026 |
| Integração e preparação da entrega | Claude Code (Anthropic), extensão do VS Code | Ampliação da base para 15 registros, vocabulário do dia a dia nas palavras-chave, novas perguntas de teste, aplicação do roteiro de usabilidade, adaptação dos testes da Parte B, comparação dos modelos de resposta, roteiro de usabilidade e README | Victor de Camargo Gomes — RM 568912 | 18/11/2026 |

## IA dentro do protótipo

**O protótipo não chama nenhum modelo de IA durante a execução.** Todas as respostas são montadas por regras determinísticas em Python:

- as orientações vêm somente de `data/base_conhecimento.json`, com textos conferidos em fontes oficiais (Parte A);
- a busca compara palavras da pergunta com as palavras-chave dos registros (Parte B);
- os "modelos de prompt" da Parte C são estratégias documentadas de instrução e formatação, aplicadas pelo próprio código, sem envio a uma API externa;
- a avaliação da Parte E executa a busca e a resposta e compara o resultado com um gabarito.

Por isso, não existem respostas de modelo externo para confrontar com a base verificada. A IA foi usada apenas como apoio ao desenvolvimento: código, textos, testes e revisão.

**Dados pessoais:** em nenhuma frente foram usados ou enviados dados de usuários do assistente.

---

## Parte A — Base de conhecimento e leitura de arquivos

### Ferramenta e materiais

- **Ferramenta:** Claude (Anthropic), no claude.ai. Modelos usados na conversa: Claude Fable 5.2 (código e base) e Claude Opus 5.5 (documento de conferência e este registro).
- **Data:** 13/11/2026.
- **Materiais entregues à IA:** o enunciado da Global Solution 2026.2 e o PDF com o material das aulas das fases 4, 5 e 6.

### O que foi pedido

- **Papel:** parceiro de desenvolvimento Python de nível iniciante-intermediário, fiel ao conteúdo das fases 4 a 6, explicando cada decisão para que a equipe consiga justificá-la.
- **Restrições:** Python puro com a biblioteca padrão (`json`, `os`); sem APIs pagas, LangChain ou bibliotecas externas; código comentado com nomes em português; a base guarda só orientações e fontes, sem dados pessoais.
- **Entregas:**
  1. `data/base_conhecimento.json` com exatamente os campos `id`, `tema`, `palavras_chave`, `orientacao`, `referencia` (nome e link) e `data_verificacao`, com 3 registros de exemplo.
  2. `src/base.py` com `carregar_base`, `validar_registros`, `listar_temas`, `buscar_por_id`, `filtrar_por_tema` e `buscar_por_palavra_chave`, tratando arquivo ausente, vazio e malformado.
  3. Dados separados das regras: incluir ou corrigir uma orientação deve exigir só a edição do JSON.
  4. Um teste rápido em `if __name__ == "__main__":`.
  5. Um resumo para o README e a lista de limites e decisões a defender.

### O que a IA produziu e o que foi decisão da equipe

| Item | Arquivo | Origem |
| --- | --- | --- |
| Lista dos 6 campos de cada registro | `data/base_conhecimento.json` | Definida pela equipe no pedido; a IA seguiu |
| Escolha dos 3 assuntos de exemplo (Carteira de Identidade Nacional, canais do INSS, alertas da Defesa Civil) | `data/base_conhecimento.json` | Sugerida pela IA; a equipe decide se mantém |
| Texto das 3 orientações | `data/base_conhecimento.json` | Redigido pela IA a partir de páginas gov.br |
| Código de leitura, validação e consulta | `src/base.py` | Gerado pela IA; revisão e explicação pela equipe |
| Script com 50 cenários de teste | Rascunho fora do repositório | Gerado e executado pela IA |
| Documento de conferência com o enunciado e as fases 4 a 6 | Arquivo Word, fora do repositório | Gerado pela IA |
| Resumo da base para o README | `README.md` | Rascunho da IA; a equipe adapta |

### Validação crítica realizada

| O que foi conferido | Como | Resultado |
| --- | --- | --- |
| Conteúdo das 3 orientações | Cada frase comparada com a página oficial citada no campo `referencia` | Confere. Divergência encontrada: o prazo de validade do RG antigo aparece como 28/02/2032 (MGI), 23/02/2032 (governo de Minas Gerais) e 01/03/2032 (Espírito Santo). Todas as fontes concordam com 2032 |
| Aderência ao enunciado | Cada requisito do bloco "Base de conhecimento e leitura de arquivos" ligado a uma linha do código | Todos atendidos. Lacuna apontada: a base não tem subtemas nem assuntos relacionados, que o enunciado pede para a navegação |
| Aderência ao material das aulas | Cada recurso de Python procurado no PDF das fases 4 a 6 | Os recursos principais (arquivos, `with`, `json.loads`, listas, dicionários, lista de dicionários como tabela) estão no material. Recursos fora do PDF (`try/except`, `isinstance`, `os.path`, `encoding="utf-8-sig"` e alguns métodos de texto) foram identificados e justificados com a documentação oficial do Python |
| Funcionamento do código | `python src/base.py` executado, mais 50 cenários simulados: arquivo ausente, vazio e malformado, registros com campo faltando, campo extra, tipo errado, data inválida, id repetido e buscas com e sem acento | 50 de 50 sem falha; o programa não parou em nenhum cenário de erro |

### Erros da IA encontrados na revisão

- A IA informou 49 cenários de teste; a recontagem mostrou 50. Corrigido.
- A IA não conseguiu abrir o repositório modelo da coordenação. Os nomes das pastas (`data/`, `src/`, `docs/`) precisam ser conferidos manualmente.
- A página de perguntas frequentes do Governo Digital sobre a carteira de identidade não abriu. A IA usou a página do Ministério da Gestão (MGI), que é de 2024. Por isso, a orientação manda confirmar no órgão de identificação do estado.

### Validação pela equipe (antes da entrega)

- [ ] Rodar `python src/base.py` em um computador da equipe e conferir a saída
- [ ] Abrir os 3 links oficiais e confirmar cada frase das orientações
- [ ] Simular os erros: renomear o JSON (ausente), apagar o conteúdo (vazio) e tirar uma vírgula (malformado)
- [ ] Decidir como escrever o prazo de validade do RG no registro DOC-01
- [ ] Conferir os nomes das pastas no repositório modelo da coordenação
- [ ] Cada integrante consegue explicar `carregar_base` e `validar_registros` sem consultar a IA

### Limites do uso de IA nesta parte

- A IA não substitui a conferência das fontes: páginas oficiais mudam, e o campo `data_verificacao` registra quando cada uma foi vista.
- Os testes mostram que o código se comporta como esperado nos cenários simulados. Eles não provam que as orientações estão corretas; isso depende da conferência das fontes.
- As explicações e justificativas da apresentação são responsabilidade da equipe.

---

## Parte B — Consulta, navegação e algoritmos

### Ferramenta e materiais

- **Ferramenta:** Codex (OpenAI). Versão exata do modelo não registrada.
- **Data:** 17/11/2026.
- **Materiais entregues à IA:** enunciado em texto, plano de trabalho do grupo e os arquivos da Parte A (`base.py` e `base_conhecimento.json`).

O estudante responsável autorizou a geração do código e da documentação, limitada à Parte B. A ferramenta auxiliou na leitura dos requisitos, na definição das funções, na implementação da busca, da hierarquia e da navegação, na elaboração dos testes, na execução das verificações e na organização da entrega.

### O que foi decisão da equipe

- Entregar somente a Parte B, os testes e o guia de integração, sem uma aplicação demonstrável própria.
- Preservar os arquivos da Parte A sem alterações.
- Usar Python com a biblioteca padrão e explicações adequadas ao início do curso.
- Usar os três registros recebidos para a integração, sem ampliar a base nesta parte.
- Manter as demais frentes sob responsabilidade do grupo.

### Decisões técnicas propostas e implementadas pela IA

- Reutilizar as consultas exatas e a normalização de texto disponíveis na Parte A.
- Buscar perguntas por palavras úteis e por expressões de `palavras_chave`.
- Somar 1 ponto por termo útil distinto e 2 pontos por expressão composta distinta.
- Devolver todas as correspondências positivas, ordenadas por pontuação e, em caso de empate, por ID.
- Organizar a hierarquia raiz → tema → assunto fora dos registros validados da Parte A.
- Oferecer navegação para outros assuntos do mesmo tema e para os demais temas, sem afirmar dependências entre os serviços.
- Registrar estados de consulta e preservar os dados e as referências recebidos.

Essas escolhas estão descritas em `docs/busca_navegacao.md` e devem ser estudadas e revisadas pelo estudante antes da apresentação. Não se afirma que houve aprovação humana individual de cada linha de código.

### Validação crítica realizada

| Verificação | Evidência |
| --- | --- |
| Compatibilidade com a Parte A | Importação do módulo original e leitura e validação dos registros reais em pasta temporária |
| Comportamentos da Parte B | Suíte `unittest` em `tests/test_busca.py`, com casos sintéticos e de integração |
| Consultas e ambiguidades | IDs, estados e pontuações comparados com expectativas explícitas |
| Preservação dos dados | Comparação dos registros antes e depois e dos bytes dos arquivos da Parte A |
| Ausência de interface no núcleo | Teste de importação em processo novo e operações sem `input` nem saída na tela |
| Manutenção | Inclusão fictícia de um novo registro e de um novo tema, sem alterar o algoritmo |
| Limitações | Documentadas: coincidência apenas por palavras, ausência de sinônimos automáticos e base incompleta |

Os dados `FIC-*` e a fonte `example.invalid` existem somente nos testes. Não foram produzidas novas orientações para completar os 15 registros.

### Erros da IA encontrados na revisão

- Na primeira execução dos testes, todos passaram, mas o Python emitiu um aviso por causa de uma barra invertida no exemplo de caminho de uma docstring. A docstring foi ajustada para texto bruto (`r"""..."""`) e a suíte foi verificada novamente com avisos tratados como erros.
- A contagem das palavras ignoradas na explicação foi conferida para corresponder às 34 entradas do código.

Esses ajustes vieram da revisão automatizada da ferramenta e não equivalem a revisão humana ou a teste com um cidadão.

### Validação pela equipe (antes da entrega)

- [ ] Estudar e conseguir explicar as funções, a pontuação, os empates e a navegação
- [ ] Revisar a adequação dos termos e da linguagem ao público do projeto
- [ ] Conferir a atualidade das orientações nas fontes oficiais da Parte A
- [x] Ampliar a base para pelo menos 15 registros
- [x] Integrar e avaliar as Partes C, D e E com a base final
- [ ] Fazer a avaliação de facilidade de uso prevista no enunciado (roteiro aplicado na interface; falta a aplicação com participante externo)

### Limites do uso de IA nesta parte

- As fontes cidadãs não foram reabertas na implementação da Parte B. Preservar os textos não é uma nova certificação do seu conteúdo ou das suas datas.
- O material completo das aulas não foi disponibilizado à ferramenta. A adequação de nível foi orientada pelos requisitos e pelo pedido do estudante, sem conferência página a página das apostilas.

---

## Parte C — Lógica de resposta e estratégias de prompts

### Ferramenta e materiais

- **Ferramenta:** ChatGPT (OpenAI).
- **Data:** 18/11/2026.

### Para que foi usada

- Elaborar e comparar dois modelos de prompt: um objetivo e direto e outro didático e passo a passo.
- Sugerir instruções para definir o papel do assistente, o formato das respostas e cuidados para evitar informações inventadas.
- Revisar textos, mensagens, avisos e a documentação da Parte C.
- Apoiar a identificação de cenários de teste e a preparação dos testes automatizados em `tests/testes_resposta.py`, com registros simulados.
- Apoiar a análise da integração da Parte C com o formato de retorno da Parte B.

### O que foi decisão da equipe

- Definir e utilizar as estratégias de resposta objetiva e didática como modelos documentados para o assistente.
- Conferir a compatibilidade dos campos utilizados pela Parte C com a estrutura da Parte A.
- Manter a revisão humana como parte necessária da validação das respostas, fontes e orientações.
- Tratar os prompts como instruções documentadas em texto: o protótipo não realiza chamada a uma API externa de IA.
- Adaptar a Parte C ao retorno da Parte B, que contém `estado` e `resultados`, com o registro dentro do campo `registro`, incluindo tratamento para múltiplas correspondências sem selecionar automaticamente a primeira.

### Validação crítica realizada

- As sugestões da IA foram revisadas e comparadas com a estrutura e os arquivos do projeto.
- Foram conferidos os campos `id`, `tema`, `palavras_chave`, `orientacao`, `referencia` e `data_verificacao`.
- Foi verificado que os 3 registros disponíveis no JSON seguem a estrutura esperada e abrangem os temas Documentos, Serviços e Orientações comunitárias.
- Os testes automatizados da Parte C foram executados: **15 de 15 passaram** no ambiente utilizado, com dados simulados.
- Também foi realizada uma execução local A → B → C com os arquivos disponibilizados, verificando consultas com uma, múltiplas e nenhuma correspondência.
- Foi identificado que a base possui somente 3 registros, embora o `base.py` indique o mínimo de 15 registros em 3 temas. Portanto, a base ainda precisa ser ampliada.
- Os testes simulados e a execução local não substituem a validação ponta a ponta com a base ampliada, a interface e as versões finais de todas as partes.

### Erros da IA encontrados na revisão

- **Detecção de confirmação por trecho de texto:** foi sugerido procurar uma palavra como "confirm" para identificar a necessidade de confirmação. Essa abordagem poderia gerar falsos positivos ou deixar passar outros avisos. A lógica foi simplificada para apresentar um aviso uniforme, sem depender dessa busca.
- **Conclusões além do que os testes demonstravam:** resultados com registros simulados não comprovavam a integração com a base real. Por isso, foi necessário distinguir os testes automatizados da verificação com os arquivos reais.
- **Limitação da avaliação automática:** critérios que verificam apenas a presença de fonte, link, data e avisos não garantem que a orientação esteja correta ou seja fácil de entender. Foi mantida a necessidade de avaliação humana.

### Limites do uso de IA nesta parte

A equipe permanece responsável por compreender, revisar, testar e validar o código, as respostas e as fontes utilizadas no projeto.

---

## Parte D — Interação e tratamento de erros

### Ferramenta e materiais

- **Ferramenta:** Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5.
- **Data:** 18/11/2026.
- **Materiais entregues à IA:** enunciado da Global Solution 2026.2, plano de trabalho do grupo e o repositório com as Partes A, B, C e E já integradas.

### Forma de trabalho

Nesta frente, **o código foi escrito inteiramente pela IA**, com supervisão da equipe. O trabalho foi feito em etapas: antes de cada criação ou alteração, a IA informava o que pretendia fazer, e a equipe aprovava, pedia ajustes ou sugeria outro caminho. Nenhuma alteração foi aplicada sem essa aprovação.

### O que a IA produziu e o que foi decisão da equipe

| Item | Arquivo | Origem |
| --- | --- | --- |
| Interface em texto: menu principal, menu de temas e assuntos, pergunta digitada, troca do formato de resposta e opção "Sobre" | `src/sistema.py` | Escrita pela IA, com aprovação da equipe em cada etapa |
| Tratamento de entrada vazia, texto no lugar de número, opção inexistente e encerramento com Ctrl+C ou Ctrl+Z | `src/sistema.py` | Escrito pela IA, com aprovação da equipe |
| Opção "Nenhuma dessas opções" no menu de ambiguidade, levando ao aviso de limitação | `src/sistema.py` | Ideia da equipe, surgida na definição dos critérios de teste; implementada pela IA |
| Assuntos relacionados depois de cada resposta (até 3 do mesmo tema e 1 de cada outro tema) e alternativas depois de uma pergunta sem resposta | `src/sistema.py` | Escrito pela IA, usando as funções de navegação da Parte B |
| Formato de resposta inicial "guiado" (Modelo 2), escolhido a partir da comparação dos modelos da Parte C | `src/sistema.py` | Proposto pela IA; aprovado pela equipe |
| Aviso para não digitar dados pessoais na tela de pergunta; nada do que a pessoa digita é gravado | `src/sistema.py` | Escrito pela IA, com aprovação da equipe |
| 11 testes automatizados da interface, que simulam o que a pessoa digita e conferem a tela | `tests/test_sistema.py` | Escritos pela IA, com aprovação da equipe |

### Validação crítica realizada

| O que foi conferido | Como | Resultado |
| --- | --- | --- |
| Funcionamento da interface | 11 testes automatizados: sair pelo menu, fim da entrada, opção vazia, inexistente e em texto, navegação por temas, continuidade, pergunta vazia, pergunta sem resposta, ambiguidade (escolhendo uma opção e escolhendo "nenhuma"), troca de formato e base inválida | 11 de 11 passam |
| Integração com as outras partes | `python -B -W error -m unittest discover -s tests` | 92 de 92 testes passam (busca, respostas e interface) |
| Uso real | Execução de `python src/sistema.py` seguindo o roteiro de tarefas do teste de facilidade de uso (Aplicação 1, `docs/teste_usabilidade.md`) | 11 de 11 tarefas concluídas; as dificuldades observadas estão registradas no documento |

### Erros da IA encontrados na revisão

- [preencher: ajustes pedidos pela equipe ou sugestões da IA recusadas durante a supervisão]

### Limites do uso de IA nesta parte

- Esta é a frente com maior participação da IA no projeto: o código foi escrito por ela, e a contribuição da equipe foi supervisionar, aprovar e ajustar cada etapa.
- Os testes automatizados conferem o que aparece na tela, mas não substituem o teste com uma pessoa de fora da equipe (Aplicação 2 do teste de facilidade de uso).

### Validação pela equipe (antes da entrega)

- [ ] Conseguir explicar o fluxo de `menu_principal`, `fazer_pergunta`, `tratar_ambiguidade` e `escolher_numero` sem consultar a IA
- [ ] Aplicar o teste de facilidade de uso com uma pessoa de fora da equipe (Aplicação 2)

---

## Parte E — Testes e indicadores de desempenho

### Ferramenta e materiais

- **Ferramentas:**
  - Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5: tutoria durante a escrita do código, complemento das perguntas de teste e redação dos documentos.
  - Claude (Anthropic), via claude.ai: orientação inicial e revisão do script e dos documentos da Parte E.
- **Data:** 18/11/2026.
- **Materiais entregues à IA:** enunciado da Global Solution 2026.2, plano de trabalho do grupo e o repositório com as Partes A, B e C já integradas (`src/base.py`, `src/busca.py`, `src/resposta.py`, `data/base_conhecimento.json`).

### Forma de trabalho

A IA foi usada como tutora: explicava o que precisava ser feito e o estudante escrevia o código. Só em dois trechos, em que o estudante travou, a IA escreveu o código, e o estudante revisou o resultado. As decisões de critério foram discutidas antes de serem aplicadas.

### O que a IA produziu e o que foi decisão da equipe

| Item | Arquivo | Origem |
| --- | --- | --- |
| Perguntas de teste T01 a T05 | `data/perguntas_teste.json` | Escritas pelo estudante, com todos os campos |
| Perguntas de teste T06 a T15 | `data/perguntas_teste.json` | Pergunta e `id_esperado` escritos pelo estudante; `tipo`, `resultado_esperado` e `observacao` completados pela IA |
| Perguntas de teste T16 a T31 | `data/perguntas_teste.json` | Geradas pela IA na integração, para os registros novos da base (ver "Integração e preparação da entrega") |
| Renomear `id` para `id_teste` e usar em `resultado_esperado` os mesmos estados da Parte B | `data/perguntas_teste.json` | Decisão do estudante |
| Critério de acerto: menu com o registro certo conta como acerto, separado em "direto" e "via menu" | `docs/resultados_testes.md` | Decisão do estudante |
| Limite de 3 primeiras opções do menu para contar acerto | `docs/resultados_testes.md` | Decisão do estudante |
| Falso positivo como erro explícito | `docs/resultados_testes.md` | Sugerido pela IA (Claude Code); aceito pelo estudante |
| Texto do relatório de resultados (critérios, resultados, interpretação, melhorias e limitações) | `docs/resultados_testes.md` | Redigido pela IA a partir das definições do estudante e da execução real do script; revisado pelo estudante, que reescreveu trechos mantendo o sentido |
| Funções `carregar_perguntas`, `executar_teste`, `classificar`, `montar_linha`, `media`, `percentual`, `calcular_indicadores`, `salvar_csv` e `mostrar_relatorio` | `src/testes.py` | Escritas pelo estudante, com orientação da IA |
| Função `br` e bloco principal (`if __name__ == "__main__":`) | `src/testes.py` | Escritos pela IA a pedido do estudante; revisados pelo estudante |
| Roteiro do teste de facilidade de uso | `docs/teste_usabilidade.md` | Redigido pela IA |

### Validação crítica realizada

| O que foi conferido | Como | Resultado |
| --- | --- | --- |
| Gabarito sem viés | O `resultado_esperado` de cada pergunta foi definido **antes** de executar a busca, a partir das palavras-chave da base | A execução confirmou as previsões feitas antes do teste: erro nas reformulações e falsos positivos onde uma palavra solta coincide com outro registro |
| Função `classificar` | 13 casos inventados, um para cada caminho possível (acerto direto, via menu, fora do top 3, registro errado, falso positivo, ausência de aviso etc.) | 13 de 13 com a classificação esperada |
| Função `carregar_perguntas` | 8 arquivos de teste: real, ausente, vazio, JSON quebrado, objeto em vez de lista, lista vazia, pergunta sem campos e pergunta sem `id_esperado` | Os 8 devolvem uma mensagem clara sem travar |
| Execução completa | `python src/testes.py` com a base real | Sem erros. Com 3 registros e 15 perguntas: 11 acertos (73,3%). Com 15 registros e 31 perguntas: 24 acertos (77,4%). Com 42 perguntas e o vocabulário ampliado: 38 acertos (90,5%) |
| Compatibilidade com as Partes B e C | Conferência no código dos nomes dos estados devolvidos por `buscar_pergunta` e dos textos fixos de aviso de `src/resposta.py` | Nomes e textos conferem |

### Erros da IA encontrados na revisão

Os pontos abaixo foram identificados na revisão do script e dos documentos (com apoio do Claude, via claude.ai) e corrigidos por decisão do estudante.

- **Pergunta ambígua classificada como "via menu".** Na pergunta ambígua, mostrar o menu é o comportamento esperado; contar como "via menu" faria parecer que o assistente teve dificuldade onde acertou. Corrigido para acerto direto.
- **Critério que prometia mais do que o teste media.** O critério de "sem resposta" dizia que o sistema mostrava aviso e sugestão de temas, mas o script só conferia o estado da busca. Agora o script passa o resultado pela Parte C e confere o aviso; a sugestão de temas ficou para o teste de usabilidade.
- **Tempo de consulta incompleto.** A primeira versão media só a busca. Passou a medir também a montagem da resposta (Parte C), que é o que a pessoa espera de fato.
- **Medição única de tempo.** Com cerca de 0,05 ms por consulta, uma única medição variava muito. Agora cada consulta é medida 100 vezes, depois de uma execução de aquecimento.
- **CSV com padrão misturado.** O separador era `;` (padrão do Excel em português), mas os tempos tinham ponto decimal. Os tempos passaram a usar vírgula.
- **Coluna enganosa no CSV.** A coluna `tamanho_menu` mostrava 1 ou 0 mesmo quando não havia menu. Agora fica vazia nesses casos.
- **Comentários dependentes do documento.** Os comentários do código citavam "seção 2.3" e similares. Foram reescritos para explicar o que cada coisa faz sem depender de outro arquivo.
- **Edições antes de decidir.** Em alguns momentos o Claude Code alterou arquivos logo depois de receber comentários, antes de a decisão estar tomada. O estudante pediu que as ressalvas fossem discutidas primeiro e só depois aplicadas.

### Validação pela equipe (antes da entrega)

- [x] Rodar de novo com a base de 15 registros e atualizar as seções 3 e 4 de `docs/resultados_testes.md`
- [x] Acrescentar perguntas de teste para os registros novos (T16 a T31)
- [ ] Rodar `python src/testes.py` em um computador da equipe e conferir a saída
- [ ] Abrir `docs/resultados_testes.csv` no Excel e conferir acentos e números
- [x] Aplicar o roteiro de tarefas na interface (Aplicação 1)
- [ ] Aplicar o teste de facilidade de uso com uma pessoa de fora da equipe (Aplicação 2)
- [ ] Conseguir explicar `classificar`, `executar_teste` e o cálculo dos indicadores sem consultar a IA

### Limites do uso de IA nesta parte

- Os testes automatizados conferem o comportamento do assistente (estado da busca, registro encontrado e presença dos avisos). Eles não avaliam se as orientações estão corretas ou claras para o público; isso depende da conferência das fontes e do teste com usuário.
- A interpretação dos resultados foi redigida pela IA a partir de dados reais da execução e revisada pelo estudante; a responsabilidade pelas conclusões apresentadas é da equipe.

---

## Integração e preparação da entrega

### Ferramenta e materiais

- **Ferramenta:** Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com ferramenta de busca na web.
- **Data:** 18/11/2026.
- **Pedido:** deixar o repositório pronto para a entrega, seguindo o enunciado e o plano de trabalho. A interface (frente D) tem seção própria neste documento.

### O que a IA produziu e o que foi decisão da equipe

| Item | Arquivo | Origem |
| --- | --- | --- |
| Ampliação da base de 3 para 15 registros (12 novos: DOC-02 a DOC-05, SER-02 a SER-05, COM-02 a COM-05) | `data/base_conhecimento.json` | Decisão da equipe de ampliar a base; escolha dos assuntos, pesquisa das fontes oficiais e redação das orientações pela IA |
| 16 perguntas de teste novas (T16 a T31), com gabarito definido antes da execução | `data/perguntas_teste.json` | Geradas pela IA |
| Atualização dos resultados, da interpretação, das melhorias e das limitações | `docs/resultados_testes.md` | Redigidas pela IA a partir da execução real |
| Adaptação dos testes da Parte B para usarem os arquivos do repositório, sem o ZIP externo, e para a base de 15 registros | `tests/test_busca.py` | Feita pela IA a pedido do estudante |
| Comparação dos dois modelos de resposta nas 18 perguntas diretas | `docs/modelos_prompt.md` | Dados gerados com as funções da Parte C; texto e conclusão redigidos pela IA |
| Roteiro do teste de facilidade de uso | `docs/teste_usabilidade.md` | Redigido pela IA |
| Aplicação do roteiro de tarefas na interface real (Aplicação 1) | `docs/teste_usabilidade.md` | [confirmar: executada pelo estudante ou pela IA] |
| 11 reformulações de validação (T32 a T42), escritas antes da ampliação do vocabulário e com gabarito não alterado depois | `data/perguntas_teste.json` | [confirmar: geradas pela IA ou escritas pelo estudante] |
| Vocabulário do dia a dia nas palavras-chave dos 15 registros (63 palavras-chave novas) | `data/base_conhecimento.json` | Melhoria proposta na avaliação; [confirmar: termos escolhidos pela IA e aprovados pelo estudante, ou escolhidos pelo estudante] |
| Unificação dos registros de uso de IA e reorganização da pasta `docs/` | `docs/` | Feita pela IA; o estudante decidiu apagar os arquivos de origem e as evidências internas da Parte B |
| README completo | `README.md` | Redigido pela IA a partir dos documentos do projeto |

### Validação crítica realizada

| O que foi conferido | Como | Resultado |
| --- | --- | --- |
| Formato da base ampliada | `python src/base.py` | 15 registros válidos, 5 em cada tema; a base atende ao mínimo do enunciado |
| Palavras-chave dos registros novos | Antes de escrever, cada palavra-chave foi conferida contra as dos outros registros, para evitar coincidências que gerassem ambiguidade sem motivo (por exemplo, "civil", "nacional" e "gov.br" foram evitadas onde puxariam outro registro) | Restaram coincidências conhecidas e documentadas ("carteira", "conta", "direito"), que aparecem nos testes T01, T13, T19, T28 e T31 |
| Gabarito das perguntas novas | O resultado esperado foi escrito antes de rodar a busca | As previsões registradas no campo `observacao` se confirmaram, inclusive os erros esperados (T28, T29 e T31) |
| Testes automatizados de B e C | `python -B -W error -m unittest discover -s tests` | 81 de 81 testes passam, sem a variável do ZIP (92 de 92 depois da entrada dos testes da interface) |
| Efeito do vocabulário ampliado | `python src/testes.py`, antes e depois da ampliação | Reformulações de validação (T32 a T42) passaram de 0/11 para 9/11, sem nenhum falso positivo novo |

### Erros e limites encontrados

- **As fontes foram consultadas por meio de resumos da ferramenta de busca, e não pela leitura integral de cada página.** A data `18/11/2026` nos registros novos indica quando as fontes foram consultadas dessa forma. Antes da entrega, a equipe precisa abrir cada um dos 12 links e confirmar cada frase.
- **Algumas fontes são antigas ou têm informações que mudam com frequência:** a página da certidão de nascimento é uma notícia de 2021, o prazo de 7 a 120 dias do seguro-desemprego vem de uma página de perguntas antiga do Ministério do Trabalho, e os bancos aceitos para o nível prata da conta gov.br mudam com o tempo. Nessas orientações, a frase de confirmação na fonte oficial foi mantida de propósito.
- **Afirmações que não estavam nas fontes foram retiradas ou suavizadas:** por exemplo, o valor da taxa do CPF em unidades conveniadas foi substituído por "pode haver cobrança de uma taxa", e não foi afirmado que a segunda via da certidão é gratuita para todos.

### Validação pela equipe (antes da entrega)

- [ ] Abrir os 12 links novos da base e confirmar cada frase das orientações
- [ ] Conferir se as 63 palavras-chave novas fazem sentido para a orientação de cada registro
- [ ] Rodar `python src/base.py`, `python src/testes.py` e `python -B -m unittest discover -s tests` em um computador da equipe
- [ ] A pessoa da frente B revisar as adaptações em `tests/test_busca.py`
- [ ] A pessoa da frente C revisar a comparação dos modelos em `docs/modelos_prompt.md`

---

## Responsabilidade da equipe

Em todas as frentes, a IA foi uma ferramenta de apoio. A equipe é responsável por compreender, testar e justificar o código, as orientações, as fontes e os resultados apresentados, e cada integrante deve conseguir explicar a sua parte sem consultar a IA.
