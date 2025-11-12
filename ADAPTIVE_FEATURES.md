# 🚀 Fitur Adaptif Sistem Sentivize

## Overview
Sistem Sentivize telah ditingkatkan dengan kemampuan **adaptif** yang dapat menangani berbagai tipe dan struktur data secara otomatis.

## ✨ Fitur-Fitur Adaptif

### 1. **Smart Excel Parsing**
Sistem dapat membaca file Excel dengan struktur kompleks:

#### Kemampuan:
- ✅ **Multi-Sheet Detection**: Otomatis mencari sheet yang paling relevan
- ✅ **Dynamic Header Detection**: Mencoba berbagai baris (0-10) sebagai header
- ✅ **Unnamed Column Handling**: Menangani file dengan semua kolom "unnamed"
- ✅ **Merged Cell Recovery**: Mendeteksi dan menggunakan header yang benar
- ✅ **Quality Scoring**: Memilih sheet dengan data terbaik berdasarkan scoring

#### Scoring Algorithm:
```python
score = (valid_columns * 10) + 
        (non_empty_ratio * 100) + 
        (string_columns * 5) + 
        min(num_rows, 100)
```

#### Contoh:
```python
# File dengan struktur kompleks akan otomatis diperbaiki:
# Before: unnamed:_0, unnamed:_1, unnamed:_2, ...
# After: nama_pegawai, jabatan, unit_kerja, ...
```

---

### 2. **Intelligent Column Detection**

#### 4-Tier Detection Strategy:

**Tier 1: Keyword Matching**
- Mencari kolom dengan kata kunci spesifik
- Keywords: `nama`, `pegawai`, `karyawan`, `nip`, `staff`, dll
- Case-insensitive dan flexible

**Tier 2: Content Analysis**
- Menganalisis isi kolom dengan algoritma scoring
- Cek karakteristik nama:
  - ✅ Mengandung spasi (nama depan + belakang)
  - ✅ Memiliki huruf kapital
  - ✅ Panjang 5-50 karakter
  - ✅ Unik (tidak berulang)
  - ❌ Bukan email, URL, atau angka

**Tier 3: String Analysis**
- Mencari kolom dengan mayoritas data string
- Threshold: 50% data harus string valid
- Panjang minimal: 3 karakter

**Tier 4: First Available**
- Menggunakan kolom pertama dengan data valid
- Last resort untuk file yang sangat tidak standar

#### Scoring Details:
```python
# Name Detection Score
score += (has_spaces / total) * 30        # Spaces in name
score += (has_capitals / total) * 20      # Capital letters
score += 20 if 5 <= avg_length <= 50     # Reasonable length
score += 20 if unique_ratio > 0.7         # Uniqueness
score += (10 - col_index) * 2             # Earlier columns
score *= 0.3 if has_non_name_patterns     # Penalize URLs/emails
```

---

### 3. **Multi-Format Support**

#### Supported Formats:
| Format | Extension | Features |
|--------|-----------|----------|
| CSV | `.csv` | Multiple encoding detection (utf-8, latin-1, cp1252) |
| Excel | `.xlsx`, `.xls` | Multi-sheet, dynamic headers, merged cells |
| JSON | `.json` | Nested object flattening |

#### Auto-Encoding Detection:
```python
encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
# Tries each encoding until successful
```

---

### 4. **Column Normalization**

#### Automatic Cleanup:
- ✅ Lowercase semua nama kolom
- ✅ Replace spasi dengan underscore
- ✅ Remove special characters
- ✅ Remove multiple underscores
- ✅ Trim leading/trailing underscores

#### Example:
```python
# Before
"Nama Lengkap Pegawai"
"No. Induk Pegawai (NIP)"
"Unit Kerja / Bagian"

# After
"nama_lengkap_pegawai"
"no_induk_pegawai_nip"
"unit_kerja_bagian"
```

---

### 5. **Auto Column Detection**

