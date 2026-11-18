# Uso de Inteligência Artificial no projeto

Registro pedido no enunciado da Global Solution 2026.2 (seção "Uso de inteligência artificial"): onde a IA foi usada, para quê e como a equipe validou o resultado. Cada parte do projeto registra o seu uso na tabela e na sua própria seção.

## Resumo

| Parte | Ferramenta | Para que foi usada | Responsável pela validação | Data |
| --- | --- | --- | --- | --- |
| A — Base de conhecimento e leitura de arquivos | Claude (Anthropic), via claude.ai | Primeira versão do código, pesquisa de 3 orientações, testes de cenários de erro, documento de conferência | Mayara — RM [preencher] | 13/11/2026 |
| B — [preencher] | | | | |
| C — Lógica de resposta e estratégias de prompts | ChatGPT (OpenAI) | A IA foi utilizada para elaborar e comparar modelos de prompts, definir instruções para o assistente, revisar textos e documentações, preparar cenários e testes automatizados e analisar a integração da Parte C com o formato de retorno da Parte B | Pietra Fanticelli - RM 573229 | 18/11/2026 | 
| D — [preencher] | | | | |

## IA dentro do protótipo

A Parte A não chama nenhum modelo de IA durante a execução. As orientações vêm somente do arquivo `data/base_conhecimento.json`, que guarda textos conferidos em fontes oficiais. Por isso, na Parte A, não existem respostas de modelo externo para confrontar com a base.

Se outra parte usar um modelo de IA no protótipo, ela deve descrever aqui como as respostas dele são comparadas com a base verificada (enunciado, seção "Uso de inteligência artificial").

---

## Parte A — Base de conhecimento e leitura de arquivos

### Ferramenta e materiais

- **Ferramenta:** Claude (Anthropic), no claude.ai. Modelos usados na conversa: Claude Fable 5.2 (código e base) e Claude Opus 5.5 (documento de conferência e este registro).
- **Data:** 13/11/2026.
- **Materiais entregues à IA:** o enunciado da Global Solution 2026.2 e o PDF com o material das aulas das fases 4, 5 e 6.
- **Dados pessoais:** nenhum dado de usuários do assistente foi usado ou enviado.

### O que foi pedido

Resumo do pedido feito à IA:

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

## Parte B — [nome da parte]

- **Ferramenta e data:**
- **Para que foi usada:**
- **O que foi decisão da equipe:**
- **Validação crítica realizada:**
- **Erros da IA encontrados:**

## Parte C — Lógica de resposta e estratégias de prompts

- **Ferramenta e data:**
  - Ferramenta: ChatGPT (OpenAI).
  - Data: 18/11/2026
- **Para que foi usada:**
  - Elaborar e comparar dois modelos de prompt: um objetivo e direto e outro didático e passo a passo.
  - Sugerir instruções para definir o papel do assistente, o formato das respostas e cuidados para evitar informações inventadas.
  - Revisar textos, mensagens, avisos e a documentação da Parte C.
  - Apoiar a identificação de cenários de teste e a preparação dos testes automatizados em `tests/testes_resposta.py`, com registros simulados.
  - Apoiar a análise da integração da Parte C com o formato de retorno da Parte B.
- **O que foi decisão da equipe:**
  - Definir e utilizar as estratégias de resposta objetiva e didática como modelos documentados para o assistente.
  - Conferir a compatibilidade dos campos utilizados pela Parte C com a estrutura da Parte A.
  - Manter a revisão humana como parte necessária da validação das respostas, fontes e orientações.
  - Tratar os prompts como instruções documentadas em texto: o protótipo não realiza chamada a uma API externa de IA.
  - Adaptar a Parte C ao retorno da Parte B, que contém `estado` e `resultados`, com o registro dentro do campo `registro`, incluindo tratamento para múltiplas      correspondências sem selecionar automaticamente a primeira.
- **Validação crítica realizada:**
  - As sugestões da IA foram revisadas e comparadas com a estrutura e os arquivos do projeto.
  - Foram conferidos os campos `id`, `tema`, `palavras_chave`, `orientacao`, `referencia` e `data_verificacao`.
  - Foi verificado que os 3 registros disponíveis no JSON seguem a estrutura esperada e abrangem os temas Documentos, Serviços e Orientações comunitárias.
  - Os testes automatizados da Parte C foram executados: **15 de 15 passaram** no ambiente utilizado, com dados simulados.
  - Também foi realizada uma execução local A → B → C com os arquivos disponibilizados, verificando consultas com uma, múltiplas e nenhuma correspondência.
  - Foi identificado que a base possui somente 3 registros, embora o `base.py` indique o mínimo de 15 registros em 3 temas. Portanto, a base ainda precisa ser ampliada.
  - Os testes simulados e a execução local não substituem a validação ponta a ponta com a base ampliada, a interface e as versões finais de todas as partes.
- **Erros da IA encontrados:**
  - **Detecção de confirmação por trecho de texto:** foi sugerido procurar uma palavra como “confirm” para identificar a necessidade de confirmação. Essa abordagem poderia gerar falsos positivos ou deixar passar outros avisos. A lógica foi simplificada para apresentar um aviso uniforme, sem depender dessa busca.
  - **Conclusões além do que os testes demonstravam:** resultados com registros simulados não comprovavam a integração com a base real. Por isso, foi necessário distinguir os testes automatizados da verificação com os arquivos reais.
  - **Limitação de avaliação automática:** critérios que verificam apenas a presença de fonte, link, data e avisos não garantem que a orientação esteja correta ou seja fácil de entender. Foi mantida a necessidade de avaliação humana.

A equipe permanece responsável por compreender, revisar, testar e validar o código, as respostas e as fontes utilizadas no projeto.

## Parte D — [nome da parte]

- **Ferramenta e data:**
- **Para que foi usada:**
- **O que foi decisão da equipe:**
- **Validação crítica realizada:**
- **Erros da IA encontrados:**
