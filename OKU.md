# Göz Molası — 20·20·20

**📱 Telefon/tablet:** https://meteotr06.github.io/goz-molasi/
**💻 Bilgisayar:** `Goz Molasi.exe` (bu klasörde)


Her **20 dakikada** bir, **20 saniye** boyunca ekranı kapatan; bu sırada gözünü
**6 metre** uzağa çevirmeni isteyen bir mola uygulaması.
Molanın birkaç saniyesinde, molanın *neden* gerektiğini kaynağıyla anlatır.

**İki sürüm var. İkisi de aynı bilgileri ve aynı mantığı kullanır.**

| Sürüm | Nerede | Ne için |
|---|---|---|
| **Windows programı** (`Goz Molasi.exe`) | Bilgisayar | Asıl sürüm. Arka planda çalışır, ekranı gerçekten kaplar. |
| **Web / PWA** (`index.html`) | Telefon, tablet, Mac, Linux — her cihaz | Tarayıcısı olan her yerde çalışır. |

---

## 1. Bilgisayar (Windows)

### Kurulum — iki çift tık

1. `Windows Acilisinda Baslat.bat` → bilgisayar her açıldığında program da açılır.
2. `Masaustu Kisayolu.bat` → masaüstüne kısayol koyar (istersen).

İlk çalıştırmada program sana **kullanım analizi için izin sorar**. Hayır dersen
molalar aynen çalışır.

`Windows Acilisinda Baslat.bat` bir **açma/kapama düğmesidir**: tekrar
çalıştırırsan otomatik açılmayı kaldırır.

### Tepsi simgesi (saatin yanında)

**İlk açılışta pencere görünür.** Sonraki açılışlarda program doğrudan arka
plana geçer ve saatin yanındaki küçük simgeden yönetilir.

> **Simgeyi göremiyor musun?** Windows yeni simgeleri saatin solundaki
> **^ (yukarı ok)** altına saklar. Oka tıkla, Göz Molası simgesini görev
> çubuğuna sürükle — bir daha kaybolmaz.
>
> Kısayola tekrar tıklamak da pencereyi geri getirir; ikinci bir kopya açılmaz. Üstüne gelince "sonraki mola 14:32" yazar. Sağ tık menüsü:

| Menü | Ne yapar |
|---|---|
| **Göster** | Paneli açar (simgeye çift tıklamak da aynı) |
| **Şimdi mola ver** | Beklemeden mola başlatır |
| **Duraklat ▸** | 30 dakika / 1 saat / 2 saat molaları durdurur (film, sunum) |
| **Devam et** | Duraklatmayı iptal eder |
| **Ayarlar** | Ayar penceresi |
| **Çıkış** | Programı kapatır |

Şifre koyduysan **Duraklat**, **Ayarlar** ve **Çıkış** şifre ister.

Tepsi simgesi bir sebeple kurulamazsa program görev çubuğunda normal pencere
olarak kalır — programa ulaşamama durumu olmaz.

### Nasıl davranır?

- **Arka planda** durur, ekranı kaplamaz, görev çubuğunda yer tutmaz.
- 20 dakika sonra **bütün monitörleri kaplar**, en üstte durur, 20 saniye sayar.
- Mola ekranının **X düğmesi yoktur**. Alt+F4 ve Esc çalışmaz. Başka pencere öne
  geçerse mola ekranı kendini tekrar öne alır.
- 20 saniye dolunca kendiliğinden kapanır ve ne yapıyorsan ona dönersin.

### Sen yokken sayaç boşa dönmez

Program, tüm bilgisayardaki klavye/fare hareketini Windows'a sorar:

- **90 saniye** dokunulmazsa sayaç kendini durdurur.
- İlk dokunuşta kaldığı yerden devam eder.
- **5 dakikadan uzun** uzak kaldıysan **baştan sayar** — gözlerin zaten dinlendi.

Yani bilgisayarı sabah açıp öğlene kadar dokunmasan, öğlen dokunduğun anda
temiz bir 20 dakika başlar.

### Gerektiğinde izin ister

| Durum | Ne sorar | Cevap gelmezse |
|---|---|---|
| **Görüşmedesin** (aşağıdaki üç kademe) | "5 dakika erteleyeyim mi?" | **Mola verilir.** Varsayılan her zaman molanın lehine. |
| Mola vakti geldi ama **tam ekran** bir program açık (sunum, video, oyun) | "5 dakika erteleyeyim mi?" | **Mola verilir.** |
| **2 saat** kesintisiz çalıştın | "5 dakikalık uzun mola vereyim mi?" | Mola verilmez, 20 sn'likler devam eder. |
| İlk açılış | "Kullanımını analiz edeyim mi?" | Hayır sayılır. |

### Rehberli göz egzersizleri

Mola ekranı boş bir geri sayım değil. Her molada **ne yapman gerektiğini
adım adım gösteren bir animasyon** oynar. Rakip uygulamaların hiçbiri o
20 saniyeyi içerik olarak kullanmıyor — asıl fark burada.

| Egzersiz | Ekranda ne olur | Dayanağı |
|---|---|---|
| **Uzağa bak** | Ortadaki nokta küçülür, halkalar dışarı açılır — göz onları takip ederken uzağa odaklanır | 6 m = optik sonsuzluk, odak kası tamamen gevşer |
| **Göz kırp** | 2 saniyede bir kapanan göz kapağı, 1/10 sayacı | Ekranda kırpma 15'ten 5–7'ye düşüyor (AAO 2024) |
| **Yakın — uzak** | Nokta büyür (yakın) / küçülür (uzak), yönerge değişir | Yakın işe bağlı geçici miyopiyi çözer |
| **Gözünü kapat** | Nefes ritmiyle parlayıp sönen halkalar, "al… ver…" | Kapalı göz de dinlenmedir |
| **Boynunu gevşet** | Sağa-sola giden bir işaret | Molalar bel/boyun ağrısını azaltabiliyor (Cochrane 2025) |

**Sıralama kasıtlı:** molaların yarısı "Uzağa bak" — asıl egzersiz o.
Diğerleri araya girip ekranın ezberlenip görünmez hale gelmesini önlüyor.
Uzun molalarda sıra farklı; "Gözünü kapat" ile başlıyor.

Hiçbir animasyon saniyede 3 kereden hızlı yanıp sönmez (WCAG 2.3.1, epilepsi
riski) ve hareketler yavaştır — tam ekran hızlı hareket denge bozukluğu olan
kişilerde rahatsızlık yapar.

### Renk temaları

Ayarlar penceresinin en üstünde beş tema var; birine tıklayınca **hemen**
uygulanır:

**Gece moru** · **Okyanus** · **Orman** · **Şafak** · **Açık (gündüz)**

Aynı beş tema web/mobil sürümde de var (sağ üstteki ◐ düğmesi ya da
Ayarlar → Tema).

Açık tema seçsen bile **mola ekranı koyu kalır** — amaç gözü dinlendirmek,
parlak bir ekran tam tersini yapar. Sadece rengi temaya uyar.

Beş temanın da metin kontrastları ölçüldü, hepsi WCAG AA sınırını (4.5:1)
geçiyor.

### Ses

Mola başında, sonunda ve ön uyarıda yumuşak bir çan sesi çalar.
`winsound.Beep` sert ve kulak tırmalayıcı olduğu için ses **kendimiz
üretiliyor**: sinüs dalgası + yavaş sönen ses zarfı. Dosyaya yazılmıyor,
bellekte oluşup oradan çalınıyor. Ayarlardan kapatılabilir.

### 7 günlük geçmiş ve seri

Grafik kartındaki **Programlar / 7 gün** sekmeleriyle geçiş yapılır.
7 gün görünümü her günün mola sayısını çubuk olarak gösterir; kesikli çizgi
günlük hedeftir (8 mola).

Başlıkta **🔥 kaç gün üst üste** hedefi tutturduğun yazar. Bugün henüz hedefe
ulaşmadıysan seri bozulmuş sayılmaz — sabahın köründe "serin bitti" demek
haksızlık olurdu, dünden geriye doğru sayılır.

Geçmiş `gecmis.json`'da son 120 gün için saklanır.

### Görüşme tespiti — üç kademe

| Kademe | Nasıl | Ne kadar kesin |
|---|---|---|
| 1 | **Mikrofon veya kamera gerçekten kullanılıyor mu?** Windows'un gizlilik göstergesinin okuduğu kayıt kullanılıyor (`LastUsedTimeStop = 0`) | **Kesin** |
| 2 | Öndeki program bilinen bir görüşme programı mı (Zoom, Teams, Webex, Discord…) | Muhtemel |
| 3 | Pencere başlığında görüşme belirtisi var mı ("Google Meet", "Jitsi"…) | İpucu |

