# Uso de IA — Parte B

## Identificação e finalidade

- **Parte:** B — Consulta, navegação e algoritmos.
- **Ferramenta utilizada:** Codex, assistente da OpenAI, neste chat.
- **Data de referência da sessão:** 17/11/2026, America/Sao_Paulo.
- **Versão exata do modelo:** não registrada neste documento.
- **Materiais:** enunciado em texto, plano de trabalho do grupo e ZIP de A.

O usuário autorizou a geração do código e da documentação, limitada à parte B.
A ferramenta auxiliou na leitura dos requisitos, definição das funções,
implementação da busca, hierarquia e navegação, elaboração dos testes, execução
das verificações e organização do pacote.

Não há IA executando consultas no protótipo. O código usa as orientações já
presentes em A, sem chamar um serviço externo ou gerar novos conteúdos cidadãos.
Não houve coleta de dados pessoais de usuários do assistente.

## Decisões aprovadas pelo usuário

- Entregar somente B, testes e guia de integração, sem aplicação demonstrável.
- Preservar os arquivos de A e os trabalhos de outra atividade na pasta local.
- Usar Python com biblioteca padrão e explicações apropriadas ao início do curso.
- Usar os três registros recebidos para integração, sem ampliar a base nesta parte.
- Manter as demais frentes sob responsabilidade do grupo.

## Decisões técnicas propostas e implementadas pela ferramenta

- Reutilizar as consultas exatas e a normalização disponíveis em A.
- Buscar perguntas por palavras úteis e expressões de `palavras_chave`.
- Somar 1 ponto por termo útil distinto e 2 por expressão composta distinta.
- Devolver todas as correspondências positivas, ordenadas por pontos e ID.
- Organizar raiz → tema → assunto fora dos registros validados de A.
- Oferecer navegação do mesmo tema e exploração dos demais temas, sem afirmar
  dependências entre os serviços.
- Registrar estados de consulta e preservar os dados e referências recebidos.

Essas escolhas estão descritas em `parte_b.md` e devem ser estudadas e revisadas
pelo estudante antes da apresentação. Não se afirma que houve aprovação humana
individual de cada linha de código.

## Validação crítica executada

| Verificação | Evidência |
| --- | --- |
| Compatibilidade com A | Importação do módulo original e leitura/validação dos registros reais em pasta temporária |
| Comportamentos de B | Suíte `unittest` com casos sintéticos e integração; saída em `resultados_execucao.txt` |
| Consultas e ambiguidades | IDs, estados e pontuações comparados com expectativas explícitas |
| Preservação dos dados | Comparação dos registros antes/depois e dos bytes dos arquivos de A |
| Ausência de interface no núcleo | Teste de importação em processo novo e operações sem input/saída |
| Manutenção | Inclusão fictícia de novo registro e tema, sem alterar o algoritmo |
| Limitações | Documentadas coincidência lexical, ausência de semântica/sinônimos automáticos e base incompleta |
| Empacotamento | Conferência final descrita em `verificacao.md` |

Os dados `FIC-*` e a fonte `example.invalid` existem somente nos testes. Não
foram produzidas novas orientações para completar os 15 registros.

## Ajustes encontrados durante a revisão

Na primeira execução dos testes, todos passaram, mas Python emitiu um aviso
por uma barra invertida no exemplo de caminho da docstring de testes. A
docstring foi ajustada para texto bruto (`r"""..."""`) e a suíte foi verificada
com avisos tratados como erros. A contagem das palavras ignoradas na explicação
também foi conferida para corresponder às 34 entradas do código.

Esses registros descrevem revisão automatizada da ferramenta. Não equivalem
a revisão humana ou teste com um cidadão.

## Validação humana e do grupo ainda necessária

- Estudar e conseguir explicar funções, pontos, empates e navegação.
- Revisar a adequação dos termos e da linguagem ao público do projeto.
- Conferir a atualidade das orientações nas fontes oficiais recebidas de A.
- Ampliar a base para pelo menos 15 registros.
- Integrar e avaliar as partes C, D e E com a base final.
- Fazer a avaliação de facilidade de uso prevista no enunciado.

As fontes cidadãs não foram reabertas nesta implementação de B. A preservação
dos textos não é uma nova certificação de seu conteúdo ou de suas datas.
Também não foi disponibilizado o material completo das aulas nesta sessão;
a adequação de nível foi orientada pelos requisitos e pelo pedido do usuário,
sem alegar uma conferência página a página das apostilas.

## Como incorporar ao documento do grupo

Preserve `docs/uso_ia.md` da colega. Na integração, acrescente a este documento
uma seção intitulada **Parte B — Consulta, navegação e algoritmos**, incorporando
o conteúdo deste registro. Na tabela-resumo, registre Codex/OpenAI, a finalidade,
a data e o responsável humano somente quando o grupo preencher e validar esse
dado. Não atribua à colega a validação da parte B nem substitua o histórico de A.
