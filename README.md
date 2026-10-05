# Projeto G1 — Análise de Redes Sociais e Engajamento Digital

**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python

**Professor:** Alexandre Neves Louzada

**Aluno:** Thomas Andrew de Souza Batista

Base simulada do Tema 20, 4.440 registros entre 2015 e 2024. Trabalho individual.

## Executar no computador

Instale Python 3.11 ou 3.12. Extraia o ZIP e abra um terminal na pasta `projeto-redes-sociais`.

```bash
python -m venv .venv
```

Windows: `.venv\Scripts\activate`

macOS/Linux: `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Para estudar a análise, execute `jupyter notebook notebooks/analise_redes_sociais.ipynb`. Use Kernel > Restart and Run All para reproduzir os resultados.

## Conteúdo

- app.py: dashboard com três páginas e todos os filtros obrigatórios.
- analise.py: leitura, validação, atributos, KPIs e persistência SQL.
- notebooks/analise_redes_sociais.ipynb: análise executada, com gráficos e interpretação.
- dados/: CSV original fornecido.
- imagens/: gráficos gerados com Matplotlib e Seaborn.
- database/: destino do banco SQLite, criado ao clicar no botão da página Método.
- index.html: apresentação para GitHub Pages.

## Requisitos atendidos

Python, Pandas, Matplotlib, Seaborn, Plotly e Streamlit. Intermediárias: filtros múltiplos, KPIs dinâmicos, análise temporal, comparações, gráficos interativos e download de recortes. Avançadas: dashboard multipágina e persistência SQLite com SQLAlchemy. Correlação de Pearson como análise adicional.

## Limitações e método

Dados simulados, sem campanhas identificadas. Soma de seguidores repete contas e não corresponde a pessoas únicas. Evolução usa medianas por conta/ano, sem comprovar crescimento real. Taxa informada e taxa por alcance são mantidas separadas. Médias simples por publicação. Correlação não implica causalidade. Alcance elevado: percentil 95 do recorte.

## Publicação — ainda pendente

1. Crie um repositório GitHub e envie o conteúdo desta pasta para a raiz do repositório, mantendo as subpastas.
2. Em Settings > Pages, configure a publicação a partir da branch principal e da pasta raiz. O arquivo inicial é index.html.
3. No Streamlit Community Cloud, conecte o repositório, escolha a branch principal e app.py. Use Python 3.11 ou 3.12.
4. Copie os links públicos do repositório, da página e do dashboard para a seção de links de index.html. Teste os três links sem estar conectado.

O banco local do Streamlit Cloud pode ser descartado após reinícios. O CSV mantém a reprodução da análise.

## Entrega

Links GitHub, GitHub Pages e Streamlit; notebook .ipynb; app.py; CSV. A publicação não foi realizada neste pacote. Leia o código e explique as fórmulas e as limitações antes da apresentação.
