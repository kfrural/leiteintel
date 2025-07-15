# LeiteIntel - Intelligent Dashboard for Milk Production Analysis

## 📊 About the Project

**LeiteIntel** is a data analysis system focused on the milk production chain in Brazil, designed to support rural producers, technicians, and researchers in making strategic decisions. Using advanced data analysis techniques, the project allows exploration of trends, forecasting, and generation of customized reports on milk production across different states and periods.

The system is built following the **CRISP-DM (Cross-Industry Standard Process for Data Mining)** model, a well-established framework for conducting data mining and analysis projects in an organized and efficient manner. This process includes the stages of business understanding, data understanding, data preparation, modeling, evaluation, and deployment.

Additionally, the project works with **Big Data** concepts, handling expanded and complex datasets to extract valuable insights, focusing on production, price, climate, and technology applied to dairy farming.

## 🚀 Main Features

- **Interactive data visualization** by state and year, with detailed milk production charts.
- **Statistical analyses** and summarized tables showing averages by production type and technology use.
- **Prediction model** to estimate future production based on climatic and economic variables.
- **Personalized PDF report generation**, including interpretative texts and graphs/tables, with user customization options.
- **Modular structure** facilitating maintenance and system expansion.

## 🛠️ Technologies Used

- **Python** with **Streamlit** for building the interactive web interface.
- **Pandas, Seaborn, and Matplotlib** for data manipulation and visualization.
- **Scikit-learn** for predictive modeling using linear regression and preprocessing.
- **FPDF** for generating PDF reports.
- Clear modular organization to ease development and reuse.

## 📁 Project Structure

- `app.py` — main application integrating all components.
- `componentes.py` — functions for sidebar and widgets.
- `graficos.py` — functions for creating charts.
- `modelos.py` — logic for training and prediction.
- `relatorio.py` — PDF report generation with interpretative analysis.
- `data/` — folder containing raw and processed data.
- `relatorios/` — folder where PDF reports are saved.

## ⚙️ How to Run

1. Make sure the data file `leiteintel_base_ampliada.csv` is in the `data/` folder.
2. Run the app with:
