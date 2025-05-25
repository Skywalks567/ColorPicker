import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io # Diperlukan untuk menangani byte gambar dari unggahan

# Fungsi untuk mengekstrak warna dominan
def get_dominant_colors(image, k=5):
    # Mengubah ukuran gambar untuk pemrosesan lebih cepat (opsional)
    image = image.resize((150, 150))
    # Mengonversi gambar ke array NumPy
    img_array = np.array(image)
    # Meratakan array gambar menjadi daftar piksel RGB
    pixels = img_array.reshape(-1, 3)

    # Menerapkan K-Means
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto') # Menambahkan n_init untuk menghindari warning
    kmeans.fit(pixels)

    # Mendapatkan pusat cluster (warna dominan)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

# Fungsi untuk menampilkan palet warna
def display_color_palette(colors):
    st.subheader("Palet Warna Dominan:")
    cols = st.columns(len(colors)) # Buat kolom sebanyak jumlah warna
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6 !important;
        }
        main {
            background-color: #f0f2f6 !important;
        }
        html, body, main {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        </style>
        
        """,
        unsafe_allow_html=True
    )
    for i, color in enumerate(colors):
        with cols[i]:
            # Membuat kotak warna dengan HTML dan CSS sederhana
            st.markdown(
                f"""
                <div style="
                    background-color: rgb({color[0]}, {color[1]}, {color[2]});
                    width: 100px;
                    height: 100px;
                    border-radius: 10px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white; /* Warna teks agar kontras */
                    font-weight: bold;
                    text-shadow: 1px 1px 2px black; /* Bayangan teks untuk keterbacaan */
                    text-align: center;
                ">
                    <div>
                        RGB:<br>
                        {color[0]}, {color[1]}, {color[2]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# Judul Aplikasi
st.set_page_config(page_title="Color Palette Generator", layout="wide") # Mengatur konfigurasi halaman
st.title("Color Picker Gambar")
st.markdown("Upload Gambar")

# Komponen Unggah File
uploaded_file = st.file_uploader("Pilih sebuah gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Membaca gambar yang diunggah
    image_bytes = uploaded_file.getvalue()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB') # Pastikan gambar dalam format RGB

        st.image(image, caption="Gambar yang Diunggah", use_column_width=True)
        with st.spinner("Menganalisis warna... ⏳"):
            dominant_colors = get_dominant_colors(image, k=5)
        st.success("Palet Warna Berhasil Dibuat!")
        display_color_palette(dominant_colors)

    except Exception as e:
        st.error(f"Error: Gagal memproses gambar. Pastikan file gambar valid. Detail: {e}")

