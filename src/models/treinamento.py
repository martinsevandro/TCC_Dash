# #%%
# import pandas as pd

# # Supondo que df_horizontal seja o seu DataFrame no formato horizontal
# df_horizontal = pd.read_csv('../../datasets/processados/df_horizontal.csv')

# df_horizontal.head()    

# #%%

# import pandas as pd

# # Supondo que 'df_horizontal' seja o DataFrame horizontal com notas dos bimestres
# # Filtrar apenas as colunas de notas das disciplinas
# disciplinas = [col for col in df_horizontal.columns if col.startswith(('cien', 'geog', 'mate', 'port', 'ingl'))]

# # Calcular a média das notas por disciplina em cada ano
# df_horizontal.set_index('turma', inplace=True)  # Define 'turma' como índice para facilitar a análise
# df_media_disciplinas = df_horizontal.groupby('turma')[disciplinas].mean()

# # Visualizar o DataFrame resultante
# df_media_disciplinas.head(10)

# #%%
# df_media_disciplinas = df_media_disciplinas.reset_index()

# # Criar um índice de data usando o ano
# df_media_disciplinas['data'] = pd.to_datetime(df_media_disciplinas['turma'], format='%Y')
# df_media_disciplinas.set_index('data', inplace=True)
# df_media_disciplinas = df_media_disciplinas.drop(columns='turma')

# # Verificar o DataFrame
# df_media_disciplinas.head(10)

# #%%
# # Definir a frequência anual
# df_media_disciplinas.index = df_media_disciplinas.index.to_period('A').to_timestamp()

# #%%
# df_media_disciplinas.head()
# #%%
# df_media_disciplinas.index
# #%%
# import matplotlib.pyplot as plt

# for disciplina in disciplinas:
#     plt.figure(figsize=(12, 6))
#     plt.plot(df_media_disciplinas.index, df_media_disciplinas[disciplina], marker='o', linestyle='-', label=disciplina)
#     plt.title(f'Média Geral das Notas de {disciplina.upper()} ao Longo dos Anos')
#     plt.xlabel('Ano')
#     plt.ylabel('Média Geral das Notas')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


# #%%
# from statsmodels.tsa.seasonal import seasonal_decompose

# for disciplina in disciplinas:
#     df_discipline = df_media_disciplinas[disciplina].dropna()
    
#     # Verificar se a série temporal tem uma frequência definida
#     if df_discipline.index.freq is None:
#         df_discipline.index = pd.date_range(start=df_discipline.index.min(), 
#                                             end=df_discipline.index.max(), 
#                                             freq='A')  # Frequência Anual
    
#     # Decomposição aditiva
#     result = seasonal_decompose(df_discipline, model='additive')
#     result.plot()
#     plt.title(f'Decomposição da Média Geral das Notas de {disciplina.upper()}')
#     plt.show()


# #%%
# from statsmodels.tsa.arima_model import ARIMA
# import pandas as pd

# # Exemplo para uma disciplina específica
# disciplina = 'cien'  # Troque pelo nome da disciplina desejada
# df_discipline = df_media_disciplinas[disciplina].dropna()

# # Ajustar o modelo ARIMA
# model = ARIMA(df_discipline, order=(1, 1, 1))  # Ajuste os parâmetros conforme necessário
# model_fit = model.fit()

# # Fazer a previsão para o próximo ano
# forecast = model_fit.forecast(steps=1)
# print(f'Previsão para o próximo ano para {disciplina.upper()}: {forecast[0][0]}')

# #%%
# # Plotar a previsão
# plt.figure(figsize=(10, 6))
# plt.plot(df_discipline.index, df_discipline, label='Dados Históricos')
# plt.axvline(x=df_discipline.index[-1], color='red', linestyle='--', label='Ponto de Previsão')
# plt.plot(df_discipline.index[-1] + pd.DateOffset(years=1), forecast[0], 'ro', label='Previsão')
# plt.title(f'Previsão da Média Geral das Notas de {disciplina.upper()}')
# plt.xlabel('Ano')
# plt.ylabel('Média das Notas')
# plt.legend()
# plt.show()

# #%%
# ##########


# #%%
# from statsmodels.tsa.statespace.sarimax import SARIMAX

