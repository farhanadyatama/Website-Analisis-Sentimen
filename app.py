# Impor semua library yang dibutuhkan
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import traceback
import os 
import uuid 
from collections import Counter

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# --- Konfigurasi Folder ---
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Tentukan path untuk model IndoBERT
MODEL_PATH = './indobert' 

# --- Memuat Model IndoBERT ---
try:
    print("Memuat Model IndoBERT...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    print("IndoBERT berhasil dimuat.")
except Exception as e:
    print(f"Error saat memuat model: {e}")
    # Jika model gagal dimuat, hentikan aplikasi
    exit()

# Definisikan label sentimen
sentiment_labels = {0: "Positif", 1: "Netral", 2: "Negatif"}

# --- Fungsi Prediksi Sentimen ---
def predict_sentiment(text):
    """Fungsi untuk memprediksi sentimen dari satu teks menggunakan model yang sudah dimuat."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    prediction_idx = torch.argmax(outputs.logits, dim=1).item()
    return sentiment_labels.get(prediction_idx, "Tidak Diketahui")

# --- Rute Halaman Utama ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Rute untuk Prediksi ---
@app.route('/predict', methods=['POST'])
def predict_route():
    file = request.files.get('file_upload')
    text_input = request.form.get('text_input')

    # --- Logika untuk Analisis File CSV ---
    if file and file.filename != '':
        try:
            # --- BLOK UNTUK MEMBACA FILE DENGAN AMAN ---
            try:
                # 1. Coba baca dengan encoding standar (UTF-8) dan engine python yang lebih fleksibel
                df = pd.read_csv(file, encoding='utf-8', engine='python')
            except UnicodeDecodeError:
                # 2. Jika gagal, coba lagi dengan encoding alternatif (latin-1)
                file.seek(0) # Penting: kembalikan pointer file ke awal
                df = pd.read_csv(file, encoding='latin-1', engine='python')
            
            # Cek apakah kolom 'text' ada setelah file berhasil dibaca
            if 'text' not in df.columns:
                error_message = "File yang Anda unggah wajib .csv dan memiliki kolom dengan nama 'text'."
                return render_template('400.html', error_message=error_message), 400
            
            # Hapus baris yang kosong di kolom 'text'
            df.dropna(subset=['text'], inplace=True)

            # Lakukan prediksi untuk setiap baris
            results = [{'text': text, 'sentiment': predict_sentiment(str(text))} for text in df['text']]
            
            # Hitung jumlah setiap sentimen
            sentiment_counts = Counter(item['sentiment'] for item in results)
            
            # Siapkan data untuk chart agar urutannya tetap
            fixed_labels = ["Positif", "Netral", "Negatif"]
            chart_data = [sentiment_counts.get(label, 0) for label in fixed_labels]

            # Simpan hasil ke file CSV baru
            results_df = pd.DataFrame(results)
            unique_filename = f"hasil_analisis_{uuid.uuid4().hex}.csv"
            filepath = os.path.join(DOWNLOAD_FOLDER, unique_filename)
            results_df.to_csv(filepath, index=False, encoding='utf-8-sig')

            return render_template(
                'result_table.html', 
                results=results[:5],
                counts=sentiment_counts,
                total_data=len(results),
                result_filename=unique_filename,
                model_used="IndoBERT",
                chart_labels=fixed_labels,
                chart_data=chart_data
            )
            
        except pd.errors.ParserError:
            # Tangani jika struktur CSV tidak konsisten (misal: jumlah kolom berbeda-beda)
            error_message = "Gagal membaca file. Mohon pastikan file Anda adalah file CSV dan memiliki kolom 'text', bukan format file lain."
            return render_template('400.html', error_message=error_message), 400
        except Exception as e:
            # Tangani semua error tak terduga lainnya
            print(traceback.format_exc())
            return render_template('500.html'), 500
    
    # --- Logika untuk Analisis Teks Tunggal ---
    elif text_input:
        prediction = predict_sentiment(text_input)
        return render_template('result.html', text_input=text_input, prediction=prediction, model_used='INDOBERT')
    
    # Jika tidak ada input, kembali ke halaman utama
    return redirect(url_for('home'))

# --- Rute Download dan Error Handler ---
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.errorhandler(500)
def internal_server_error(e):
    print(traceback.format_exc())
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)