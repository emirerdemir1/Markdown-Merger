# Markdown Dönüştürücü

Markdown dosyalarını **verdiğiniz sırayla tek belgede birleştirir** ve
**Word (.docx) / PDF (.pdf) / Excel (.xlsx)** olarak kaydeder.

- Kaynak kod: https://github.com/emirerdemir1/Markdown-Birle-tirici (Public)

---

## 1. Mac'te çalıştırma (geliştirme)

Terminal'de proje klasörüne girin:

```bash
cd "/Users/emirerdemir/Documents/Varsayılan Proje"
source .venv/bin/activate
python3 app.py
```

İlk kurulum bir kez yapılır:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Açılan pencerede:

1. **Dosya Ekle** ile markdown dosyalarını sırayla seçin.
2. Listedeki **↑ / ↓** oklarıyla sırayı değiştirin, **×** ile çıkarın.
3. Başlık yazın (isteğe bağlı).
4. Format seçin: **Word / PDF / Excel**.
5. **Önizle** ile bakın veya **Dönüştür ve Kaydet** ile kaydedin.

Komut satırından da kullanılabilir:

```bash
python3 -c "from converter import convert_files; convert_files(['samples/1-giris.md','samples/2-detay.md'], 'pdf', 'cikti/rapor.pdf')"
```

---

## 2. Windows `.exe` üretme (GitHub Actions)

Windows makinesi gerekmez; GitHub'ın bulut Windows bilgisayarı derler.

1. Tarayıcıda repo'ya gidin: https://github.com/emirerdemir1/Markdown-Birle-tirici
2. **Actions** sekmesine tıklayın.
3. Solda **"Windows EXE üret"** işine tıklayın.
4. **Run workflow** → açılan kutuda tekrar **Run workflow**.
5. 2–5 dakika bekleyin; iş yeşil ✅ olunca en altta **Artifacts** bölümünden
   **MarkdownDonusturucu-Windows** dosyasını indirin.
6. ZIP'i açın → `MarkdownDonusturucu.exe` hazır. Windows'ta çift tıklayın.

> İndirilen `.exe` tek dosyadır; ayrıca Python veya tarayıcı kurulumu gerekmez.
> PDF için Windows'ta hazır gelen **Microsoft Edge** kullanılır.

---

## 3. Kodda değişiklik yapıp GitHub'a gönderme (GitHub Desktop)

Terminal komutu yok — 3 tık yeterli:

1. **GitHub Desktop**'u açın (repo zaten ekli).
2. Değişiklik yaptıktan sonra altta **Summary** kutusuna açıklama yazın
   (örn. `excel hücre renkleri düzeltildi`).
3. **Commit to main** → sağ üstteki **Push origin** düğmesine tıklayın.

GitHub otomatik olarak yeni `.exe` üretir; Actions sekmesinden indirirsiniz.

> Klasörü elle taşıdıysanız GitHub Desktop'ta **File → Add Local Repository** ile
> tekrar göstermeniz gerekebilir.

---

## 4. Klasör yapısı

```
app.py                      Uygulamayı açar (pywebview penceresi)
converter/
  merge.py                  Markdown'ları sırayla birleştirir
  render.py                 Markdown -> HTML
  to_docx.py                Word üretir
  to_pdf.py                 PDF üretir (Chromium / Edge)
  to_xlsx.py                Excel üretir
  pipeline.py               Hepsinin orkestrası
ui/
  index.html                Arayüz
  style.css                 Görünüm
  app.js                    Buton mantığı
samples/                    Deneme markdown'ları
.github/workflows/          Windows .exe derleme ayarı
requirements.txt            Gerekli kütüphaneler
.gitignore                  GitHub'a gitmeyecek dosyalar (.venv, cikti, pycache)
```

---

## 5. Bilinen noktalar

- Her markdown dosyası arasına sayfa sonu eklenir.
- Excel'de tablolar ayrı sayfalara, tablo dışındaki metinler **"Metin"** sayfasına yazılır.
- `.venv`, `cikti/` ve `__pycache__` GitHub'a gönderilmez (`.gitignore` sayesinde).
- Repo public olduğu için herkes kodu görebilir/indirebilir; isterseniz GitHub Desktop
  veya web arayüzünden **Private** yapabilirsiniz.
