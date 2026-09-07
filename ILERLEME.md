# ⚠️ ÖNCE BUNU OKU — 28.08.2026 sabahı

## Windows programı ESKİ, web güncel

```
exe derlenme : 26.08 21:53
kaynak       : 27.08 23:28
arada        : 8 commit masaüstü işi
```

**Web sürümü v93 yayında ve her şeye sahip.** Ama bilgisayarda çalışan
`.exe` bunların HİÇBİRİNİ içermiyor:

| Eksik olan | Ne işe yarıyor |
|---|---|
| Köprü | Tarayıcı sürümü sayacı devralır, süre başa sarmaz |
| Hayalet mola düzeltmesi | Boştayken sahte mola üretilmesini önler |
| Aile kipi: 6 sessiz atlatma | Çocuk kayıt dosyasını düzenleyip sınırı kaldıramaz |
| Ebeveyn dürüstlük metni | Neyin garanti olmadığını ayar ekranında yazar |
| Uyarı genişliği | "Koruma uygulanmıyor" uyarıları panelden taşmaz |

**Yapılacak:** `DERLE.bat` çalıştırmak. Ama o, sonunda uygulamayı
AÇIYOR — kullanıcının kendi kararı. Sorulmadan çalıştırılmadı.

Derleme sınamaları geçmeden exe üretmiyor; sınamalar şu an 8/8.

## Bu gece yapılanlar

Köprü (Windows ↔ tarayıcı) · hayalet mola · köprü sağlamlaştırma
(DNS rebinding, kilitlenme, ikinci kopya) · aile kipinde 7 sessiz
atlatma · ebeveyne dürüstlük · damga tutarlılığı + iki yeni nöbetçi ·
okunamayan uyarılar · İngilizce çeviri kaçakları (mola ekranı, hafta
grafiği, tema adları) · ekran okuyucu metinleri · uzun mola ·
süreli duraklatma · duraklatma türünün ekranda görünmesi.

Sınamalar: masaüstü 8/8 · web İngilizce 69/69 · web Türkçe 66/66.

---

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
| Web | yerelde **v79** · YAYINDA **v73** (K-25: kullanıcı yokken push yok) |
| Windows | ⚠️ **exe KAYNAKTAN ESKİ** — aşağı bak · Releases **v1.0** |
| Depo | github.com/meteotr06/goz-molasi · dal `main` |
| Sınama | masaüstü **6 takım** · web **41 senaryo** |

---

## ⚠️ Şu anki durum — okumadan devam etme

**exe kaynaktan ESKİ.** Son derleme 26 Ağustos ~21:53. Ondan sonra
şunlar eklendi ve **exe'ye girmedi**: sızıntı yalıtımı, `saat_oku()`
doğrulaması, saat alanlarının sessizce varsayılana dönmemesi.

Neden derlemedim: `DERLE.bat` sonunda **uygulamayı açıyor**. Kullanıcı
"bana bulaşmasın" dedi ve program kapalı tutuluyor. Sınamayı bozup
derlemek yerine derlemeyi hiç yapmadım.

Kullanıcı "aç" dediğinde: `DERLE.bat` — sınamaları koşar, derler,
exe'nin gerçekten açıldığını dener, sonra açar.

**Yerelde 1 commit push edilmedi** (K-25: kullanıcı başında değilken
dışarıya bir şey gitmez).

### Bugün yaşanan kaza — tekrarlamasın

Bir sınama kullanıcının **gerçek** `ayarlar.json` dosyasına yazdı:
`kip=aile`, sınama şifresi, 60 dakikalık günlük sınır. O günkü ekran
süresi 339 dakikaydı; engel ekranı kalıcı açıldı ve **bilgisayar
kullanılamaz hâle geldi**.

Sebebi: sahte uygulama nesnesi yalnızca METOTLARI eziyordu, modül
düzeyindeki `ayarlari_yaz()` açıktı. Çözüm `sinama_yalitim.py` +
`sinama_sizinti.py`. Ayrıntısı aşağıda.

Ayrıca: o sırada alınan yedek **temiz hâli değil kirli hâli** tutuyor.
Ürün klasöründen çıkarıldı. **"Yedek" adı temiz olduğu anlamına
gelmez** — içini aç, bak.

