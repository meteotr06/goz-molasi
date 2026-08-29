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

### Kapanan bulgu — dar ekran + %200 yazı (sebep bulundu, düzeltildi)

**Ve burada yanılmışım: bu gerileme BENİM ÜRETTİĞİMDİ.** Önce "eski hâl
zaten kötüydü, sadece ulaşılamıyordu" demiştim. Ölçünce tersi çıktı.

**Sebep** (paneli zorla daraltıp en derindeki sığmayanı arayarak
bulundu): sayaç halkası `.halka-ic` 238px'e çıkıp sıkışamıyordu. Çünkü
px→rem dönüşümünde `clamp()` **alt sınırlarını** da rem yapmıştım:

```
clamp(38px, 12vw, 56px)   →   clamp(2.375rem, 12vw, 3.5rem)
```

Kök punto 32px olunca taban 38px yerine **76px** oluyor. Sayaç yazısı
iki katına çıkıyor, halka sıkışamıyor, sayfa yatay kayıyor.

**Düzeltme:** o altı `clamp()` px'e geri alındı. Zaten duyarlılar —
ortadaki `vw`/`vh` ekrana göre ölçekliyor. "Yazıları büyüt" ayarının
asıl hedefi gövde yazısı; ekran boyu sayacı ayrıca büyütmek gerekmiyor.

**Ölçüldü (sonrası):**

| Ölçü | Yatay kayma | Büyüyen yazı |
|---|---|---|
| 360×640 · normal | yok | — (normal boyutta değişiklik yok) |
| 375×812 · %200 | yok | 209 / 213 |
| 360×640 · %200 | **yok** (345 = 345) | 210 / 213 |

Büyümeyen 3 öge, bilerek px bırakılan sayaç/mola yazıları.

**Elenen adaylar** (bir sonraki tur aynı kapıları çalmasın): panele
`min-width: 0` — hiçbir şey değiştirmedi; çocuklara da vermek — taşmayı
354'ten 439'a **büyüttü**; `max-width: 100%` — panel doğru genişliğe
indi ama taşma 434'te kaldı. Üçü de sebebe dokunmuyordu.

### Kapanan bulgu — uyarı balonu %200 yazıda taşıyordu (v139)

`.uyari-balon b` kuralındaki `white-space: nowrap` yüzünden uyarı yazısı
%200 yazıda **398px**'e çıkıyor, balon **331px** kalıyordu: yazı balonun
**ve ekranın** dışına taşıyor, kullanıcı *"ekran birazdan kararacak"*
uyarısını **tam okuyamıyordu**.

**Üç seçenek ölçüldü** (375px ekran, iki dil):

| Seçenek | İngilizce (normal) | Türkçe (normal) | %200 |
|---|---|---|---|
| şimdiki (`nowrap`) | 235×155 | 324×103 | **taşıyor** |
| yalnız `nowrap`'siz | 180×184 | — | yazı gereksiz sarıyor |
| `min-width: 235` | 235×155 (aynı) | **235×174 (bozuldu)** | temiz |
| **`width: max-content`** | **345×103** | **345×103** | **temiz** |

**Tek bir genişlik iki dili birden koruyamıyor** — Türkçe metin daha
uzun. `max-content` ikisini de aynı genişliğe getiriyor ve ikisinde de
taşmayı bitiriyor. **Sapma bilerek kabul edildi:** İngilizce balon
235→345, Türkçe zaten 324'tü.

**Doğrulandı — 8 durumun 8'i temiz:** 375 ve 360 genişlik × iki dil ×
normal ve %200 → hiçbirinde taşma ya da yatay kayma yok. Değişikliğin
kapsamı da ölçüldü: 150 ögede 14 fark, **hepsi balonun kendi içinde**.

### Kapanan bulgu — Türkçe arayüz + dar ekran (v140)

**Bugüne kadarki bütün dar ekran ölçümlerim İngilizce koştu.** Türkçeye
geçince yeni bir hata çıktı — aynı ekran İngilizcede temiz, Türkçede
bozuk:

| Ölçü | Önce | Sonra |
|---|---|---|
| 360 · normal | temiz | temiz |
| 375 · %200 · **TR** | **18 taşan, sayfa kayıyor** | **0** |
| 360 · %200 · **TR** | **37 taşan, sayfa kayıyor** | **0** |
| 375 · %200 · EN | 0 | 0 (bozulmadı) |

