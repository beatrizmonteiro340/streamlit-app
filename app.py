import streamlit as st
import uuid
import json

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

def guardar_dados():
    fk = st.session_state.get("form_key", "default")
    supabase.table("sessoes").upsert({
        "session_id": st.session_state.session_id,
        "dados": {

            "form_keyTAGPRICE": st.session_state.get("form_keyTAGPRICE", "default"),
            "form_keyROTULOS": st.session_state.get("form_keyROTULOS", "default"),

            "formulario_uma_bobineTAGPRICE":
                st.session_state.get("formulario_uma_bobineTAGPRICE", {}),
            "formulario_todas_bobinesTAGPRICE":
                st.session_state.get("formulario_todas_bobinesTAGPRICE", {}),

            "formulario_uma_bobineROTULOS":
                st.session_state.get("formulario_uma_bobineROTULOS", {}),

            "formulario_todas_bobinesROTULOS":
                st.session_state.get("formulario_todas_bobinesROTULOS", {})
        }
    }).execute()
def carregar_dados():

    res = supabase.table("sessoes") \
        .select("*") \
        .eq("session_id", st.session_state.session_id) \
        .execute()
    if res.data and "dados" in res.data[0]:
        dados = res.data[0]["dados"]
        if "form_keyTAGPRICE" in dados:
            st.session_state["form_keyTAGPRICE"] = dados["form_keyTAGPRICE"]
        if "form_keyROTULOS" in dados:
            st.session_state["form_keyROTULOS"] = dados["form_keyROTULOS"]
        if "formulario_uma_bobineTAGPRICE" in dados:
            st.session_state["formulario_uma_bobineTAGPRICE"] = dados["formulario_uma_bobineTAGPRICE"]

        if "formulario_todas_bobinesTAGPRICE" in dados:
            st.session_state["formulario_todas_bobinesTAGPRICE"] = dados["formulario_todas_bobinesTAGPRICE"]

        if "formulario_uma_bobineROTULOS" in dados:
            st.session_state["formulario_uma_bobineROTULOS"] = dados["formulario_uma_bobineROTULOS"]

        if "formulario_todas_bobinesROTULOS" in dados:
            st.session_state["formulario_todas_bobinesROTULOS"] = dados["formulario_todas_bobinesROTULOS"]
# -------------------------
# ID ÚNICO DA SESSÃO
# -------------------------
query_params = st.query_params

if "session_id" not in query_params:

    novo_id = str(uuid.uuid4())

    st.query_params["session_id"] = novo_id

    st.session_state.session_id = novo_id

else:

    st.session_state.session_id = query_params["session_id"]

st.session_state.setdefault("pagina", "menu_inicial")
st.session_state.setdefault("pagina_anterior", None)
st.session_state.setdefault("dados_carregados", False)
st.session_state.setdefault("form_keyTAGPRICE", "default")
st.session_state.setdefault("form_keyROTULOS", "default")

if not st.session_state.get("dados_carregados", False):
    carregar_dados()
    st.session_state.dados_carregados = True

if st.session_state.pagina_anterior != st.session_state.pagina:
    carregar_dados()
    st.session_state.pagina_anterior = st.session_state.pagina

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
footer {display: none;}
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
# MENU INICIAL
# -------------------------

