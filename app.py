import streamlit as st

# 👇 AQUI: esconder sidebar
hide_sidebar_style = """
<style>
[data-testid="stSidebar"] {display: none;}
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.title("Reconciliação de Rótulos/Etiquetas")

st.set_page_config(layout="wide")

st.markdown("""

<style>
div.stButton > button {
    width: 100%;
    height: 100px;
    border-radius: 20px;
}

div.stButton > button > div,
div.stButton > button > div > p {
    font-size: 48px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Estado inicial
# -------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"

# -------------------------
# MENU INICIAL
# -------------------------
if st.session_state.pagina == "menu":

    st.write("Escolha uma opção:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("**Reconciliação de uma bobine**"):
            st.session_state.pagina = "uma_bobine"
            st.rerun() 

    with col2:
        if st.button("**Reconciliação de todas as bobines**"):
            st.session_state.pagina = "todas_bobines"
            st.rerun() 

elif st.session_state.pagina == "uma_bobine":

    #Inputs Troca da bobine (contando que as contas anteriores foram bem feitas, basta fazer as contas para a bobine acabada)
    st.markdown("<p style='font-size:22px;font-weight:700;'>Inserir dados de produção</p>", unsafe_allow_html=True)

    # Linha 1
    col1, col2 = st.columns(2)

    with col1:
        u1 = unidades_por_caixa = st.number_input("Número de unidades por caixa contentora (parâmetro de embalagem)", min_value=0, step=1)

    # Linha 2
    col3, col4 = st.columns(2)

    with col3:
        u3 = primeiracaixa = st.number_input("Número da primeira caixa contentora completa", min_value=0, step=1)

    with col4:
        u4 = ultimacaixa=st.number_input("Número da última caixa contentora completa", min_value=0, step=1)

    # Linha 3
    col5, col6 = st.columns(2)

    with col5:
        u5 = unidades_soltas_primeira=st.number_input("Número de unidades na primeira caixa contentora incompleta", min_value=0, step=1)

    with col6:
        u6 = unidades_soltas_ultima=st.number_input("Número de unidades na última caixa contentora incompleta", min_value=0, step=1)

    st.divider()

    st.markdown("<p style='font-size:22px; font-weight:700;'>Inserir dados dos rótulos</p>", unsafe_allow_html=True)

    # Linha 1
    col1, col2 = st.columns(2)

    with col1:
        u1 = primeiro_rotulo = st.number_input("Número do primeiro rótulo da bobine", min_value=0, step=1)

    with col2:
        u2=ultimo_rotulo = st.number_input("Número do último rótulo da bobine", min_value=0, step=1)

    # Linha 2
    col3, col4 = st.columns(2)

    with col3:
        u3 = rejeitados = st.number_input("Número de rejeitados (inutilizados + amostras)", min_value=0, step=1)

    #Cálculos
    if st.button("Calcular"):

        # Produção total
        producao_total = (ultimacaixa-primeiracaixa+1)*unidades_por_caixa +unidades_soltas_primeira+unidades_soltas_ultima

        # Total de rótulos válidos
        total_rotulos = (ultimo_rotulo - primeiro_rotulo + 1) - rejeitados

        #Resultados
        st.subheader("Resultados")

        st.write(f"✔ Produção: **{producao_total} unidades**")
        st.write(f"✔ Rótulos válidos (excluindo inutilizados e amostras): **{total_rotulos} unidades**")

        #Verificação
        if producao_total == total_rotulos:
            st.success("Número de unidades produzidas e número de rótulos consistentes")
        else:
            st.error(f"Diferença: {abs(producao_total - total_rotulos)} unidades")
            if (producao_total-total_rotulos)>0:
                st.error("O número de unidades produzidas é superior ao número de rótulos utilizados")
            else:
                st.error("O número de unidades produzidas é inferior ao número de rótulos utilizados")
            
    if st.button("⬅ Voltar ao menu"):
        st.session_state.pagina = "menu"
        st.rerun() 

elif st.session_state.pagina == "todas_bobines":

    #Inputs Reconciliação de todas as bobines
    st.markdown("<p style='font-size:22px;font-weight:700;'>Inserir dados de produção</p>", unsafe_allow_html=True)

     # Linha 1
    col1, col2 = st.columns(2)

    with col1:
        u1 = unidades_por_caixa = st.number_input("Número de unidades por caixa contentora (parâmetro de embalagem)", min_value=0, step=1)

    # Linha 2
    col3, col4 = st.columns(2)

    with col3:
        u3 = caixas = st.number_input("Número de caixas contentoras completas produzidas", min_value=0, step=1)

    with col4:
        u4 = unidades_soltas=st.number_input("Número de unidades na última caixa contentora incompleta", min_value=0, step=1)

    st.divider()

    st.markdown("<p style='font-size:22px; font-weight:700;'>Inserir dados dos rótulos</p>", unsafe_allow_html=True)

    # Número de bobines
    num_bobines = st.number_input(
        "Número de bobines utilizadas:",
        min_value=1,
        step=1
    )

    # Guardar dados
    dados_bobines = []

    for i in range(num_bobines):

        st.markdown(f"<p style='font-size:18px; font-weight:700;'>Bobine {i+1}</p>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            primeiro = st.number_input(
                f"Número do primeiro rótulo da bobine {i+1}",
                key=f"primeiro_{i}",min_value=0, step=1
            )

        with col2:
            ultimo = st.number_input(
                f"Número do último rótulo da bobine {i+1}",
                key=f"ultimo_{i}",min_value=0, step=1
            )

        with col3:
            inutilizados=st.number_input(
                f"Número de rótulos inutilizados da bobine {i+1}",
                key=f"inutilizados_{i}",min_value=0, step=1
            )

        with col4:
            amostras=st.number_input(
                f"Número de amostras da bobine {i+1}",
                key=f"amostras_{i}",min_value=0, step=1
            )

        dados_bobines.append({
            "Bobine": i+1,
            "Primeiro": primeiro,
            "Último": ultimo,
            "Inutilizados":inutilizados,
            "Amostras":amostras
        })

    #Cálculos
    if st.button("Calcular"):

        # Produção total esperada
        producao_total = (caixas)*unidades_por_caixa+unidades_soltas

        soma_primeiros = sum(b["Primeiro"] for b in dados_bobines)
        soma_ultimos = sum(b["Último"] for b in dados_bobines)

        soma_inutilizados=sum(b["Inutilizados"] for b in dados_bobines)
        soma_amostras=sum(b["Amostras"] for b in dados_bobines)
        soma_rejeitados=soma_amostras+soma_inutilizados

        somatotal_rotulos=soma_ultimos-soma_primeiros
        
        total_rotulos=somatotal_rotulos+num_bobines

        total_rotulosvalidos=total_rotulos-soma_rejeitados

        #Resultados
        st.subheader("Resultados")
        st.write(f"✔ Produção: **{producao_total} unidades**")
        st.write(f"✔ Rótulos válidos (excluindo inutilizados e amostras): **{total_rotulosvalidos} unidades**")

        #Verificação
        if producao_total == total_rotulosvalidos:
            st.success("Número de unidades produzidas e número de rótulos consistentes")
        else:
            st.error(f"Diferença: {abs(producao_total - total_rotulosvalidos)} unidades")
            if (producao_total-total_rotulos)>0:
                st.error("O número de unidades produzidas é superior ao número de rótulos utilizados")
            else:
                st.error("O número de unidades produzidas é inferior ao número de rótulos utilizados")

        st.text(f"""Se estiver a fechar o processo e tiver obtido um resultado positivo na reconciliação dos rótulos, coloque os seguintes valores nos locais indicados:
        A={soma_primeiros}
        B={soma_ultimos}
        C={soma_inutilizados}
        D={soma_amostras}
        B-A={somatotal_rotulos}
        C+D={soma_rejeitados}
        Nº de bobines utilizadas={num_bobines}
        E+F={total_rotulos}
        G-H={total_rotulosvalidos}
        Quantidade final obtida={producao_total}""")
        

    if st.button("⬅ Voltar ao menu"):
        st.session_state.pagina = "menu"
        st.rerun() 
