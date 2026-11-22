# Contraplano

Blog de críticas e resenhas de cinema, feito com [Jekyll](https://jekyllrb.com/) e publicado de graça pelo GitHub Pages.

## Como publicar um texto novo

1. Abra a pasta **`_posts`** aqui no GitHub.
2. Clique em **Add file → Create new file**.
3. Dê um nome no formato **`ANO-MÊS-DIA-titulo-do-texto.md`**, por exemplo `2026-12-05-aftersun.md`. A data do nome é a data de publicação, e o resto vira o endereço do texto.
4. Copie o conteúdo do arquivo **`modelo-de-texto.md`**, cole e troque pelos dados do seu filme e pelo seu texto.
5. Clique em **Commit changes**. Em 1 ou 2 minutos o texto aparece no site.

> Atenção: texto com data no futuro só aparece no site quando chegar aquele dia.

Para **editar** um texto: abra o arquivo em `_posts`, clique no lápis (Edit), mude e faça **Commit changes**.
Para **apagar**: abra o arquivo, clique nos três pontinhos e em **Delete file**.

## Campos do topo de cada texto

| Campo     | O que é                                                        |
|-----------|----------------------------------------------------------------|
| `title`   | Título do seu texto                                             |
| `filme`   | Nome do filme (aparece grande)                                  |
| `ano`     | Ano do filme                                                    |
| `direcao` | Quem dirigiu                                                    |
| `nota`    | De 0.5 a 5 (use ponto: `4.5`). Apague a linha se não quiser nota |
| `cor`     | Cor da página: `rosa`, `azul`, `amarelo`, `menta`, `laranja` ou `lilas` |
| `tags`    | Entre colchetes e separadas por vírgula: `[Drama, Cannes 2026]` |

## Formatação do texto

- Linha em branco entre parágrafos.
- `*itálico*` (bom para nomes de filmes) e `**negrito**`.
- `> ` no começo da linha para uma citação.

## Outras mudanças

- **Nome do blog, frase de apresentação, autor, cor da página inicial e links**: arquivo `_config.yml`.
- **Texto da página Sobre**: arquivo `sobre.md`.
- **Visual**: `assets/style.css`.
