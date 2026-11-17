# Markdown Dönüştürücü

Markdown dosyalarını **verdiğiniz sırayla tek belgede birleştirir** ve
**Word (.docx) / PDF (.pdf) / Excel (.xlsx)** olarak kaydeder.

---

## 1. Mac'te çalıştırma (geliştirme)

Terminal'de proje klasörüne girin:

```bash
cd "/Users/emirerdemir/Documents/Varsayılan Proje"
source .venv/bin/activate
python3 app.py
```

İlk kurulumu yapmadıysanız (bir kez yeterli):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

> `.venv` klasörü sanal ortamdır; kütüphaneleri temiz tutar. Silerseniz yeniden kurmanız gerekir.

### Komut satırından da kullanılabilir

```bash
python3 -c "from converter import convert_files; convert_files(['samples/1-giris.md','samples/2-detay.md'], 'pdf', 'cikti/rapor.pdf')"
```

---

## 2. Windows `.exe` üretme (önerilen yöntem: GitHub Actions)

Windows makineniz olmasa bile olur. GitHub'ın bulut Windows bilgisayarı sizin yerinize derler.

### Adım adım

1. **GitHub'a giriş yapın:** https://github.com (hesabınız yoksa ücretsiz açın).
2. **Yeni repository oluşturun:** sağ üst `+` → `New repository`.
   - Repository name: `markdown-donusturucu`
   - **Public** seçin (ücretsiz).
   - `Create repository` deyin.
3. **Terminal'de proje klasöründe şunları çalıştırın** (kendi kullanıcı adınızı yazın):

   ```bash
   git init
   git add .
   git commit -m "ilk surum"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADINIZ/markdown-donusturucu.git
   git push -u origin main
   ```

   > GitHub "kodunuzu nasıl yükleyeceğiniz" ekranında bu komutları zaten gösterir;
   > oradakileri kopyalayıp yapıştırmanız en kolayıdır.

4. **GitHub'da `Actions` sekmesine tıklayın.** Sol tarafta **"Windows EXE üret"** işini görün.
   - Otomatik başlamadıysa işe tıklayıp **"Run workflow"** → **"Run workflow"** deyin.
5. **2–5 dakika bekleyin.** İş yeşil tik ile bitince:
   - İşin adına tıklayın → en altta **"Artifacts"** bölümünde
     **"MarkdownDonusturucu-Windows"** bağlantısına tıklayın → ZIP iner.
6. **ZIP'i açın, `MarkdownDonusturucu.exe` dosyasını Windows'ta çalıştırın.**

### Sonraki değişikliklerde

Kodda bir şey değiştirince şu 3 komut yeterli:

```bash
git add .
git commit -m "degisiklik aciklamasi"
git push
```

GitHub otomatik olarak yeni `.exe` üretir.

---

## 3. Klasör yapısı

```
app.py                      Uygulamayı açar (masaüstü penceresi)
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
cikti/                      Üretilen örnek çıktılar
.github/workflows/          Windows .exe derleme ayarı
requirements.txt            Gerekli kütüphaneler
```

---

## 4. Bilinen noktalar

- PDF için Windows'ta **Microsoft Edge** kullanılır (Windows 10/11'de hazır gelir).
  Mac'te `playwright install chromium` ile indirilen Chromium kullanılır.
- Excel çıktısında tablolar ayrı sayfalara, tablo dışındaki metinler **"Metin"** sayfasına yazılır.
- Her markdown dosyası arasına sayfa sonu eklenir.
