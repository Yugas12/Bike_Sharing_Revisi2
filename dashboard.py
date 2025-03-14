import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load dataset
file_path = os.path.join(os.path.dirname(__file__), "data_terbaru.csv")
df = pd.read_csv(file_path)

# Konversi tanggal ke format datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Sidebar filter
st.sidebar.header("Filter Data")

# Filter Tahun
years = sorted(df["dteday"].dt.year.unique())
selected_year = st.sidebar.selectbox("Pilih Tahun", years, index=len(years)-1)
df_filtered = df[df["dteday"].dt.year == selected_year]

# Filter Musim (Pilihan Tunggal)
seasons = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season = st.sidebar.selectbox("Pilih Musim", options=seasons.keys(), format_func=lambda x: seasons[x])
df_filtered = df_filtered[df_filtered["season_y"] == selected_season]

# Dashboard Title
st.title("Dashboard Peminjaman Sepeda")

# Grafik 1: Tren Peminjaman Sepeda dari Bulan ke Bulan
st.subheader("📈 Tren Jumlah Peminjaman Sepeda dari Bulan ke Bulan")
plt.figure(figsize=(10, 5))
sns.lineplot(x=df_filtered.resample('M', on='dteday').mean().index, y=df_filtered.resample('M', on='dteday').mean()['cnt_y'], marker='o', linewidth=2)
plt.xlabel("Bulan")
plt.ylabel("Rata-rata Jumlah Peminjaman")
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Grafik 2: Hubungan Suhu dengan Peminjaman Sepeda
st.subheader("🌡️ Hubungan antara Suhu dan Jumlah Peminjaman Sepeda")
plt.figure(figsize=(8, 5))
sns.regplot(x=df_filtered["temp_y"], y=df_filtered["cnt_y"], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.xlabel("Suhu (Normalized)")
plt.ylabel("Jumlah Peminjaman Sepeda")
plt.grid(True)
st.pyplot(plt)

st.write("Dashboard ini memungkinkan eksplorasi tren peminjaman sepeda berdasarkan tahun dan musim yang dipilih serta melihat korelasi antara suhu dan jumlah peminjaman.")