# # Ajuste o modelo SARIMA
# model = SARIMAX(df_media['media_geral'], order=(1,1,1), seasonal_order=(1,1,1,1))  # Ajuste os parâmetros conforme necessário
# model_fit = model.fit()

# # Fazer previsões
# forecast = model_fit.forecast(steps=1)  # Previsão para o próximo ano

# print(f'Previsão da média geral para o próximo ano: {forecast.iloc[0]}')

# #%%
# from sklearn.metrics import mean_squared_error

# Exemplo de validação (ajuste conforme a disponibilidade dos dados de teste)
# y_test e y_pred precisam ser definidos com base nos dados históricos de treinamento e teste
# mse = mean_squared_error(y_test, y_pred)
# print(f'Erro Quadrático Médio: {mse}')

#############################################
# ARIMA TESTE
#%%import pandas as pd
# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA
# import matplotlib.pyplot as plt

# # Carregar o DataFrame horizontal
# df_horizontal = pd.read_csv('../../datasets/processados/df_horizontal.csv')

# # Lista das disciplinas
# disciplinas = [
#     "cien1", "cien2", "cien3", "cien4", "geog1", "geog2", "geog3", "geog4",
#     "hist1", "hist2", "hist3", "hist4", "reli1", "reli2", "reli3", "reli4",
#     "arte1", "arte2", "arte3", "arte4", "edfi1", "edfi2", "edfi3", "edfi4",
#     "ingl1", "ingl2", "ingl3", "ingl4", "port1", "port2", "port3", "port4",
#     "mate1", "mate2", "mate3", "mate4"
# ]

# # Calcular a média anual das notas por disciplina
# df_media_disciplinas = df_horizontal.groupby('turma')[disciplinas].mean()

# # Definir o índice como o ano e certificar-se de que o índice seja um DatetimeIndex
# df_media_disciplinas.index = pd.to_datetime(df_media_disciplinas.index.astype(str) + '-01-01')

# # Certifique-se de que o índice seja um DatetimeIndex com frequência anual
# df_media_disciplinas.index = pd.DatetimeIndex(df_media_disciplinas.index).to_period('Y').to_timestamp()

# # Escolher uma disciplina para prever
# disciplina = 'cien2'  # Ajuste conforme o nome correto da coluna
# if disciplina not in df_media_disciplinas.columns:
#     raise KeyError(f"Coluna '{disciplina}' não encontrada no DataFrame.")

# # Selecionar a série temporal para a disciplina escolhida
# df_discipline = df_media_disciplinas[disciplina].dropna()

# # Ajustar o modelo ARIMA
# model = ARIMA(df_discipline, order=(1, 1, 1))  # Ajuste os parâmetros conforme necessário
# model_fit = model.fit()

# # Fazer a previsão para o próximo ano
# forecast = model_fit.forecast(steps=1)

# # Plotar a previsão
# plt.figure(figsize=(10, 6))
# plt.plot(df_discipline.index, df_discipline, label='Dados Históricos')
# plt.axvline(x=df_discipline.index[-1], color='red', linestyle='--', label='Ponto de Previsão')
# plt.plot(df_discipline.index[-1] + pd.DateOffset(years=1), forecast[0], 'ro', label='Previsão')
# plt.title(f'Previsão da Média Geral das Notas de {disciplina.upper()}')
# plt.xlabel('Ano')
# plt.ylabel('Média das Notas')
# plt.legend()
# plt.show()

# print(f'Previsão para o próximo ano para {disciplina.upper()}: {forecast[0]:.2f}')


########################
# SEPARANDO TREINO E TESTE - ARIMA E SARIMA
# %%
# pip install pmdarima - para facilitar a modelagem SARIMA:
# import pandas as pd
# import matplotlib.pyplot as plt
# from statsmodels.tsa.arima.model import ARIMA
# from pmdarima import auto_arima
# from sklearn.metrics import mean_squared_error

# # Carregar o DataFrame horizontal
# df_horizontal = pd.read_csv('../../datasets/processados/df_horizontal.csv')

# # Lista das disciplinas
# disciplinas = [
#     "cien1", "cien2", "cien3", "cien4", "geog1", "geog2", "geog3", "geog4",
#     "hist1", "hist2", "hist3", "hist4", "reli1", "reli2", "reli3", "reli4",
#     "arte1", "arte2", "arte3", "arte4", "edfi1", "edfi2", "edfi3", "edfi4",
#     "ingl1", "ingl2", "ingl3", "ingl4", "port1", "port2", "port3", "port4",
#     "mate1", "mate2", "mate3", "mate4"
# ]

# # Calcular a média anual das notas por disciplina
# df_media_disciplinas = df_horizontal.groupby('turma')[disciplinas].mean()

# # Definir o índice como o ano e certificar-se de que o índice seja um DatetimeIndex
# df_media_disciplinas.index = pd.to_datetime(df_media_disciplinas.index.astype(str) + '-01-01')

# # Certifique-se de que o índice seja um DatetimeIndex com frequência anual
# df_media_disciplinas.index = pd.DatetimeIndex(df_media_disciplinas.index).to_period('Y').to_timestamp()

# # Escolher uma disciplina para prever
# disciplina = 'port3'  # Ajuste conforme o nome correto da coluna
# if disciplina not in df_media_disciplinas.columns:
#     raise KeyError(f"Coluna '{disciplina}' não encontrada no DataFrame.")

# # Selecionar a série temporal para a disciplina escolhida
# df_discipline = df_media_disciplinas[disciplina].dropna()

# # Dividir os dados em treino e teste
# train_size = len(df_discipline) - 1
# df_train = df_discipline.iloc[:train_size]
# df_test = df_discipline.iloc[train_size:]
# test_year = df_test.index[0]  # Ano para o qual estamos testando
# real_value_test = df_test.values[0]  # Valor real para o ano de teste

# # Ajustar o modelo ARIMA
# model_arima = ARIMA(df_train, order=(1, 1, 1))  # Ajuste os parâmetros conforme necessário
# model_fit_arima = model_arima.fit()

# # Fazer a previsão para o próximo ano com ARIMA
# forecast_arima = model_fit_arima.forecast(steps=1)

# # Ajustar o modelo SARIMA
# model_sarima = auto_arima(df_train, seasonal=True, m=1)  # Ajuste m conforme a periodicidade (m=1 para anual)
# model_fit_sarima = model_sarima.fit(df_train)

# # Fazer a previsão para o próximo ano com SARIMA
# forecast_sarima = model_fit_sarima.predict(n_periods=1)

# # Avaliar a performance dos modelos
# mse_arima = mean_squared_error([real_value_test], [forecast_arima[0]])
# mse_sarima = mean_squared_error([real_value_test], [forecast_sarima[0]])

# # Plotar as previsões
# plt.figure(figsize=(12, 8))

# # Plot ARIMA
# plt.subplot(2, 1, 1)
# plt.plot(df_discipline.index, df_discipline, label='Dados Históricos')
# plt.axvline(x=test_year, color='red', linestyle='--', label='Ponto de Previsão')
# plt.plot(test_year, forecast_arima[0], 'ro', label='Previsão ARIMA')
# plt.plot(test_year, real_value_test, 'go', label='Real (Teste)')
# plt.title(f'Previsão da Média Geral das Notas de {disciplina.upper()} com ARIMA')
# plt.xlabel('Ano')
# plt.ylabel('Média das Notas')
# plt.legend()

# # Plot SARIMA
# plt.subplot(2, 1, 2)
# plt.plot(df_discipline.index, df_discipline, label='Dados Históricos')
# plt.axvline(x=test_year, color='red', linestyle='--', label='Ponto de Previsão')
# plt.plot(test_year, forecast_sarima[0], 'bo', label='Previsão SARIMA')
# plt.plot(test_year, real_value_test, 'go', label='Real (Teste)')
# plt.title(f'Previsão da Média Geral das Notas de {disciplina.upper()} com SARIMA')
# plt.xlabel('Ano')
# plt.ylabel('Média das Notas')
# plt.legend()

# plt.tight_layout()
# plt.show()

