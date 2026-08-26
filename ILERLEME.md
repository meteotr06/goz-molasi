# Göz Molası — ilerleme

Neyin bittiğini, neyin kaldığını ve **neyin denenip bırakıldığını** tutar.

Neden ayrı dosya: `OKU.md` uygulamanın nasıl kullanıldığını ve nasıl
çalıştığını anlatıyor — o belge kalıcı. Burası ise zamanla değişen kısım.
İkisini karıştırmak, kullanım belgesini her ilerlemede kirletiyor.

**Bayat belge, belge olmamasından tehlikelidir.** Bir iş bitince ya da
bir yol çıkmaz çıkınca burayı güncelle.

---

## Durum — 26 Ağustos 2026

| | |
|---|---|
| Web | https://meteotr06.github.io/goz-molasi/ · servis işçisi **v73** |
| Windows | kodda **1.1** · GitHub Releases'te **v1.0** ⚠️ |
| Depo | github.com/meteotr06/goz-molasi · dal `main` |
| Sınama | masaüstü 4 takım · web 37 senaryo |

---

## Yapıldı

### Altyapı
- **Otomatik sınama derlemeye bağlandı.** `DERLE.bat` önce ucuz
  sınamaları koşuyor, sonra derliyor, sonra derlenen exe'yi gerçekten
  açıp deniyor. Biri kalırsa uygulama açılmıyor.
  Sebebi: bir keresinde "başarıyla derlendi" diyen sürüm hiç açılmadı.
- `sinama_veri.py` · `sinama_aile.py` · `sinama_yerlesim.py` (16 tema ×
  3 ölçek) · `sinama_acilis.py`
- Web: `sinama.js` 37 senaryo.
- `dunya.py` artık **üretiliyor** (`dunya_uret.py`). Elle ikiz tutulan
  `bilgiler.py`/`bilgiler.js` bir kez ayrıştı; aynı hatayı tekrarlamamak
  için.

### Özellikler
- **Aile kipi** — şifreli ayarlar, atlanamayan mola, günlük süre sınırı,
  saat yasağı, zorunlu bekçi, ebeveyn ek süresi.
- **Bilgiler sekmesi** — 43 kart tek yerde + rehber çalışma anında
  çekiliyor (kopyalanmıyor).
- **Dünyadan kartlar** — 18 kaynaklı genel kültür kartı.
- **Mola telafisi** — atlanınca nedeni söyleniyor, mola daha kısa olarak
  yeniden konuyor.
- **Güncelleme bildirimi** — masaüstü GitHub Releases'e bakıyor, web
  servis işçisi güncellenince şerit çıkarıyor.
- **Kısayollar** — PWA hızlı eylemleri + klavye (web/masaüstü aynı
  harfler) + görünür liste.
- **Diyafram egzersizi** — "göz kırp" yenilendi.
- **Şifre** PBKDF2 600.000 tur; eski kayıtlar kendiliğinden yükseliyor.

---

## Kaldı

- [ ] **GitHub Releases v1.1** — kodda `SURUM = "1.1"` ama Releases'te
      hâlâ v1.0. Yayınlanmadan güncelleme bildirimi kimseye görünmez.
      Sürüm notu hazır (TR+EN), onay bekliyor.
- [ ] **AdSense** — onay bekliyor. `reklam.js` içinde `AKTIF: false`,
      birim numaraları boş. Onay gelince numaraları girip açmak yeterli.
      **Mola ekranına reklam KONULMAZ** — politika ihlali, kalıcı kural.
- [ ] Web sürümünde **uzun mola** ve **süreli duraklatma** (masaüstünde
      var).
- [ ] **Haftalık HTML rapor** dışa aktarma.
- [ ] Dünya kartlarının **İngilizcesi** — şu an İngilizce kipte o tür
      sessizce atlanıyor.
- [ ] `robots.txt` `/goz-molasi/` altında; tarayıcılar yalnızca kök
      `robots.txt` okur. Zararsız (kök zaten sitemap'i listeliyor).

---

## Denendi, olmadı — tekrar araştırma

### Mobilde arka planda ekran süresi ölçmek
**Web ile mümkün değil.** Tarayıcı, sekmesi kapalıyken hiçbir kod
çalıştırmaz; bu bir izin eksiği değil, tarayıcının sınırı. Periodic
Background Sync 20 dakikalık hassasiyet vermiyor, Notification Triggers
Chrome'dan kaldırıldı.

StayFree gibi ölçmenin tek yolu **native Android uygulaması**:
`UsageStats` izni + ön plan servisi. Makinede Android Studio/SDK yok,
Java 8 var (17+ gerekiyor). Kullanıcı bunu sonraya bıraktı.

### Aile kipini "kırılmaz" yapmak
Windows tuşunu ve Görev Yöneticisi'ni engellemek için düşük seviyeli
klavye kancası ya da kayıt defteri politikası gerekiyor. İkisi de
sistemi kalıcı bozabilir; bir hata kullanıcının kendi bilgisayarına
girişini engelleyebilir. Bir göz molası uygulamasının alacağı risk
değil. Sınır ebeveyne açıkça yazılıyor.

---

## Tuzaklar

`OKU.md` sonundaki "Geliştirirken düşülen tuzaklar" listesine ek olarak:

1. **Derleme başarılı ≠ uygulama açılıyor.** `sinama_acilis.py` bunun
   için var.
2. **"Hepsi geçti" demeden önce neyi ölçmediğini sor.** Bilgiler sekmesi
   gizliyken içeriği ölçülmüyordu; sınama 31/31 diyordu, telefonda 123
   piksel taşma vardı. Gizli içerik denetlenmemiş içeriktir.
3. **Panele satır eklersen `yerlesim_kutulari` listesine de ekle.**
   Çakışma denetimi o listeyi okuyor.
4. **Web sürümü yayınlarken `sw.js` içindeki `SURUM`'u artır** ve
   `surum_ekle.py` çalıştır. Yapılmazsa kullanıcı önbellekteki eski
   dosyalarla kalır — geliştirme sırasında bizzat yaşandı.
5. **Masaüstü ile web aynı kuralı paylaşmaz.** "5 dakika uzak kalındıysa
   gözler dinlendi" masaüstünde doğru (program hep açık), web'de yanlış
   (sekmenin kapalı olması uzaklaşma değil). Ayrı eşik gerekti.
