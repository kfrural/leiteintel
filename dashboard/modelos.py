from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def treinar_modelo(df):
    X = df.drop("producao_litros", axis=1)
    y = df["producao_litros"]

    prep = ColumnTransformer([
        ("onehot", OneHotEncoder(), ["tipo_producao"])
    ], remainder='passthrough')

    modelo = Pipeline([
        ("prep", prep),
        ("reg", LinearRegression())
    ])

    modelo.fit(X, y)
    return modelo
