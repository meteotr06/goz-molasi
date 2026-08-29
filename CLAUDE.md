# Göz Molası — bu klasörde açılan oturum için

**Sen bu projenin kaptanısın.** Klasörün: `D:\Projeler Ekran koruması`

## İlk iş: senkron ol (tek dosya)

```
C:\Users\KACB\OneDrive\Desktop\HESAP MAKİNESİ\BASLANGIC.md
```

Onu oku — kimlik, görev dağılımı, ortak kararlar, çalışma kuralları hepsi orada. **Kimsenin sana brifing vermesine gerek yok.**

## Bu projeye özel

**Envanter 45/48.** Kendi deposundan yayınlanır (`meteotr06/goz-molasi`). Sınama sayfaları `_sinama/` altında — depoda dururlar, siteye çıkmazlar (Jekyll alt tireli klasörü yayınlamaz; `.nojekyll` eklenirse bu koruma çöker).
**Canlı damgayı yazmıyoruz, ölçüyoruz** — sayı yazan satır gün içinde eskiyip bir sonraki oturumu yanıltıyor (30.08.2026'da bu satır "v141" diyordu). Yerel damga `sw.js` içindeki `SURUM`; canlıyı görmek için siteden `sw.js` çekilir. Bekleyen yayın: `git rev-list --count origin/main..HEAD`.
**Açık ve önemli:** masaüstü `.exe` **26.08'den** — 30.08 gecesi kapanan **25 kusurun hiçbiri** o kopyada yok (açılışta çökme, ekran süresinin eksik sayması, saati ileri alıp sınırı sıfırlama, bozuk geçmişin sayacı kalıcı dondurması). Derledikten sonra `masaustu/exe_icerik.py` **26 işareti** doğruluyor; `DERLE.bat`'in 5. adımı olarak kendiliğinden koşuyor. Derleme kullanıcının kararı (`DERLE.bat` uygulamayı açıyor).
**Kalan 3 özellik gerçek telefon istiyor**, `ENVANTER.md` sonunda kullanıcıya 7 soru yazılı.

## Değişmeyen üç sınır

- **Yayın · sürüm damgası · yayın penceresi** merkezindir. Sen yayınlamazsın.
- **Mağaza · para · geri alınamaz silme · makineyi ele geçiren hiçbir şey** kullanıcının **kendi** onayını ister.
- **Rapor üç satır:** `YAPILDI:` / `KALDI:` / `TAKILDI:` — başında `[5 · Göz Molası]`.