**Sebep:** uzun Türkçe düğme yazıları. "🔕 Bildirimlere izin verilmedi"
%200'de 201px'ten **356px**'e çıkıyor (çerçeve 360), "⬇ Windows sürümünü
indir" 189'dan 349'a. Esnek ögelerin varsayılan `min-width: auto`
değeri, ögenin kendi en küçük içeriğinin altına inmesini engelliyor;
panel 402px'e çıkıp ekranı taşırıyordu.

**Elenen adaylar** (hiçbiri işe yaramadı — sayılarıyla):
`.dugme { max-width: 100% }` → 18, değişmedi · `#sekmeSayac
{ min-width: 0 }` → 18, değişmedi · `#sekmeSayac * { max-width: 100% }`
→ 18, değişmedi. **İşe yarayan, en azı:** `#sekmeSayac * { min-width: 0 }`
→ 0, panel 402→328.

**Normal boyutta üç ölçümde de sıfır fark** (375 TR, 360 TR, 375 EN).

### Sınıf taraması — `min-width: auto` başka yüzeylerde de var mı? (yok)

v140'ta düzelttiğim hata sekme panellerindeydi. *"Bu tek mi, örnek mi?"*
diye sorup uygulamanın **bütün yüzeylerini** Türkçe %200 yazıda taradım
(360 ve 375 genişlik):

| Yüzey | Ölçüm geçerli mi | Taşan |
|---|---|---|
| Ayar penceresi | açık, 211 görünür öge | **0** |
| Kısayol penceresi | açık, 41 görünür öge | **0** |
| Mola ekranı | açık, 15 görünür öge | **0** |
| Başlık (header) | — | **0** |
| Alt bilgi | — | **0** |

**Sonuç: tek örnekti**, sınıf değil.

**Ölçümün kendisi bir kez geçersiz çıktı ve yakalandı:** ilk turda mola
ekranı "0 taşan" verdi ama **görünür çocuk sayısı da 0'dı** — yani
hiçbir şey ölçülmemişti. Bölme işlemediği için görünürlük geçişi
donuyor. Geçişler kapatılınca (`transition: none`) 15 görünür öge çıktı
ve ölçüm geçerli hâle geldi. **"0 taşan" ile "0 ölçüldü" aynı şey
değil** — payda yazılmadan sonuç okunmamalı.

### Masaüstü kopyası neyi kaçırıyor (ölçüldü, 29.08.2026)

Ön listenin 10. maddesi: *"Kaynakta düzeltmek, kullanıcıya ulaştırmak
değildir."* Kullanıcının çalıştırdığı `.exe` **26.08 21:53**'ten.

**Yanlış çerçeve:** "40'tan fazla düzeltme exe'de yok." Bugünkü işlerin
**çoğu web tarafındaydı** (`arayuz.js`, `stil.css`, `cekirdek.js`) —
masaüstü ayrı Python kodu, o dosyalar exe'ye hiç girmiyor.

**Doğru sayı: masaüstü davranışını değiştiren 9 iş.** (Exe'ye giren
modüller `goz_molasi.py`, `kopru.py`, `kilit.py`, `tepsi.py`, … olarak
ayrıldı; `sinama_*.py` ve üretici betikler paketlenmiyor.)

| Ne | Kaç iş | Neden önemli |
|---|---|---|
| **Aile kipi: 7 sessiz atlatma** | 3 | Çocuk molayı sessizce atlayabiliyor; koruma çalışmıyor |
| **Hayalet mola + köprü** | 3 | Sahte molalar istatistiğe yazılıyordu; sayaç paylaşımı |
| Panele sığmayan 3 uyarı | 1 | Uyarı okunamıyor |
| Güncellenince ne değişti | 1 | Kullanıcı ne kazandığını görmüyor |
| Sürüm zinciri | 1 | Sürüm numarası tutarlılığı |

**En ağırı:** aile kipinin **yedi sessiz atlatma yolu** kullanıcının
kopyasında **hâlâ açık**. Ebeveyn korumanın çalıştığını sanıyor.

**Tek çıkış derleme** — ve `DERLE.bat` uygulamayı açtığı için onu
kullanıcı başlatmalı (K-25).

### Sürüm 1.2 "Sağlık" — K-36 ön ölçümü (ÖNCE ÖLÇ, sonra yap)

Merkez üç özellik önerdi. **Ölçtüm: ikisi zaten var, üçüncüsü de yapılmış
— eksik olan özellik değil, varsayılan ve cümle.**