1. kademe olmasaydı: **açık ama görüşmede olmayan Teams** boşuna mola
erteletirdi; **listede olmayan bir görüşme programı** ise hiç yakalanmazdı.
Kontrol 2 milisaniye sürüyor ve sadece mola vakti geldiğinde bir kez çalışıyor.

### Kullanım analizi (izne bağlı, varsayılan kapalı)

İzin verirsen hangi programda ne kadar vakit geçirdiğini sayar ve panelde
renkli çubuk grafik olarak gösterir.

- Sadece **program adı ve süre** tutulur (`chrome.exe — 42 dk`).
- **Pencere başlıkları, yazdıkların, gezdiğin siteler kaydedilmez.**
- Her şey `%AppData%\GozMolasi` klasöründe, bu bilgisayarda kalır.
- Ayarlardan istediğin an kapatabilirsin.

### Şifre kilidi

Ayarlar → *Kilit şifresi* (4–12 rakam). Açıkken şu üçü şifre ister:

1. **Ayarları açmak**
2. **Programı kapatmak**
3. **Molayı erken bitirmek** (Ctrl+Alt+Shift acil çıkışı)

Üçüncüsü önemli: şifre koyup acil çıkışı serbest bıraksaydık kilidin hiçbir
anlamı kalmazdı.

**Şifre nasıl saklanıyor?** Düz metin asla saklanmaz. Düz SHA-256 de yetmez:
4 haneli şifrede sadece 10.000 ihtimal var, sıradan bir bilgisayar SHA-256 ile
saniyede milyonlarca deneme yapar. Bu yüzden **PBKDF2-HMAC-SHA256, 240.000 tur**
kullanılıyor — her deneme ~0,1 saniye sürüyor:

| Şifre uzunluğu | Kaba kuvvetle kırma süresi |
|---|---|
| 4 hane | ~16 dakika |
| 6 hane | ~1 gün |
| 8 hane | ~115 gün |

Her şifrenin kendi rastgele tuzu var, yani aynı şifre iki cihazda farklı özet
üretir. Yanlış denemede her 3 hatada bekleme süresi artar (15, 30, 45 sn…).

### Zorla kapatılırsa geri açılır

Şifre koyduğunda **bekçi** devreye girer: programı izleyen ikinci bir küçük
süreç. Görev Yöneticisi'nden programı kapatan olursa bekçi bunu görür ve
programı yeniden açar. Şifreni girip *Programı kapat* dediğinde bekçi
sessizce çekilir.

Ayarlardan kapatabilirsin (*Zorla kapatılırsa geri aç*).

**Dürüst sınır:** Ayar dosyasını (`%AppData%\GozMolasi`) silen kişi kilidi de
siler. Program ile bekçiyi aynı anda kapatan da kurtulur. Bu bir cihaz
güvenliği değil, kendi kendine disiplin aracı.

### Acil çıkış

Mola ekranında **Ctrl + Alt + Shift** tuşlarını **3 saniye** basılı tutarsan mola
iptal olur.

Bunu bilerek koydum ve bilerek zorlaştırdım. Kimseyi ekranın önünde kilitli
bırakmak doğru değil — acil bir telefon, bir sunum, bir kaza olabilir. Kazayla
basılamayacak kadar zor, gerçekten gerektiğinde ulaşılabilecek kadar kolay.
İstemiyorsan `masaustu\goz_molasi.py` içinde `kisayol_basili_mi` geçen satırları
silmen yeter.

---

## 2. Telefon / tablet / diğer cihazlar

### 🌐 YAYINDA — hiçbir kurulum gerekmez

```
https://meteotr06.github.io/goz-molasi/
```

Telefonun tarayıcısında bu adresi aç, menüden **Ana ekrana ekle** de.
Artık normal bir uygulama gibi açılıyor. Bilgisayarın açık olmasına gerek yok.

### Neden yerel sunucu yerine internet?

Tarayıcılar bazı özellikleri **sadece https:// üzerinden** veriyor. Bilgisayardaki
`http://192.168.1.x:8451` adresi "güvenli bağlam" sayılmıyor ve şunlar çalışmıyor:

