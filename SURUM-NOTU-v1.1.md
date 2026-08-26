# Göz Molası v1.1

*GitHub Releases'e konulmayı bekliyor. Kodda `SURUM = "1.1"`;
etiket birebir `v1.1` olmalı — güncelleme denetimi ikisini
karşılaştırıyor.*

---

## 🇹🇷 Türkçe

### Yeni: Aile kipi

Artık iki kip var. **Bireysel** kip eskisi gibi çalışıyor — ayarlar senin,
molayı istersen geçersin.

**Aile kipi** ebeveynler için: ayarlara girmek şifre ister, mola
atlanamaz, günlük ekran süresi sınırı konabilir ve belli saatlerde
bilgisayar kullanımı kapatılabilir. Süre dolduğunda tam ekran bir uyarı
çıkıyor; ebeveyn şifresiyle 15 veya 30 dakika ek süre verilebiliyor.

Aile kipi şifresiz açılmıyor — şifresiz bir ebeveyn kilidi, anahtarı
kapının üstünde bırakmak olurdu.

*Dürüst olalım:* bu bir güvenlik duvarı değil. Görev Yöneticisi'nden
kapatılabilir. "Zorla kapatılırsa geri aç" ayarı bunu zorlaştırıyor ama
kararlı biri yine de aşar. Amaç engellemek değil, sınırı görünür kılmak.

### Yeni: Bilgiler sekmesi

Uygulamadaki bütün bilgiler artık tek yerde — 43 kart. Göz sağlığı
bilgileri, pratik ipuçları, mola egzersizleri ve ayrıntılı rehber.
Eskiden bunlar yalnızca molalarda tek tek çıkıyordu; merak edenin hepsini
görebileceği bir yer yoktu.

### Yeni: Molalarda dünyadan bilgiler

Bütün kartlar göz sağlığı üzerineydi ve hepsi aynı şeyi söylüyordu.
Günde 20-30 mola veren biri için bu bir süre sonra okunmaz oluyor.
Artık araya dünyanın her yerinden, her konudan 18 kart giriyor — uzay,
okyanus, dil, tarih. Hepsinin kaynağı var. Göz bilgileri hâlâ baskın.

### Yeni: Mola atlarsan ne olur

Molayı atlayınca eskiden hiçbir şey olmuyordu; mola sessizce düşüyordu.
Artık neyi atladığın söyleniyor ve mola birkaç dakika sonraya, **daha
kısa** olarak yeniden konuyor. Yoğun bir günde üst üste atlayan biri
tamamen molasız kalmasın diye.

### Yeni: Klavye kısayolları

`M` mola · `A` ayarlar · `T` tema · `H` gizle · `F1` liste.
Web sürümüyle aynı harfler.

### Yeni: Güncelleme bildirimi

Yeni sürüm çıktığında program sana söylüyor. Günde en fazla bir kez
internete bakıyor, hiçbir kişisel bilgi göndermiyor ve indirmeyi
kendiliğinden yapmıyor — karar senin.

### Düzeltmeler

- **Sayaç artık kaybolmuyor.** Program çökerse ya da zorla kapatılırsa
  en fazla 30 saniye kayıp oluyor; eskiden 20 dakika baştan başlıyordu.
- **Pencerenin altı görev çubuğunun altında kalmıyor.** "Programı kapat"
  düğmesi bazı ekranlarda tıklanamıyordu.
- **Panelde üst üste binen yazılar düzeldi.** "Arka planda çalışıyorum"
  şeridi sayaç kartının içine düşüyordu.
- **Şerit ilk açılışta boş kalmıyor.**
- Mola ekranındaki "göz kırp" egzersizi yenilendi — artık objektif
  diyaframı gibi açılıp kapanıyor.
- Şifre koruması güçlendirildi (PBKDF2, 600.000 tur). Var olan şifreler
  ilk doğru girişte kendiliğinden yükseliyor, kimse şifresini kaybetmiyor.
  Şifre gücü tahmini de gerçekçi hale getirildi: eskiden 4 haneli bir
  PIN için "1000 dakika dayanır" yazıyordu, gerçekte birkaç saniye.

### Görünmeyen ama önemli

Bu sürümden itibaren program **sınamalardan geçmeden derlenemiyor**.
Panelde çakışma var mı, pencere ekrana sığıyor mu, bilgilerin kaynağı
var mı, aile kipi kuralları işliyor mu ve en önemlisi **derlenen program
gerçekten açılıyor mu** — hepsi otomatik denetleniyor. Biri kalırsa
uygulama açılmıyor.

Sebebi: bir keresinde "başarıyla derlendi" diyen bir sürüm
çalıştırıldığında hiç açılmadı.

---

## 🇬🇧 English

### New: Family mode

There are now two modes. **Individual** mode works as before — the
settings are yours and you can skip a break if you want.

**Family mode** is for parents: opening settings requires a password,
breaks cannot be skipped, a daily screen-time limit can be set, and
computer use can be blocked during chosen hours. When the limit is
reached a full-screen notice appears; a parent can grant 15 or 30 extra
minutes with the password.

Family mode cannot be enabled without a password — a parental lock with
no password would be leaving the key in the door.

*To be honest:* this is not a security barrier. It can be closed from
Task Manager. The "restart if force-closed" setting makes that harder,
but a determined person will still get around it. The goal is not to
block, but to make the limit visible.

### New: Facts tab

Every fact in the app is now in one place — 43 cards. Eye-health facts,
practical tips, break exercises and the full guide. They used to appear
only one at a time during breaks, with no place to see them all.

### New: Facts from around the world

Every card used to be about eye health, all saying much the same thing.
For someone taking 20-30 breaks a day that stops being read. Now 18
sourced cards from all over the world are mixed in — space, oceans,
language, history. Eye-health facts still dominate.

### New: What happens if you skip a break

Skipping used to do nothing; the break simply vanished. Now the app
tells you what you skipped and schedules the break again a few minutes
later, **shorter**. So a busy day doesn't end with no breaks at all.

### New: Keyboard shortcuts

`M` break · `A` settings · `T` theme · `H` hide · `F1` list.
Same keys as the web version.

### New: Update notice

The app tells you when a new version is out. It checks at most once a
day, sends no personal data, and never downloads anything on its own —
the decision is yours.

### Fixes

- **The timer no longer gets lost.** If the program crashes or is
  force-closed, at most 30 seconds are lost; it used to restart the full
  20 minutes.
- **The bottom of the window no longer hides behind the taskbar.** The
  "Close program" button was unclickable on some screens.
- **Overlapping text in the panel is fixed.** The "running in the
  background" strip was drawn inside the timer card.
- **The strip is no longer empty on first launch.**
- The "blink" exercise was redesigned — it now opens and closes like a
  camera aperture.
- Password protection strengthened (PBKDF2, 600,000 rounds). Existing
  passwords upgrade themselves on the first correct entry, so nobody
  loses their password. The strength estimate is realistic now: a
  4-digit PIN used to be shown as lasting "1000 minutes"; in reality it
  is a few seconds.

### Invisible but important

From this version on, the program **cannot be built without passing its
tests**: panel overlap, whether the window fits the screen, whether
every claim has a source, whether family-mode rules actually apply, and
most importantly **whether the built program really opens**. If any
check fails, the app does not launch.

The reason: once, a build that reported "success" did not open at all.
