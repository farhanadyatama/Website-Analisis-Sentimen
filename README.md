# Website Analisis Sentimen (IndoBERT)

Aplikasi web sederhana yang dibangun menggunakan Flask untuk menganalisis sentimen teks berbahasa Indonesia. Aplikasi ini menggunakan model IndoBERT untuk melakukan prediksi sentimen (Positif, Negatif, Netral).

## Fitur Utama
- **Analisis Teks Tunggal**: Menganalisis sentimen dari satu kalimat yang dimasukkan pengguna.
- **Analisis File CSV**: Menganalisis banyak kalimat sekaligus dengan mengunggah file `.csv`.
- **Hasil Analisis Komprehensif (CSV)**: Menampilkan ringkasan jumlah sentimen dan pratinjau data.
- **Hasil Teks Tunggal**: Menampilkan hasil prediksi dari teks tunggal yaitu positif, negatif, atau netral.
- **Unduh Hasil**: Pengguna dapat mengunduh hasil analisis lengkap dalam format `.csv`.

## Cara Menjalankan Proyek Secara Lokal

1.  **Clone Repositori**
    ```bash
    git clone [https://github.com/farhanadyatama/Website-Analisis-Sentimen.git](https://github.com/farhanadyatama/Website-Analisis-Sentimen.git)
    cd Website-Analisis-Sentimen
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    ```bash
    # Membuat venv
    python -m venv venv

    # Mengaktifkan venv (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install Library yang Dibutuhkan**
    Pastikan Anda berada di lingkungan virtual yang aktif, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Siapkan Model**
    Unduh model IndoBERT yang sudah di-*fine-tune*, lalu letakkan di dalam folder proyek dengan nama `indobert`. Strukturnya akan terlihat seperti ini:
    ```
    /Website-Analisis-Sentimen
        /indobert
        /templates
        .gitignore
        app.py
        requirements.txt
    ```

5.  **Jalankan Aplikasi**
    ```bash
    python app.py
    ```
    Buka browser dan akses alamat `http://127.0.0.1:5000`.


* ### `Model yang digunakan pada website (Indobert)`
    * https://drive.google.com/drive/folders/1SixFVfE1fsBTQ13PNahvdefldMAaodNq?usp=sharing.