| Özellik | `http://` yerel IP | `https://` yayın |
|---|---|---|
| Çevrimdışı çalışma (service worker) | ❌ | ✅ |
| Ana ekrana ekleme (PWA) | ❌ | ✅ |
| Ekranı uyanık tutma | ❌ | ✅ |
| Güçlü şifre saklama (crypto.subtle) | ❌ zayıf yönteme düşer | ✅ |
| Bildirimler | kısmi | ✅ |

Bu yüzden telefonda **yayındaki adresi** kullan. `Telefona Sunucu Ac.bat` sadece
geliştirme/deneme için duruyor.

### Güncelleme yayınlama

Dosyaları değiştirdikten sonra:

```bash
cd "D:\Projeler\05 Ekran koruması" && git add -A && git commit -m "guncelleme" && git push
```

1–2 dakika içinde yayına çıkar. `sw.js` içindeki `SURUM` satırını da artırırsan
telefonlardaki önbellek kesin yenilenir.

### Web sürümünde neler var?

20 dk sayaç · 15 sn ön uyarı · tam sayfa mola ekranı ·
**rehberli göz egzersizleri (masaüstüyle aynı beşi)** · kaynaklı "neden?" kartı ·
boşta durdurma · **şifreli kilit** · basılı tutarak atlama · bildirim ·
ekranı uyanık tutma · çevrimdışı çalışma · **beş renk teması** ·
günlük sayaçlar · **son 7 gün grafiği ve seri (🔥 kaç gün üst üste)**.

Egzersiz animasyonları telefonda da oynar. Cihaz ayarlarında "hareketi azalt"
açıksa animasyon durur, sadece yönerge yazısı kalır.

**Kısayollar:** `Boşluk` başlat/duraklat · `M` hemen mola · `Esc` pencereyi kapat.

---

## Tarayıcının yapamadıkları — ve Windows sürümünün neden var olduğu

Web sürümü telefonda mükemmel, ama bilgisayarda bir duvara çarpıyor:

| İstenen | Tarayıcı | Windows programı |
|---|---|---|
| Arka plandayken kendini öne getirmek | ❌ **Yapamaz** | ✅ Yapar |
| Diğer programların üstünü kaplamak | ❌ Sadece kendi sekmesini kapatır | ✅ Tüm monitörleri kaplar |
| Kapatılamayan pencere | ❌ Sekme her zaman kapatılabilir | ✅ X yok, Alt+F4 yok |
| Tüm bilgisayarda boşta algılama | ❌ Sadece kendi sayfasında | ✅ Windows'a sorar |
| Hangi programı kullandığını görmek | ❌ Yapamaz | ✅ İzinle yapar |
| Program kapalıyken hatırlatmak | ❌ Sunucu gerekir | ✅ Gerek yok |

Bu yüzden bilgisayarda Windows sürümünü, telefonda web sürümünü kullan.

**Windows sürümünün de yapamadıkları** (dürüst olmak gerekirse):
Ctrl+Alt+Del ve Windows tuşu engellenemez; Görev Yöneticisi'nden program
kapatılabilir. Bunları engellemek zaten zararlı yazılım davranışıdır.

---

## Renkler neden böyle?

Mola ekranı **koyu** kalıyor — amaç gözü dinlendirmek, parlak bir ekran tam
tersini yapar. Ama gri/siyah da değil: gece mavisinden mora, oradan sıcak bir
şafak tonuna giden bir gökyüzü gradyanı. Vurgular sıcak (kehribar) ve nane
yeşili; tek başına soğuk mavi klinik hissi veriyordu.

Panelin tamamı tuvale çizilir. Tkinter'ın hazır düğme ve çerçeveleri keskin
köşeli, gölgesiz ve 1995'ten kalma görünüyor; bu yüzden yuvarlak kartları,
gölgeleri ve üstüne gelince renk değiştiren düğmeleri `ogeler.py` içinde
kendimiz çiziyoruz.

Program **DPI farkındadır**: ekranın %125 / %150 büyütmesini kendi hesaplar.
Bunu yapmasaydı Windows programı bulanık şekilde büyütür, panelin sağı ve altı
taşar, mola ekranı da tüm ekranı kaplayamazdı.

Nefes halkası 10 saniyede bir yavaşça büyüyüp küçülür (4 sn içeri, 6 sn dışarı).
Hızlı yanıp sönen hiçbir şey yok — tam ekran hareket, denge bozukluğu olan
kişilerde rahatsızlık yapabilir ve epilepsi açısından riskli olabilir. Web
sürümü `prefers-reduced-motion` ayarını da dinler.

