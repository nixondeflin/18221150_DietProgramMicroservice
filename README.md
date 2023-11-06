# Diet Program Recommendation Service

## Tentang
Diet Program Service merupakan RESTful API yang dirancang untuk memberikan rekomendasi diet yang dipersonalisasi berdasarkan profil pengguna. API ini mengelola informasi pengguna, termasuk berat badan, tinggi badan, usia, jenis kelamin, tingkat aktivitas, dan tujuan diet. Layanan ini menghitung dan merekomendasikan asupan kalori harian, distribusi makronutrien, dan makanan yang disarankan untuk makanan-makanan berbeda. API ini dibangun menggunakan FastAPI dan menggunakan file JSON untuk penyimpanan data.

## Fitur
* Menambahkan pengguna baru, mengambil detail pengguna, memperbarui informasi pengguna, dan menghapus pengguna dari sistem.
* Memberikan rekomendasi diet yang dipersonalisasi berdasarkan profil pengguna, termasuk asupan kalori harian, distribusi makronutrien, dan makanan yang disarankan untuk makanan.
* Data pengguna dan rekomendasi diet disimpan dalam file JSON untuk pengambilan data dan modifikasi data yang mudah.

## How to Use

Sebelum menggunakan API Service, terlebih dahulu kita harus mempunyai hal-hal di bawah ini
* Python 3.6+
* FastAPI
* Uvicorn (for running the API server)
