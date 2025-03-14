import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ambil dataset yang sudah diclear pada file ipynb
@st.cache_data
def load_data():
    return pd.read_csv("all_data.csv")

df = load_data()
df["order_date"] = pd.to_datetime(df["order_purchase_timestamp"]).dt.date
min_date, max_date = df["order_date"].min(), df["order_date"].max()

# Filter Rentang Waktu, bagian ini mengikuti conoh yang ada ada modul
with st.sidebar:
    st.image("icon.png", width=200)
    start_date, end_date = st.date_input(
        "Tentukan Rentang Waktu:", min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

    st.markdown(
        """
        <style>
            .profile-box {
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 5px;
                text-align: center;
            }
        </style>

        <h4 style="text-align: center;">👤 Data Diri</h4>

        <div class="profile-box"><b>Ananta Boemi Adji</b></div>
        <div class="profile-box">Universitas Brawijaya</div>
        <div class="profile-box"><b>Cohort ID:</b> Ananta Boemi Adji</div>
        <div class="profile-box"><b>Study Group:</b> MC-49</div>
        """,
        unsafe_allow_html=True
    )

# Filter dataset berdasarkan rentang waktu
main_df = df[(df["order_date"] >= start_date) & (df["order_date"] <= end_date)]

st.title("📊 Dashboard Analisis E-Commerce")

st.markdown("""
    **Dashboard ini akan menunjukkan hasil analisis data e-commerce dalam rentang waktu 4 September 2016 - 3 September 2018.**  
    Informasi yang ditampilkan adalah sebagai berikut:  
    1️⃣ **Jumlah Review Score Pengguna**  
    2️⃣ **Distribusi Metode Pembayaran** (metode yang paling sering digunakan)  
    3️⃣ **Kategori produk yang paling laris dibeli**  
    4️⃣ **Jumlah Pengguna dari setiap State**  
    5️⃣ **Pengaruh Harga Barang terhadap Review**  
    6️⃣ **Hubungan Waktu Pengiriman dengan Review**  

    📌 **Anda juga bisa melihat hasil data dalam rentang waktu yang lebih spesifik dengan mengatur filter di samping kiri.**  

    🔍 **Selamat mencoba! 🎉**
""")

# 1. Bagaimana jumlah Review Score Pengguna?
st.header("1. Jumlah Review Score Pengguna ⭐")
review_counts = main_df["review_score"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.bar(review_counts.index.astype(str), review_counts.values, color="#3498db")  # Biru cerah
ax.set_title("Jumlah Review Skor")
ax.set_xlabel("Review Score")
ax.set_ylabel("Jumlah Review")
st.pyplot(fig)

st.write("""
    📍 **Kesimpulan data pengguna dalam rentang waktu 4 September 2016 - 3 September 2018:​**
    Sebagian besar review score menunjukan nilai yang baik yaitu pada score 5. 
Tapi score review 1 masih bisa dibilang cukup banyak dengan jumlah menyentuh 10000 review.
    """)

# 2. Bagaimana Distribusi Metode Pembayaran, Mana yang Paling Sering Digunakan?
st.header("2. Distribusi Metode Pembayaran 💳")

payment_counts = main_df["payment_type"].value_counts()
selected_payments = ["credit_card", "boleto", "voucher", "debit_card", "not_defined"]
filtered_payment_counts = payment_counts[payment_counts.index.isin(selected_payments)]
fig, ax = plt.subplots()

ax.bar(filtered_payment_counts.index, filtered_payment_counts.values, color="#3498db")

ax.set_xticklabels(filtered_payment_counts.index, rotation=45)
ax.set_title("Distribusi Metode Pembayaran")
ax.set_xlabel("Metode Pembayaran")
ax.set_ylabel("Jumlah Transaksi")

st.pyplot(fig)

st.write("""
    📍 **Kesimpulan data pengguna dalam rentang waktu 4 September 2016 - 3 September 2018:**
    Metode pembayaran yang paling sering digunakan adalah menggunakan Credit card
""")

# 3. Bagaimana hasil penjualan produk?
st.header("3. Kategori produk yang paling laris dibeli Pengguna 🛒")
category_counts = main_df["product_category_name"].value_counts().nlargest(10)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax, color="#3498db")
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Pembelian")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
st.pyplot(fig)

# Karena saya lupa untuk mengubah translate dari kategori produk maka saya menggantikan denan sebuah tabel agar pengguna bisa melihat terjemahan
data = {
    "Kategori Asli": [
        "agro_industria_e_comercio", "alimentos_bebidas", "artigos_de_festas",
        "artes", "artes_e_artesanato", "automotivo", "bebe", "beleza_saude",
        "brindes", "cama_mesa_banho", "casa_construcao", "cine_foto",
        "clinica_medica", "consoles_games", "construcao_ferramentas",
        "cool_stuff", "eletrodomesticos", "eletroportateis", "esporte_lazer",
        "fashion_bolsas_e_acessorios", "fashion_calcados", "fashion_esporte",
        "fashion_roupa_masculina", "fashion_roupa_feminina", "fashion_roupa_infantil",
        "flores", "ferramentas", "fraldas_higiene", "industria_comercio_e_negocios",
        "informatica_acessorios", "instrumentos_musicais", "livros_interesse_geral",
        "livros_tecnicos", "malas_acessorios", "mercado", "moveis_decoracao",
        "moveis_escritorio", "moveis_sala", "papelaria", "perfumaria", "pet_shop",
        "relogios_presentes", "roupas_e_acessorios", "smartphones_tablets",
        "tablets_impressao_imagem", "telefonia", "utilidades_domesticas"
    ],
    "Terjemahan": [
        "Agribusiness & Commerce", "Food & Beverages", "Party Supplies",
        "Arts", "Arts & Crafts", "Automotive", "Baby", "Beauty & Health",
        "Gifts", "Bedding & Bath", "Home & Construction", "Cinema & Photography",
        "Medical Clinic Equipment", "Consoles & Games", "Construction & Tools",
        "Cool Stuff", "Home Appliances", "Small Appliances", "Sports & Leisure",
        "Fashion Bags & Accessories", "Footwear", "Sports Fashion",
        "Men's Clothing", "Women's Clothing", "Children's Clothing",
        "Flowers", "Tools", "Diapers & Hygiene", "Industry, Commerce & Business",
        "Computer Accessories", "Musical Instruments", "General Interest Books",
        "Technical Books", "Suitcases & Accessories", "Market", "Furniture & Decoration",
        "Office Furniture", "Living Room Furniture", "Stationery", "Perfumery", "Pet Shop",
        "Watches & Gifts", "Clothes & Accessories", "Smartphones & Tablets",
        "Tablets, Printing & Imaging", "Telephony", "Household Utilities"
    ]
}

# Dataframe translate
df_kategori = pd.DataFrame(data)

# Menampilkan tabel
st.write("### **Kategori Produk dalam Bahasa Inggris**")
st.dataframe(df_kategori, use_container_width=True)

# 4. Demografik Pengguna dari setiap State
st.header("4. Demografik Pengguna dari Setiap State 🌍")
state_counts = main_df["customer_state"].value_counts()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=state_counts.index, y=state_counts.values, ax=ax, color="#3498db"
            )