# print(f'Previsão para o próximo ano com ARIMA para {disciplina.upper()}: {forecast_arima[0]:.2f}')
# print(f'Previsão para o próximo ano com SARIMA para {disciplina.upper()}: {forecast_sarima[0]:.2f}')
# print(f'Valor Real para o Próximo Ano: {real_value_test:.2f}')
# print(f'Erro Quadrático Médio (MSE) ARIMA: {mse_arima:.2f}')
# print(f'Erro Quadrático Médio (MSE) SARIMA: {mse_sarima:.2f}')


# %%
# ARIMA, incluindo a análise de ACF e PACF para auxiliar na escolha dos parâmetros 
# p (auto-regressão) e q (média móvel) do modelo. 
# E a métrica de avaliação RMSE 
##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error
from math import sqrt

# Carregar o dataset processado
df_horizontal = pd.read_csv('../../datasets/processados/df_horizontal.csv')

# Lista das disciplinas
disciplinas = [
    "cien1", "cien2", "cien3", "cien4", "geog1", "geog2", "geog3", "geog4",
    "hist1", "hist2", "hist3", "hist4", "reli1", "reli2", "reli3", "reli4",
    "arte1", "arte2", "arte3", "arte4", "edfi1", "edfi2", "edfi3", "edfi4",
    "ingl1", "ingl2", "ingl3", "ingl4", "port1", "port2", "port3", "port4",
    "mate1", "mate2", "mate3", "mate4"
]

# Calcular a média anual das notas por disciplina
df_media_disciplinas = df_horizontal.groupby('turma')[disciplinas].mean()

# Definir o índice como o ano e certificar-se de que o índice seja um DatetimeIndex
df_media_disciplinas.index = pd.to_datetime(df_media_disciplinas.index.astype(str) + '-01-01')

# Certifique-se de que o índice seja um DatetimeIndex com frequência anual
df_media_disciplinas.index = pd.DatetimeIndex(df_media_disciplinas.index).to_period('Y').to_timestamp()

# Escolher a disciplina e o bimestre crítico identificados previamente
disciplina = 'port3'  # Ajuste conforme o nome correto da disciplina
if disciplina not in df_media_disciplinas.columns:
    raise KeyError(f"Coluna '{disciplina}' não encontrada no DataFrame.")

# Selecionar a série temporal para a disciplina escolhida
df_discipline = df_media_disciplinas[disciplina].dropna()

# Separar em treino e teste (último ano como teste)
train = df_discipline[:-1]
test = df_discipline[-1:]

# Plot ACF e PACF para análise dos parâmetros p e q
fig, ax = plt.subplots(1, 2, figsize=(16, 6))
plot_acf(train, ax=ax[0], lags=4)  # Ajuste o número de lags
plot_pacf(train, ax=ax[1], lags=4)
plt.show()

# Definir o modelo ARIMA com parâmetros escolhidos (ajuste conforme análise de ACF/PACF)
p = 2  # Auto-regressão (definido pela PACF)
d = 1  # Diferença (para tornar a série estacionária)
q = 3  # Média móvel (definido pela ACF)
model = ARIMA(train, order=(p, d, q))

# Ajustar o modelo ARIMA
model_fit = model.fit()

print(model_fit.summary())

# Fazer a previsão para o próximo ano
forecast = model_fit.forecast(steps=1)

# Avaliar o modelo usando RMSE
real_value = test.values[0]
predicted_value = forecast[0]
rmse = sqrt(mean_squared_error([real_value], [predicted_value]))

# Plotar o resultado
plt.figure(figsize=(10, 6))
plt.plot(train.index, train, label='Dados Históricos')

# Adiciona o valor real ao gráfico de teste
plt.plot(test.index, test, 'go', label='Valor Real (Teste)')
plt.axvline(x=train.index[-1], color='red', linestyle='--', label='Ponto de Previsão')

# Adiciona o ponto de previsão ao gráfico
plt.plot(test.index, forecast, 'ro', label='Previsão ARIMA')
plt.title(f'Previsão da Média Geral das Notas de {disciplina.upper()} (ARIMA)')
plt.xlabel('Ano')
plt.ylabel('Média das Notas')
plt.legend()
plt.show()

# Exibir os resultados
print(f'Previsão para o próximo ano para {disciplina.upper()}: {predicted_value:.2f}')
print(f'Valor real para o próximo ano: {real_value:.2f}')
print(f'RMSE da previsão: {rmse:.2f}')


#%%