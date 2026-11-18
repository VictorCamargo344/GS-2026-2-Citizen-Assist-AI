# Verificação da entrega — Parte B

## Materiais e ambiente

Foram relidos o enunciado, o plano do grupo e os três arquivos do ZIP recebido
como A. Não foram alterados o ZIP de origem ou os arquivos de outro trabalho
existentes na pasta principal.

- Ambiente executado: Windows, Python **3.12.10**, biblioteca padrão.
- Referência de data da sessão: **17/11/2026**, America/Sao_Paulo.
- Parte A: **3 registros válidos em 3 temas**.
- SHA-256 do ZIP original de A:

```text
9b76aff77563b932b7f6c84cff0e5e9ff1365c89423a58d3c6eff64e02e2a807
```

O hash identifica o arquivo recebido, não comprova a atualidade das orientações.
A integração copiou apenas os bytes originais de `base.py` e do JSON para
`src/` e `data/` temporários, importou o módulo real e chamou `carregar_base`
e `validar_registros`. Não usou substitutos dessas funções.

## Comando executado

Na raiz da pasta desta entrega, no PowerShell:

```powershell
$env:CITIZEN_PARTE_A_ZIP = 'C:\Users\Gabriel Luis\Downloads\Parte A.zip'
python -B -W error -m unittest discover -s tests -v
```

## Resultados

| Grupo | Métodos implementados | Executados e aprovados |
| --- | --- | --- |
| Testes unitários de B com fixtures fictícias | 48 | 48 |
| Integração com A original | 10 | 10 |
| Total | **58** | **58** |

Não houve teste ignorado na execução de aprovação, falha ou erro. Alguns
métodos contêm vários subcasos; eles não foram somados como novos métodos.
A saída detalhada está em `resultados_execucao.txt`.

Os 48 testes unitários usam dados fictícios `FIC-*`, com textos explicitamente
marcados como fictícios e fonte `example.invalid`. Mesmo nesses casos, as
funções de normalização e acesso da dependência A são as originais. Os dez
testes de integração carregam a base real recebida.

Além da suíte, foram registradas **15 consultas** ao algoritmo com a base real,
incluindo perguntas diretas, pontuação/acentos, empates, entrada vazia, tipo
inadequado, perguntas fora da base e repetição de palavras. O arquivo
`consultas_verificadas.json` contém entrada, resultado esperado, obtido e
classificação de cada consulta. São evidências adicionais de B, não 15 novos
registros de conhecimento e não uma avaliação geral da frente E.

O controle sem `CITIZEN_PARTE_A_ZIP` falhou explicitamente na preparação,
conforme esperado. Esse controle confirma que a ausência da dependência não
é silenciosamente convertida em aprovação de integração.

A primeira execução passou, mas revelou um aviso de barra invertida na
docstring dos testes. O texto foi corrigido e a execução acima trata avisos
como erros. A contagem das palavras ignoradas foi conferida: **34**.

## Cobertura e limites da evidência

| Comportamento | Evidência principal |
| --- | --- |
| Acesso por ID, tema e palavra-chave; valores inexistentes | Testes unitários e consultas dos três registros reais |
| Perguntas, palavras inteiras e expressões | Pontuações esperadas explícitas, caso sem substring e semântica não inferida |
| Caixa, acentos, pontuação e espaços | Subcasos de normalização; palavra-chave exata mantém o contrato de A |
| Entrada vazia/tipo inadequado e filtros | Matriz das quatro funções de consulta e filtros opcionais |
| Repetições, ordenação, empates e várias correspondências | Testes com ordem da base invertida e resultados de pontuações diferentes |
| Hierarquia e navegação entre três assuntos | Percurso dos IDs reais e casos sintéticos do mesmo tema |
| Inclusão de novos dados | Fixture com novo registro e novo tema, sem alterar o algoritmo |
| Preservação de dados/fontes e separação de metadados | Comparação antes/depois, identidade do registro e validação por A após consultas |
| Importação sem interação ou leitura de base | Processo novo sem JSON disponível e carregamento de base proibido no teste |
| Código de A preservado | Comparação byte a byte das cópias e SHA-256 do ZIP original |

Nenhum teste comprova compreensão semântica, revisão humana ou conteúdo factual
das páginas cidadãs. Não foram calculadas taxa geral de acerto, média de tempo
de consulta ou facilidade de uso do sistema. O tempo mostrado pelo `unittest`
é duração da suíte, não tempo médio de resposta ao cidadão.

Os blocos Python do guia foram conferidos com a A recebida, e os links locais
da documentação foram verificados. A revisão é técnica; o estudante ainda
precisa estudar e conseguir explicar o conteúdo.

## Conferência do ZIP final

Pacote: `Citizen_Assist_AI_Parte_B.zip`, com uma única pasta principal de mesmo
nome. Foram conferidos:

- Os **9 arquivos** documentados no README, todos com conteúdo.
- Correspondência byte a byte entre os arquivos finais da pasta e os do ZIP.
- Integridade do ZIP e caminhos relativos dentro da única pasta principal.
- Ausência de A, JSON de conhecimento, aplicação completa ou outros trabalhos.
- Ausência de `.pyc`, `__pycache__`, arquivos temporários e ambientes virtuais.
- Reexecução dos **58 testes** em uma cópia extraída do ZIP, com A fornecida
  externamente, também sem falhas, erros ou testes ignorados.

A reexecução do ZIP verifica a entrega embalada; não dobra a quantidade de
métodos implementados. A saída detalhada distribuída refere-se à execução na
pasta de trabalho, e os dois comandos usam o mesmo código final.

## Pendências do grupo

A conclusão desta parte não conclui a Global Solution. Permanecem a ampliação
para pelo menos 15 orientações, revisão das fontes e palavras-chave, integração
de C/D, avaliação geral de E, dados da equipe, README final, vídeo e publicação.
O arquivo `sistema.py` e o comando final pertencem à integração do grupo.