ax.set_xlabel("Negara Bagian (State)")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Kepanjangan state
data_states = {
    "Kode State": ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                   "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                   "RS", "RO", "RR", "SC", "SP", "SE", "TO"],
    "Nama Lengkap": ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", 
                     "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão",
                     "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", 
                     "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", 
                     "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", 
                     "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]
}

# DataFrame untuk state
df_states = pd.DataFrame(data_states)

# Menampilkan tabel
st.write("### **Kode State dan Nama Lengkap**")
st.dataframe(df_states, use_container_width=True)

st.write("""
    📍 **Kesimpulan data pengguna dalam rentang waktu 4 September 2016 - 3 September 2018:**
    Jumlah pengguna didominasi oleh pengguna dari state San Paulo dengan total melebihi 40000 pengguna atau lebih 
    tepatnya sebanyak 41746 pengguna.
""")

# 5. Bagaimana Pengaruh Harga Barang terhadap Review Pengguna?
st.header("5. Pengaruh Harga Barang terhadap Review Pengguna 💰")
price_review_avg = main_df.groupby("review_score")["price"].mean()
fig, ax = plt.subplots()
sns.barplot(x=price_review_avg.index, y=price_review_avg.values, ax=ax, color="#3498db")
ax.set_xlabel("Skor Review")
ax.set_ylabel("Harga Rata-rata (BRL)")
st.pyplot(fig)

st.write("""
    📍 **Kesimpulan pengaruh harga terhadap review barang dengan rentang waktu 4 September 2016 - 3 September 2018:**
    Score review tidak berhubungan dengan harga barang. Bisa dilihat dari setiap review score dari skala 1 - 5 memiliki nilai rata-rata yang tidak terlalu berbeda jauh.
""")

# 6. Bagaimana Hubungan Waktu Pengiriman dengan Review Pengguna?
st.header("6. Hubungan Waktu Pengiriman dengan Review Pengguna ⏳")
if "delivery_days" not in main_df.columns:
    main_df["delivery_days"] = (
        pd.to_datetime(main_df["order_delivered_customer_date"]) - 
        pd.to_datetime(main_df["order_purchase_timestamp"])
    ).dt.days

delivery_review_avg = main_df.groupby("review_score")["delivery_days"].mean()

fig, ax = plt.subplots()
sns.lineplot(x=delivery_review_avg.index, y=delivery_review_avg.values, marker="o", color="#3498db", ax=ax)
ax.set_xlabel("Skor Review")
ax.set_ylabel("Rata-rata Waktu Pengiriman (Hari)")
st.pyplot(fig)

st.write("""
    📍 **Hubungan Waktu Pengiriman dengan Review Pengguna waktu 4 September 2016 - 3 September 2018:​**
    Salah satu penyebab dari review yang rendah diakibatkan oleh waktu pengiriman yang lama, semakin cepat barang sampai review yang diberikan semakin baik
""")