import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io 

def get_dominant_colors(image, k=5):

    image = image.resize((150, 150))

    img_array = np.array(image)

    pixels = img_array.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

def display_color_palette(colors):
    with st.container(border=True):
        st.subheader("Palet Warna Dominan:")
        cols = st.columns(len(colors))
        for i, color in enumerate(colors):
            with cols[i]:
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
                        color: white;
                        font-weight: bold;
                        text-shadow: 1px 1px 2px black;
                        text-align: center;
                    ">
                        <div>
                            #{color[0]:02x}{color[1]:02x}{color[2]:02x}<br>
                            RGB:<br>({color[0]}, {color[1]}, {color[2]})
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


st.set_page_config(page_title="Tugas AI Color Picker", layout="centered")
st.title("Color Picker")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://api2.kemenparekraf.go.id/storage/app/resources/PARIWISATA_STORYNOMICS_TOURISM_shutterstock_385096972_franshendrik_Tambunan_d03d3440db.jpg");
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# untuk upload file
uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

Contoh_Gambar_URL = "https://github.com/Skywalks567/ColorPicker/blob/main/example_img/wallpaperflare.com_wallpaper%20(5).jpg?raw=true"
use_example = st.checkbox("Coba dengan gambar contoh")
if uploaded_file is not None:
    # read gambar yang diupload
    image_bytes = uploaded_file.getvalue()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        st.image(image, caption="Gambar yang Diunggah", use_container_width=True)
        with st.spinner("Menganalisis warna... ⏳"):
            dominant_colors = get_dominant_colors(image, k=5)
        st.success("Palet Warna Dominan Berhasil Dibuat!")
        display_color_palette(dominant_colors)

    except Exception as e:
        st.error(f"Error: Gagal memproses gambar. Pastikan file gambar valid. Detail: {e}")

