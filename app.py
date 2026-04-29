import streamlit as st

st.title("📦 Controlo de Produção")

st.write("Insere os dados para calcular a produção e validar os rótulos.")

# 🧾 Inputs
caixas = st.number_input("Número de caixas contentoras produzidas", min_value=0, step=1)

unidades_por_caixa = st.number_input("Número de unidades por caixa", min_value=0, step=1)

primeiro_rotulo = st.number_input("Número do primeiro rótulo", min_value=0, step=1)

ultimo_rotulo = st.number_input("Número do último rótulo", min_value=0, step=1)

rejeitados = st.number_input("Número de rejeitados", min_value=0, step=1)

# 🧠 Cálculos
if st.button("Calcular"):

    # Produção total esperada
    producao_total = caixas * unidades_por_caixa

    # Total de rótulos válidos
    total_rotulos = (ultimo_rotulo - primeiro_rotulo + 1) - rejeitados

    # 📊 Mostrar resultados
    st.subheader("📊 Resultados")

    st.write(f"✔ Produção calculada: **{producao_total} unidades**")
    st.write(f"✔ Rótulos válidos: **{total_rotulos} unidades**")

    # ✅ Verificação
    if producao_total == total_rotulos:
        st.success("✅ OK: Produção e rótulos estão consistentes.")
    else:
        st.error("❌ ERRO: Produção e rótulos NÃO coincidem.")
        st.warning(f"Diferença: {abs(producao_total - total_rotulos)} unidades")
        