# Web Documentation Scraper

Program ini adalah web scraper yang dirancang untuk mengekstrak dan menyimpan konten dari dokumentasi web. Program akan mengumpulkan semua link yang ada dalam dokumentasi dan menyimpannya ke dalam database SQLite.

Akan sangat berguna jika Anda ingin mengumpulkan informasi dari dokumentasi web untuk keperluan menambah **knowledge base** atau pengembangan **AI**

## Fitur

- Mengekstrak semua link dari halaman dokumentasi
- Menyimpan link dan konten ke dalam database SQLite
- Menghindari duplikasi dengan pengecekan URL yang sudah diproses
- Mendukung scraping konten dari link yang ditemukan
- Tracking status proses scraping untuk setiap link

## Instalasi

1. Clone repository ini
2. Buat virtual environment (opsional tapi direkomendasikan):
```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Penggunaan

Jalankan program dengan perintah:
```bash
python main.py [URL_DOKUMENTASI]
```

Contoh:
```bash
python main.py https://docs.python.org/3/
```

## Struktur Database

Program menggunakan SQLite dengan dua tabel utama:

### Tabel `documentations`
- `id`: Primary key
- `base_url`: URL utama dokumentasi
- `domain`: Domain dari dokumentasi
- `is_processed`: Status pemrosesan (boolean)
- `created_at`: Waktu pembuatan record
- `last_updated`: Waktu terakhir update

### Tabel `documentation_links`
- `id`: Primary key
- `doc_id`: Foreign key ke tabel documentations
- `url`: URL dari link
- `title`: Judul atau teks link
- `is_processed`: Status pemrosesan link
- `content`: Konten yang di-scrape
- `created_at`: Waktu pembuatan record
- `last_updated`: Waktu terakhir update

## Pengembangan Lebih Lanjut

Beberapa ide untuk pengembangan:
- Menambahkan dukungan untuk autentikasi
- Implementasi rate limiting
- Menambahkan fitur export data
- Implementasi sistem antrian untuk pemrosesan parallel
- Menambahkan GUI atau web interface
