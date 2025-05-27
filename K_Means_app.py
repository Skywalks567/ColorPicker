import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io
import requests
import matplotlib.pyplot as plt

# ===== Fungsi Utama =====
def get_dominant_colors(image, k=5):
    image_resized = image.resize((150, 150))
    img_array = np.array(image_resized)
    pixels = img_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors, pixels, kmeans.labels_

def display_color_palette(colors):
    with st.container(border=True):
        st.subheader("Palet Warna Dominan:")
        num_display_cols = min(len(colors), 5)
        cols = st.columns(num_display_cols if len(colors) > 0 else 1)
        
        for i, color in enumerate(colors):
            with cols[i % num_display_cols]:
                hex_color_val = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}".upper()
                rgb_color_val = f"({color[0]}, {color[1]}, {color[2]})"
                st.markdown(
                    f"""
                    <style>
                    .color-box {{
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }}

                    .color-box:hover {{
                        transform: scale(1.05);
                        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
                        cursor: pointer;
                    }}
                    </style>

                    <div class="color-box" style="
                        background-color: rgb({color[0]}, {color[1]}, {color[2]});
                        width: 100px;
                        height: 100px;
                        border-radius: 10px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        color: white;
                        font-weight: bold;
                        text-shadow: 1px 1px 2px black, -1px -1px 2px black, 1px -1px 2px black, -1px 1px 2px black;
                        text-align: center;
                        padding: 5px;
                        box-sizing: border-box;
                        margin-bottom: 10px;
                    ">
                        <div style="font-size: 0.8em;">
                            {hex_color_val}<br>
                            RGB:<br>{rgb_color_val}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ===== Konfigurasi Streamlit dan UI =====
st.set_page_config(page_title="Tugas AI Color Picker", page_icon="🖼️", layout="wide")

#CSS untuk page
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        overflow: hidden;
        z-index: 0;
    }

/* Tambahkan elemen pseudo untuk blur */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        background-image: url("https://github.com/Skywalks567/ColorPicker/blob/main/img/Background-image.png?raw=true");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        filter: blur(12px) brightness(0.7);
        z-index: -1; /* agar berada di belakang konten */
    }
    [data-testid="stVerticalBlockBorderWrapper"] { 
        position: relative;
        z-index: 1;
        max-width: 950px;
        margin: 48px auto;
        padding: 24px; /* Memberi jarak antara tepi kontainer ini dengan kolom kaca di dalamnya */
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stHorizontalBlock"]{
        background = None !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Color Picker")
st.markdown("Made by Raymond Frans Dodi Situmorang")

# ===== Session State =====
if 'uploaded_file_value_for_logic' not in st.session_state:
    st.session_state.uploaded_file_value_for_logic = None
if 'use_example_checked_for_logic' not in st.session_state:
    st.session_state.use_example_checked_for_logic = False
if 'show_kmeans_grafik' not in st.session_state:
    st.session_state.show_kmeans_grafik = False
if 'grafik_data_kmeans' not in st.session_state:
    st.session_state.grafik_data_kmeans = None

# ===== Callback =====
def handle_file_change_snippet():
    st.session_state.uploaded_file_value_for_logic = st.session_state.uploader_widget_key_snippet
    if st.session_state.uploaded_file_value_for_logic is not None:
        st.session_state.use_example_checked_for_logic = False
        st.session_state.grafik_data_kmeans = None

def handle_checkbox_change_snippet():
    st.session_state.use_example_checked_for_logic = st.session_state.example_checkbox_key_snippet
    if st.session_state.use_example_checked_for_logic:
        st.session_state.uploaded_file_value_for_logic = None
        st.session_state.grafik_data_kmeans = None

# ===== Input Widget =====
col_kiri, col_kanan = st.columns([1, 1.2])
with col_kiri:
    uploaded_file = st.file_uploader(
        "📁Upload Gambar",
        type=["jpg", "jpeg", "png"],
        key="uploader_widget_key_snippet",
        on_change=handle_file_change_snippet,
        disabled=st.session_state.use_example_checked_for_logic
    )

    Contoh_Gambar_URL = "https://github.com/Skywalks567/ColorPicker/blob/main/img/example.jpg?raw=true"
    use_example = st.checkbox(
        "🖼️Coba dengan gambar contoh",
        key="example_checkbox_key_snippet",
        on_change=handle_checkbox_change_snippet,
        disabled=(st.session_state.uploaded_file_value_for_logic is not None)
    )

# ===== Logika Gambar =====
image_to_process_snippet = None
k_value = 5
with col_kanan:
    
    if st.session_state.use_example_checked_for_logic:
        image_bytes_response = requests.get(Contoh_Gambar_URL)
        image_to_process_snippet = Image.open(io.BytesIO(image_bytes_response.content)).convert('RGB')
        st.info("Menggunakan gambar contoh.")
        st.image(image_to_process_snippet, caption="Gambar Contoh", use_container_width=True)

    elif st.session_state.uploaded_file_value_for_logic is not None:
        image_bytes_data = st.session_state.uploaded_file_value_for_logic.getvalue()
        image_to_process_snippet = Image.open(io.BytesIO(image_bytes_data)).convert('RGB')
        st.image(image_to_process_snippet, caption=f"Gambar Diunggah: {st.session_state.uploaded_file_value_for_logic.name}", use_container_width=True)

    else:
        if not st.session_state.use_example_checked_for_logic and st.session_state.uploaded_file_value_for_logic is None:
            st.info("Gambar kamu akan ditampilkan disini")
    
if st.session_state.use_example_checked_for_logic:
    try:
        image_bytes_response = requests.get(Contoh_Gambar_URL)
        image_bytes_response.raise_for_status()
        image_to_process_snippet = Image.open(io.BytesIO(image_bytes_response.content)).convert('RGB')
        with st.spinner("Menganalisis warna gambar contoh... ⏳"):
            dominant_colors, pixels, labels = get_dominant_colors(image_to_process_snippet, k=k_value)
            st.session_state.grafik_data_kmeans = (pixels, labels, dominant_colors)
        st.success("Palet Warna Dominan Berhasil Dibuat!")
        display_color_palette(dominant_colors)
    except Exception as e:
        st.error(f"Error: Gagal memproses gambar contoh. Detail: {e}")
        image_to_process_snippet = None
        st.session_state.grafik_data_kmeans = None

elif st.session_state.uploaded_file_value_for_logic is not None:
    image_bytes_data = st.session_state.uploaded_file_value_for_logic.getvalue()
    try:
        image_to_process_snippet = Image.open(io.BytesIO(image_bytes_data)).convert('RGB')
        with st.spinner("Menganalisis warna gambar unggahan... ⏳"):
            dominant_colors, pixels, labels = get_dominant_colors(image_to_process_snippet, k=k_value)
            st.session_state.grafik_data_kmeans = (pixels, labels, dominant_colors)
        st.success("Palet Warna Dominan Berhasil Dibuat!")
        display_color_palette(dominant_colors)
    except Exception as e:
        st.error(f"Error: Gagal memproses gambar yang diunggah. Pastikan file gambar valid. Detail: {e}")
        image_to_process_snippet = None
        st.session_state.grafik_data_kmeans = None
else:
    if not st.session_state.use_example_checked_for_logic and st.session_state.uploaded_file_value_for_logic is None:
        st.info("Silakan unggah gambar atau centang 'Coba dengan gambar contoh'.")
        st.session_state.grafik_data_kmeans = None

# ===== Grafik K-Means =====
if image_to_process_snippet is not None and st.session_state.grafik_data_kmeans is not None:
    st.markdown("---")
    st.checkbox("Tampilkan Grafik Sebaran Warna K-Means", key="show_kmeans_grafik")

    if st.session_state.show_kmeans_grafik:
        plot_pixels, plot_labels, plot_centers = st.session_state.grafik_data_kmeans
        st.markdown("#### Visualisasi Sebaran Piksel dan Pusat Cluster")
        fig, ax = plt.subplots(figsize=(8, 6))

        sample_size = min(5000, plot_pixels.shape[0])
        sample_indices = np.random.choice(plot_pixels.shape[0], size=sample_size, replace=False)
        sampled_plot_pixels = plot_pixels[sample_indices]

        ax.scatter(sampled_plot_pixels[:, 0], sampled_plot_pixels[:, 1], c=sampled_plot_pixels / 255.0, alpha=0.5, s=10)
        ax.scatter(plot_centers[:, 0], plot_centers[:, 1], c=plot_centers / 255.0, marker='X', s=200, edgecolor='black', linewidth=1.5)

        ax.set_title('Grafik K-Means berdasarkan gambar yang diupload')
        ax.set_xlabel('Principal Komponen 1')
        ax.set_ylabel('Principal Komponen 2')
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.grid(True, linestyle='--', alpha=0.7)

        st.pyplot(fig)
        st.caption("Titik-titik kecil merepresentasikan sampel piksel dari gambar. Tanda 'X' menunjukkan pusat cluster (warna dominan).")
