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

### Tugas 5

1. Debouncing adalah teknik untuk delay eksekusi dari sebuah fungsi dengan jeda waktu tertentu tanpa ada event baru. Fitur ini penting digunakan saat menggunakan pencarian AJAX karena jika tidak menggunakan debouncing, setiap karakter yang diketik akan memicu satu request ke server (mengetik "test123" berarti 7 request). Akibatnya bandwith dan query database akan terbuang sia-sia dan resposne yang lambat akan menimpa hasil pencarian yang paling baru.
2. fetch() mengembalikan sebuah Promise, sedangkan await membuat program menunggu sampai Promise tersebut selesai sebelum lanjut ke next code. Tanpa await, variabel masih berisi Promise sehingga data belum bisa digunakan. await juga hanya dapat digunakan di dalam async function.
3. XSS (Cross-Site Scripting) adalah serangan ketika penyerang menyisipkan kode JavaScript berbahaya ke halaman web. Data yang ditampilkan melalui AJAX lebih rentan jika langsung dimasukkan ke innerHTML, karena JavaScript tidak melakukan auto-escaping seperti template Django. Oleh karena itu, data dari AJAX perlu di-escape atau dimasukkan menggunakan textContent agar dianggap sebagai teks, bukan HTML.

#### Disclosure AI
Saya menggunakan Claude untuk menanyakan beberapa sintaks yang baru digunakan saat mengganti forms.py bagian academic dan unit test baru. Setelah menanyakan sintaks2 tersebut saya mengonfirmasi ulang apa yang sudah saya buat dengan ketentuan yang ada di tugas dengan bantuan Claude.


### Tugas 6

1. REST adalah gaya arsitektur API yang memperlakukan data sebagai resource dengan URL sendiri, lalu aksinya ditentukan oleh method HTTP (GET, POST, PUT/PATCH, DELETE) dan status code yang sesuai. Mengembalikan JSON saja belum cukup karena JSON hanya format datanya. Contohnya endpoint seperti /delete_academic/ yang memakai POST dan selalu membalas 200 tetap belum RESTful. PUT mengganti seluruh data sehingga semua field harus dikirim, sedangkan PATCH hanya mengubah field yang dikirim. PUT cocok saat menimpa semua isian form, PATCH cocok saat hanya sebagian yang berubah, misalnya mengganti period saja.
2. Serializer berfungsi menerjemahkan objek model menjadi JSON dan sebaliknya, sekaligus memvalidasi input yang masuk. Keuntungannya dibanding merakit dictionary manual dengan JsonResponse, satu serializer bisa dipakai di semua endpoint (daftar, detail, tambah, ubah, star) sehingga format JSON-nya konsisten. Validasi dan strip_tags juga cukup ditulis di satu tempat, field hasil perhitungan seperti star_count dibuat read-only, dan kodenya lebih singkat.
3. Autentikasi memastikan siapa penggunanya (SessionAuthentication membaca session login), sedangkan otorisasi menentukan apa yang boleh dilakukan pengguna tersebut (permission class). Hak akses harus dicek di server karena menyembunyikan tombol di template hanya mengubah tampilan, sedangkan request tetap bisa dikirim langsung lewat console browser atau curl. Contohnya editor tidak punya tombol delete, tetapi jika ia mengirim request DELETE tetap akan ditolak 403 oleh permission class.
4. SessionAuthentication memakai cookie session yang otomatis dikirim browser, termasuk saat request berasal dari situs lain, sehingga penyerang bisa memalsukan request atas nama user yang sedang login. Token CSRF mencegah hal itu karena hanya halaman kita yang bisa mengirim token yang cocok. force_authenticate tidak cukup karena langsung mengisi user tanpa melewati proses login, sehingga pengecekan CSRF tidak pernah berjalan dan request tanpa token tetap lolos. Karena itu test CSRF memakai APIClient(enforce_csrf_checks=True) dengan .login() untuk membuktikan request tanpa token ditolak.

#### Disclosure AI
Saya menggunakan Claude untuk menyesuaikan beberapa fitur yang sudah saya buat di bagian projects ke academic. Ada beberapa part yang berbeda dimana di academic ada field untuk foto yang berbeda. Ada beberapa syntax juga yang ditanyakan untuk melengkapi apa yang kurang dibanding fitur di projects. Terakhir saya menggunakan claude untuk membuatkan unit test yang sesuai.
