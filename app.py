import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cadastro Extrativista - IDEFLOR-Bio", layout="wide")

# --- FUNÇÕES DE CONEXÃO ---
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        return conn.read(worksheet="Página1", ttl=0)
    except:
        return pd.DataFrame()

def salvar_no_google_sheets(novo_dado_dict):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_existente = get_data()
    novo_df = pd.DataFrame([novo_dado_dict])
    
    if df_existente.empty:
        df_final = novo_df
    else:
        df_final = pd.concat([df_existente, novo_df], ignore_index=True)
        
    conn.update(worksheet="Página1", data=df_final)

# --- INTERFACE PRINCIPAL ---
def main():
    # 1. Controle de Estado (Memória da Tela de Sucesso)
    if "cadastro_sucesso" not in st.session_state:
        st.session_state["cadastro_sucesso"] = False

    # 2. Barra Lateral (Admin)
    with st.sidebar:
        st.header("🔒 Área Administrativa")
        senha_digitada = st.text_input("Senha de Acesso", type="password")
        
        # Botão para forçar a verificação
        if st.button("Acessar Admin"):
            if "SENHA_ADMIN" in st.secrets:
                if senha_digitada == st.secrets["SENHA_ADMIN"]:
                    st.success("✅ Acesso Liberado")
                    try:
                        df = get_data()
                        st.metric("Total Cadastrado", len(df))
                        st.download_button("📥 Baixar Planilha (Excel)", df.to_csv(index=False).encode('utf-8'), "dados_flota.csv")
                        st.dataframe(df)
                    except Exception as e:
                        st.error(f"Erro ao ler planilha: {e}")
                else:
                    st.error("Senha Incorreta")
            else:
                st.warning("Senha não configurada nos Secrets.")

    # 3. Lógica de Exibição (Formulário vs Sucesso)
    if st.session_state["cadastro_sucesso"]:
        # --- TELA DE SUCESSO ---
        st.title("✅ Cadastro Realizado com Sucesso!")
        st.markdown("---")
        st.success("As informações foram salvas no banco de dados da nuvem.")
        st.info("O sistema está pronto para o próximo extrativista.")
        
        # Botão que reinicia o processo
        if st.button("⬅️ Fazer Novo Cadastro", type="primary"):
            st.session_state["cadastro_sucesso"] = False
            st.rerun()

    else:
        # --- FORMULÁRIO COMPLETO ---
        col_logo, col_text = st.columns([1, 5])
        with col_text:
            st.title("Cadastro de Extrativista 🌳")
            st.caption("DGMUC - GRCN2 - FLOTA DO TROMBETAS")
        st.markdown("---")

        with st.form("form_cadastro", clear_on_submit=True):
            
            # BLOCO 1: DADOS PESSOAIS
            st.subheader("1. Dados Pessoais")
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome Completo*")
            cpf = c2.text_input("CPF*")
            
            c3, c4 = st.columns(2)
            rg = c3.text_input("RG")
            nasc = c4.date_input("Data de Nascimento", min_value=datetime(1920, 1, 1), format="DD/MM/YYYY")
            
            c5, c6 = st.columns(2)
            sexo = c5.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            local_nasc = c6.text_input("Local de Nascimento")

            st.markdown("---")

            # BLOCO 2: DADOS SOCIOECONÔMICOS
            st.subheader("2. Dados Socioeconômicos")
            c7, c8 = st.columns(2)
            # Lista completa conforme PDF original
            escolaridade = c7.selectbox("Escolaridade", [
                "Não Alfabetizado", "Fundamental Incompleto", "Fundamental Completo", 
                "Médio Incompleto", "Médio Completo", "Superior Incompleto", "Superior Completo"
            ])
            profissao = c8.text_input("Profissão")
            
            c9, c10 = st.columns(2)
            renda = c9.text_input("Renda Mensal (R$)")
            contato = c10.text_input("Contato(s) / Telefone")

            endereco = st.text_input("Endereço Completo")
            municipio = st.text_input("Município")

            st.markdown("---")

            # BLOCO 3: ATIVIDADE NA ÁREA
            st.subheader("3. Atividade na Área")
            tempo = st.text_input("Trabalha há quanto tempo na área?")
            local_atua = st.text_area("Descrição da localização (Onde atua?)")
            
            produtos = st.multiselect(
                "Quais produtos coleta?",
                ["Castanha-do-Pará", "Cumaru", "Copaíba", "Andiroba", "Outros"]
            )

            st.markdown("---")

            # BLOCO 4: QUESTIONÁRIO
            st.subheader("4. Opinião e Conhecimento")
            
            cp1, cp2 = st.columns(2)
            sabe_flota = cp1.radio("Sabe o que é uma Floresta Estadual?", ["SIM", "NÃO"], horizontal=True)
            exp_flota = cp2.radio("Tem experiência com extrativismo na Flota?", ["SIM", "NÃO"], horizontal=True)
            
            sabe_adm = st.radio("Sabe qual instituição administra a FLOTA?", ["SIM", "NÃO"], horizontal=True)
            
            opiniao = st.selectbox("Na sua opinião, a criação da FLOTA foi:", ["Bom", "Ruim", "Indiferente"])
            motivo = st.text_input("Por quê? (Justifique)")
            
            educ_amb = st.radio("Já participou de ação de Educação Ambiental?", ["SIM", "NÃO"], horizontal=True)

            st.markdown("---")
            termo = st.checkbox("Declaro que as informações são verdadeiras.")
            
            # BOTÃO DE ENVIO
            submitted = st.form_submit_button("Salvar Cadastro na Nuvem ☁️", type="primary")

            if submitted:
                if not nome or not cpf or not termo:
                    st.error("⚠️ Preencha Nome, CPF e aceite o Termo.")
                else:
                    # Prepara os dados
                    dados = {
                        "Data Cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "Nome": nome, "CPF": cpf, "RG": rg,
                        "Nascimento": nasc.strftime("%d/%m/%Y"), "Sexo": sexo,
                        "Local Nascimento": local_nasc,
                        "Escolaridade": escolaridade, "Profissao": profissao,
                        "Renda Mensal": renda, "Contato": contato,
                        "Endereco": endereco, "Municipio": municipio,
                        "Tempo na Area": tempo, "Local Atuacao": local_atua,
                        "Produtos": ", ".join(produtos),
                        "Sabe o que e Flota": sabe_flota,
                        "Exp Extrativismo Flota": exp_flota,
                        "Sabe quem Administra": sabe_adm,
                        "Opiniao Criacao": opiniao, "Motivo Opiniao": motivo,
                        "Educacao Ambiental": educ_amb
                    }
                    
                    try:
                        with st.spinner("Salvando no Google Drive..."):
                            salvar_no_google_sheets(dados)
                        
                        # Ativa a tela de sucesso
                        st.session_state["cadastro_sucesso"] = True
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")

if __name__ == "__main__":
    main()