---

## Yapıldı

### Altyapı
- **Otomatik sınama derlemeye bağlandı.** `DERLE.bat` önce ucuz
  sınamaları koşuyor, sonra derliyor, sonra derlenen exe'yi gerçekten
  açıp deniyor. Biri kalırsa uygulama açılmıyor.
  Sebebi: bir keresinde "başarıyla derlendi" diyen sürüm hiç açılmadı.
- `sinama_veri.py` · `sinama_aile.py` · `sinama_yerlesim.py` (16 tema ×
  3 ölçek) · `sinama_acilis.py`
- Web: `sinama.js` 41 senaryo.
- **`sinama_yalitim.py`** — sınamalar kullanıcının verisine yazamaz.
  Yolları geçiciye çevirir VE yazan modül fonksiyonlarını susturur;
  ikisi birden, çünkü tek başına biri unutulunca kaza oldu. Bittiğinde
  gerçek klasörün parmak izini karşılaştırıp dokunulmadığını KANITLAR.
- **`sinama_sizinti.py`** — her sınamayı ayrı süreçte koşup gerçek
  klasörün önce/sonra parmak izini karşılaştırır. Takımda İLK sırada:
  sızan bir sınama, diğerlerinin sonucunu da şüpheli yapar.
  Ölçüldü: dördü de temiz. Denetçinin kendisi de kasten ihlalle
  sınandı (5/5 yakalıyor).
- `sinama_zaman.py` — sahte saatle 22 senaryo: gece yarısı, saat
  geri/ileri alma, yaz-kış saati, uzun oturum. Üç sessiz hata bu
  sınamayla bulundu.
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

## Aile kipi — neyi garanti eder, neyi etmez

**Ebeveyn bunu okumalı.** Bir güvenlik özelliğinin en tehlikeli hâli,
sandığından zayıf olmasıdır. Aşağıdakiler denendi ve ölçüldü.

### Atlatılamıyor

| Deneme | Sonuç |
|---|---|
| Sistem saatini geri alma | Sayaç korunuyor; mola ertelenmiyor |
| Saati değiştirip yasak saatinden kaçma | Yakalanıyor, engel sürüyor, sebebi yazıyor |
| Saati ileri alıp günü atlama | Günlük sınır birikimli saniye tutuyor, etkilenmiyor |
| Gece yarısını bekleyip sınır sıfırlatma | Doğru çalışıyor, ek süre devretmiyor |
| Temiz çıkış bayrağını taklit etme | Gizli söz doğrulanıyor, sahte bayrak kabul edilmiyor |
| Ayarlara girip kipi kapatma | Şifre ister |
| Molayı Ctrl+Alt+Shift ile atlama | Aile kipinde şifre ister |
| Yaz/kış saati, NTP eşitlemesi | Sayaç bozulmuyor |
| `istatistik.json`'u düzenleyip ekran süresini sıfırlama | Yakalanıyor: süre gün içinde geri gidemez, ebeveyne uyarı çıkar |

### Sessiz atlatma vs. görünür atlatma

27.08.2026'da ölçüldü ve bu ayrım en önemlisi çıktı. Çocuk
`istatistik.json` dosyasındaki `ekran_sn` değerini sıfırlayınca günlük
sınır tamamen kalkıyordu — **ve ebeveyn hiçbir şey görmüyordu**: kip
açık, şifre yerinde, sınır yazılı, uyarı yok.

Belgelenmiş atlatmalardan farkı buydu: onlar **iz bırakıyor**
(ayarlar.json silinince aile kipi kapanır, ebeveyn fark eder), bu
bırakmıyordu.

Önlenemiyor — dosya çocuğun kendi kullanıcı klasöründe. Ama artık
**görünür**: ekran süresi gün içinde geri gidemez (kertme), daha düşük
bir değer görülürse son bilinen değer kullanılır ve ebeveyne uyarı
çıkar. Kararlı bir çocuk `ayarlar.json`'daki işareti de düzenler — ama
o dosyaya dokunmak zaten görünür sonuçlar doğuruyor. Kazanılan şey:
**tek bir dosyayı değiştirerek sessizce atlatılamıyor.**

