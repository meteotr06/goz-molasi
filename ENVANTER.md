# Göz Molası — özellik envanteri ve deneme durumu

**Niye var (K-47).** Kullanıcının bildirdiği beş hatanın **beşi de** kimsenin
o yoldan geçmediği yerlerde doğdu. Varlığını ölçmek yetmiyor; **çalıştığını**
ölçmek gerekiyor. Denenmemiş özellik **açık** sayılır.

**Yüzeyin ölçümü.** Çalışan uygulamada sayıldı (28.08.2026):
**94 etkileşimli öğe** — 68 düğme, 11 onay kutusu, 5 kaydırıcı, 4 pencere,
2 saat, 2 parola, 1 açılır liste, 1 arama. Bunlar aşağıda **48 özelliğe**
gruplandı.

**Payda: 48 özellik.** Durum aşağıda tek tek yazılı; toplam en altta.

**Ortam sınırı (dürüstlük notu).** Ölçümler yerel sunucuda (`localhost:8455`)
tarayıcı bölmesinde yapılıyor. Bölme sık sık **işlemeyi durduruyor**
(`visibilityState: hidden`, gövde genişliği 32px); bu hâlde CSS geçişleri
donuyor ve `opacity/visibility` **gerçeği söylemiyor**. Bu yüzden görünürlük
hükmü CSS'ten değil **sınıf/öznitelik ve içerikten** çıkarılıyor. Gerçekten
göze bakan hüküm (renk, hizalama, okunurluk) burada **verilemez** —
kullanıcının kendi ekranında bakılmalı.

---

## 1) Sayaç ve mola — çekirdek

| # | Özellik | Durum | Nasıl ölçüldü |
|---|---|---|---|
| 1 | Duraklat / devam | ✅ | Tıklandı; düğme ⏸↔▶ değişti, sayaç dondu/işledi |
| 2 | Şimdi mola ver | ✅ | Tıklandı; mola ekranı `acik` sınıfını aldı |
| 3 | Sıfırla | ✅ | Tıklandı; sayaç 18:30 → **20:00** |
| 4 | Mola ekranı — egzersiz | ✅ | "Blink" çıktı; sıradaki doğru egzersiz |
| 5 | Mola ekranı — geri sayım | ✅ | 20 → 19 → … → kapanış |
| 6 | Mola ekranı — bilgi kartı | ✅ | "Why? — Screen position matters too" |
| 7 | Bilgi kartı — kaynak | ✅ | "Source: American Optometric Association" |
| 8 | Mola tamamlanınca sayım | ✅ | Mola sayısı **1 → 2**, sayaç 20:00'a döndü |
| 9 | Molayı atla (basılı tut) | ✅ | Ayar KAPALIYKEN zorla tetiklendi: mola açık kaldı, atlanan 0. Ayar açıkken basılı tutma molayı bitirdi, atlanan **0→1** |
| 10 | Ertele 5 dk | ✅ | Uyarı balonu yakalandı; sayaç **00:51 → 04:59**, balon kapandı |
| 11 | Hemen mola (uyarı anında) | ✅ | Balon 00:55'te yakalandı; mola ekranı açıldı, geri sayım ve egzersiz geldi |
| 12 | "Burada devam et" (çok sekme) | ✅ | **Hata bulundu**: ikinci sekme de sayıyordu (v133). Ölçüldü — ikinci sekmenin sayacı **donuyor**, lider düzgün sayıyor; lider kapanınca öteki devralıp kaldığı yerden sürüyor; “Use here” elle devir çalışıyor |
| 13 | Uzun mola önerisi + ver/sonra | ✅ | Kesintisiz süre 7300 sn kuruldu → kart çıktı, **“122 dakika” doğru hesaplandı**. “Şimdi değil” kapatıyor (tekrar sormaması **bilinçli**, kodda yazılı). “Uzun mola ver” **299 sn**'lik molayı başlattı |
| 14 | Mola çıkış koruması | ⬜ | Telefonda ölçülmeli |

## 2) Kipler ve hazır süreler

| # | Özellik | Durum | Nasıl ölçüldü |
|---|---|---|---|
| 15 | Kip: Odak | ✅ | Tıklandı → **20:00**, `aria-pressed` tekil |
| 16 | Kip: Ders | ✅ | Tıklandı → **25:00** |
| 17 | Kip: Toplantı | ✅ | Tıklandı → **60:00** |
| 18 | Kip: Film · oyun | ✅ | Tıklandı → **90:00**; yeniden açılışta korundu, sayaç 89:42'den devam etti |
| 19 | Hazır süreler (4 seçenek) | ✅ | Dördü de doğru: 20/20 · 10/20 · 30/30 · 45/60 |

## 3) Ayarlar

