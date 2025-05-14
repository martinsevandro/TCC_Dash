#imports
from dash import html, dcc
import dash_bootstrap_components as dbc

import pickle
def load_sub_dataframes():
    # Importando o dicionário de dataframes
    file_path = "../../datasets/processados/sub_dataframes.pkl"
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# Carregar o dicionário de dataframes
sub_dataframes = load_sub_dataframes()

#objetos
bimestres = [1, 2, 3, 4]

disciplinas = ['port', 'cien', 'edfi', 'geog', 'hist', 'mate', 'ingl', 'arte', 'reli']


#function aux
def criar_card(titulo, descricao, icone, cor, link):
    """
    função usada para criar os cards clicáveis no página inicial.

    - titulo (str): Título do card.
    - descricao (str): Texto descritivo do card.
    - icone (str): Caminho do ícone SVG na pasta /assets/icons/.
    - cor (str): Cor do card, deve ser uma das cores do Bootstrap ('primary', 'warning', 'success').
    - link (str): URL para onde o card redireciona.

    """
    return dbc.Col(
        dbc.Card(
            dcc.Link(
                dbc.CardBody(
                    dbc.Row(
                        [
                            # Ícone do card
                            dbc.Col(
                                html.Div(
                                    html.Img(
                                        src=f"/assets/icons/{icone}.svg",
                                        style={"width": "3rem", "height": "3rem"},
                                        alt=f"Ícone {titulo}"
                                    ),
                                    className="d-flex align-items-center justify-content-center",
                                    style={"height": "100%"}  
                                ),
                                width=2,
                                className=f"bg-{cor} text-center"
                            ),
                            # Conteúdo do card
                            dbc.Col(
                                html.Div([
                                    html.H4(titulo, className="card-title text-white"),
                                    html.P(descricao, className="card-text abnt-text text-white"),
                                ]),
                                width=10,
                                className="d-flex flex-column justify-content-center"
                            ),
                        ]
                    )
                ),
                href=link,
                className="stretched-link"  #  card clicavel
            ),
            body=True,
            color=cor,
            style={"max-width": "100%"}  
        ),
        width=8,
        className="mb-4",
        style={"display": "flex", "justifyContent": "center"}  
    )

# function aux
def criar_dropdown(id_dropdown, opcoes, valor_inicial, titulo):
    """
    Cria um dropdown estilizado com título.

    Parâmetros:
    - id_dropdown (str): ID do componente.
    - opcoes (list[dict]): Lista de opções no formato [{'label': 'Texto', 'value': 'valor'}].
    - valor_inicial (str): Valor inicial selecionado.
    - titulo (str): Título do dropdown.

    Retorno:
    - html.Div: Componente contendo título e dropdown.
    """
    return html.Div([
        html.H4(titulo, className="mb-2"),
        dcc.Dropdown(
            id=id_dropdown,
            options=opcoes,
            value=valor_inicial,
            className="themed-dropdown",
            clearable=False
        )
    ], className="mb-3")

# function aux
def criar_grafico(id_grafico, altura=None):
    """
    criar um gráfico responsivo com dcc graph.

    Parâmetros:
    - id_grafico (str): ID do gráfico.
    - altura (str): Altura do gráfico (padrão: '400px').

    Retorno:
    - dcc.Graph: Componente gráfico.
    """
    estilo = {'width': '100%'}
    if altura:
        estilo['height'] = altura  # Apenas define altura se for passado

    return dcc.Graph(id=id_grafico, style=estilo)


# pagina inicial
def inicial_pagina():
    """
    página inicial do dashboard, com cads descritivos para as demais páginas 
    """
    cards_info = [
        {
            "titulo": "GERAL",
            "descricao": "Acompanhe o desempenho ao longo do tempo. Veja como cada disciplina evoluiu nos últimos anos, analise o panorama geral das turmas ou aprofunde-se nos detalhes.",
            "icone": "icone_geral",
            "cor": "primary",
            "link": "/Geral"
        },
        {
            "titulo": "BIMESTRAL",
            "descricao": "Avalie o desempenho de cada disciplina em cada bimestre, visualize padrões gerais e aprofunde-se no comportamento das disciplinas ao longo do ano.",
            "icone": "icone_semestre",
            "cor": "warning",
            "link": "/Bimestral"
        },
        {
            "titulo": "PERFIL",
            "descricao": "Explore a distribuição de idades nas turmas, identifique padrões e discrepâncias, e analise a quantidade de alunos por turma, acompanhada da taxa de aprovação geral, calculada com base nas notas bimestrais.",
            "icone": "icone_perfil",
            "cor": "success",
            "link": "/Perfil"
        }
    ]

    return html.Div([
        dbc.Container(
            [
                # Título
                dbc.Row(
                    dbc.Col(
                        html.H1("EDUC_PLOTS", className="text-center display-4 text-primary"),
                        width="auto",
                    ),
                    justify="center"
                ),
                # Subtítulo
                dbc.Row(
                    dbc.Col(
                        html.P("Bem-vindo ao Dashboard de Análise de Notas!", className="text-center mb-4"),
                        width="auto"
                    ),
                    justify="center"
                ),
                # Renderizacão dinamica dos cards pra evitar repeticoess
                *[dbc.Row(criar_card(**card), justify="center") for card in cards_info],
            ],
            className="mt-5",
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "width": "100%",
                "maxWidth": "1200px",
                "padding": "1rem",
            }
        ),
    ],
        style={
            "height": "100vh",
            "overflow": "auto",
            "overflowX": "hidden",
            "margin": "0",
            "padding": "0",
        },
        id="page-inicial",
        className="no-scroll",
    )



