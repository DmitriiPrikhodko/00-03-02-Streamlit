import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")  # Игнорируем warnings

# Название

st.title("Заполни пропуски")
st.write("Загрузи датафрейм и заполни пропуски")
# Описание

## Шаг 1. Загрузка CSV


uploaded_file = st.sidebar.file_uploader("Загрузи CSV файл")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="latin1")
    st.write(df.head(5))
else:
    st.stop()


## Шаг 2. Проверка наличия пропуска в файле


missed_values = df.isna().sum()
missed_values = missed_values[missed_values > 0]

if len(missed_values) > 0:
    fig, ax = plt.subplots()
    sns.barplot(x=missed_values.index, y=missed_values.values)
    ax.set_title("Пропуски в столбцах")
    ax.set_ylabel("Количество пропусков")
    st.pyplot(fig)

    ## Шаг 3. Заполнить пропуски

    button = st.button("Заполнить пропуски")
    if button:
        df_filled = df[missed_values.index].copy()
        for col in df_filled:
            if df_filled[col].dtype == "object":  # Категориальные признаки
                df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
            else:  # Численные признаки
                df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        st.write(df_filled.head(5))

        ## Шаг 4. Выгрузить новый csv.

        download_button = st.download_button(
            label="Скачать CVS файл", data=df_filled.to_csv(), file_name="filled.csv"
        )

else:
    st.write("Нет пропусков в данных")
    st.stop()
