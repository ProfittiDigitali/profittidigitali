
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisi PPC Amazon", layout="wide")

st.title("📈 Analisi Settimanale PPC Amazon")

uploaded_file = st.file_uploader("Carica il tuo file Excel con i dati PPC", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Anteprima dati:")
    st.dataframe(df.head())

    # Selezione delle colonne chiave
    with st.expander("🔧 Configura le colonne"):
        col_data = st.selectbox("Colonna data", df.columns)
        col_spesa = st.selectbox("Colonna spesa", df.columns)
        col_vendite = st.selectbox("Colonna vendite", df.columns)
        col_acos = st.selectbox("Colonna ACoS (%)", df.columns)

    # Raggruppamento per data
    st.subheader("📊 Analisi settimanale")
    try:
        df[col_data] = pd.to_datetime(df[col_data])
        df_grouped = df.groupby(df[col_data].dt.to_period("W")).agg({
            col_spesa: "sum",
            col_vendite: "sum",
            col_acos: "mean"
        }).reset_index()
        df_grouped[col_data] = df_grouped[col_data].astype(str)

        st.dataframe(df_grouped)

        # Grafici
        st.subheader("📉 Grafici")
        fig, ax = plt.subplots()
        ax.plot(df_grouped[col_data], df_grouped[col_spesa], marker='o', label='Spesa')
        ax.plot(df_grouped[col_data], df_grouped[col_vendite], marker='s', label='Vendite')
        ax.set_ylabel("€")
        ax.set_xlabel("Settimana")
        ax.legend()
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()
        ax2.plot(df_grouped[col_data], df_grouped[col_acos], marker='d', color='orange', label='ACoS %')
        ax2.set_ylabel("ACoS %")
        ax2.set_xlabel("Settimana")
        ax2.legend()
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"Errore durante l'elaborazione: {e}")
else:
    st.info("Carica un file Excel per iniziare l'analisi.")
