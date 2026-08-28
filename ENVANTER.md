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
| 9 | Molayı atla (basılı tut) | ⬜ | — |
| 10 | Ertele 5 dk | ⬜ | — |
| 11 | Hemen mola (uyarı anında) | ⬜ | — |
| 12 | "Burada devam et" (çok sekme) | ⬜ | — |
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
| 20 | Çalışma süresi kaydırıcısı | ⬜ | — |
| 21 | Mola süresi kaydırıcısı | ⬜ | — |
| 22 | Uyarı süresi kaydırıcısı | ⬜ | — |
| 23 | Uzun mola aç + süresi | ⬜ | — |
| 24 | Çalışma saatleri (baş/bit) | ⬜ | — |
| 25 | Molayı atlamaya izin | ⬜ | — |
| 26 | Ses | ⬜ | — |
| 27 | Otomatik başla | ⬜ | — |
| 28 | Titreşim | ⬜ | Telefonda ölçülmeli |
| 29 | Arka planda çalış | ⬜ | — |
| 30 | Uzak kalınca sıfırla | ✅ | Telefon taklidiyle 3 dal: göç olur / seçim korunur / tekrarlamaz |
| 31 | Boşta durdurma | 🟡 | Durum yazısı ayrı: “Boşta — sayaç durdu” (sessiz durma yok). 90 sn bekleyerek **denenmedi** |
| 32 | Mola kilidi | ⬜ | — |
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
| 47 | Yenilik şeridi + ayrıntı | ⬜ | — |
| 48 | İstatistik + 7 gün + seri | 🟡 | Sayılar okundu; **7 gün grafiği ve seri denenmedi** |

### Bugün ayrıca ölçülenler (özellik değil, davranış)

- **Süre/mola çelişki açıklaması** — hem kurgulanmış hem **doğal** durumda
  çıktığı görüldü (2 mola / 1 dk → açıklama görünür), tutarlı durumda
  (3 mola / 65 dk) **çıkmadığı** da ölçüldü. İki dal da kanıtlı.
- **Uzun kullanım benzetimi** (`sinama-uzun.html`) — 7 değişmez, kullanıcının
  ekran görüntüsünü birebir üretiyor (3 mola / 3 dk).

---

## Toplam

**48 özelliğin 17'si denendi** (✅ 15, 🟡 2). **31'i açık.**

Denenmemiş her satır, bugüne kadar bulunan hataların doğduğu yer olabilir —
"muhtemelen çalışıyordur" bir ölçüm değildir.

## Denenemeyecekler (K-24 — şimdiden yazılı)

- **Titreşim** ve **mola çıkış koruması**: gerçek telefon gerekiyor.
- **Bildirim izni "reddedildi"**: tarayıcı izni sıfırlamak elle yapılır.
- **Renk / okunurluk hükmü**: bölme işlemediği için buradan verilemez.
