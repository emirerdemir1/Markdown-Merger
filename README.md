# Markdown Dönüştürücü

Markdown dosyalarını **verdiğiniz sırayla tek belgede birleştirir** ve
**Word (.docx) / PDF (.pdf) / Excel (.xlsx)** olarak kaydeder.

- Kaynak kod: [GitHub reposu](https://github.com/emirerdemir1/MarkdownDonusturucu) — Public

---

## 1. Mac'te çalıştırma (geliştirme)

Terminal'de **proje klasörünüze girin**. GitHub Desktop kullanıyorsanız en kolayı:
`Repository → Open in Terminal` menüsü. Veya kendiniz:

```bash
cd ~/Documents/MarkdownDonusturucu
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

## 2. Windows `.exe` indirme

Hazır derlenmiş dosya GitHub'da:

1. [GitHub reposu](https://github.com/emirerdemir1/MarkdownDonusturucu) → **Actions** sekmesi.
2. Solda **"Windows EXE üret"** işine tıklayın.
3. En üstteki çalıştırmaya girin → en altta **Artifacts** bölümünden
   **MarkdownDonusturucu-Windows** dosyasını indirin.
4. ZIP'i açın → `MarkdownDonusturucu.exe` hazır. Windows'ta çift tıklayın.

> `.exe` tek dosyadır; ayrıca Python veya tarayıcı kurulumu gerekmez.
> PDF için Windows'ta hazır gelen **Microsoft Edge** kullanılır.

Yeni `.exe` üretmek için: Actions → **Run workflow** → tekrar **Run workflow**.
Her `push` işlemi de otomatik derleme başlatır.

---

## 3. Kodda değişiklik yapıp GitHub'a gönderme (GitHub Desktop)

Terminal komutu yok — 3 tık yeterli:

1. **GitHub Desktop**'u açın (repo zaten ekli).
2. Değişiklikten sonra altta **Summary** kutusuna açıklama yazın
   (örn. `excel hücre renkleri düzeltildi`).
3. **Commit** → sağ üstteki **Push origin** düğmesine tıklayın.

GitHub otomatik olarak yeni `.exe` üretir; Actions sekmesinden indirirsiniz.

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
- Repo public olduğu için herkes kodu görebilir/indirebilir; isterseniz **Private** yapabilirsiniz.
