# 🌳 Sistema de Cadastro de Extrativistas - Flota do Trombetas

Aplicação web desenvolvida para digitalizar o cadastramento de famílias extrativistas na Floresta Estadual (FLOTA) do Trombetas. O sistema substitui fichas de papel, coleta dados via formulário digital e salva automaticamente em uma planilha segura na nuvem (Google Sheets).

## 🚀 Funcionalidades

* **Formulário Digital:** Réplica fiel da ficha de cadastro do IDEFLOR-Bio (Dados Pessoais, Socioeconômicos, Atividade e Opinião).
* **Banco de Dados na Nuvem:** Integração direta com Google Sheets via API.
* **Área Administrativa:** Painel protegido por senha para visualizar contagem de cadastros e baixar relatórios (Excel/CSV).
* **Feedback Visual:** Tela de confirmação de envio e fluxo contínuo para múltiplos cadastros.
* **Responsividade:** Interface adaptada para celulares, tablets e computadores.

## 🛠️ Tecnologias

* **Python 3.9+**
* [Streamlit](https://streamlit.io/) (Interface Web)
* [Pandas](https://pandas.pydata.org/) (Manipulação de Dados)
* [Streamlit GSheets Connection](https://github.com/streamlit/gsheets-connection) (Conector Google)

## 📂 Como Rodar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/sistema-flota.git](https://github.com/SEU-USUARIO/sistema-flota.git)
    cd sistema-flota
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as Credenciais (Secrets):**
    Crie uma pasta `.streamlit` na raiz do projeto e um arquivo `secrets.toml` dentro dela com o seguinte formato:

    ```toml
    # Senha do Admin na primeira linha
    SENHA_ADMIN = "12345"

    [connections.gsheets]
    spreadsheet = "LINK_DA_SUA_PLANILHA_GOOGLE"
    type = "service_account"
    project_id = "seu-project-id"
    private_key_id = "..."
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
    client_email = "seu-robo@..."
    client_id = "..."
    auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
    token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
    auth_provider_x509_cert_url = "..."
    client_x509_cert_url = "..."
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

## ☁️ Deploy no Streamlit Cloud

1.  Suba este código para o GitHub.
2.  Acesse [share.streamlit.io](https://share.streamlit.io) e conecte o repositório.
3.  Nas configurações do App (**Settings > Secrets**), cole o conteúdo do seu arquivo `secrets.toml`.
4.  Certifique-se de que o **Python Version** nas configurações avançadas seja **3.9** ou **3.10**.
5.  **Importante:** Compartilhe a planilha do Google com o `client_email` do seu robô (Service Account) com permissão de **Editor**.

---
**Desenvolvido para apoio à gestão da DGMUC - GRCN2.**