#### Detected Columns:
1. **Name Column** (Required)
   - Keywords: nama, name, pegawai, karyawan, nip, staff
   - Content-based detection with scoring

2. **Position Column** (Optional)
   - Keywords: jabatan, posisi, position, title, role
   - Content detection: mencari kata seperti "kepala", "direktur", "manajer"

3. **Unit Column** (Optional)
   - Keywords: unit, bagian, divisi, departemen, dinas, kantor

4. **Social Media Column** (Optional)
   - Keywords: social, sosial, media, facebook, linkedin, instagram, link

5. **Text/Description Column** (Optional)
   - Keywords: deskripsi, description, keterangan, info, detail
   - Auto-detect: kolom dengan teks terpanjang

---

### 6. **Data Validation & Cleanup**

#### Auto-cleanup:
- ✅ Remove completely empty rows
- ✅ Remove completely empty columns
- ✅ Keep columns with ≥10% data
- ✅ Reset index after cleanup
- ✅ Validate data quality

#### Quality Metrics:
```python
non_empty_ratio = notna().sum() / total_cells
useful_column = non_empty_ratio >= 0.1  # 10% threshold
```

---

### 7. **Enhanced Error Handling**

#### Informative Error Messages:
```python
# Before
"Error: Column not found"

# After
"Kolom nama tidak ditemukan. Pastikan file memiliki kolom dengan nama karyawan/pegawai.
Kolom yang ditemukan: col_0, col_1, data_pegawai, jabatan, ..."
```

#### Debug Information:
- ✅ Jumlah baris dan kolom terdeteksi
- ✅ Nama kolom yang ditemukan
- ✅ Kolom nama yang digunakan
- ✅ Sheet yang dipilih (untuk Excel)

---

## 🎯 Use Cases

### Case 1: Excel Pemerintah dengan Merged Headers
```
File: Peta_Jabatan_Dinas_2024.xlsx
Struktur: Header di baris 3, merged cells, 98 kolom

✅ Sistem otomatis:
- Scan rows 0-10 untuk header
- Skip empty rows
- Deteksi kolom nama dengan content analysis
- Clean column names
```

### Case 2: CSV dengan Encoding Non-Standar
```
File: data_pegawai_legacy.csv
Encoding: cp1252 (Windows Latin)

✅ Sistem otomatis:
- Try utf-8 → fail
- Try latin-1 → fail
- Try cp1252 → success
```

### Case 3: Multi-Sheet Excel
```
File: laporan_sdm_lengkap.xlsx
Sheets: Cover, Data_Pegawai, Statistik, Grafik

✅ Sistem otomatis:
- Score setiap sheet
- Pilih sheet dengan data terbaik
- Ignore cover dan grafik
```

---

## 📊 Performance

### Speed:
- CSV (1000 rows): ~0.5 detik
- Excel single sheet (1000 rows): ~1-2 detik
- Excel multi-sheet dengan scanning: ~3-5 detik

### Memory:
- Efficient column filtering (remove empty columns)
- Stream processing untuk file besar
- Auto garbage collection

---

## 🔧 Configuration

### Customizable Keywords:
File: `config.py`

```python
NAME_KEYWORDS = ['nama', 'name', 'pegawai', 'karyawan', 'nip', 'no', 'staff']
POSITION_KEYWORDS = ['jabatan', 'posisi', 'position', 'title', 'role']
UNIT_KEYWORDS = ['unit', 'bagian', 'divisi', 'departemen', 'dinas']
SOCIAL_KEYWORDS = ['social', 'sosial', 'media', 'link', 'facebook', 'instagram']
TEXT_KEYWORDS = ['deskripsi', 'description', 'keterangan', 'info', 'detail']
```

### Thresholds:
```python
MIN_STRING_RATIO = 0.5      # 50% data harus string untuk kolom nama
MIN_DATA_RATIO = 0.1        # 10% data untuk kolom dianggap valid
MIN_NAME_SCORE = 20         # Score minimal untuk name detection
HEADER_SCAN_ROWS = 10       # Scan hingga baris 10 untuk header
```

