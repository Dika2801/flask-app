from flask import Flask, request, render_template
import google.generativeai as genai
from PIL import Image
import io

# Inisialisasi Aplikasi Flask
app = Flask(__name__)

# --- KONFIGURASI PENTING ---
# Ganti dengan API Key Gemini Anda yang asli
GOOGLE_API_KEY = 'AIzaSyAyK5c8fbZiRct2qErVL5ZM0wBelXs2asQ'

# --- Inisialisasi Model AI ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Berhasil terhubung ke Gemini AI.")
except Exception as e:
    print(f"Gagal konfigurasi Gemini AI: {e}")
    model = None

# --- Fungsi untuk Analisis Gambar ---
def analyze_trading_chart(image_bytes):
    if not model:
        return "Error: Model AI tidak terkonfigurasi. Cek API Key."

    # Blok try yang membutuhkan except
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # PROMPT BARU (AGRESIF) UNTUK SCALPER
        prompt = """
        Anda adalah seorang scalper dan day trading yang agresif dengan spesialisasi pada timeframe kecil dan besar. Tujuan utama Anda adalah menemukan peluang trading jangka panjang dengan target minimal (80 pips), tetapi jika tidak menemukan carilah jangka pendek dengan target profit minimal (50 pips).

        Analisis gambar chart trading ini dari sudut pandang seorang scalper ataupun day trading. Fokus pada momentum jangka pendek dan menenhah, pola candlestick kecil, dan level support/resistance minor.

        Berdasarkan analisis tersebut, berikan:
        1.  **Saran Aksi:** **BUY** atau **SELL**.
        2.  **Rekomendasi Take Profit (TP):** Berikan 1-2 level harga untuk target profit dalam rentang minimal 50 pips.
        3.  **Rekomendasi Stop Loss (SL):** Berikan level harga yang logis untuk stop loss, jaga Risk-Reward Ratio tetap baik.
        4. **Titik entry:** area entry yang baik di harga berapa.
        5.  **Alasan Singkat:** Jelaskan secara singkat dan padat mengapa Anda memilih posisi BUY atau SELL berdasarkan sinyal scalping atau day trading yang terlihat.

        Jika market terlihat sideways, gunakan indikator seperti RSI, MACD, atau breakout support/resistance kecil untuk tetap menentukan BUY atau SELL yang paling potensial. Jangan pernah menjawab dengan kata WAIT atau SKIP.
        """
        
        response = model.generate_content([prompt, img])
        return response.text

    # Ini adalah blok 'except' yang kemungkinan terhapus
    except Exception as e:
        return f"Terjadi error saat menganalisis gambar: {e}"

# --- Halaman Utama Aplikasi ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return "Tidak ada file yang dipilih!", 400
        
        file = request.files['image']
        
        if file.filename == '':
            return "Tidak ada file yang dipilih!", 400
            
        if file:
            img_bytes = file.read()
            result_text = analyze_trading_chart(img_bytes)

    return render_template('index.html', result=result_text)

# --- Menjalankan Server Flask ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