| # | Özellik | Durum | Nasıl ölçüldü |
|---|---|---|---|
| 20 | Çalışma süresi kaydırıcısı | ✅ | 1 / 20 / 90 dk denendi; sayaç ve depo birebir uydu |
| 21 | Mola süresi kaydırıcısı | ✅ | 20 sn ve en büyük değer; depoya birebir yazıldı |
| 22 | Uyarı süresi kaydırıcısı | ✅ | **Hata bulundu**: uç değerde uyarı sessizce 0 oluyordu (v132'de düzeltildi). Üç dal ölçüldü: uç 60→55, olağan 15 sabit, kipteki bilerek 0 korundu |
| 23 | Uzun mola aç + süresi | ✅ | Açık/kapalı iki dal; süre dakika→saniye ve en az 60 sn kuralı doğrulandı |
| 24 | Çalışma saatleri (baş/bit) | ✅ | 08:30 / 17:45 metin olarak birebir kaydedildi |
| 25 | Molayı atlamaya izin | ✅ | Koruma **görüntüde değil gerçek**: kapalıyken zorla tıklama molayı bitirmedi |
| 26 | Ses | ✅ | Açık/kapalı iki dal depoya doğru yazıldı (sesin duyulduğu **ölçülmedi**) |
| 27 | Otomatik başla | ✅ | İki dal: **kapalıyken** 20:00'da bekliyor (“Ready”), **açıkken** kendi başlıyor (19:59→19:54, “Running”) |
| 28 | Titreşim | ⬜ | Telefonda ölçülmeli |
| 29 | Arka planda çalış | 🟡 | Ayar kaydediliyor ve pencereye yansıyor. **Etkisi ölçülemedi**: duyulmayan 30 Hz'lik bir ses üreterek tarayıcının sekmeyi daha az kısmasını sağlıyor; işe yaradığı sayfanın içinden görülemez |
| 30 | Uzak kalınca sıfırla | ✅ | Telefon taklidiyle 3 dal: göç olur / seçim korunur / tekrarlamaz |
| 31 | Boşta durdurma | ✅ | **Canlı görüldü**: 90 sn dokunmayınca sayaç durdu ve durum yazısı sebebini söyledi (“Idle — timer paused”) |
| 32 | Mola kilidi | 🟡 | Ayar açık/kapalı doğru kaydediliyor; **mola ekranından çıkamama davranışı telefonda ölçülmeli** |
| 33 | Etkinlik izni (masaüstü) | ✅ | Dört hâl de var. **Hata bulundu**: üçünün yazısı çeviriden geçmiyordu ve “reddedildi” hâli ne kaybedildiğini söylemiyordu (v135) |
| 34 | Hava durumu molada | ✅ | Açılıyor, konum satırı ve gizlilik notu geliyor. **Molada hava kartının çıktığı ölçülmedi** (gerçek konum gerekiyordu) |
| 35 | Konum bul / unut / şehir ara | ✅ | **Hata bulundu**: izin reddedilince İngilizce arayüzde Türkçe yazı çıkıyordu (v136). Reddetme benzetildi — artık çevrili ve iki çıkış yolu birden yazıyor. “Konumu unut” çalışıyor |
| 36 | PIN kur / kaldır | ✅ | Kuruldu (**düz metin değil**, tuzlu özet); silme şifre sordu, yanlış şifre reddedildi ve deneme hakkı sayıldı, doğru şifre geçti |
| 37 | Canlılık kaydırıcısı | ✅ | 100 → 150; CSS değişkeni `--canlilik` **1.50** oldu, yani ayar gerçekten çizime ulaşıyor |
| 38 | Tema (18 tema) | ✅ | 18 tema sayıldı; ilk ve son denendi, kök özniteliği `beyaz` → `kagit` değişti. **Renklerin göze nasıl göründüğü buradan ölçülemez** |
| 39 | Dil (TR / EN) | ✅ | Ekran taraması 0 hata verdi; **kural denetimi 6 gerçek eksik buldu** (çevrildi, bekçi kuruldu) |
| 40 | Hepsini sil | ✅ | **Hata bulundu**: geçmişi silmiyordu (v134). Şimdi bütün kayıtlar kuralla siliniyor; sınama eklendi ve düzeltme geri alınınca yakaladığı doğrulandı |
| 41 | Ayar kaydet / vazgeç | ✅ | 90→33 değiştirip **Vazgeç** → 90'a döndü, sayaç bozulmadı; **Kaydet** → 33:00 uygulandı |

## 4) Kabuk ve bildirimler

| # | Özellik | Durum | Nasıl ölçüldü |
|---|---|---|---|
| 42 | Sekmeler: Sayaç / Bilgiler | ✅ | Geçiş çalışıyor, `aria-selected` tekil |
| 43 | Bildirim izni | ✅ | Bu tarayıcıda **gerçekten reddedilmiş** hâlde ölçüldü: ne kaybedildiği **ve** nasıl geri alınacağı yazılı; “hiç sorulmadı” hâli ayrı (tıklanabilir düğme). Reddedilmişken uygulamanın geri kalanı tam çalışıyor |
| 44 | Uygulama olarak kur (+ iOS yolu) | ⬜ | — |
| 45 | Paylaş | ✅ | **Hata bulundu**: son çare `window.prompt`'tu ve engellenirse ekranda iz kalmıyordu (v135). Pano reddi benzetildi — `prompt` **hiç çağrılmadı**, link uygulamanın kutusunda çıktı |
| 46 | Kısayollar penceresi | ✅ | Açılıyor, içeriği dolu, kapanıyor |
| 47 | Yenilik şeridi + ayrıntı | ✅ | Üç dal: yükselten kullanıcıya çıkıyor (doğru metinle), görmüş kullanıcıya çıkmıyor, **yeni kullanıcıya “güncellendi” denmiyor** |
| 48 | İstatistik + 7 gün + seri | ✅ | Bilinen geçmiş kuruldu; grafik (5-12-3-8-9-10), toplam **47**, ortalama **6.7**, seri **3** birebir tuttu. Seri ikinci dalı (bugün de hedefi tutuyor) **2** verdi; sınırdaki 8 hedefe sayıldı |

### Bugün ayrıca ölçülenler (özellik değil, davranış)

- **Süre/mola çelişki açıklaması** — hem kurgulanmış hem **doğal** durumda
  çıktığı görüldü (2 mola / 1 dk → açıklama görünür), tutarlı durumda
  (3 mola / 65 dk) **çıkmadığı** da ölçüldü. İki dal da kanıtlı.
- **Uzun kullanım benzetimi** (`sinama-uzun.html`) — 7 değişmez, kullanıcının
  ekran görüntüsünü birebir üretiyor (3 mola / 3 dk).
- **Ayar sınaması** (`sinama-ayar.html`) — 21 ayar için *ekranda yazan*
  değerle *depoda duran* değer yan yana ölçülüyor. `kaydet()` doğrudan
  `motor.disaAktar()` yazdığı için depodaki değer **davranışın kullandığı**
  değerdir; yani üç ayak da kapsanıyor. Boş sınama olmadığı kanıtlandı:
  v132 düzeltmesi geçici geri alınınca **yakaladı** (ekranda 60, depoda 0),
  geri konunca geçti.

### Kapanan risk — sınama takımı artık sürüm denetiminde

Önce şu açık risk yazılmıştı: iç sınama sayfaları yayına sızmasın diye
`.gitignore`'daydı, yani **yalnızca bu diskte** duruyorlardı; kaybolsalar
bugünkü ölçümlerin hiçbiri tekrarlanamazdı.

Varsayım **ölçüldü** (28.08.2026, canlı adres):

```
_sinama/deneme.html  ->  404          ana sayfa  ->  200
```

GitHub Pages Jekyll kullanıyor ve alt tire ile başlayan klasörleri
yayınlamıyor. Dört sınama sayfası `_sinama/` altına taşındı: **depoda
duruyorlar, siteye çıkmıyorlar.** Taşındıktan sonra dördü de koşturuldu
(14/14 · 7/7 · 21/21 · 19/19).

**Bu korumanın tek bir dosyalık bir zayıflığı var** ve o da denetleniyor:
depoya `.nojekyll` eklenirse Jekyll kapanır ve `_sinama/` **bir anda yayına
çıkar**. Kimse bunu sınama sayfalarıyla ilişkilendirmez. `sinama_yayin.py`
artık bunu da ölçüyor; `.nojekyll` oluşturulup denendi — **yakaladı**,
silinince geçti.

---

## Toplam

**48 özelliğin 45'i denendi** (✅ 43, 🟡 2). **3'ü açık — üçü de gerçek telefon istiyor.**

Denenmemiş her satır, bugüne kadar bulunan hataların doğduğu yer olabilir —
"muhtemelen çalışıyordur" bir ölçüm değildir.

## Buradan ölçülemeyenler — kullanıcıya sorular

Bunlar “çalışıyor” sayılmıyor; **denenmedi** sayılıyor.
Üçü de kullanıcının kendi telefonunda, kendi oturumunda denenmeli (K-24).

1. **Mola ekranından çıkılabiliyor mu?** “Yanlışlıkla çıkmayı
   önle” açıkken, mola sürerken geri tuşu / kenardan kaydırma ile
   ekrandan çıkabiliyor musun?
2. **Titreşim geliyor mu?** Mola başlarken ve uyarı anında telefon
   titriyor mu?
3. **“Uygulama olarak kur” çalışıyor mu?** Ana ekrana ekleniyor mu,
   eklendikten sonra açılıyor mu?

Önceki turlardan **hâlâ cevapsız** olanlar:

4. **Mola ekranının alt kenarı okunuyor mu?** (tarayıcı çubuğu
   örtüyordu — düzeltildi, doğrulanmadı)
5. **10 dakika başka uygulamada kalıp dönünce sayacın korunuyor mu?**

### Ayrıca ölçülemeyenler

- **Renk / okunurluk hükmü**: tarayıcı bölmesi sık sık işlemeyi
  durduruyor; göze dair hükmü buradan veremem.
- **Arka planda çalış ayarının etkisi**: mekanizma sayfanın
  içinden görülemiyor.
- **Bildirim izninin “hiç sorulmamış” hâli**: bu tarayıcıda izin
  zaten reddedilmiş. (“Reddedilmiş” ve “verilmiş” hâlleri
  ölçüldü.)
- **Molada hava kartı**: gerçek konum gerekiyordu.
