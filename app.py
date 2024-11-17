import streamlit as st
from auth import login_user, register_user
from encryption import extract_text_from_image, encrypt_text, encrypt_image, save_encrypted_data, decrypt_text
from db_config import get_db_connection
import base64
from io import BytesIO
from PIL import Image


st.title("SISTEM PENNYIMPANAN HASIL EKSTRAKSI TEKS DARI GAMBAR")

menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Enkripsi", "Dekripsi", "Lihat Data"])

if menu == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success("Login berhasil!")
            st.session_state["authenticated"] = True
        else:
            st.error("Username atau password salah!")

elif menu == "Register":
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Pendaftaran berhasil!")
        else:
            st.error("Username sudah ada!")

elif menu == "Enkripsi":
    if st.session_state.get("authenticated"):
        st.subheader("Enkripsi")
        uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])
        
        if uploaded_file:
            # Load image
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar diunggah", use_column_width=True)
            
            # Extract text from image
            extracted_text = extract_text_from_image(image)
            st.write("Teks yang diambil:", extracted_text)

            # Encrypt text
            encrypted_text = encrypt_text(extracted_text)
            st.write("Teks terenkripsi:", encrypted_text)

            # Encrypt image (convert image to base64)
            encrypted_image = encrypt_image(image)
            st.write("Gambar terenkripsi:")
            st.image(base64.b64decode(encrypted_image), caption="Gambar Terenkripsi", use_column_width=True)

            # Save encrypted data to DB
            save_encrypted_data(uploaded_file.getvalue(), extracted_text, encrypted_text, encrypted_image)

            st.success("Data berhasil dienkripsi dan disimpan.")
        else:
            st.warning("Silakan unggah gambar terlebih dahulu!")
    else:
        st.warning("Silakan login terlebih dahulu!")


elif menu == "Dekripsi":
    if st.session_state.get("authenticated"):
        st.subheader("Dekripsi")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, encrypted_image FROM encrypted_data")
        data = cursor.fetchall()
        conn.close()

        if data:
            selected_id = st.selectbox("Pilih ID untuk dekripsi", [row[0] for row in data])
            selected_encrypted_image = next(row[1] for row in data if row[0] == selected_id)
            
            # Decrypt the image
            decrypted_image = base64.b64decode(selected_encrypted_image)
            image = Image.open(BytesIO(decrypted_image))
            
            st.image(image, caption="Gambar yang Dikembalikan", use_column_width=True)
            
            st.success("Gambar berhasil didekripsi.")
        else:
            st.warning("Tidak ada data terenkripsi.")
    else:
        st.warning("Silakan login terlebih dahulu!")

elif menu == "Lihat Data":
    if st.session_state.get("authenticated"):
        st.subheader("Data Terenkripsi")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text, encrypted_text, date FROM encrypted_data")
        data = cursor.fetchall()
        conn.close()

        if data:
            st.write(data)
        else:
            st.warning("Tidak ada data di database.")
    else:
        st.warning("Silakan login terlebih dahulu!")