> **Sessiz atlatma, gürültülü atlatmadan tehlikelidir.** Gürültülüsünde
> ebeveyn bilir ve karar verir; sessizinde korunduğunu sanır.

### Atlatılabiliyor — ebeveyn bunları bilmeli

1. **Ayar dosyasını silmek.** `%APPDATA%` altındaki `GozMolasi` klasöründeki `ayarlar.json`
   silinirse şifre de aile kipi de gider. En kolay yol ve **çözümü
   yok**: dosya kullanıcının kendi klasöründe, okuma-yazma hakkı onda.
   Gerçek koruma ancak ayrı bir Windows hesabı ve yönetici hakları ile
   olur — o da bu uygulamanın işi değil.
2. **Görev Yöneticisi'nden iki süreci birden öldürmek.** Bekçi programı
   geri açar, ama bekçi de öldürülürse biter.
3. **Bekçinin komut satırındaki gizli sözü okumak.** Görev
   Yöneticisi'nin komut satırı sütunu gösteriyor. Çubuğu yükselttik,
   kaldırmadık.
4. **Windows'u güvenli kipte başlatmak.** Açılışta hiçbir program
   başlamaz.
5. **Web sürümünü kullanmak.** Aile kipi yalnızca Windows sürümünde
   var. Çocuk tarayıcıdan siteyi açarsa hiçbir kural geçerli değil —
   ama web sürümü bilgisayarı zaten engellemiyor, yalnızca mola
   hatırlatıcısı. Yani bu "engeli kaldırma" değil, "mola
   hatırlatmalarından kaçma".
6. **Başka bir Windows hesabı açmak.** Program o hesapta kurulu değilse
   çalışmaz.

### Neden daha ileri gitmedik

Windows tuşunu ve Görev Yöneticisi'ni engellemek için düşük seviyeli
klavye kancası ya da kayıt defteri politikası gerekiyor. İkisi de
sistemi kalıcı bozabilir; bir hata kullanıcının **kendi bilgisayarına**
girişini engelleyebilir. Bir göz molası uygulamasının alacağı risk
değil.

Bu yüzden uygulama hiçbir yerde "kırılmaz" demiyor. Amaç engellemek
değil, **sınırı görünür kılmak**.

## Ölçüldü — varsayılmadı

### Servis işçisi eski kod servis ediyor mu? **Hayır**
Başka projelerde sınamalar eski koda bakıp "geçti" diyordu. Bende ölçtüm:
`dunya.js`'e sürüm damgasını **artırmadan** bir kayıt ekledim, sayfa
19 kayıt yükledi — güncel kodu okudu. Sebebi: servis işçisi "önce ağ" +
`cache: 'no-cache'`.

Bir kez ölçüp geçmek yetmez; servis işçisi değişirse sessizce bozulur.
`sinama.js` artık her çalışmada veri dosyalarını taze çekip sayfadaki
dizilerle karşılaştırıyor ("diskte 18, sayfada 18"). Ayrılırsa bütün
sonuçlar şüpheli sayılır.

### `type="number"` Türkçe sayı tuzağı? **Yok**
Web tarafında sayı girdisi kullanılmıyor; kaydırıcı ve saat girdisi var.

### Aile kipinin canlı ortamda atlatılması? **ÖLÇÜLEMEDİ**
Tam ekran kilit, kullanıcının kendi oturumunda sınanmaz — bir kez
denendi ve bilgisayarı kilitledi. Ayrı hesap ya da sanal makine yok.
Mantık `sinama_aile.py` ve `sinama_zaman.py` ile ölçülüyor; gerçek
ortamda **denenmedi**. Sınanmamış olmak, kullanıcıyı kilitlemekten iyi.

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

## Köprü — Windows ↔ tarayıcı (27.08.2026)

İki sürüm iki ayrı yere yazıyordu, sayaç kopuyordu. Windows sürümü artık
`127.0.0.1:8452`'de bir **okuma** ucu açıyor; tarayıcı sürümü oradan
devralıyor.

**ÇALIŞTIĞI YER — ve çalışmadığı yer.** Ölçüldü:

