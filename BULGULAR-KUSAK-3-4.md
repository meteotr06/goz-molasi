# Bulgular — 3. kuşak (eşzamanlılık) ve 4. kuşak (girdi uçları)

Ölçen: denetçi oturumu · 28.08.2026 · yalnız **ölçüm**, uygulama dosyalarına
dokunulmadı. Düzeltmeleri f2 alıyor (`arayuz.js` ve `cekirdek.js` onda).

Ölçüm dosyaları: `test-eszamanli.html`, `test-girdi-uclari.html`
(kendi sunucumda, 8456 — f2'nin 8455'iyle karışmasın diye ayrı).

---

## 3. KUŞAK — İki sekme

### İyi çalışanlar (dokunmayın)
- Sayaç eşitlemesi tutuyor: A ve B `kalan=1195.751` ile birebir aynı.
- İkinci sekmeye örtü çıkıyor (lider seçimi çalışıyor).
- Duraklatma karşı sekmeye yansıyor: `A=duraklatildi · B=duraklatildi`.

### BULGU — Kapanan eski sekme, yeni sekmenin sayısını eziyor
Senaryo tam da kullanıcının yapacağı şey: iki sekme açık, birinde molalar
birikiyor, sonra **eski** sekme kapanıyor.

| Adım | Kayıttaki mola |
|---|---|
| B sekmesinde 9 mola birikti, yazıldı | 9 |
| Eski A sekmesi (hâlâ 3'te) kapandı → `pagehide` → `kaydet()` | **3** |

**Ve kalıcı geçmiş de bozuldu:** `2026-08-28 → 3 mola`. Yani kayıp
oturumluk değil. 7 gün grafiği ve seri sayısı bundan besleniyor;
kullanıcının altı molası **kalıcı olarak** siliniyor.

Çökme yok, uyarı yok — sadece yanlış sayı. Kullanıcı kendini gerçekte
olduğundan **az dinlenmiş** sanır. (f2 aynı kökü bağımsız olarak dört kez
gördü: `pagehide → kaydet()` kendi ölçümünü de eziyordu.)

**Önerilen değişmez: ARTAN SAYAÇLAR ASLA AZALMAZ.**
1. `Gecmis.gunuIsle`: `veri[gun] = { mola: Math.max(varolan|0, yeni), ... }`.
   Bir günün tamamlanmış mola sayısı geriye gidemez.
2. `kaydet()`: yazmadan önce depoyu yeniden oku; `tamamlananMola`,
   `atlananMola`, `ekranSuresi` için kendi değerini değil MAX'ı yaz.
   `kayitAni` zaten kayıtta duruyor.

Lider seçimini bozmaz; kapanan sekmenin yazması artık zarar veremez.

---

## 4. KUŞAK — Girdi uçları

**Arayüzden 0 girilemiyor** (ayarlar kaydırıcı, `min`/`max` gerçek).
Ama ayarlar bir de **depodan** geliyor ve orada doğrulama yok:

```js
this.ayarlar = { ...VARSAYILAN_AYARLAR, ...ayarlar };   // cekirdek.js:57
if (veri.ayarlar) this.ayarlar = { ...this.ayarlar, ...veri.ayarlar };  // :459
```

"Kullanıcı giremiyor" korumanın kendisi değil, **sadece bir yolun kapalı
olması.** Depo bozulabilir, eski sürümden kalabilir; 09'a eklediğimiz gibi
bir aktarım özelliği gelirse üçüncü bir yol daha açılır.

### Ölçülen (7 uç, hepsi kaldı)

| Depodan gelen | Sonuç | Kullanıcı ne görür |
|---|---|---|
| `calismaSuresi: 0` | doğrudan **mola** durumunda başlıyor | "19", mola hiç bitmiyor |
| `calismaSuresi: -600` | aynı | "19" |
| `calismaSuresi: null` | aynı | "19" |
| `calismaSuresi: NaN` | aynı | "19" |
| `calismaSuresi: "yirmi"` | sayaç NaN | ekranda **`NaN:NaN`** |
| `molaSuresi: 0` | olduğu gibi kabul | mola biter bitmez başlar |
| `molaSuresi: -20` | olduğu gibi kabul | — |

Sağlam çıkanlar: 1.000.000 sn (`16666:39` — çirkin ama doğru), ondalıklı
süre (12,5 dk → `12:29`), çok büyük mola süresi, uyarı süresi molayı aşması.

**Önerilen düzeltme — tek yerde.** Süre ayarlarının hepsi bir kelepçeden
geçsin (`enAz`/`enCok` ile), hem yapıcıda hem `iceAktar`'da. Sayı değilse
ya da aralık dışıysa **varsayılana** düşsün. İki yerde ayrı ayrı
doğrulamak, er geç ayrışan iki liste demektir.

### Ölçüm dersi: gevşek ölçüt hatayı "geçti" diye yazar

`null` denemesi önce **geçti**. Ölçütüm "kalan > 0" idi; uygulama molaya
düşmüştü ve ölçtüğüm 18,3 sayısı **molanın** kalan süresiydi. Çalışma
süresi soruluyorsa cevabın `durum === "calisiyor"` olması gerekir.
Ölçüt sıkılaştırılınca 5 kalan 7 oldu — yani iki hata, yanlış ölçüt
yüzünden görünmüyordu.

---

## 10. KUŞAK — Dışarı ne gidiyor (paylaşma ve konum)

### Paylaş düğmesi TEMİZ
`PAYLASIM` sabit bir nesne: başlık, tanıtım cümlesi, site adresi. Kişisel
veri yok, istatistik yok. (09'da bulduğum sızıntının burada karşılığı yok.)

### BULGU — Ham konum üçüncü tarafa gidiyordu

Hava durumu açıkken “Konumumu kullan” denince giden gerçek adres
(ölçüldü, `test-konum-gizlilik.html`, konum servisi taklit edilerek):

```
.../v1/search?latitude=39.9207431&longitude=32.8540719&count=1...
```

**Yedi ondalık basamak** — yaklaşık bir santimetre çözünürlük; ev adresi
demektir. Oysa kodda yuvarlama VARDI:

```js
enlem: +p.coords.latitude.toFixed(3),
boylam: +p.coords.longitude.toFixed(3),
ad: await yerAdiBul(p.coords.latitude, p.coords.longitude),   // HAM
```

Yuvarlama yalnız **saklanan** değere uygulanıyordu; isteğe ham konum
gidiyordu. Üç satır aynı nesne içinde durduğu için kodu okuyan
“korunuyor” sanıyordu — **koruma gibi görünen, korumayan bir satır.**
Bu sınıfı 09'da da yaşadık (`type="text"` üstündeki ölü `min`/`max`).

**Düzeltildi:** yuvarlama önce yapılıyor, sonra hem saklanıyor hem
gönderiliyor. Ölçüldü: giden adres artık `latitude=39.921` — 3 basamak.

### BULGU — Gizlilik metni iki YANLIŞ cümle içeriyordu

1. **“Konumun”** ifadesi *“Hangi veriler saklanmıyor?”* listesindeydi.
   Oysa uygulama konumu `goz-molasi-konum` anahtarında **saklıyor**.
2. **“Veriler nereye gidiyor? Hiçbir yere.”** Hava durumu açıkken
   yaklaşık konum **open-meteo.com**'a gidiyor.

Yayında olan bir gizlilik metninin yanlış olması, eksik olmasından
ağırdır: kullanıcı okuyup güveniyor. Metin gerçeğe uyduruldu — konum
saklananlar listesine taşındı (koşuluyla ve hassasiyetiyle), “hiçbir
yere” cümlesi koşullandı, open-meteo adıyla ve bağlantısıyla yazıldı.

### KALAN — düğmenin yanında uyarı yok
Kullanıcı **basmadan önce** konumunun dışarı gideceğini öğrenmiyor;
düğmenin çevresinde yalnız “Konumumu kullan / Konumu unut” yazıyor.
Gizlilik sayfasında yazması yeterli değil — **çekince, kararın verildiği
yerde durmalı** (bu projede daha önce alınmış bir karar). `index.html`
ve iki dilli metin gerektiği için sıraya kondu.

### Ölçüm dersi: sessizce başarısız olan sahte

`navigator.geolocation = {...}` düz ataması **hata vermeden başarısız
oluyor** (prototipte salt-okunur erişimci). İlk koşumda taklit hiç
yerleşmedi, hiçbir istek görülmedi ve bir süre “düğme çalışmıyor”
sanıldı. `Object.defineProperty` şart — ve sınama artık taklidin
yerleştiğini de ayrı bir madde olarak ölçüyor. Ayrıca hava özelliği
kapalıyken konum satırı `display:none`; açılmadan yapılan tıklama
hiçbir şey ölçmez.
