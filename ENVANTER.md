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
| 10 | Ertele 5 dk | ⬜ | — |
| 11 | Hemen mola (uyarı anında) | ⬜ | — |
| 12 | "Burada devam et" (çok sekme) | ✅ | **Hata bulundu**: ikinci sekme de sayıyordu (v133). Ölçüldü — ikinci sekmenin sayacı **donuyor**, lider düzgün sayıyor; lider kapanınca öteki devralıp kaldığı yerden sürüyor; “Use here” elle devir çalışıyor |
| 13 | Uzun mola önerisi + ver/sonra | ⬜ | — |
| 14 | Mola çıkış koruması | ⬜ | Telefonda ölçülmeli |

## 2) Kipler ve hazır süreler

| # | Özellik | Durum | Nasıl ölçüldü |
|---|---|---|---|
| 15 | Kip: Odak | ✅ | Tıklandı → **20:00**, `aria-pressed` tekil |
| 16 | Kip: Ders | ✅ | Tıklandı → **25:00** |
| 17 | Kip: Toplantı | ✅ | Tıklandı → **60:00** |
| 18 | Kip: Film · oyun | ✅ | Tıklandı → **90:00**; yeniden açılışta korundu, sayaç 89:42'den devam etti |
| 19 | Hazır süreler (4 seçenek) | ⬜ | — |

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
| 27 | Otomatik başla | ⬜ | — |
| 28 | Titreşim | ⬜ | Telefonda ölçülmeli |
| 29 | Arka planda çalış | ⬜ | — |
| 30 | Uzak kalınca sıfırla | ✅ | Telefon taklidiyle 3 dal: göç olur / seçim korunur / tekrarlamaz |
| 31 | Boşta durdurma | ✅ | **Canlı görüldü**: 90 sn dokunmayınca sayaç durdu ve durum yazısı sebebini söyledi (“Idle — timer paused”) |
| 32 | Mola kilidi | 🟡 | Ayar açık/kapalı doğru kaydediliyor; **mola ekranından çıkamama davranışı telefonda ölçülmeli** |
| 33 | Etkinlik izni (masaüstü) | ⬜ | İzin **reddedildi** dalı da denenmeli |
| 34 | Hava durumu molada | ⬜ | — |
| 35 | Konum bul / unut / şehir ara | ⬜ | Çevrimdışı dalı da denenmeli |
| 36 | PIN kur / kaldır | ⬜ | — |
| 37 | Canlılık kaydırıcısı | ⬜ | — |
| 38 | Tema (18 tema) | ⬜ | — |
| 39 | Dil (TR / EN) | ✅ | Ekran taraması 0 hata verdi; **kural denetimi 6 gerçek eksik buldu** (çevrildi, bekçi kuruldu) |
| 40 | Hepsini sil | ⬜ | Geri alınamaz — dikkatli |
| 41 | Ayar kaydet / vazgeç | ✅ | 90→33 değiştirip **Vazgeç** → 90'a döndü, sayaç bozulmadı; **Kaydet** → 33:00 uygulandı |

## 4) Kabuk ve bildirimler

| # | Özellik | Durum | Nasıl ölçüldü |
|---|---|---|---|
| 42 | Sekmeler: Sayaç / Bilgiler | ⬜ | — |
| 43 | Bildirim izni | ⬜ | **Reddedildi** dalı önemli |
| 44 | Uygulama olarak kur (+ iOS yolu) | ⬜ | — |
| 45 | Paylaş | ⬜ | — |
| 46 | Kısayollar penceresi | ⬜ | — |
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

### Açık risk — sınama takımı sürüm denetiminde DEĞİL

İç sınama sayfaları (`sinama-*.html`) yayına sızmasın diye `.gitignore`'da.
Bu doğru ama bir yan etkisi var: **dört sınama sayfası yalnızca bu diskte
duruyor.** Kaybolurlarsa bugünkü ölçümlerin hiçbiri tekrarlanamaz.

Olası çözüm (ölçülmedi): GitHub Pages'te `.nojekyll` yok, yani Jekyll etkin
ve alt tire ile başlayan klasörler yayınlanmaz — `_sinama/` altında tutulursa
depoda dururlar ama siteye çıkmazlar. **Bu bir varsayım**; yanlışsa yeni
kapatılan sızıntıyı geri açar, o yüzden önce canlıda doğrulanmalı.

---

## Toplam

**48 özelliğin 28'i denendi** (✅ 27, 🟡 1). **20'si açık.**

Denenmemiş her satır, bugüne kadar bulunan hataların doğduğu yer olabilir —
"muhtemelen çalışıyordur" bir ölçüm değildir.

## Denenemeyecekler (K-24 — şimdiden yazılı)

- **Titreşim** ve **mola çıkış koruması**: gerçek telefon gerekiyor.
- **Bildirim izni "reddedildi"**: tarayıcı izni sıfırlamak elle yapılır.
- **Renk / okunurluk hükmü**: bölme işlemediği için buradan verilemez.