| Sayfa nereden açıldı | Köprüyü gördü mü |
|---|---|
| `http://localhost:...` (yerel sunucu, `Telefona Sunucu Ac.bat`) | **evet** |
| `https://meteotr06.github.io` (yayın) | **hayır** — `ERR_BLOCKED_BY_CLIENT` |

Yayındaki sayfayı bu makinede bir tarayıcı eklentisi kesiyor. Başka
makinede çalışabilir ama **söz verilmiyor**. Eşitleme isteyen kullanıcı
tarayıcı sürümünü yerel sunucudan açmalı.

Köprü ulaşılamazsa uygulama bugünkü gibi çalışır ve **hata gösterilmez** —
olmayan bir şeyin eksikliği hata değildir.

**Kapatılabilir:** `ayarlar.json` içinde `"kopru": false`.

**Yön tek:** Windows → tarayıcı. Windows sürümü sürekli açık ve sekme
kapalıyken de ölçebiliyor; hangisi daha çok şey biliyorsa doğru odur.
Tarayıcıda verilen mola Windows tarafına GEÇMEZ — bilinen sınır.


---

## Uzun oturum ölçümü (03.09.2026) — bir daha koşturmaya gerek yok

Merkez sordu: *sayaç kayıyor mu, bellek büyüyor mu, mola ekranı üst üste
biniyor mu?* Üçü de ölçüldü; kod okunarak değil, uygulama **kullanılarak**.

**25 dakika, kullanıcı hareketiyle** (dakikada bir örnek, düzenli girdi):

| ölçülen | sonuç |
|---|---|
| sayaç kayması | 20 dakikada **±1 saniye** (duvar saatine karşı) |
| bellek | 1,6–2,3 MB, **düz** — yükselen eğilim yok |
| düğüm sayısı | 609 → 645 (ilk molada), sonra sabit |
| örtü sayısı | mola sırasında **1**, diğer zaman 0 — üst üste binme yok |
| JS hatası | **0** |

**Altı mola çevrimi** ayrıca koşuldu, çünkü tek molayla "bir kerelik mi, her
molada mı" ayırt edilemiyordu: düğüm sayısı ilk molada 645 olup **altı
çevrim boyunca 645'te kaldı**. Yani mola ekranı bir kez kuruluyor; sızıntı
yok. Bellek 2,5–4,9 MB arasında dalgalandı (çöp toplama gürültüsü).

**Boşta bir saat** (girdi üretmeden): 6. dakikada durum `bosta` oldu ve sayaç
dondu — **doğru davranış**, kullanıcı başında değilken saymamalı. O hâlde
kayma ölçülemez; hareketli ölçüm bu yüzden ayrıca yapıldı. Boşta bellek
2,0–2,3 MB düz, düğüm 609 sabit, JS hatası 0.

**Ölçüm aracının kendi kusuru:** ilk denemede `#baslatDugme`ye koşulsuz
basıyordum; uygulama zaten kendiliğinden başladığı için o basış sayacı
**durdurdu** ve prova boyunca 19:58'de dondu. Bir saati duran sayaçla
ölçecektim. Artık ölçüm, durum `calisiyor` olmadan **başlamıyor**. Ayrıca üç
seçicinin üçü de yanlıştı (`#sayac`, `#baslatDur`, `#molaEkrani`) — kısa
prova koşulmasaydı bir saat boyunca hiçbir şey ölçmemiş olacaktım.


## SAYAÇ SİSTEMİ DENETİMİ — 06.09.2026 (78 alt görev)

Altı ayrı mercek (durum makinesi · gün dönümü · ekranda yazan sayı ·
köprü/masaüstü · yaşam döngüsü · aile sınırı) bulguları çıkardı; her
bulgu ÜÇ bağımsız çürütücüden geçti (ikisi çürütürse düşüyor).
**23 bulgu ayakta kaldı, 1 çürütüldü.**

### v237–v238'de kapatılanlar (13)