---

## 🎨 UI Features

### Preview dengan Deteksi Kolom:
```
📊 Informasi File: 67 baris, 15 kolom

🎯 Kolom Terdeteksi:
✅ Nama: `nama_lengkap`
✅ Jabatan: `jabatan_fungsional`
✅ Unit: `unit_kerja`
⚪ Social Media: Tidak terdeteksi (opsional)
⚪ Teks/Deskripsi: Tidak terdeteksi (opsional)

📋 Preview Data:
[Tabel 10 baris pertama]

📂 Lihat Semua Nama Kolom
nama_lengkap, nip, jabatan_fungsional, unit_kerja, ...
```

---

## 🚦 Status Indicators

| Icon | Meaning | Action |
|------|---------|--------|
| ✅ | Column detected | Ready to analyze |
| ❌ | Required column missing | Fix file or manual mapping |
| ⚪ | Optional column missing | Can still analyze |
| ⚠️ | Warning/fallback used | Review detection |

---

## 💡 Best Practices

### For Users:
1. **Upload file dengan struktur standar jika memungkinkan**
2. **Gunakan preview untuk validasi deteksi kolom**
3. **Pastikan kolom nama terdeteksi (✅) sebelum analisis**
4. **File dengan <100 kolom lebih cepat diproses**

### For Data Preparation:
1. **Hindari merged cells jika memungkinkan**
2. **Header sebaiknya di baris pertama**
3. **Gunakan nama kolom yang jelas**
4. **Hapus rows dan columns kosong**

### For Troubleshooting:
1. **Lihat preview untuk cek deteksi**
2. **Periksa "Semua Nama Kolom" jika deteksi gagal**
3. **Cek encoding jika ada karakter aneh**
4. **Export ke CSV standar jika Excel terlalu kompleks**

---

## 🔮 Future Enhancements

### Planned:
- [ ] Manual column mapping UI
- [ ] Custom keyword configuration in UI
- [ ] Template management (save/load column mappings)
- [ ] Batch file processing
- [ ] Database connection support
- [ ] API for programmatic access

### Under Consideration:
- [ ] ML-based column detection
- [ ] Auto data type inference
- [ ] Data quality scoring
- [ ] Duplicate detection
- [ ] Data validation rules

---

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Multi-sheet Excel support
- ✅ Dynamic header detection
- ✅ 4-tier column detection
- ✅ Content-based name detection with scoring
- ✅ Auto encoding detection
- ✅ Column normalization
- ✅ Enhanced preview with status indicators

### Version 1.0
- ✅ Basic CSV/Excel reading
- ✅ Simple keyword-based detection
- ✅ Single sheet Excel support

---

## 🆘 Support

### Common Issues:

**Q: Kolom nama tidak terdeteksi?**
A: Periksa preview untuk melihat nama kolom actual. Sistem mencari keywords seperti "nama", "pegawai", "karyawan". Jika tidak ada, gunakan kolom pertama dengan data string.

**Q: File Excel tidak bisa dibaca?**
A: Sistem akan scan hingga 10 baris pertama untuk header. Jika masih gagal, coba export ke CSV terlebih dahulu.

**Q: Encoding error pada CSV?**
A: Sistem otomatis mencoba 4 encoding umum (utf-8, latin-1, iso-8859-1, cp1252). Jika masih error, save as UTF-8 di Excel.

**Q: Aplikasi lambat dengan file besar?**
A: Sistem otomatis filter kolom kosong dan limit scan. Untuk file >10MB, pertimbangkan untuk split data atau filter baris di Excel terlebih dahulu.

---

## 📧 Contact

Untuk pertanyaan atau feedback:
- GitHub Issues: [Link to repo]
- Email: support@sentivize.ai
- Dokumentasi: `/docs`

---

**Dibuat dengan ❤️ untuk HR Analytics yang lebih baik**
