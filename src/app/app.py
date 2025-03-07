#imports
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) # adicionar diretorios ao PATH para importaçoes

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output # para callback
from src.app.layouts import inicial_pagina, geral_pagina, bimestral_pagina, perfil_pagina
from src.app.callbacks import register_callbacks # gerenciar estados callback
import pickle # para chamar os dados serializados
from src.data.processamento import processa_dados
from dash import State
import dash_daq as daq # botao booleanswitch trocar tema 
 

# processamento dos dados antes de carregá-los ( do arquivo em ../../datasets/brutos/Dataset_Boletim_Completo.csv )
processa_dados()

# carregar dataframes processados a partir do arquivo .pkl
def load_sub_dataframes():
    file_path = "../../datasets/processados/sub_dataframes.pkl"
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# carregar o dicionario de dataframes processados
sub_dataframes = load_sub_dataframes()

# configuração do aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# layout da pagina
app.layout = html.Div(        
    id="body",   
    className="light-theme",   
    children=[        
        # salva o tema atual
        dcc.Store(id='theme-store', data='light'),

        # rastreia a URL atual para navegar entre as paginas
        dcc.Location(id='url', refresh=False),
            
        # Barra de navegação
        dbc.NavbarSimple(
            children=[
                    dbc.Row(
                        [
                            # navbar paginas
                            dbc.Col(dbc.NavItem(dbc.NavLink("Inicial", href="/"))),
                            dbc.Col(dbc.NavItem(dbc.NavLink("Geral", href="/Geral"))),
                            dbc.Col(dbc.NavItem(dbc.NavLink("Bimestral", href="/Bimestral"))),
                            dbc.Col(dbc.NavItem(dbc.NavLink("Perfil", href="/Perfil"))),
                            
                            # switch para alterar entre modo escuro e claro
                            dbc.Col(
                                dbc.NavItem(
                                    daq.BooleanSwitch(
                                        id='theme-switch',
                                        on=False,  
                                        labelPosition='top'
                                    )
                                ),
                                width="auto",  
                                className="ml-auto d-flex align-items-center"  
                            ),
                        ],
                        align="center",  
                        justify="start",  
                        
                    ),
            ],
            brand="EDUC_PLOTS",
            brand_href="/",
            color="#007bff",
            dark=True,
            id='navbar',
            fluid=True,
            class_name="navbar-custom",
            className="navbar-custom",
            expand="md",  
        ), 
        
        # exibir aqui o conteúdo       
        html.Div(id='page-content', style={"flex-grow": "1"}),

        
    ]
)

# callback para ativar/des scroll
@app.callback(
    Output("page-content", "className"),
    Input("url", "pathname")
)
def update_page_class(pathname):
    if pathname == "/":  # pagina inicial
        return "no-scroll"
    else:  # outras páginas
        return "with-scroll"

# callback para alternar entre as paginas
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Geral':
        return geral_pagina()
    elif pathname == '/Bimestral':
        return bimestral_pagina()
    elif pathname == '/Perfil':
        return perfil_pagina()
    else:
        return inicial_pagina()

# registrar callbacks adds
register_callbacks(app, sub_dataframes)

# executar
if __name__ == '__main__':
    app.run_server(debug=True)