---

## Dosyalar

```
Goz Molasi.exe                 Windows programı (tek dosya, Python gerekmez)
Windows Acilisinda Baslat.bat  Otomatik başlatmayı açar/kapatır
Masaustu Kisayolu.bat          Masaüstü kısayolu
Telefona Sunucu Ac.bat         Telefondan bağlanmak için sunucu

masaustu\                      Windows programının kaynak kodu
  goz_molasi.py                Ana program
  izleyici.py                  Windows'a soru soran katman (boşta, ön pencere, DPI)
  kilit.py                     Şifre saklama (PBKDF2) ve bekçi süreç
  egzersiz.py                  Mola ekranındaki rehberli göz egzersizleri
  tepsi.py                     Saatin yanındaki simge ve menüsü
  gecmis.py                    Gün gün kayıt ve seri hesabı
  ses.py                       Çan seslerinin üretimi
  gorunum.py                   Beş tema, renk paleti ve gradyan çizimi
  ogeler.py                    Tuvale çizilen yuvarlak kart / düğme / çubuk
  bilgiler.py                  14 bilgi kartı (kaynaklarıyla)
  dunya.py                     ÜRETİLEN dosya — elle düzenleme (aşağı bak)
  dunya_uret.py                dunya.js'ten dunya.py üretir
  guncelleme.py                GitHub Releases'e bakıp yeni sürüm var mı sorar
  kilit.py                     Şifre (PBKDF2), bekçi süreç, açılışta başlatma
  izleyici.py                  Boşta süresi, ön pencere, çalışma alanı ölçümü
  sinama.py                    Bütün sınamaları koşan betik
  sinama_veri.py               Kaynak denetimi + sürümler arası tutarlılık
  sinama_aile.py               Ebeveyn kontrolü mantığı
  sinama_yerlesim.py           Panelde çakışma/taşma (16 tema x 3 ölçek)
  sinama_acilis.py             Derlenen exe gerçekten açılıyor mu
  ikon.ico

index.html / stil.css          Web sürümü arayüzü
cekirdek.js                    Zamanlayıcı motoru + geçmiş/seri hesabı
arayuz.js                      Motoru ekrana bağlayan katman
dil.js                         Türkçe/İngilizce sözlük
egzersiz.js                    Aynı beş rehberli egzersiz (tuval animasyonu)
bilgiler.js                    Aynı 14 bilgi kartı
bilgiler_en.js                 Bilgilerin İngilizcesi
dunya.js                       18 genel kültür kartı (dunya.py'nin KAYNAĞI)
mola_icerik.js                 Mola kartı sırası: bilgi/hava/özet/ipucu/dünya
reklam.js                      AdSense yerleri (numaralar boşken kapalı)
sinama.js                      31 senaryoluk web sınaması
sw.js / manifest.json          Çevrimdışı çalışma, "ana ekrana ekle", kısayollar
```

**İKİZ DOSYALAR — dikkat**

`bilgiler.py` ile `bilgiler.js` aynı içerikte tutuluyor. Bunu insanın
hatırlamasına bırakmak bir kez tuttu, bir kez tutmadı: iki dosya kesme
işaretinde ayrıştı. Artık `sinama_veri.py` bu ikizliği denetliyor ve
ayrışırlarsa derleme durur.

`dunya.py` **ÜRETİLEN** dosyadır, elle düzenleme. Kaynağı `dunya.js`:

```
cd masaustu
python dunya_uret.py
```

### Sınama

Değişiklikten sonra **önce bunu çalıştır**:

```
cd masaustu
python sinama.py hizli
```

Dört takım var: **veri · aile · yerlesim · acilis**. `hizli` kipi exe
gerektireni atlar. Web tarafı için sayfayı aç ve konsola yaz:

```
fetch('sinama.js').then(r=>r.text()).then(k=>eval(k)).then(console.log)
```

### Web sürümü yayınlama

Dosya değiştirdiysen `sw.js` içindeki `SURUM` numarasını artır, sonra
`masaustu/surum_ekle.py` çalıştır. Bu, HTML'deki `?s=v..` etiketlerini
tazeler. Yapılmazsa kullanıcı tarayıcı önbelleğindeki eski dosyalarla
kalır — geliştirme sırasında bunu bizzat yaşadık: dosya sunucuda vardı,
sayfada yoktu.