- [AGIR] Tamamlanan UZUN mola hiçbir mola sayısına girmiyor: ne ekrandaki kutucuğa, ne 7 gün grafiğine, ne seriye, ne de kalıcı geçmişe yazılıyor
- [AGIR] Köprü açıkken "takip edilen süre" kutucuğu tarayıcının ölçüsünü, hemen altındaki saatlik grafik Windows'un ölçüsünü gösteriyor — Windows'tan gelen ekran_sn hiçbir yerde okunmuyor
- [AGIR] Ana ekrandaki "günde ortalama mola" ile Rapor ekranındaki "günde ortalama" aynı 7 gün için farklı bölen kullanıyor; aynı anda iki farklı sayı gösteriyorlar.
- [AGIR] Windows köprüsünün bugün için gösterdiği saatlik dizi hiçbir yere arşivlenmiyor; ertesi gün aynı gün "‹ Dün" ile açılınca çok daha küçük bir sayı çıkıyor.
- [AGIR] Ana ekrandaki sure kutusu tarayicinin olcusunu, hemen altindaki saatlik grafik Windows'un olcusunu gosteriyor -- ayni gun, iki sayi.
- [AGIR] 'Bugun X mola' yazisi bugunun degil SON 7 GUNUN toplamini yaziyor.
- [AGIR] Windows sürümü kapanınca aynı "Bugün" grafiği 5 sa 0 dk'dan 1 dk'ya düşüyor ve o gün bir daha geri gelmiyor
- [AGIR] aileyiTazele() saniye sayısını Date biçimleyicisi saatYaz()'a veriyor; istisna atıyor ve Ayarlar penceresi hiç açılmıyor.
- [AGIR] Engel ekranında kalan süre saniye olarak saatYaz()'a veriliyor; yasak saatinde engel hiç çıkmıyor ve bütün ekran donuyor.
- [AGIR] Bugünün saatlik grafiği Windows'un ölçüsünü, günlük sınır ve "bugünkü durum" kutucuğu tarayıcının ölçüsünü kullanıyor.
- [ORTA] Aynı kartta iki farklı "en yoğun saat": alışkanlık etiketi tarayıcı ölçümünden, grafiğin alt yazısı Windows köprüsünden okuyor.
- [ORTA] Ayni etiketli 'gunde ortalama' iki sekmede iki farkli bolenle hesaplaniyor.
- [ORTA] "En yoğun saat" aynı ekranda iki ayrı kaynaktan hesaplanıp iki farklı saat gösteriyor.

### KAPANDI — hepsi v237–v240'ta (10/10)

Aşağıdaki liste tarihçe olarak duruyor. **Denetimin bıraktığı 23
bulgunun 23'ü de kapandı**; ölçümleri `scratchpad/olc_arkada.py`
içinde (40 kontrol, her biri kendi karşı-kontrolüyle).

Üçü zaten v238–v239'da kapanmıştı (saatlik kova taşması, köprü
verisinin arşivlenmemesi); kalan yedisi v240'ta.

### Kapatılan maddeler (eski "açık" listesi)

