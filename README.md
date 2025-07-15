# LeiteIntel - Dashboard Inteligente para Análise da Produção de Leite

## 📊 Sobre o Projeto

O **LeiteIntel** é um sistema de análise de dados voltado para a cadeia produtiva do leite no Brasil, desenvolvido para apoiar produtores rurais, técnicos e pesquisadores na tomada de decisões estratégicas. Utilizando técnicas avançadas de análise de dados, o projeto permite explorar tendências, realizar previsões e gerar relatórios customizados sobre a produção leiteira em diferentes estados e períodos.

O sistema é construído seguindo o modelo **CRISP-DM (Cross-Industry Standard Process for Data Mining)**, um framework consolidado para conduzir projetos de mineração e análise de dados de forma organizada e eficiente. Este processo inclui as etapas de entendimento do negócio, entendimento dos dados, preparação dos dados, modelagem, avaliação e implantação.

Além disso, o projeto trabalha com conceitos de **Big Data**, tratando bases de dados ampliadas e complexas para extrair insights valiosos, com foco em produção, preço, clima e tecnologia aplicada à pecuária leiteira.

## 🚀 Funcionalidades Principais

- **Visualização interativa** de dados por estado e ano, com gráficos detalhados da produção de leite.
- **Análises estatísticas** e tabelas resumidas, mostrando médias por tipo de produção e uso de tecnologia.
- **Modelo de previsão** para estimar produção futura com base em variáveis climáticas e econômicas.
- **Geração de relatórios PDF personalizados**, incluindo textos interpretativos e gráficos/tabelas, com opções de customização pelo usuário.
- **Estrutura modular** facilitando manutenção e expansão do sistema.

## 🛠️ Tecnologias Utilizadas

- **Python** com a biblioteca **Streamlit** para criação da interface web interativa.
- **Pandas, Seaborn e Matplotlib** para manipulação e visualização de dados.
- **Scikit-learn** para modelagem preditiva usando regressão linear e pré-processamento.
- **FPDF** para geração de relatórios em PDF.
- Organização do projeto em módulos claros para facilitar o desenvolvimento e reuso.

## 📁 Estrutura do Projeto

- `app.py` — aplicação principal que integra todos os componentes.
- `componentes.py` — funções para a barra lateral e widgets.
- `graficos.py` — funções para criação de gráficos.
- `modelos.py` — lógica de treinamento e predição.
- `relatorio.py` — geração do relatório em PDF com análise interpretativa.
- `data/` — pasta contendo os dados brutos e processados.
- `relatorios/` — pasta onde os relatórios PDF são salvos.

## ⚙️ Como Executar

1. Garanta que o arquivo de dados `leiteintel_base_ampliada.csv` esteja na pasta `data/`.
2. Execute o app com:
