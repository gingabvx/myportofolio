Nama : Rama

NPM : 2506606490

Kelas : PBP D


## Instruksi Setup Menjalankan Proyek
Untuk run proyek statid web ini secara lokal, lakukan langkah-langkah berikut:
1. Pull versi terbaru atau clone repositori ini.
2. Buka terminal dan arahkan ke dalam root direktori.
3. Aktifkan virtual environment (jika menggunakan) dan pastikan dependensi Django sudah terinstal.
4. Jalankan server lokal dengan command: `python manage.py runserver`
5. Buka browser dan akses alamat `http://localhost:8000/`.

### Tugas 1

1. Iya, saya gunakan <section> seperti di contoh template di index untuk di academics.html. Iya ini membantu untuk langsung mengorganisir div lebih mudah dari biasanya serta lebih mudah dibaca.
2. Tantangan tata letak terbesar yang saya temukan adalah menyesuaikan posisi konten agar tidak berantakan saat ukuran layar menyempit. Karena saya tidak mengubah terlalu banyak layout dari kerangka awal yang disediakan, penyesuaian yang saya lakukan adalah menambah class baru untuk mengatur grid yang saya reverse dari yang disediakan.
3. Karena website yang saya buat saat ini masih static web, salah satu batasan yang saya rasakan adalah saya masih harus menulis segala teks deskriptif langsung di file html nya. Berdasarkan batasan tersebut, di iterasi proyek selanjutnya saya akan mencoba implementasi database menggunakan MVT agar isi portofolio bisa ditambah secara otomatis.

#### Disclosure AI
Saya menggunakan Gemini AI untuk membantu dalam styling CSS. Ada bagian yang cukup membuat error dimana saya awalnya ingin membuat ulang dari awal untuk section 2 di academis.html. Daripada saya bingung terlalu lama saya menanyakan hint ke Gemini AI untuk jawabannya dan memberikan konteks permasalahan css untuk mendapatkan solusinyas.
https://share.gemini.google/RB0PeBvM1hf3


### Tugas 2
1. Ketika user mengakses web portofolio, request pertama kali diterima oleh urls.py proyek untuk diteruskan ke urls.py aplikasi. Di urls.py aplikasi, rute academic/ dicocokkan lalu diarahkan ke fungsi view terkait, yaitu show_academic. View ini bertugas memproses logic dan memanggil data dari model Academic di models.py yang mengambil datanya dari database. Terakhir, view mengirimkan data tersebut ke template (academic.html) untuk dirender, lalu akhirnya browser menampilkan web portofolio tersebut ke user.
2. Karena dengan menggunakan model, kita tidak perlu menghardcode semuanya langsung di file htmlnya. Kita bisa langsung menginput dan mendelete data dengan menggunakan django admin. Dengan cara ini, jika kita memiliki puluhan data, kita dapat lebih mudah untuk merawat dan membuat perubahan untuk datanya. 
3. makemigrations menginisiasi pembuatan file migration baru dan membaca models.py, namun tidak mengubah database. migrate lalu mengupdate database kita sesuai model baru yang sudah dibaca makemigrations di models.py. Contoh saat kita memerlukan kedua perintah ini ketika kita membuat model baru. Seperti saya di web ini dimana saya membuat model Academic. Saya memerlukan kedua perintah itu setelah saya selesai membuat model Academic saya.

#### Disclosure AI
Saya menggunakan Gemini AI untuk menanyakan sintaks dan memberikan hint. Di html saya, saya hanya kekurangan satu sintaks untuk menampilkan grid yang berbeda secara selang seling. Oleh karena itu, saya menanyakan sintaks dan hint untuk memakainya ke Gemini AI. Di akhir saya mengonfirmasi kalau perubahan yang saya lakukan di academic.html tidak memperlukan perubahan di cssnya.
https://share.gemini.google/tAauFX55OXzA

### Tugas 3
1. Kita menggunakan ModelForm karena Django secara otomatis membuatkan struktur form dan validasi data langsung dari model yang sudah kita buat sehingga kita tidak perlu menulis tag input HTML dan logika validasinya secara manual dari nol. Lalu, {% csrf_token %} wajib ditambahkan untuk melindungi aplikasi dari serangan CSRF dengan memastikan bahwa request POST yang masuk benar-benar berasal dari website kita, bukan dari pihak luar.
2. JSON lebih disukai daripada XML dalam pengembangan web modern karena formatnya jauh lebih ringkas, ringan, dan mudah dibaca manusia karena struktur pasangan key-value. Selain itu, JSON dapat langsung diparse secara native dan cepat oleh javascript di sisi frontend tanpa membutuhkan parser XML yang rumit.
3. Alur dimulai saat client mengakses rute API, lalu fungsi view mengambil data dari database melalui model Django, kemudian data tersebut diubah ke bentuk teks JSON lewat fungsi serializer, dan akhirnya dikembalikan sebagai respons menggunakan HttpResponse dengan tipe application/json. Proses serialization wajib dilakukan karena data yang diambil dari database masih berbentuk objek Python (QuerySet), yang tidak bisa langsung dikirimkan atau dipahami oleh browser atau aplikasi lain melalui protokol HTTP sebelum diubah ke format teks standar seperti JSON.

#### Disclosure AI
Saya menggunakan Gemini AI untuk menanyakan sintaks dan memberikan hint. Saya membutuhkan beberapa sintaks untuk field2 baru di academic dan beberapa konfirmasi ulang untuk code yang baru saya buat.
https://share.gemini.google/1uxH14Cc2W2R