- **[AGIR]** Bir saati kesintisiz ekranda geçiren kullanıcıda o saatin kovası 3600'ü aşıyor; sayfa yenilenince istatistikSuz o saati SIFIRLIYOR
  - yer: `cekirdek.js:221` · mercek: durum-makinesi
  - doğrusu: O saatin çubuğu 60 dk; saatlik kovaların toplamı ekranSuresi ile tutmalı (133 dk'lık günde 133 dk). Şu an grafik bir tam saati eksik gösteriyor.
- **[AGIR]** Windows sayilariyla cizilen bugunun saatlik grafigi diske hic yazilmiyor; yarin ayni gune 'Dun' diye bakinca sayilar kuculuyor.
  - yer: `arayuz.js:2813` · mercek: ekranda-yazan
  - doğrusu: Dun icin 6 sa 10 dk. Ekranda gosterilen kova dizisi hangisiyse gunluk gecmise de o yazilmali (ya da kaynak isaretiyle birlikte ayri saklanmali).
- **[AGIR]** Çubuğa tıklayıp gün değiştirince ayrıntı satırı eski günün sayısını göstermeye devam ediyor — kaydı olmayan bir gün için "ölçülen 50 dk" yazıyor
  - yer: `arayuz.js:2713` · mercek: kopru-masaustu
  - doğrusu: O gün için kayıt yok (ayrıntı satırı temizlenmeli); ekranda 50 dk yazıyor
- **[AGIR]** Masaüstünün tik döngüsü ölürse köprü hâlâ "sayiyor: true, kalan_sn: 0" diyor; tarayıcı bunu devralıp sonsuz sahte mola veriyor
  - yer: `goz_molasi.py:2556` · mercek: kopru-masaustu
  - doğrusu: Sahte mola sayısı 0 olmalı; ölçülen ~2 mola/dakika (40 sn'de 1) ve hepsi istatistiğe kalıcı yazılıyor
- **[AGIR]** lideriDevral() devralirken `puan` diskten YENIDEN OKUNMUYOR; bayat deger once ekrana ciziliyor sonra diski eziyor
  - yer: `arayuz.js:663` · mercek: yasam-dongusu
  - doğrusu: Ekranda ve diskte 240 puan (ve o puana karsilik gelen seviye) kalmaliydi. lideriDevral, `kilitOzeti`/`kilitTuz` icin yaptigi seyi `puan` icin yapmiyor.
- **[AGIR]** Devralan sekme `arkaPlanAcik` ayarini da geri yuklemiyor; ayar sessizce KAPANIYOR ve arka planda ekran suresi hic sayilmiyor
  - yer: `arayuz.js:4916` · mercek: yasam-dongusu
  - doğrusu: Ayar ACIK kalmali, Worker 250 ms'de bir tiklamali ve o bir saat `ekranSuresi`ne +3600 sn olarak girmeliydi (ekranda 'X + 60 dk'). Gorulen: +0 dk.
- **[AGIR]** kaydiDuzelt(), devralma sirasinda diskteki `uzakKalincaSifirla` ayarini sekmenin KENDI bayat degeriyle EZIYOR
  - yer: `arayuz.js:298` · mercek: yasam-dongusu
  - doğrusu: Ayar KAPALI kaldigi icin esik Infinity olmali, sayac 30 dakika oncekinden devam etmeliydi (ornek: 07:12). Gorulen: 20:00 ve anahtar yeniden acik.
- **[ORTA]** Tanıtım (örnek) molası ATLANINCA bayrak temizlenmiyor: sahte bir "atlanan mola" kalıcı geçmişe yazılıyor ve bir sonraki GERÇEK tamamlanan mola sayıdan düşülüyor
  - yer: `arayuz.js:3399` · mercek: durum-makinesi
  - doğrusu: Tanıtım molası ne atlanan ne tamamlanan sayılmalı: "atlanan mola" 0 (şu an 1, kalıcı), "tamamlanan mola" ilk gerçek moladan sonra 1 (şu an 0).
- **[ORTA]** Bir saatlik kova 3600 saniyeyi birkaç yüz milisaniye aşabiliyor; sayfa yenilenince istatistikSuz o kovayı kırpmak yerine SIFIRLIYOR ve bir saatlik ölçülmüş süre grafikten tümüyle siliniyor.
  - yer: `cekirdek.js:221` · mercek: gun-donumu
  - doğrusu: 11:00 kovası 1 sa (3600 sn) görünmeli ve grafiğin toplamı "takip edilen süre" ile tutmalı. Şu an o saat 0 sn, günün toplamı bir saat eksik.
- **[ORTA]** `pagehide` lider damgasini siliyor ama `liderMiyim` true kaliyor: bfcache'ten donen sekme, gercek liderin sayacini bayat degeriyle diske yazip eziyor
  - yer: `arayuz.js:745` · mercek: yasam-dongusu
  - doğrusu: B'de sayac 18:00'den devam etmeliydi; A donunce 'baska sekmede acik' ortusunu gosterip hic yazmamaliydi. Gorulen: B'de 00:00 + gecikmis mola seridi.

> Bulguların tam gerekçesi ve çürütme hükümleri iş akışı günlüğünde;
> buraya BAŞLIK + YER yazıldı ki arama tekrarlanmasın.


## BİLİNEN AÇIK: masaüstünün saat dağılımı arşivlenmiyor (06.09.2026)

`ARSIV_ALANLARI` üç sayı arşivliyor (`mola`, `uzun`, `ekran_sn`);
bugün eklenen `saatlik` dizisi arşivlenmiyor. Gece yarısı
`ist_baslangic()` ile sıfırlanıyor ve **o günün saat dağılımı kalıcı
olarak siliniyor.**

**Neden bugün kapatılmadı:** masaüstü penceresinde saatlik grafik
sekmesi yok (yalnız *Programlar* | *7 gün*), yani arşivlenen veriyi
gösteren bir yer de yok. Okunmayan veri biriktirmek, ölçülmeyen bir
kural yazmak gibidir.

**Ne zaman ACİL olur:** kullanıcı gün boyu yalnız masaüstünü açık
tutar, tarayıcıyı hiç açmazsa — ertesi gün web'de "‹ Dün"e bakınca
yalnızca tarayıcının küçük ölçüsü görünür. Masaüstü 6 saat ölçmüştür,
ekranda 2 dakika yazar. Bu, bu depoda **sessiz yanlış sayı** sınıfıdır.

**Kapatmanın yolu (üç küçük adım):**
1. `masaustu/gecmis.py` → `ALANLAR`'a dizi desteği + `saatlik`.
2. `_kopru_verisi` → bugünün yanında DÜNÜN dağılımını da yayınla.
3. `arayuz.js/olcumuAl` → geleni `Gecmis.gunuIsle` ile birleştir
   (yol zaten var, v238'de bugün için yazıldı).


## MOBİLDE UYGULAMA BAŞINA ÖLÇÜM — 07.09.2026 kararı

**Kullanıcı:** "arka planda sayaç var ama uygulamaları ve ekranı kaç
kere ne kadar olduğunu sayabilen bir şey yok" · "bunu öbürü gibi
yapamıyor muyuz mobilde de"

**Durum.** Masaüstü sürümü bunu YAPIYOR (ölçüldü, ekran görüntüsüyle:
Brave 19 dk %74, Claude 6 dk %23...). Web sürümü YAPAMAZ.

**Neden yapamaz — bu bir hata değil, sınır.** Android, uygulama
kullanım istatistiklerini (`UsageStatsManager`) yalnızca
`PACKAGE_USAGE_STATS` izni verilmiş KURULU uygulamalara açıyor.
Tarayıcıya vermiyor. StayFree yerli bir Android uygulaması, o yüzden
yapabiliyor; PWA aynı kutuda değil. Aynı sebeple "ekran kaç kere
açıldı" da web'den ölçülemez.

**TWA TEK BAŞINA YETMEZ** — bu önemli, çünkü ilk akla gelen o.
TWA bir Chrome sekmesini uygulama kabuğuna koyuyor; içerik yine
tarayıcı korumalı alanında koşuyor ve JS köprüsü YOK. Yani izin
alınsa bile veriyi sayfaya geçirecek yol olmuyor.

**Gereken mimari (bounded, sıfırdan yazım DEĞİL):**
1. `WebView` taşıyan küçük bir yerli Android uygulaması — mevcut arayüz
   olduğu gibi içine giriyor.
2. `UsageStatsManager` + `PACKAGE_USAGE_STATS` → uygulama başına süre
   ve ekran açılma sayısı.
3. Ön plan servisi (foreground service) → telefonda gerçek arka plan
   sayımı; tarayıcının donma sınırı ortadan kalkar.
4. `@JavascriptInterface` köprüsü → veriler mevcut grafiklere akar.

**BUGÜNKÜ ENGEL — ölçüldü:** bu makinede Android araç zinciri YOK.
`gradle`, `adb`, `sdkmanager`, `node` yok; Android SDK klasörü yok.
Yalnız `java` var (JRE). Yani derlenemez; önce ~1-2 GB'lık bir kurulum
gerekiyor ve o kullanıcının kararı.

**Play Store notu:** kullanım erişimi isteyen uygulamalar ek incelemeye
giriyor, gerekçe beyanı isteniyor. Arsa Rehberi'yle Play deneyimi ve
25$ ücreti zaten ödenmiş durumda.

**Şimdilik kapatılmadı, PARK EDİLDİ.** Karar kullanıcının: yerli
Android uygulaması ayrı bir proje.