if st.session_state.pagina == "menu_inicial":

    st.title("Reconciliação Etiquetas")

    st.write("Escolha uma opção:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("**Reconciliação de Etiquetas Tag-Price**"):
            st.session_state.pagina = "menuTAGPRICE"
            st.rerun()

    with col2:
        if st.button("**Reconciliação de Etiquetas de Maço**"):
            st.session_state.pagina = "menuROTULOS"
            st.rerun()

elif st.session_state.pagina == "menuTAGPRICE":

    st.title("Reconciliação de Etiquetas Tag-Price")

    st.write("Escolha uma opção:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("**Reconciliação de uma bobine**"):
            st.session_state.pagina = "uma_bobineTAGPRICE"
            st.rerun() 

    with col2:
        if st.button("**Reconciliação de todas as bobines**"):
            st.session_state.pagina = "todas_bobinesTAGPRICE"
            st.rerun() 

    if st.button("⬅ Voltar ao menu"):    
        guardar_dados()                                 
        st.session_state.pagina = "menu_inicial"
        st.rerun() 

elif st.session_state.pagina == "uma_bobineTAGPRICE":
    fk = st.session_state["form_keyTAGPRICE"]
    f = st.session_state.get("formulario_uma_bobineTAGPRICE", {})

    if f"unidades_por_caixa_TAGPRICE{fk}" not in st.session_state:
        st.session_state[f"unidades_por_caixa_TAGPRICE{fk}"] = f.get("unidades_por_caixa", 0)
        st.session_state[f"primeiracaixa_TAGPRICE{fk}"] = f.get("primeiracaixa", 0)
        st.session_state[f"ultimacaixa_TAGPRICE{fk}"] = f.get("ultimacaixa", 0)
        st.session_state[f"unidades_soltas_primeira_TAGPRICE{fk}"] = f.get("unidades_soltas_primeira", 0)
        st.session_state[f"unidades_soltas_ultima_TAGPRICE{fk}"] = f.get("unidades_soltas_ultima", 0)
        st.session_state[f"primeiro_rotulo_TAGPRICE{fk}"] = f.get("primeiro_rotulo", 0)
        st.session_state[f"ultimo_rotulo_TAGPRICE{fk}"] = f.get("ultimo_rotulo", 0)
        st.session_state[f"rejeitados_TAGPRICE{fk}"] = f.get("rejeitados", 0)

    with st.form(f"form_uma_bobine_TAGPRICE{fk}"):            
    
        #Inputs Troca da bobine (contando que as contas anteriores foram bem feitas, basta fazer as contas para a bobine acabada)
        st.markdown("<p style='font-size:22px;font-weight:700;'>Inserir dados de produção</p>", unsafe_allow_html=True)

        # Linha 1
        col1, col2 = st.columns(2)

        with col1:
            u1 = unidades_por_caixa = st.number_input("Número de unidades por caixa contentora (parâmetro de embalagem)", min_value=0, step=1, key=f"unidades_por_caixa_TAGPRICE{fk}",value=f.get("unidades_por_caixa", 0))

        # Linha 2
        col3, col4 = st.columns(2)

        with col3:
            u3 = primeiracaixa = st.number_input("Número da primeira caixa contentora completa", min_value=0, step=1, key=f"primeiracaixa_TAGPRICE{fk}",value=f.get("primeiracaixa", 0))

        with col4:
            u4 = ultimacaixa=st.number_input("Número da última caixa contentora completa", min_value=0, step=1,key=f"ultimacaixa_TAGPRICE{fk}",value=f.get("ultimacaixa", 0))

        # Linha 3
        col5, col6 = st.columns(2)

        with col5:
            u5 = unidades_soltas_primeira=st.number_input("Número de unidades na primeira caixa contentora incompleta", min_value=0, step=1,key=f"unidades_soltas_primeira_TAGPRICE{fk}",value=f.get("unidades_soltas_primeira", 0))

        with col6:
            u6 = unidades_soltas_ultima=st.number_input("Número de unidades na última caixa contentora incompleta", min_value=0, step=1,key=f"unidades_soltas_ultima_TAGPRICE{fk}",value=f.get("unidades_soltas_ultima", 0))

        st.divider()

        st.markdown("<p style='font-size:22px; font-weight:700;'>Inserir dados dos rótulos</p>", unsafe_allow_html=True)

        # Linha 1
        col1, col2 = st.columns(2)

        with col1:
            u1 = primeiro_rotulo = st.number_input("Número da primeira etiqueta da bobine", min_value=0, step=1, key=f"primeiro_rotulo_TAGPRICE{fk}",value=f.get("primeiro_rotulo", 0))

        with col2:
            u2=ultimo_rotulo = st.number_input("Número da última etiqueta da bobine", min_value=0, step=1, key=f"ultimo_rotulo_TAGPRICE{fk}",value=f.get("ultimo_rotulo", 0))

        # Linha 2
        col3, col4 = st.columns(2)

        with col3:
            u3 = rejeitados = st.number_input("Número de rejeitados (inutilizados + amostras)", min_value=0, step=1, key=f"rejeitados_TAGPRICE{fk}",value=f.get("rejeitados", 0))

        submitted = st.form_submit_button("Calcular")

    if st.button("⬅ Voltar ao menu"): 
        guardar_dados()                                
        st.session_state.pagina = "menuTAGPRICE"
        st.rerun() 

    if st.button("Nova reconciliação"):
        st.session_state["formulario_uma_bobineTAGPRICE"] = {} 
        novo_fk = str(uuid.uuid4()) 
        keys_manter = ["session_id", "pagina", "dados_carregados", "pagina_anterior",
                       "formulario_todas_bobinesTAGPRICE", "formulario_uma_bobineROTULOS", "formulario_todas_bobinesROTULOS"]
        keys_apagar = [k for k in st.session_state if k not in keys_manter]
        for k in keys_apagar:
            del st.session_state[k]
        st.session_state["form_keyTAGPRICE"] = novo_fk
        st.session_state["dados_carregados"] = True
        guardar_dados()
        st.rerun()

    #Cálculos
    if submitted:
    
        st.session_state["formulario_uma_bobineTAGPRICE"] = {
        "unidades_por_caixa": unidades_por_caixa,
        "primeiracaixa": primeiracaixa,
        "ultimacaixa": ultimacaixa,
        "unidades_soltas_primeira": unidades_soltas_primeira,
        "unidades_soltas_ultima": unidades_soltas_ultima,
        "primeiro_rotulo": primeiro_rotulo,
        "ultimo_rotulo": ultimo_rotulo,
        "rejeitados": rejeitados,
        }

        guardar_dados()

        # Produção total
        producao_total = (ultimacaixa-primeiracaixa+1)*unidades_por_caixa +unidades_soltas_primeira+unidades_soltas_ultima

        # Total de rótulos válidos
        total_rotulos = (primeiro_rotulo - ultimo_rotulo + 1) - rejeitados

        #Resultados
        st.subheader("Resultados")

        st.write(f"✔ Produção: **{producao_total} unidades**")
        st.write(f"✔ Etiquetas válidas (excluindo inutilizados e amostras): **{total_rotulos} unidades**")

        #Verificação
        if producao_total == total_rotulos:
            st.success("Número de unidades produzidas e número de etiquetas consistentes")
        else:
            st.warning(f"Diferença: {abs(producao_total - total_rotulos)} unidades")
            if (producao_total-total_rotulos)>0:
                st.error("O número de unidades produzidas é **superior** ao número de etiquetas utilizadas")
            else:
                st.error("O número de unidades produzidas é **inferior** ao número de etiquetas utilizadas")
                
        st.text(f"""Se estiver a fechar o processo e tiver obtido um resultado positivo na reconciliação das etiquetas, coloque os seguintes valores nos locais indicados:
        A={soma_ultimos}
        B={soma_primeiros}
        C={soma_inutilizados}
        D={soma_amostras}
        B-A={somatotal_rotulos}
        C+D={soma_rejeitados}
        Nº de bobines utilizadas={num_bobines}
        E+F={total_rotulos}
        G-H={total_rotulosvalidos}
        Quantidade final obtida={producao_total}""")


elif st.session_state.pagina == "todas_bobinesTAGPRICE":
    fk = st.session_state["form_keyTAGPRICE"]
    f = st.session_state.get("formulario_todas_bobinesTAGPRICE", {})
    bobines_guardadas = f.get("bobines", [])

    if not st.session_state.get("dados_restaurados_TAGPRICE", False):
        st.session_state[f"unidades_por_caixa_TAGPRICE{fk}"] = f.get("unidades_por_caixa", 0)
        st.session_state[f"caixas_TAGPRICE{fk}"] = f.get("caixas", 0)
        st.session_state[f"unidades_soltas_TAGPRICE{fk}"] = f.get("unidades_soltas", 0)
        st.session_state[f"num_bobines_TAGPRICE{fk}"] = f.get("num_bobines", 1)
        st.session_state["dados_restaurados_TAGPRICE"] = True


    for i, b in enumerate(bobines_guardadas):
        if f"primeiro_TAGPRICE{i}_{fk}" not in st.session_state:
            st.session_state[f"primeiro_TAGPRICE{i}_{fk}"] = b.get("Primeiro", 0)
            st.session_state[f"ultimo_TAGPRICE{i}_{fk}"] = b.get("Último", 0)
            st.session_state[f"inutilizados_TAGPRICE{i}_{fk}"] = b.get("Inutilizados", 0)
            st.session_state[f"amostras_TAGPRICE{i}_{fk}"] = b.get("Amostras", 0)

    # Número de bobines
    num_bobines = st.number_input(
        "Número de bobines utilizadas:", min_value=1, step=1, key=f"num_bobines_TAGPRICE{fk}",value=f.get("num_bobines", 1))

    with st.form(f"form_várias_bobine_TAGPRICE{fk}"):    

        #Inputs Reconciliação de todas as bobines
        st.markdown("<p style='font-size:22px;font-weight:700;'>Inserir dados de produção</p>", unsafe_allow_html=True)

        # Linha 1
        col1, col2 = st.columns(2)

        with col1:
            u1 = unidades_por_caixa = st.number_input("Número de unidades por caixa contentora (parâmetro de embalagem)", min_value=0, step=1, key=f"unidades_por_caixa_TAGPRICE{fk}",value=f.get("unidades_por_caixa", 0))

        # Linha 2
        col3, col4 = st.columns(2)

        with col3:
            u3 = caixas = st.number_input("Número de caixas contentoras completas produzidas", min_value=0, step=1, key=f"caixas_TAGPRICE{fk}",value=f.get("caixas", 0))

        with col4:
            u4 = unidades_soltas=st.number_input("Número de unidades na última caixa contentora incompleta", min_value=0, step=1, key=f"unidades_soltas_TAGPRICE{fk}",value=f.get("unidades_soltas", 0))

        st.divider()

        st.markdown("<p style='font-size:22px; font-weight:700;'>Inserir dados dos rótulos</p>", unsafe_allow_html=True)

        # Guardar dados
        dados_bobines = []
        bobines_guardadas = f.get("bobines", [])

        for i in range(num_bobines):

            st.markdown(f"<p style='font-size:18px; font-weight:700;'>Bobine {i+1}</p>", unsafe_allow_html=True)
            b = bobines_guardadas[i] if i < len(bobines_guardadas) else {}
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                primeiro = st.number_input(
                    f"Número da primeira etiqueta da bobine {i+1}",
                    key=f"primeiro_TAGPRICE{i}_{fk}",min_value=0, step=1,value=b.get("primeiro", 0)
                )

            with col2:
                ultimo = st.number_input(
                    f"Número da última etiqueta da bobine {i+1}",
                    key=f"ultimo_TAGPRICE{i}_{fk}",min_value=0, step=1,value=b.get("ultimo", 0)
                )

            with col3:
                inutilizados=st.number_input(
                    f"Número de etiquetas inutilizadas da bobine {i+1}",
                    key=f"inutilizados_TAGPRICE{i}_{fk}",min_value=0, step=1,value=b.get("inutilizados", 0)
                )

            with col4:
                amostras=st.number_input(
                    f"Número de amostras da bobine{i+1}",
                    key=f"amostras_TAGPRICE{i}_{fk}",min_value=0, step=1,value=b.get("amostras", 0)
                )

            dados_bobines.append({
                "Bobine": i+1,
                "Primeiro": primeiro,
                "Último": ultimo,
                "Inutilizados":inutilizados,
                "Amostras":amostras
            })

        submitted = st.form_submit_button("Calcular")

    if st.button("⬅ Voltar ao menu"):    
        guardar_dados()                                
        st.session_state.pagina = "menuTAGPRICE"
        st.rerun() 

    if st.button("Nova reconciliação"):
        st.session_state["formulario_todas_bobinesTAGPRICE"] = {}
        st.session_state["dados_restaurados_TAGPRICE"] = False                             
        novo_fk = str(uuid.uuid4()) 
        keys_manter = ["session_id", "pagina", "dados_carregados"]
        keys_apagar = [k for k in st.session_state if k not in keys_manter]
        for k in keys_apagar:
            del st.session_state[k]
        st.session_state["form_keyTAGPRICE"] = novo_fk
        st.session_state["dados_carregados"] = True
        guardar_dados()
        st.rerun()  

    #Cálculos
    if submitted: 
        st.session_state["formulario_todas_bobinesTAGPRICE"] = {
            "unidades_por_caixa": unidades_por_caixa,
            "caixas": caixas,
            "unidades_soltas": unidades_soltas,
            "num_bobines": num_bobines,
            "bobines": dados_bobines, 
        }
        guardar_dados()
        # Produção total esperada
        producao_total = (caixas)*unidades_por_caixa+unidades_soltas
        soma_primeiros = sum(b["Primeiro"] for b in dados_bobines)
        soma_ultimos = sum(b["Último"] for b in dados_bobines)

        soma_inutilizados=sum(b["Inutilizados"] for b in dados_bobines)
        soma_amostras=sum(b["Amostras"] for b in dados_bobines)
        soma_rejeitados=soma_amostras+soma_inutilizados

        somatotal_rotulos=soma_primeiros-soma_ultimos
            
        total_rotulos=somatotal_rotulos+num_bobines

        total_rotulosvalidos=total_rotulos-soma_rejeitados

        #Resultados
        st.subheader("Resultados")
        st.write(f"✔ Produção: **{producao_total} unidades**")
        st.write(f"✔ Etiquetas válidas (excluindo inutilizados e amostras): **{total_rotulosvalidos} unidades**")

        #Verificação
        if producao_total == total_rotulosvalidos:
            st.success("Número de unidades produzidas e número de etiquetas consistentes")
        else:
            st.warning(f"Diferença: {abs(producao_total - total_rotulosvalidos)} unidades")
            if (producao_total-total_rotulosvalidos)>0:
                st.error("O número de unidades produzidas é **superior** ao número de etiquetas utilizadas")
            else:
                st.error("O número de unidades produzidas é **inferior** ao número de etiquetas utilizadas")

        st.text(f"""Se estiver a fechar o processo e tiver obtido um resultado positivo na reconciliação das etiquetas, coloque os seguintes valores nos locais indicados:
        A={soma_ultimos}
        B={soma_primeiros}
        C={soma_inutilizados}
        D={soma_amostras}
        B-A={somatotal_rotulos}
        C+D={soma_rejeitados}
        Nº de bobines utilizadas={num_bobines}
        E+F={total_rotulos}
        G-H={total_rotulosvalidos}
        Quantidade final obtida={producao_total}""")

elif st.session_state.pagina == "menuROTULOS":

    st.title("Reconciliação de Etiquetas de Maço")

    st.write("Escolha uma opção:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("**Reconciliação de uma bobine**"):
            st.session_state.pagina = "uma_bobineROTULOS"
            st.rerun() 

    with col2:
        if st.button("**Reconciliação de todas as bobines**"):
            st.session_state.pagina = "todas_bobinesROTULOS"
            st.rerun() 

    if st.button("⬅ Voltar ao menu"):    
        guardar_dados()                                 
        st.session_state.pagina = "menu_inicial"
        st.rerun() 

elif st.session_state.pagina == "uma_bobineROTULOS":
    fk = st.session_state["form_keyROTULOS"]
    f = st.session_state.get("formulario_uma_bobineROTULOS", {})

    if f"unidades_por_caixa_ROTULOS{fk}" not in st.session_state:
        st.session_state[f"unidades_por_caixa_ROTULOS{fk}"] = f.get("unidades_por_caixa", 0)
        st.session_state[f"primeiracaixa_ROTULOS{fk}"] = f.get("primeiracaixa", 0)
        st.session_state[f"ultimacaixa_ROTULOS{fk}"] = f.get("ultimacaixa", 0)
        st.session_state[f"unidades_soltas_primeira_ROTULOS{fk}"] = f.get("unidades_soltas_primeira", 0)
        st.session_state[f"unidades_soltas_ultima_ROTULOS{fk}"] = f.get("unidades_soltas_ultima", 0)
        st.session_state[f"primeiro_rotulo_ROTULOS{fk}"] = f.get("primeiro_rotulo", 0)
        st.session_state[f"ultimo_rotulo_ROTULOS{fk}"] = f.get("ultimo_rotulo", 0)
        st.session_state[f"rejeitados_ROTULOS{fk}"] = f.get("rejeitados", 0)

    with st.form(f"form_uma_bobine_ROTULOS{fk}"):            
    
        #Inputs Troca da bobine (contando que as contas anteriores foram bem feitas, basta fazer as contas para a bobine acabada)
        st.markdown("<p style='font-size:22px;font-weight:700;'>Inserir dados de produção</p>", unsafe_allow_html=True)

        # Linha 1
        col1, col2 = st.columns(2)

        with col1:
            u1 = unidades_por_caixa = st.number_input("Número de maços por caixa contentora (parâmetro de embalagem)", min_value=0, step=1, key=f"unidades_por_caixa_ROTULOS{fk}",value=f.get("unidades_por_caixa", 0))

        # Linha 2
        col3, col4 = st.columns(2)

        with col3:
            u3 = primeiracaixa = st.number_input("Número da primeira caixa contentora completa", min_value=0, step=1, key=f"primeiracaixa_ROTULOS{fk}",value=f.get("primeiracaixa", 0))

        with col4:
            u4 = ultimacaixa=st.number_input("Número da última caixa contentora completa", min_value=0, step=1,key=f"ultimacaixa_ROTULOS{fk}",value=f.get("ultimacaixa", 0))

        # Linha 3
        col5, col6 = st.columns(2)

        with col5:
            u5 = unidades_soltas_primeira=st.number_input("Número de maços na primeira caixa contentora incompleta", min_value=0, step=1,key=f"unidades_soltas_primeira_ROTULOS{fk}",value=f.get("unidades_soltas_primeira", 0))

        with col6:
            u6 = unidades_soltas_ultima=st.number_input("Número de maços na última caixa contentora incompleta", min_value=0, step=1,key=f"unidades_soltas_ultima_ROTULOS{fk}",value=f.get("unidades_soltas_ultima", 0))

        st.divider()

        st.markdown("<p style='font-size:22px; font-weight:700;'>Inserir dados dos rótulos</p>", unsafe_allow_html=True)

        # Linha 1
        col1, col2 = st.columns(2)

        with col1:
            u1 = primeiro_rotulo = st.number_input("Número da primeira etiqueta da bobine", min_value=0, step=1, key=f"primeiro_rotulo_ROTULOS{fk}",value=f.get("primeiro_rotulo", 0))

        with col2:
            u2=ultimo_rotulo = st.number_input("Número da última etiqueta da bobine", min_value=0, step=1, key=f"ultimo_rotulo_ROTULOS{fk}",value=f.get("ultimo_rotulo", 0))

        # Linha 2
        col3, col4 = st.columns(2)

        with col3:
            u3 = rejeitados = st.number_input("Número de rejeitados (inutilizados + amostras)", min_value=0, step=1, key=f"rejeitados_ROTULOS{fk}",value=f.get("rejeitados", 0))

        submitted = st.form_submit_button("Calcular")

    if st.button("⬅ Voltar ao menu"): 
        guardar_dados()                                 
        st.session_state.pagina = "menuROTULOS"
        st.rerun() 


    if st.button("Nova reconciliação"):
        st.session_state["formulario_uma_bobineROTULOS"] = {} 
        novo_fk = str(uuid.uuid4()) 
        keys_manter = ["session_id", "pagina", "dados_carregados"]
        keys_apagar = [k for k in st.session_state if k not in keys_manter]
        for k in keys_apagar:
            del st.session_state[k]
        st.session_state["form_keyROTULOS"] = novo_fk
        st.session_state["dados_carregados"] = True
        guardar_dados()
        st.rerun()

    #Cálculos
    if submitted:
    
        st.session_state["formulario_uma_bobineROTULOS"] = {
        "unidades_por_caixa": unidades_por_caixa,
        "primeiracaixa": primeiracaixa,
        "ultimacaixa": ultimacaixa,
        "unidades_soltas_primeira": unidades_soltas_primeira,
        "unidades_soltas_ultima": unidades_soltas_ultima,
        "primeiro_rotulo": primeiro_rotulo,
        "ultimo_rotulo": ultimo_rotulo,
        "rejeitados": rejeitados,
        }

        guardar_dados()

        # Produção total
        producao_total = (ultimacaixa-primeiracaixa+1)*unidades_por_caixa +unidades_soltas_primeira+unidades_soltas_ultima

        # Total de rótulos válidos
        total_rotulos = (ultimo_rotulo - primeiro_rotulo + 1) - rejeitados

        #Resultados
        st.subheader("Resultados")

        st.write(f"✔ Produção: **{producao_total} unidades**")
        st.write(f"✔ Etiquetas válidos (excluindo inutilizados e amostras): **{total_rotulos} unidades**")

        #Verificação
        if producao_total == total_rotulos:
            st.success("Número de maços produzidos e número de etiquetas consistentes")
        else:
            st.warning(f"Diferença: {abs(producao_total - total_rotulos)} unidades")
            if (producao_total-total_rotulos)>0:
                st.error("O número de maços produzidos é **superior** ao número de etiquetas utilizadas")
            else:
                st.error("O número de maços produzidos é **inferior** ao número de etiquetas utilizadas")

        st.text(f"""Se estiver a fechar o processo e tiver obtido um resultado positivo na reconciliação das etiquetas, coloque os seguintes valores nos locais indicados:
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


elif st.session_state.pagina == "todas_bobinesROTULOS":
    fk = st.session_state["form_keyROTULOS"]
    f = st.session_state.get("formulario_todas_bobinesROTULOS", {})
    bobines_guardadas = f.get("bobines", [])

    if not st.session_state.get("dados_restauradosROTULOS", False):
        st.session_state[f"unidades_por_caixa_ROTULOS{fk}"] = f.get("unidades_por_caixa", 0)
        st.session_state[f"caixas_ROTULOS{fk}"] = f.get("caixas", 0)
        st.session_state[f"unidades_soltas_ROTULOS{fk}"] = f.get("unidades_soltas", 0)
        st.session_state[f"num_bobines_ROTULOS{fk}"] = f.get("num_bobines", 1)
        st.session_state["dados_restauradosROTULOS"] = True


    for i, b in enumerate(bobines_guardadas):
        if f"primeiro_ROTULOS{i}_{fk}" not in st.session_state:
            st.session_state[f"primeiro_ROTULOS{i}_{fk}"] = b.get("Primeiro", 0)
            st.session_state[f"ultimo_ROTULOS{i}_{fk}"] = b.get("Último", 0)
            st.session_state[f"inutilizados_ROTULOS{i}_{fk}"] = b.get("Inutilizados", 0)
            st.session_state[f"amostras_ROTULOS{i}_{fk}"] = b.get("Amostras", 0)

    # Número de bobines
    num_bobines = st.number_input(
        "Número de bobines utilizadas:", min_value=1, step=1, key=f"num_bobines_{fk}",value=f.get("num_bobines", 1))

    with st.form(f"form_várias_bobine_ROTULOS{fk}"):    

        #Inputs Reconciliação de todas as bobines
        st.markdown("<p style='font-size:22px;font-weight:700;'>Inserir dados de produção</p>", unsafe_allow_html=True)

        # Linha 1
        col1, col2 = st.columns(2)

        with col1:
            u1 = unidades_por_caixa = st.number_input("Número de maços por caixa contentora (parâmetro de embalagem)", min_value=0, step=1, key=f"unidades_por_caixa_ROTULOS{fk}",value=f.get("unidades_por_caixa", 0))

        # Linha 2
        col3, col4 = st.columns(2)

        with col3:
            u3 = caixas = st.number_input("Número de caixas contentoras completas produzidas", min_value=0, step=1, key=f"caixas_ROTULOS{fk}",value=f.get("caixas", 0))

        with col4:
            u4 = unidades_soltas=st.number_input("Número de maços na última caixa contentora incompleta", min_value=0, step=1, key=f"unidades_soltas_ROTULOS{fk}",value=f.get("unidades_soltas", 0))

        st.divider()

        st.markdown("<p style='font-size:22px; font-weight:700;'>Inserir dados dos rótulos</p>", unsafe_allow_html=True)

        # Guardar dados
        dados_bobines = []
        bobines_guardadas = f.get("bobines", [])

        for i in range(num_bobines):

            st.markdown(f"<p style='font-size:18px; font-weight:700;'>Bobine {i+1}</p>", unsafe_allow_html=True)
            b = bobines_guardadas[i] if i < len(bobines_guardadas) else {}
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                primeiro = st.number_input(
                    f"Número da primeira etiqueta da bobine {i+1}",
                    key=f"primeiro_ROTULOS{i}_{fk}",min_value=0, step=1,value=b.get("primeiro", 0)
                )

            with col2:
                ultimo = st.number_input(
                    f"Número da última etiqueta da bobine {i+1}",
                    key=f"ultimo_ROTULOS{i}_{fk}",min_value=0, step=1,value=b.get("ultimo", 0)
                )

            with col3:
                inutilizados=st.number_input(
                    f"Número de etiquetas inutilizadas da bobine {i+1}",
                    key=f"inutilizados_ROTULOS{i}_{fk}",min_value=0, step=1,value=b.get("inutilizados", 0)
                )

            with col4:
                amostras=st.number_input(
                    f"Número de amostras da bobine {i+1}",
                    key=f"amostras_ROTULOS{i}_{fk}",min_value=0, step=1,value=b.get("amostras", 0)
                )

            dados_bobines.append({
                "Bobine": i+1,
                "Primeiro": primeiro,
                "Último": ultimo,
                "Inutilizados":inutilizados,
                "Amostras":amostras
            })

        submitted = st.form_submit_button("Calcular")

    if st.button("⬅ Voltar ao menu"):    
        guardar_dados()                                 
        st.session_state.pagina = "menuROTULOS"
        st.rerun() 


    if st.button("Nova reconciliação"):
        st.session_state["formulario_todas_bobinesROTULOS"] = {}
        st.session_state["dados_restaurados_ROTULOS"] = False                              
        novo_fk = str(uuid.uuid4()) 
        keys_manter = ["session_id", "pagina", "dados_carregados"]
        keys_apagar = [k for k in st.session_state if k not in keys_manter]
        for k in keys_apagar:
            del st.session_state[k]
        st.session_state["form_keyROTULOS"] = novo_fk
        st.session_state["dados_carregados"] = True
        supabase.table("sessoes").upsert({
            "session_id": st.session_state.session_id,
            "dados": {}
        }).execute()
        st.rerun()  

    #Cálculos
    if submitted: 
        st.session_state["formulario_todas_bobinesROTULOS"] = {
            "unidades_por_caixa": unidades_por_caixa,
            "caixas": caixas,
            "unidades_soltas": unidades_soltas,
            "num_bobines": num_bobines,
            "bobines": dados_bobines,  # <- lista completa das bobines
        }
        guardar_dados()
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
        st.write(f"✔ Etiquetas válidas (excluindo inutilizados e amostras): **{total_rotulosvalidos} unidades**")

        #Verificação
        if producao_total == total_rotulosvalidos:
            st.success("Número de maços produzidos e número de etiquetas consistentes")
        else:
            st.warning(f"Diferença: {abs(producao_total - total_rotulosvalidos)} unidades")
            if (producao_total-total_rotulosvalidos)>0:
                st.error("O número de maços produzidos é **superior** ao número de etiquetas utilizadas")
            else:
                st.error("O número de maços produzidos é **inferior** ao número de etiquetas utilizadas")

        st.text(f"""Se estiver a fechar o processo e tiver obtido um resultado positivo na reconciliação das etiquetas, coloque os seguintes valores nos locais indicados:
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