| Önerilen | Durum | Kanıt |
|---|---|---|
| **Göz kırpma koçluğu** | ✅ **ZATEN VAR** | `GozKirp`, animasyonlu tam egzersiz: *"Kapak kapandığında sen de tam kırp"*. Sırada 6 molada bir çıkıyor (`KISA_SIRA`) |
| **Hareketsizlikte duraklama** | ✅ **ZATEN VAR** | `bostaEsigi: 90` sn, **varsayılan açık**, ayarı var (`ayBosta`). Canlı görüldü: durum satırı *"Idle — timer paused"* yazdı |
| **Ayakta mola** | 🟡 **MEKANİZMA VAR, KAPALI** | Uzun mola uçtan uca çalışıyor (kart çıktı, *"122 dakikadır"* sayısı doğru, iki düğme de sınandı). Ama `uzunMolaAcik: false` — **varsayılan kapalı** |

**İkisini yeniden yapmak, yapılmışı ikinci kez yapmak olurdu.**

Duraklama özelliğinde ayrıca **ince bir iş zaten yapılmış**: `hareketVar()`,
*"klavyeye dokunmadı"* ile *"makineden uzaklaştı"* arasını ayırıyor — çünkü
ölçülmüş, eskisi uzun metin okuyanın sayacını sıfırlıyormuş (masaüstünde
132 dakika ekran süresine karşılık **0 mola**).

**Gerçek iş üçüncüde ve küçük:** uzun molayı varsayılan açmak (ya da bir
kez sormak) ve *"kalk, biraz hareket et"* diye çerçevelemek. Mekanizma
hazır ve sınanmış.

**AMA:** "ayakta mola" bir **sağlık iddiası**. Bugün AOA'yı yanlış
aktardığımızı bulduk (v141). Oturmanın zararına dair bir cümle yazacaksak
**önce kaynağı okumalı** — kaynağın adını yazmadan da yazmamalı.
Yani bu madde, **yazılmadan önce bir dış referans ölçümü** istiyor.

### "Ayakta mola" — dış referans ölçümü (yazmadan ÖNCE)

Merkez haklıydı: bu bir **sağlık iddiası**, ve dün AOA'yı yanlış
aktardığımızı bulduk. Kaynaklara bakıldı.

**NHS** — *Why sitting too much is bad for us*:
> Öneri: **"set a reminder to get up every 30 minutes"**
> Ama aynı sayfada: **"there is currently not enough evidence to set a
> time limit on how much time people should sit each day."**

**WHO** — *Physical activity* bilgi sayfası:
> **"all age groups should limit the amount of time being sedentary"**
> — **hiçbir süre eşiği vermiyor.**

**Üç sonuç:**

1. **Sayı var ama EŞİK DEĞİL.** 30 dakika, NHS'in *pratik önerisi*; aynı
   kurum "sınır koyacak kadar kanıt yok" diyor. *"30 dakikada bir kalkman
   gerekir"* diye yazarsak, dün AOA'da yaptığımız hatanın aynısını
   yaparız: **öneriyi eşiğe çevirmek.**
2. **İki farklı şeyden söz ediyoruz.** Bizim uzun molamız **2 saat** ve
   **göz** için (AOA). Oturmak **ayrı** bir konu ve **30 dakika**
   ölçeğinde. Uzun molaya "ayağa kalk" demek, iki ayrı gerekçeyi tek
   düğmede birleştirmek olur — ve ikisinin süresi tutmuyor.
3. **Kaynaklar çelişmiyor, ikisi de "sınır bilinmiyor" diyor** (K-45).
   Yani dürüst cümle şu: *"Ne kadar oturmanın zararlı olduğuna dair kesin
   bir sınır yok; NHS 30 dakikada bir kalkmayı öneriyor."*

**Karar merkeze/kullanıcıya bırakılan tek nokta:** uygulama zaten **20
dakikada bir** araya giriyor. Bu araları ara sıra *"kalk, biraz hareket
et"* diye kullanmak, yeni özellik yazmadan NHS önerisini fazlasıyla
karşılar. Ama mola ekranının işi **gözü dinlendirmek**; oraya ikinci bir
amaç koymak, asıl işi zayıflatabilir. **Bu bir ürün kararı, ölçümle
çözülmez.**

### Ayrıca ölçülemeyenler

- **Renk / okunurluk hükmü**: tarayıcı bölmesi sık sık işlemeyi
  durduruyor; göze dair hükmü buradan veremem.
- **Arka planda çalış ayarının etkisi**: mekanizma sayfanın
  içinden görülemiyor.
- **Bildirim izninin “hiç sorulmamış” hâli**: bu tarayıcıda izin
  zaten reddedilmiş. (“Reddedilmiş” ve “verilmiş” hâlleri
  ölçüldü.)
- **Molada hava kartı**: gerçek konum gerekiyordu.
