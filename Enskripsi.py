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
# =========================
# Kunci Dinamis
# =========================
# Default key (bisa diubah user)
DEFAULT_KEY = "101011"

key_input = st.text_input("Masukkan Key Barcode (contoh: 101011)", DEFAULT_KEY)
KEY_PATTERN = ''.join([c for c in key_input if c in ['0','1']])

st.caption("Bit 1 = garis hitam | Bit 0 = garis putih")

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
# Fungsi Generate Barcode Custom (EAN-like, Hitam-Putih Murni)
# =========================
def generate_custom_barcode(cipher_numbers):
    """
    Membuat barcode hitam-putih sederhana ala EAN.
    Hitam = 1, Putih = 0
    Setiap angka diubah ke biner 7-bit (mirip EAN concept)
    """
    bars = []
    for num in cipher_numbers:
        binary = format(num, '07b')  # 7-bit biner
        bars.extend(list(binary))
        bars.append('0')  # separator
    return bars


def render_barcode_image(bars):
    from PIL import Image, ImageDraw

    bar_width = 4
    height = 120
    width = len(bars) * bar_width

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    for i, bit in enumerate(bars):
        if bit == '1':
            x0 = i * bar_width
            x1 = x0 + bar_width
            draw.rectangle([x0, 0, x1, height], fill="black")

    return img


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

        st.write("### Barcode Custom (EAN-like)")
        st.info("Barcode ini adalah representasi biner hitam-putih ala EAN (custom, tanpa library)")

        bars = generate_custom_barcode(cipher)
        barcode_img = render_barcode_image(bars)
        st.image(barcode_img, caption="Custom Barcode B-ENC (Hitam = 1, Putih = 0)", use_column_width=True)

        st.write("### Diagram Transformasi")
        st.markdown("Plaintext → Angka → Ciphertext → Biner → Barcode")

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

