import streamlit as st
from typing import List

# =========================
# Konfigurasi Halaman
# =========================
st.set_page_config(
    page_title="B-ENC Barcode Cipher",
    page_icon="📊",
    layout="centered"
)

st.title("📊 B-ENC: Barcode-Based Encryption Cipher")
st.write("Aplikasi enkripsi & dekripsi teks berbasis konsep barcode (sesuai laporan B-ENC)")

# =========================
# Konstanta & Kunci
# =========================
KEY_PATTERN = "101011"  # barcode key

# =========================
# Fungsi Konversi
# =========================
def text_to_numbers(text: str) -> List[int]:
    result = []
    for char in text.lower():
        if char == " ":
            result.append(0)
        elif 'a' <= char <= 'z':
            result.append(ord(char) - 96)
    return result


def numbers_to_text(numbers: List[int]) -> str:
    text = ""
    for num in numbers:
        if num == 0:
            text += " "
        elif 1 <= num <= 26:
            text += chr(num + 96)
    return text


# =========================
# Fungsi Enkripsi
# =========================
def encrypt(numbers: List[int]) -> List[int]:
    encrypted = []
    for num in numbers:
        value = num
        for bit in KEY_PATTERN:
            if bit == '1':
                value += 3
            else:
                value -= 1
        encrypted.append(value)
    return encrypted


# =========================
# Fungsi Generate Barcode (Code128)
# =========================
def generate_barcode(data: str):
    import barcode
    from barcode.writer import ImageWriter
    from io import BytesIO

    code128 = barcode.get('code128', data, writer=ImageWriter())
    buffer = BytesIO()
    code128.write(buffer)
    return buffer


# =========================
# Fungsi Dekripsi
# =========================
def decrypt(numbers: List[int]) -> List[int]:
    decrypted = []
    for num in numbers:
        value = num
        for bit in KEY_PATTERN:
            if bit == '1':
                value -= 3
            else:
                value += 1
        decrypted.append(value)
    return decrypted


# =========================
# UI Streamlit
# =========================
menu = st.radio("Pilih Mode:", ["🔐 Enkripsi", "🔓 Dekripsi"])

if menu == "🔐 Enkripsi":
    st.subheader("Enkripsi Plaintext → Barcode Cipher")
    plaintext = st.text_area("Masukkan plaintext:", "kriptografi menyenangkan")

    if st.button("Enkripsi"):
        numeric = text_to_numbers(plaintext)
        cipher = encrypt(numeric)

        st.write("### Konversi ke Angka")
        st.code(numeric)

        st.write("### Ciphertext (Angka Barcode)")
        cipher_str = ' '.join(map(str, cipher))
        st.code(cipher_str)

        st.write("### Visual Barcode (Scannable)")
        st.info("Barcode di bawah ini dapat dipindai menggunakan scanner / Google Lens")
        barcode_img = generate_barcode(cipher_str)
        st.image(barcode_img, caption="Barcode Ciphertext (Code-128)", use_column_width=True)

elif menu == "🔓 Dekripsi":
    st.subheader("Dekripsi Barcode Cipher → Plaintext")
    cipher_input = st.text_area(
        "Masukkan ciphertext (pisahkan dengan spasi):",
        "20 27 18 25 29 24 16 27 10 15 18 9 22 14 23 34 14 23 10 23 16 20 10 23"
    )

    if st.button("Dekripsi"):
        cipher_numbers = list(map(int, cipher_input.split()))
        decrypted_nums = decrypt(cipher_numbers)
        plaintext = numbers_to_text(decrypted_nums)

        st.write("### Hasil Angka Dekripsi")
        st.code(decrypted_nums)

        st.write("### Plaintext")
        st.success(plaintext)


st.markdown("---")
st.caption("Metode B-ENC | Kriptografi Simetris Berbasis Barcode | Nayla Rachmaddina")
