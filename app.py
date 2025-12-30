import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cadastro Extrativista - IDEFLOR-Bio", layout="wide")

# --- FUNÇÕES DE CONEXÃO COM GOOGLE SHEETS ---
def get_data():
    """Busca os dados atuais da planilha na nuvem."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        # Lê a planilha (ttl=0 garante que não pegue cache antigo)
        return conn.read(worksheet="Página1", ttl=0)
    except:
        # Se der erro ou estiver vazia, retorna DataFrame vazio
        return pd.DataFrame()

def salvar_no_google_sheets(novo_dado_dict):
    """Salva uma nova linha na planilha."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # 1. Carrega o que já existe lá
    df_existente = get_data()
    
    # 2. Cria o novo dado
    novo_df = pd.DataFrame([novo_dado_dict])
    
    # 3. Junta o antigo com o novo
    if df_existente.empty:
        df_final = novo_df
    else:
        df_final = pd.concat([df_existente, novo_df], ignore_index=True)
        
    # 4. Atualiza a planilha
    conn.update(worksheet="Página1", data=df_final)

# --- INTERFACE PRINCIPAL ---
def main():
    
# --- BARRA LATERAL (ADMIN) ---
    with st.sidebar:
        st.header("🔒 Área Administrativa")
        senha_digitada = st.text_input("Senha de Acesso", type="password")
        
        # Botão para validar (ajuda a garantir que o enter foi processado)
        validar = st.button("Acessar")

        if validar or senha_digitada:
            # Verifica se a senha existe nos Secrets
            if "SENHA_ADMIN" not in st.secrets:
                st.error("ERRO: A senha não foi configurada nos Secrets!")
            
            # Verifica se a senha bate
            elif senha_digitada == st.secrets["SENHA_ADMIN"]:
                st.success("✅ Acesso Liberado")
                
                try:
                    df = get_data()
                    if not df.empty:
                        st.write(f"📊 **{len(df)}** cadastros encontrados.")
                        st.dataframe(df)
                        
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "📥 Baixar Excel",
                            data=csv,
                            file_name="relatorio.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("⚠️ Conectado, mas a planilha está vazia ou com nome errado.")
                        st.info("Verifique se a aba da planilha chama 'Página1' ou 'Sheet1'.")
                except Exception as e:
                    st.error(f"Erro ao ler planilha: {e}")
            
            else:
                st.error("❌ Senha Incorreta!")
                st.caption(f"Dica: A senha configurada nos Secrets é '{st.secrets['SENHA_ADMIN']}'") 
                # (Remova a linha acima depois de testar por segurança!)

        st.markdown("---")
        st.info("Sistema v2.2 - Debug Mode 🐞")

    # --- CABEÇALHO DO FORMULÁRIO ---
    st.title("Cadastro de Extrativista 🌳")
    st.markdown("**INSTITUTO DE DESENVOLVIMENTO FLORESTAL E DA BIODIVERSIDADE - IDEFLOR-Bio**")
    st.caption("DGMUC - GRCN2 - FLOTA DO TROMBETAS")
    st.markdown("---")

    # --- INÍCIO DO FORMULÁRIO ---
    with st.form("form_cadastro", clear_on_submit=True):
        
        # 1. Dados Pessoais
        st.subheader("1. Dados Pessoais")
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo*")
        cpf = col2.text_input("CPF*")
        
        col3, col4 = st.columns(2)
        rg = col3.text_input("RG")
        nasc = col4.date_input("Data de Nascimento", min_value=datetime(1920, 1, 1), format="DD/MM/YYYY")
        
        col5, col6 = st.columns(2)
        sexo = col5.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        local_nasc = col6.text_input("Local de Nascimento")

        st.markdown("---")

        # 2. Dados Socioeconômicos
        st.subheader("2. Dados Socioeconômicos")
        col7, col8 = st.columns(2)
        escolaridade = col7.selectbox("Escolaridade", [
            "Não Alfabetizado", "Fundamental Incompleto", "Fundamental Completo", 
            "Médio Incompleto", "Médio Completo", "Superior Incompleto", "Superior Completo"
        ])
        profissao = col8.text_input("Profissão")
        
        col9, col10 = st.columns(2)
        renda = col9.text_input("Renda Mensal (R$)")
        contato = col10.text_input("Contato(s) / Telefone")

        endereco = st.text_input("Endereço Completo")
        municipio = st.text_input("Município")

        st.markdown("---")

        # 3. Atividade na Área
        st.subheader("3. Atividade na Área (Flota do Trombetas)")
        tempo = st.text_input("Trabalha há quanto tempo na área?")
        local_atua = st.text_area("Descrição da localização (Onde atua?)")
        
        produtos = st.multiselect(
            "Quais produtos coleta?",
            ["Castanha-do-Pará", "Cumaru", "Copaíba", "Andiroba", "Outros"]
        )

        st.markdown("---")

        # 4. Questionário
        st.subheader("4. Questionário e Opinião")
        
        c_p1, c_p2 = st.columns(2)
        sabe_flota = c_p1.radio("Sabe o que é uma Floresta Estadual?", ["SIM", "NÃO"], horizontal=True)
        exp_flota = c_p2.radio("Tem experiência com extrativismo na Flota?", ["SIM", "NÃO"], horizontal=True)
        
        sabe_adm = st.radio("Sabe qual Instituição administra a FLOTA?", ["SIM", "NÃO"], horizontal=True)
        
        opiniao = st.selectbox("Na sua opinião, a criação da FLOTA foi:", ["Bom", "Ruim", "Indiferente"])
        motivo = st.text_input("Por quê? (Justifique)")
        
        educ_amb = st.radio("Você já participou de alguma ação de Educação Ambiental?", ["SIM", "NÃO"], horizontal=True)

        st.markdown("---")
        
        # Termo e Envio
        termo = st.checkbox("Declaro que as informações são verdadeiras e assumo o compromisso de apresentar comprovantes quando solicitado.")
        
        submitted = st.form_submit_button("💾 SALVAR CADASTRO NA NUVEM", type="primary")

        if submitted:
            # Validação básica
            if not nome or not cpf or not termo:
                st.error("⚠️ Atenção: Preencha o NOME, CPF e aceite o TERMO DE COMPROMISSO.")
            else:
                # Prepara os dados para salvar
                dados = {
                    "Data Cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Nome": nome,
                    "CPF": cpf,
                    "RG": rg,
                    "Nascimento": nasc.strftime("%d/%m/%Y"),
                    "Sexo": sexo,
                    "Local Nascimento": local_nasc,
                    "Escolaridade": escolaridade,
                    "Profissao": profissao,
                    "Renda Mensal": renda,
                    "Contato": contato,
                    "Endereco": endereco,
                    "Municipio": municipio,
                    "Tempo na Area": tempo,
                    "Local Atuacao": local_atua,
                    "Produtos": ", ".join(produtos), # Transforma a lista em texto
                    "Sabe o que e Flota": sabe_flota,
                    "Exp Extrativismo Flota": exp_flota,
                    "Sabe quem Administra": sabe_adm,
                    "Opiniao Criacao": opiniao,
                    "Motivo Opiniao": motivo,
                    "Educacao Ambiental": educ_amb
                }
                
                try:
                    with st.spinner("Conectando ao Google Sheets..."):
                        salvar_no_google_sheets(dados)
                    st.success("✅ Cadastro realizado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
                    st.warning("Verifique se a planilha está compartilhada corretamente com o email do robô (service account).")

if __name__ == "__main__":

    main()