# pagina geral
def geral_pagina():
    """
    pagina de análise geral, organizando gráficos e controles de seleção.

    1. **Médias Finais da Disciplina**:
        - Exibe um gráfico de linhas representando a evolução das médias finais das disciplinas ao longo do tempo.

    2. **Médias por Turma**:
        - Permite selecionar uma turma específica para visualizar a distribuição das médias.
        - Inclui um dropdown para selecionar a turma desejada.
        - Exibe um gráfico de barras horizontal.

    3. **Boxplot de Médias Gerais por Disciplina**:
        - Permite analisar a distribuição das médias gerais de cada disciplina.
        - Inclui um dropdown para selecionar a disciplina desejada.
        - Exibe um boxplot para análise detalhada.
    """

    # Opções do dropdown de turmas
    opcoes_turmas = [{'label': str(turma), 'value': turma} for turma in sub_dataframes.keys()]
    turma_inicial = list(sub_dataframes.keys())[0]

    # Opções do dropdown de disciplinas (usando a variável existente)
    opcoes_disciplinas = [{'label': disc, 'value': disc} for disc in disciplinas]

    return dbc.Container([
        html.H3("Médias Finais da Disciplina", className="mb-4"),

        # Linha 1: Gráfico de Médias Finais
        dbc.Row([
            dbc.Col(criar_grafico('lineplot-output-page-1', altura="400px"))
        ], className="mb-4"),

        # Linha 2: Gráfico de Médias por Turma
        dbc.Row([
            dbc.Col([
                criar_dropdown('media-horizontal-page-1b', opcoes_turmas, turma_inicial, "Especificando a turma - (Média das Notas)"),
                criar_grafico('plot-horizontal-page-1b', altura="400px")
            ]),
        ], className="mb-4"),

        # Linha 3: Boxplot de Médias Gerais por Disciplina
        dbc.Row([
            dbc.Col([
                criar_dropdown('discipline-dropdown-page-3', opcoes_disciplinas, 'port', "Detalhado - Médias Gerais por Disciplina"),
                criar_grafico('boxplot-output-page-3', altura="400px")
            ]),
        ], className="mb-4"),

    ], className="page-content", fluid=True)


# pagina bimestral 
def bimestral_pagina():
    """
    página de análise bimestral, organizando os gráficos e seleções necessários.

    1. **4 Bimestres por Disciplina**:
        - Apresenta a média das notas ao longo dos quatro bimestres para uma disciplina selecionada.
        - Inclui um dropdown para seleção da disciplina.
        - Exibe um gráfico de linhas.

    2. **Bimestrais Detalhado (Boxplot)**:
        - Permite a análise detalhada de uma disciplina em um bimestre específico.
        - Inclui dropdowns para selecionar tanto a disciplina quanto o bimestre desejado.
        - Exibe um gráfico do tipo boxplot.

    3. **Bimestre Crítico (Heatmap)**:
        - Mostra um mapa de calor com as médias das notas para identificar os bimestres mais críticos.
        - Exibe um gráfico de heatmap.
    """
    return html.Div([
        ## Seção 1: 4 Bimestres por Disciplina
        html.H3("4 Bimestres por Disciplina - (Média das Notas)"),
        
        criar_dropdown('discipline-dropdown-page-2a', disciplinas, 'port', ""),
        
        criar_grafico('lineplot-output-page-2a'),
               
        #Seção 2: Bimestrais Detalhado (Boxplot)
        html.Br(), 
        html.H3("Detalhado - Especificar Bimestre e Disciplina - (dados bimestrais)"),
        
        criar_dropdown('discipline-dropdown-page-4', disciplinas, 'port', ""),
        criar_dropdown('bimestre-dropdown-page-4', bimestres, 1, ""),
        
        criar_grafico('boxplot-output-page-4'),
       
        ##Seção 3: Bimestre Crítico - Heatmap
        html.Br(), 
        html.H3("Bimestre Crítico - (Média das Notas)"),
        
        criar_grafico('bimestre-critico-page'),
        
    ],
        className="page-content"
    )


# pagina perfil
def perfil_pagina():
    """
    página de análise de perfil dos alunos.

    1. **Comparativo de Idades por Turma**:
        - Exibe um gráfico histograma para comparar a distribuição das idades entre as turmas.

    2. **Distribuição Geral de Idades**:
        - Apresenta a distribuição de idades dos alunos no contexto geral, através de um boxplot.

    3. **Perfil de Aprovação**:
        - Mostra a relação entre idade, quantidade de alunos por turma e taxa de aprovação dos alunos.
        - Usando gráfico de barras coloridas, na escala de gradiente do azul para a taxa de aprovação.
    """
    return html.Div([
        html.H3("Comparativo de Idades por Turma"),
        
        criar_grafico('histograma_idade_turma'), #histograma_idade_turma
        
        criar_grafico('boxplot_idade_turma'), #boxplot_idade_turma
        
        criar_grafico('perfil_aprovacao_page'), #alunos_e_taxa_aprovacao
    ],
        className="page-content" 
    )
