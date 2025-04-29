import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import cv2  

# Load model
MODEL_PATH = 'model/my_model.keras'
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image, target_size=(128, 128)):
    img = image.resize(target_size)  # Ubah ukuran gambar ke (128, 128)
    img = img.convert('RGB')  # Pastikan gambar dalam format RGB
    img_array = np.array(img) / 255.0  # Normalisasi gambar
    return np.expand_dims(img_array, axis=0)  # Tambahkan batch dimension


# Custom CSS with updated styles
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        color: #2c3e50;
        background: linear-gradient(to right, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # st.image("images/logo code scanner.jpeg", width=100)  # Tambahkan logo Anda di sini
    st.markdown("## Tentang Aplikasi")
    st.write("Aplikasi ini membantu Anda mendeteksi kode QR yang berpotensi berbahaya")
    
    st.markdown("### Cara penggunaan:")
    st.write("1. Unggah gambar kode QR")
    st.write("2. Tunggu proses analisis")
    st.write("3. Periksa status keamanan")
    
    st.markdown("### Format yang didukung:")
    st.write("PNG, JPG, JPEG")

# Main content
st.markdown("<h1 class='main-header'>🔍 QR Code Safety Scanner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Lindungi dirimu dari kode QR berbahaya</p>", unsafe_allow_html=True)

# Upload section with new layout
# st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Pilih gambar kode QR untuk dipindai", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Membuat tab untuk organisasi yang lebih baik
    tab1, tab2 = st.tabs(["Hasil Analisis", "Detail Gambar"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption='Kode QR yang Diunggah', use_column_width=True)
        
        with col2:
            with st.spinner('Menganalisis Kode QR...'):
                input_data = preprocess_image(image)
                prediction = model.predict(input_data)
                
                if prediction[0][0] > 0.5:
                    st.error("⚠️ Kode QR Berbahaya Terdeteksi!")
                    st.markdown("""
                        <div style='background-color: #ffe6e6; padding: 15px; border-radius: 10px; border: 1px solid #ff9999;'>
                            <h4 style='color: #cc0000;'>Peringatan Keamanan:</h4>
                            <ul>
                                <li>Kode QR ini telah diidentifikasi sebagai berpotensi berbahaya</li>
                                <li>Pemindaian tidak direkomendasikan</li>
                                <li>Harap buang kode QR ini dengan aman</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ Kode QR Aman Terverifikasi")
                    st.markdown("""
                        <div style='background-color: #e6ffe6; padding: 15px; border-radius: 10px; border: 1px solid #99ff99;'>
                            <h4 style='color: #006600;'>Konfirmasi Keamanan:</h4>
                            <ul>
                                <li>Kode QR ini tampak sah</li>
                                <li>Aman untuk dipindai</li>
                                <li>Tetap berhati-hati seperti biasa</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        st.write("Informasi Gambar:")
        st.write(f"Nama file: {uploaded_file.name}")
        st.write(f"Ukuran file: {uploaded_file.size/1024:.2f} KB")
        st.write(f"Dimensi gambar: {image.size}")

# Footer with updated styling
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Made with ❤️ by Rifdah Hansya Rofifah </p>
        <p style='font-size: 0.8em;'>Versi 1.0</p>
    </div>
""", unsafe_allow_html=True)
