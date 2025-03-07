#imports
from dash import Input, Output, State    # dash e seus componentess
import plotly.graph_objects as go   # graficos com plotly
from src.visualization.functions import (plot_4_bimestres_disciplina_por_turma_plotly, 
                                         plot_boxplot_com_interatividade, 
                                         plot_boxplot_disc_bim_interativo, 
                                         plot_alunos_e_taxa_aprovacao, 
                                         plot_boxplot_idade_turma, 
                                         plot_histogram_idade_turma, 
                                         plot_medias_disciplina_por_turma, 
                                         plot_medias_todas_disciplinas_plotly, 
                                         plot_heatmap_bimestres_criticos
)

def register_callbacks(app, sub_dataframes):
    """
    todos os callbacks para a aplicação Dash, como o tema da página e seus gráficos correspondentes.

    Args:
        app (dash.Dash): instância da aplicação Dash
        sub_dataframes (dict): dicionário com os dataframes processados
    """
    
    # mudança html geral
    @app.callback(
        Output('body', 'className'),  # att a classe do body
        Input('theme-store', 'data')  # tema armazenado no store
    )
    def update_theme_class(theme):
        """
        atualiza a classe CSS do body com base no tema atual.

        Args:
            theme (str): Tema atual ('light' ou 'dark').

        Returns:
            str: Classe CSS correspondente ao tema.
        """
        return f"{theme}-theme"


    # mudanca estilo da pagina de conteúdo com base no tema
    @app.callback(
        Output('page-content', 'style'),  # att o estilo da pagina
        [Input('theme-store', 'data')]    # pega o tema armazenado ('light' ou 'dark')
    )
    def update_page_style(theme):
        # att o estilo da página com base no tema selecionado.
        if theme == 'dark':
            return {
                'backgroundColor': '#1e1e1e',  # Fundo escuro
                'color': 'white'  # Cor do texto
            }
        else:
            return {
                'backgroundColor': '#FFFFFF',  # Fundo claro
                'color': 'black'  
            }


    # muda tema com switch - funcional
    # callback para alternar o tema
    @app.callback(
        Output('theme-store', 'data'),  # altera o estado do tema
        Input('theme-switch', 'on'),    # estado do botão de switch 
    )
    def toggle_theme(on):
        # alterna o tema da aplicação entre 'light' e 'dark' com base no estado do switch, on e off.
        return 'dark' if on else 'light'


    # pagina geral
    ## medias finais por disciplina - grafico de linha
    @app.callback(
        Output('lineplot-output-page-1', 'figure'),     # att o grafico de linha
        [Input('theme-store', 'data')]
    )
    def update_boxplot_page_1(tema):
        """
        atualiza o gráfico de médias finais por disciplina (primeiro grafico da página geral).
        """
        try:
            fig = plot_medias_todas_disciplinas_plotly(sub_dataframes, tema)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()
        

    ## medias finais por disciplina especificando a turma - grafico de barras horizontais
    ### Callback para preencher as opções do dropdown
    @app.callback(
        Output('plot-horizontal-page-1b', 'figure'),
        [Input('media-horizontal-page-1b', 'value'),
         Input('theme-store', 'data')
         ]
    )
    def update_grafico_medias_disciplina(turma, theme):
        """
        atualiza o grafico de barras horizontais (segundo grafico da página geral).
        """
        try:
            fig = plot_medias_disciplina_por_turma(sub_dataframes, turma, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()

    
    ## medias gerais por disciplina - bloxplot
    @app.callback(
        Output('boxplot-output-page-3', 'figure'),
        [
            Input('discipline-dropdown-page-3', 'value'),  # dsciplina selecionada
            Input('theme-store', 'data')
        ]
    )
    def update_boxplot_page_3(discipline, tema):
        """
        atualiza o grafico bloxplot (terceiro grafico da página geral).
        """
        try:
            fig = plot_boxplot_com_interatividade(sub_dataframes, discipline, tema)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()



    # pagina bimestral   
    ## 4 bimestres ao longo dos anos especificando a disciplina (bimestre critico) - grafico de linha
    @app.callback(
        Output('lineplot-output-page-2a', 'figure'),
        [
            Input('discipline-dropdown-page-2a', 'value'),  # Valor selecionado do dropdown de disciplina
            Input('theme-store', 'data')  # tema armazenado no Store
        ]
    )
    def update_lineplot_page_2a(discipline, theme):
        """
        atualiza o grafico de linhas (primeiro grafico da página bimestral).
        """
        try:            
            fig = plot_4_bimestres_disciplina_por_turma_plotly(sub_dataframes, discipline, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()  # pra retornar um gráfico vazio em caso de error



    ## especificando a disciplina e o bimestre - boxplot
    @app.callback(
        Output('boxplot-output-page-4', 'figure'),
        [Input('discipline-dropdown-page-4', 'value'),
         Input('bimestre-dropdown-page-4', 'value'),
         Input('theme-store', 'data')
        ]
    )
    def update_boxplot_page_4(discipline, bimestre, theme):
        """
        atualiza o gráfico de boxplot (segundo grafico da página bimestral).
        """
        try:
            fig = plot_boxplot_disc_bim_interativo(sub_dataframes, discipline, bimestre, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()

    ## bimestre critico x disciplina - mapa de calor
    @app.callback(
        Output('bimestre-critico-page', 'figure'),
        [Input('bimestre-critico-page', 'id'),
         Input('theme-store', 'data')
        ]
    )
    def update_bimestre_critico_page(_, theme):
        """
        atualiza o gráfico heatmap (terceiro gráfico da página bimestral).
        """
        try:
            fig = plot_heatmap_bimestres_criticos(sub_dataframes, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()


    # pagina perfil
    ## distribuicao as idades por turmas - histograma colorido
    @app.callback(
        Output('histograma_idade_turma', 'figure'),
        [Input('histograma_idade_turma', 'id'),
         Input('theme-store', 'data') 
        ]
    )
    def update_histograma_idade_turma(_, theme):
        # att o histograma de idades
        try:
            fig = plot_histogram_idade_turma(sub_dataframes, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()
        

    ## detalhando idades por turmas - boxplot
    @app.callback(
        Output('boxplot_idade_turma', 'figure'),
        [Input('boxplot_idade_turma', 'id'),
         Input('theme-store', 'data')
        ]
    )
    def update_boxplot_idade_turma(_, theme):
        ##  att o boxplot de idades
        try:
            fig = plot_boxplot_idade_turma(sub_dataframes, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()
        

    ## quantidade de alunos e taxa de aprovados - histograma
    @app.callback(
        Output('perfil_aprovacao_page', 'figure'),
        [Input('perfil_aprovacao_page', 'id'),
         Input('theme-store', 'data') 
        ]
    )
    def update_perfil_aprovacao_page(_, theme):
        ##  att graf de barras sobre qtd de alunos por turma e sua taxa de aprovação correspondente
        try:
            fig = plot_alunos_e_taxa_aprovacao(sub_dataframes, theme)
            return fig
        except Exception as e:
            print(f"Erro: {e}")
            return go.Figure()
        