### Yeniden derleme

```
DERLE.bat
```

**Elle PyInstaller çalıştırma.** Bu bölüm eskiden elle bir komut veriyor
ve `dist\` klasöründen kopyalamayı söylüyordu. O yol bütün sınamaları
atlıyor — tam da önlemek istediğimiz şey. Bir keresinde "başarılı"
derlenen bir sürüm çalıştırıldığında hiç açılmadı; derleme çıktısına
bakılıp geçilmişti.

`DERLE.bat` sırayla:

1. Ucuz sınamalar (veri + aile + yerleşim) — kalırsa derleme HİÇ BAŞLAMAZ
2. Çalışan sürümü kapatır, derler
3. Açılış sınaması — exe gerçekten açılıyor mu, penceresi geliyor mu,
   ekrana sığıyor mu
4. Hepsi geçerse uygulamayı açar

Herhangi biri kalırsa uygulama **açılmaz**. Bozuk derleme yayına çıkamaz.

Çıktı `Goz Molasi.exe` olarak ana klasöre gelir; ara dosyalar
`masaustu\build` içinde kalır.

---

## Bilgiler nereden geliyor?

Uygulamadaki her iddianın kaynağı kartın altında yazar. Özet:

- **20-20-20 kuralı** Amerikan Optometri Birliği'nin (AOA) önerisi; 1990'larda
  optometrist Jeffrey Anshel'in akılda kalıcı olsun diye ortaya attığı bir formül.
  Büyük bir klinik çalışmayla kanıtlanmış değil — uygulama bunu saklamıyor,
  ayrı bir kartta açıkça söylüyor.
- **Göz kırpma düşüşü** (22 → 7 /dk) *New England Journal of Medicine*, 1993.
- **%66 yaygınlık** 45 çalışmalık derleme, *Scientific Reports*, 2023.
- **Türkiye'de ~%48** *BMC Public Health*, 2024.
- **Hatırlatıcı kalkınca şikâyetler geri dönüyor** *Cont Lens Anterior Eye*, 2023.
- **2 saat eşiği** AOA.
- **Çocuklarda miyopiyi açık hava yavaşlatıyor, molalar değil** *JAMA*, 2015.

Bilerek **söylemediklerimiz**: "ekran gözü kalıcı bozar" (doğru değil),
"20-20-20 miyopiyi önler" (kanıtı yok), "klinik olarak kanıtlanmıştır" (değil).

Bu uygulama tıbbi tavsiye değildir. Gözünde sürekli ağrı, bulanık görme veya
baş ağrısı varsa göz hekimine görün.

---

## Sonraki adımlar (yapılmadı)

- Web sürümünde **uzun mola** ve **süreli duraklatma** (masaüstünde var).
- **Haftalık HTML rapor** dışa aktarma.

---

## Geliştirirken düşülen tuzaklar

Kod üzerinde çalışacaksan bunları bilmek zaman kazandırır:

1. **`ctypes` dönüş tipi bildirilmeli.** `GetAsyncKeyState` 16 bitlik SHORT
   döndürür; bildirmezsen ctypes 32 bit int sanar, üst bitler çöp kalır ve
   `& 0x8000` testi rastgele doğru çıkar. Bu yüzden acil çıkış kısayolu kimse
   basmadan tetikleniyor, molalar sessizce iptal oluyordu. `izleyici.py`
   başındaki `restype` satırlarını silme.
2. **`OpenProcess` başarılı olması süreç yaşıyor demek değil.** Tutamacı açık
   tutan biri varsa ölmüş sürecin PID'i serbest kalmaz. Bekçi bu yüzden
   sonsuza kadar bekliyordu; `WaitForSingleObject` ile kontrol şart.
3. **Tuvale çizilen her parçaya etiket ver.** Etiketsiz parçalar
   `delete(etiket)` ile silinmez; sekme değiştirince eski grafik altta kalıyordu.
4. **JSON dosyalarını `utf-8-sig` ile oku.** BOM'lu dosya sessizce
   varsayılanlara düşürüyordu.
5. **Test için ekran görüntüsünü Python içinden al.** PowerShell DPI farkında
   değil; dışarıdan alınca pencere kırpık çıkıyor.
