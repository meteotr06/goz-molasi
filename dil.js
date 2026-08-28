/* ============================================================
   DİL — Türkçe / English

   TASARIM KARARI: sözlüğün anahtarı Türkçe metnin KENDİSİ.
   Alternatifi her HTML öğesine data-c="anahtar" eklemekti; bu 179
   ayrı düzenleme demekti ve yeni oturmuş arayüzü bozma riski yüksekti.
   Bu yöntemde HTML'e hiç dokunulmuyor: sayfa yüklenince metin
   düğümleri geziliyor ve sözlükte TAM eşleşen varsa değiştiriliyor.

   "Tam eşleşme" şart: parça eşleştirmek, içinde Türkçe geçen her
   yeri bozardı.

   Dil seçimi: kayıtlı tercih → tarayıcı dili → Türkçe.
   ============================================================ */

const DIL_ANAHTAR = 'goz-molasi-dil';

const SOZLUK = {
  /* ---- 28.08.2026: HARF TABANLI OLMAYAN TARAMAYLA BULUNANLAR ----
     Yontem: sayfa iki dilde ayri ayri acilip metin dugumleri
     karsilastirildi; iki dilde BIREBIR AYNI kalan her metin aday
     sayildi (test-dil.html). Payda 338 metin, 34 aday.

     Neden onemli: eski denetim `cgiosu` harflerini ariyordu ve 34
     adayin ancak 19'unu gorebiliyordu -- 15'i harf tasimadigi ya da
     cumle parcasi oldugu icin gorunmuyordu. Harfe bakmak yerine iki
     dili karsilastirmak, dilin kendisine degil DAVRANISA bakiyor.

     Cumle parcalari da ayri anahtar: HTML'de `<b>` araya girince metin
     birden cok dugume boluniyor ve sozluk tam eslesme istiyor. */
  'seç': 'select',
  'Şimdi değil': 'Not now',
  'Bilgiler sekmesi': 'Info tab',
  'Sayaç sekmesi': 'Timer tab',
  'Atlamak için basılı tut': 'Press and hold to skip',
  'Küçük bir çalışmada daha iyi': 'Better in a small study',
  'Windows sürümünü': 'the Windows version',
  'Uygulamadaki bütün bilgiler burada. Her sağlık iddiasının kaynağı altında yazıyor; kanıtı zayıf olanlarda bunu açıkça söylüyoruz.':
    'Everything the app knows is here. Every health claim cites its source underneath, and where the evidence is weak we say so plainly.',
  'Telefonda:': 'On phones:',
  'uygulamayı ana ekrana kurduysan simgeye basılı tutunca “Şimdi mola ver”, “5 dakika duraklat” ve “Rehber” kısayolları çıkar.':
    'if you added the app to your home screen, press and hold the icon for the “Take a break now”, “Pause 5 minutes” and “Guide” shortcuts.',
  'Mola ekranındayken kısayollar çalışmaz — 20 saniye tuşla geçilebilseydi mola olmazdı.':
    'Shortcuts do not work while the break screen is up — if 20 seconds could be skipped with a key, it would not be a break.',

  /* Istatistik cumlesi `<b>` ile parcalanmis: dort ayri dugum. */
  '8 saatlik bir günde': 'In an 8-hour day',
  '· toplam': '· total',
  'göz dinlenmesi': 'of eye rest',

  /* Bosta esigi cumlesi de parcali. */
  'Telefonda': 'On phones',
  ', bilgisayarda': ', on computers',
  'kapalı': 'off',
  'açık': 'on',
  'geliyor. Sebebi: telefonda başka uygulamaya geçmek ekrandan kalkmak değildir, hâlâ ekrana bakıyorsundur. Açıkken 5 dakikadan uzun uzaklaşırsan sayaç baştan başlar; kapalıyken hiç sıfırlanmaz, saatler sonra açsan bile kaldığın yerden devam eder.':
    'by default. Why: on a phone, switching to another app is not the same as looking away — you are still at the screen. When it is on, stepping away for more than 5 minutes restarts the timer; when it is off it never resets, so it carries on from where you left it even hours later.',

  /* ---- Kurulum şeridi ----
     DİKKAT: bu iki metinde hiç çğıöşü YOK; sınamanın harf tabanlı
     taraması onları göremez. 28.08.2026'da gözle bulundu. */
  'Uygulama olarak kurulabilir': 'Can be installed as an app',
  'Tarayıcı çubuğu olmadan, kendi penceresinde çalışır':
    'Runs in its own window, without the browser bar',

  /* ---- Tema adları ----
     `title` ve `aria-label` olarak yazılıyorlar; gözle görünmezler.
     DİKKAT: "Okyanus", "Kiraz", "Lavanta", "Buz", "Kum", "Zeytin",
     "Beyaz" Türkçe harf TAŞIMIYOR — sınamanın harf tabanlı denetimi
     onları göremez. Buraya elle eklendiler. */
  'Beyaz': 'White',
  'Gece moru': 'Night purple',
  'Dinginlik': 'Calm',
  'Okyanus': 'Ocean',
  'Orman': 'Forest',
  'Şafak': 'Dawn',
  'Gün batımı': 'Sunset',
  'Buz': 'Ice',
  'Lavanta': 'Lavender',
  'Kiraz': 'Cherry',
  'Bakır': 'Copper',
  'Kömür (renksiz)': 'Charcoal (colourless)',
  'Gökyüzü': 'Sky',
  'Kum': 'Sand',
  'Zeytin': 'Olive',
  'Açık (gündüz)': 'Light (daytime)',
  'Kâğıt (açık)': 'Paper (light)',

  /* ---- Gezinme etiketleri (HTML'de aria-label) ---- */
  'Bölümler': 'Sections',
  'Diğer uygulamalar': 'Other apps',

  /* ---- Ekran okuyucu ve ipucu metinleri ----
     Gözle görünmedikleri için görsel tarama bunları yakalayamaz.
     28.08.2026'da ölçüldü: İngilizce sayfada grafiğin aria-label'ı
     Türkçe okunuyordu. */
  'Link kopyalandı': 'Link copied',
  'Paylaş': 'Share',
  'Linki kopyala:': 'Copy the link:',

  /* ---- Hafta grafiği: gün adları ----
     Grafik yalnızca VERİ VARKEN çiziliyor; boş geçmişle sınama
     koşunca bu metinler DOM'da hiç olmuyor ve sınama geçiyordu. */
  'Bugün': 'Today',
  'Paz': 'Sun', 'Pzt': 'Mon', 'Sal': 'Tue', 'Çar': 'Wed',
  'Per': 'Thu', 'Cum': 'Fri', 'Cmt': 'Sat',

  /* ---- Mola ekranı: egzersizler ----
     BURASI SONRADAN ÜRETİLEN İÇERİK. Sayfa kurulduktan sonra
     yazıldığı için `sayfayiCevir` onu göremez; yazan satır `C()`
     kullanmak zorunda (arayuz.js, molaEkraniAc yakını).
     28.08.2026'da ölçüldü: İngilizce sayfada mola ekranı Türkçe
     kalıyordu — kullanıcının NE YAPACAĞINI söyleyen tek metin. */
  'Uzağa bak': 'Look far away',
  'Pencereden dışarı ya da odanın en uzak köşesine bak':
    'Look out the window, or at the farthest corner of the room',
  'Göz kırp': 'Blink',
  'Kapak kapandığında sen de tam kırp — gözünü sıkıca kapat':
    'Blink as the lid closes — shut your eyes tightly',
  'Yakın — uzak': 'Near — far',
  'Nokta büyüyünce parmağına, küçülünce uzağa bak':
    'Look at your finger as the dot grows, far away as it shrinks',
  'Gözünü kapat': 'Close your eyes',
  'Gözlerini kapat, yavaşça nefes al — bitince ses gelecek':
    'Close your eyes and breathe slowly — a sound plays when it ends',
  'Boynunu gevşet': 'Relax your neck',
  'Başını yavaşça çevir — omuzlarını geriye at':
    'Turn your head slowly — roll your shoulders back',

  /* ---- Başlık ve kimlik ---- */
  'Göz Molası — Ekran Başında Göz Yorgunluğu İçin 20-20-20 Hatırlatıcısı':
    'Eye Break — 20-20-20 Reminder for Screen Eye Strain',
  'Göz Molası': 'Eye Break',
  'Göz Molası başka bir sekmede açık': 'Eye Break is open in another tab',
  'Sayacın doğru işlemesi için aynı anda tek sekme sayar. Bu sekmede devam etmek istersen diğeri durur — verilerin aynen taşınır, hiçbir şey kaybolmaz.':
    'Only one tab counts at a time so the timer stays accurate. Continue here and the other one stops — your data carries over, nothing is lost.',
  'Buradan devam et': 'Use here',
  '20 DAKİKA · 20 SANİYE · 6 METRE': '20 MINUTES · 20 SECONDS · 6 METRES',

  /* ---- Ana ekran ---- */
  '▶ Başlat': '▶ Start',
  'Duraklat': 'Pause',
  'Devam et': 'Resume',
  'Şimdi mola ver': 'Take a break now',
  '↺ Sıfırla': '↺ Reset',
  'Sıfırla': 'Reset',
  '🔔 Bildirimlere izin ver': '🔔 Allow notifications',
  'Bildirimler uygulama açıkken çalışır. Telefon kilitliyken ya da tarayıcı arka plandayken uyarı gelmeyebilir; bunun için verilerin bir sunucuya gitmesi gerekirdi, göndermiyoruz.':
    'Notifications work while the app is open. If your phone is locked or the browser is in the background, the alert may not arrive — delivering it would mean sending your data to a server, and we do not.',
  'Bilgisayarda başka pencereye geçsen de sayaç döner. Telefonda tarayıcı arka plandaki sayfayı uyutabilir; o sırada mola uyarısı gelmeyebilir. Geri döndüğünde geçen süre gerçek saatten hesaplanır. Pili biraz daha çok kullanır.':
    'On a computer the timer keeps running even if you switch windows. On a phone the browser may suspend a backgrounded page, so the break alert may not arrive while you are away. When you come back, the elapsed time is worked out from the clock. Uses a little more battery.',
  '⬇ Uygulama olarak kur': '⬇ Install as app',
  'Uygulama olarak kur': 'Install as app',
  'tamamlanan mola': 'breaks taken',
  'atlanan mola': 'breaks skipped',
  'takip edilen süre': 'time tracked',
  'bu sekmede geçen süre': 'time in this tab',
  'Bu sayaç sekme açıldığından beri işler. Bilgisayarın açık olduğu her anı ölçmek için Windows sürümünü kullan.':
    'This counter runs from the moment the tab opened. To measure every minute your computer is on, use the Windows version.',
  'cihaz başında süre': 'time at device',
  'Son 7 gün': 'Last 7 days',
  'Bugünkü durum': 'Today',
  'Kesikli çizgi günlük hedef:': 'Dashed line is the daily goal:',
  'mola': 'breaks',
  'Yükleniyor…': 'Loading…',
  'Neden?': 'Why?',
  'Başka bir bilgi göster': 'Show another fact',
  '📖 Ayrıntılı rehberi oku': '📖 Read the full guide',
  'Sayaç': 'Timer',
  'Bilgiler': 'Facts',
  'Göz sağlığı': 'Eye health',
  'Pratik ipuçları': 'Practical tips',
  'Molalardaki egzersizler': 'Break exercises',
  'Dünyadan': 'From the world',
  'Ayrıntılı rehber': 'The full guide',
  'Nasıl?': 'How?',
  'Windows sürümü imzalı olmadığı için ilk açılışta':
    'Because the Windows version is unsigned, the first launch shows',
  'Windows bilgisayarınızı korudu': 'Windows protected your PC',
  'uyarısı çıkar.\n        Zararlı olduğu anlamına gelmez —':
    'That does not mean it is harmful —',
  'Ek bilgi': 'More info',
  'Yine de çalıştır': 'Run anyway',
  'ile açılır.\n        Kaynak kodun tamamı açık, istersen kendin derleyebilirsin.':
    'opens it. The full source is public; you can build it yourself.',
  'Kısayollar': 'Shortcuts',
  'Başlat / duraklat': 'Start / pause',
  'Temayı değiştir': 'Change theme',
  'Sayacı sıfırla': 'Reset the timer',
  'Bu liste': 'This list',
  'Boşluk': 'Space',
  'Anladım': 'Got it',
  'Sayaç sıfırdan başladı': 'The timer started over',
  'Yeni sürüm hazır': 'A new version is ready',
  'Yenile': 'Reload',
  'Paylaş': 'Share',
  'Temayı değiştir': 'Change theme',
  'Ayarlar': 'Settings',
  'Kip': 'Mode',

  /* ---- Kipler ---- */
  'Çalışma': 'Focus',
  'Ders': 'Study',
  'Toplantı': 'Meeting',
  'Film · oyun': 'Film · gaming',
  '20 dk · 20 sn': '20 min · 20 s',
  '25 dk · 30 sn': '25 min · 30 s',
  'sessiz, seyrek': 'quiet, rare',
  'neredeyse hiç': 'almost never',

  /* ---- İlk açılış tanıtımı ---- */
  '20 dakikada bir ekranın 20 saniye kapanacak.':
    'Every 20 minutes your screen goes dark for 20 seconds.',
  'O sırada gözünü 6 metre uzağa çevirmen yeterli. Nasıl bir şey olduğunu şimdi 6 saniyede görebilirsin.':
    'All you have to do is look 6 metres away. See what it feels like — takes 6 seconds.',
  'Örnek molayı göster': 'Show me a sample break',
  'Gerek yok, başla': 'No need, just start',
  'Tekrar göster': 'Show again',
  'Anladım, başla': 'Got it, start',
  'Tanıtımı kapat': 'Dismiss',

  /* ---- Mola ekranı ---- */
  'Gözünü ekrandan ayır': 'Look away from the screen',
  'Az kaldı — hazırlan': 'Almost done — get ready',
  'Odayı, pencereyi, uzaktaki bir noktayı süz. Yaklaşık 6 metre.':
    'Gaze at the room, the window, something far away. About 6 metres.',
  'saniye': 'seconds',
  'Atlamak için basılı tut': 'Press and hold to skip',
  'Molayı atla — basılı tut': 'Skip the break — press and hold',
  'Bırakma…': 'Keep holding…',
  'Mola tamam': 'Break done',
  'Mola atlandı': 'Break skipped',
  '5 dk ertele': 'Snooze 5 min',
  'Dışarısı': 'Outside',
  'Senin durumun': 'Your progress',
  'İpucu': 'Tip',
  'Hava kalitesi': 'Air quality',

  /* ---- Ayarlar ---- */
  'Hazır süreler': 'Presets',
  '20 dk · 20 sn': '20 min · 20 s',
  '10 dk · 20 sn': '10 min · 20 s',
  '30 dk · 30 sn': '30 min · 30 s',
  '45 dk · 1 dk': '45 min · 1 min',
  'Klasik 20-20-20 kuralı': 'The classic 20-20-20 rule',
  '2023 çalışması bunu öneriyor': 'Suggested by a 2023 study',
  'Daha seyrek, daha uzun': 'Less often, but longer',
  'Odak bloğu sevenler için': 'For deep-focus blocks',
  'Uygulamanın dili': 'Interface language',
  'Dil / Language': 'Dil / Language',
  'Şifre yalnızca': 'The PIN protects',
  'Bugünkü durum': 'Today',
  'Kendine uyanı seç, istersen aşağıdan elle değiştir':
    'Pick one that suits you, or adjust below',
  'Çalışma süresi': 'Work interval',
  'Kaç dakikada bir mola verilsin': 'How often to take a break',
  'Mola süresi': 'Break length',
  'Ekranın kaç saniye kapalı kalacağı': 'How long the screen stays dark',
  'Ön uyarı': 'Advance warning',
  'Molaya kaç saniye kala haber verilsin (0 = uyarma)':
    'Seconds of warning before a break (0 = none)',
  'Uzun mola': 'Long break',
  'Uzun çalışmadan sonra daha uzun bir mola':
    'A longer break after a long stretch of work',
  'Uzun mola süresi': 'Long break length',
  'Çalışma saatleri': 'Working hours',
  'Bu saatlerin dışında hatırlatma gelmez':
    'No reminders outside these hours',
  'Saat aralığı': 'Time range',
  'Mola atlanabilsin': 'Allow skipping breaks',
  'Kapatırsan molayı geçemezsin': 'Turn this off and breaks cannot be skipped',
  'Uyarı sesi': 'Sound',
  'Mola başında ve sonunda kısa bir ses':
    'A short sound at the start and end of a break',
  'Titreşim': 'Vibration',
  'Mola başında ve sonunda telefon titresin':
    'Phone vibrates at the start and end of a break',
  'Açılışta kendiliğinden başla': 'Start automatically',
  'Uygulama açılır açılmaz sayaç dönmeye başlar':
    'The timer starts as soon as the app opens',
  'Arka planda çalışmaya devam et': 'Keep running in the background',
  'Başka uygulamaya geçsen de sayaç dönmeye devam eder. Pili biraz daha çok kullanır.':
    'The timer keeps running when you switch apps. Uses a little more battery.',
  'Uzun süre uzak kalınca sayacı sıfırla': 'Reset the timer after a long absence',
  'Telefonda <b>kapalı</b>, bilgisayarda <b>açık</b> geliyor. Sebebi: telefonda başka uygulamaya geçmek ekrandan kalkmak değildir, hâlâ ekrana bakıyorsundur. Açıkken 5 dakikadan uzun uzaklaşırsan sayaç baştan başlar; kapalıyken hiç sıfırlanmaz, saatler sonra açsan bile kaldığın yerden devam eder.':
    'Off by default on phones, on by default on computers. The reason: on a phone, switching to another app is not the same as looking away from a screen — you are still looking at one. When on, being away for more than 5 minutes restarts the timer; when off it is never reset, and carries on even if you open the app hours later.',
  'Molada kazayla çıkmayı önle': 'Prevent leaving the break by accident',
  'Mola boyunca tam ekrana geçer ve geri tuşu molayı bitirmez. Kilitlemez: Esc her zaman çıkarır, istersen molayı yine atlayabilirsin.':
    'Goes full screen during the break and the back button no longer ends it. It does not lock you in: Esc always exits, and you can still skip the break.',
  'Ekran birazdan kararacak': 'The screen is about to go dark',
  'Şimdi molaya geç': 'Take the break now',
  'Çalışma saatleri — başlangıç': 'Working hours — start',
  'Çalışma saatleri — bitiş': 'Working hours — end',
  'Şehir ara': 'Search for a city',
  'Şifre': 'Password',
  'Boşta durdurma': 'Pause when idle',
  "Dokunulmazsa sayaç durur; 5 dk'dan uzun uzak kalırsan baştan sayar":
    'The timer pauses if untouched; away longer than 5 min and it restarts',
  'Cihaz etkinliğini izle': 'Track device activity',
  'Sekme arka plandayken de çalışsın': 'Works while the tab is in the background',
  'Molalarda hava durumu': 'Weather during breaks',
  'Kapalı — molalarda yalnızca göz bilgisi gösterilir':
    'Off — breaks show eye facts only',
  'Konumumu kullan': 'Use my location',
  'Konumu unut': 'Forget location',
  'ya da şehir ara — örn. İzmir, Berlin':
    'or search a city — e.g. Izmir, Berlin',
  'Canlılık': 'Vividness',
  'Renklerin doygunluğu — yazı okunaklılığı değişmez':
    'Colour saturation — text legibility is unaffected',
  'Sakin': 'Calm',
  'Dengeli': 'Balanced',
  'Canlı': 'Vivid',
  'Renk teması': 'Colour theme',
  'Sistemle aynı': 'Match system',
  'Açık — şifreyi değiştirme ve verileri silme korumalı':
    'On — changing the PIN and erasing data are protected',
  'Seçince hemen uygulanır': 'Applies immediately',
  'Kilit şifresi': 'Lock PIN',
  'Kapalı — verileri silmek serbest': 'Off — data can be erased freely',
  'Şifreyi koy': 'Set PIN',
  'Şifreyi kaldır': 'Remove PIN',
  'Şifreyi değiştir': 'Change PIN',
  '4–8 hane': '4–8 digits',
  'Tüm verileri sıfırla': 'Erase all data',
  'Ayarlar, sayaçlar ve şifre silinir': 'Settings, counters and PIN are deleted',
  'Emin misin? Tekrar bas': 'Are you sure? Press again',
  'Bu işlem geri alınamaz.': 'This cannot be undone.',
  'Kaydet': 'Save',
  'Vazgeç': 'Cancel',
  'Onayla': 'Confirm',
  'Kapat': 'Close',
  'Neler değişti?': 'What changed?',
  'Ekle': 'Add',
  'Kur': 'Install',
  'İzin ver': 'Allow',
  'Desteklenmiyor': 'Not supported',
  'Hazır': 'Ready',
  'Çalışıyor': 'Running',
  'Duraklatıldı': 'Paused',
  'Boşta — sayaç durdu': 'Idle — timer paused',
  'Mola geliyor': 'Break coming up',
  'Mola': 'Break',
  'Çalışma saati dışı': 'Outside working hours',
  '⏸ Duraklat': '⏸ Pause',
  '▶ Devam et': '▶ Resume',

  /* ---- Çalışma anında yazılan metinler ---- */
  'Mola bitti, devam edebilirsin.': 'Break over, carry on.',
  'Mola atlandı.': 'Break skipped.',
  'Açık — önce konum ver ya da şehir ara':
    'On — set a location or search for a city first',
  'Sonuç yok.': 'No results.',
  '⬇ Ana ekrana ekle': '⬇ Add to home screen',
  '🔔 Bildirimler açık': '🔔 Notifications on',
  '🔕 Bildirimlere izin verilmedi': '🔕 Notifications not allowed',
  '🔕 Bu tarayıcı bildirim desteklemiyor':
    '🔕 This browser does not support notifications',
  'Çok fazla yanlış deneme — 30 saniye bekle.':
    'Too many wrong attempts — wait 30 seconds.',
  'Açık — sekme arka plandayken de cihazda hareket olup olmadığı görülüyor. Sadece "etkin mi, ekran kilitli mi" bilgisi; ne yaptığın değil.':
    'On — device activity is visible even while the tab is in the background. Only "active or idle, screen locked or not"; never what you are doing.',
  'Kapalı — sayaç yalnızca bu sekmedeki hareketi görüyor. Başka pencerede çalışırken "boşta" sanılabilir.':
    'Off — the timer only sees activity in this tab. Working in another window may look like idling.',
  'İzin reddedilmiş. Adres çubuğundaki kilit simgesinden açabilirsin.':
    'Permission was denied. You can allow it from the lock icon in the address bar.',
  'Bu tarayıcı cihaz etkinliğini paylaşmıyor (Chrome ve Edge destekliyor). Sayaç yalnızca bu sekmedeki hareketi görüyor.':
    'This browser does not share device activity (Chrome and Edge do). The timer only sees activity in this tab.',
  'Henüz mola yok. İlk molanı tamamladığında buraya günlük çubuğun düşecek.':
    'No breaks yet. Your daily bar appears here once you finish your first one.',
  'İşte böyle görünüyor. Gerçeğinde 20 saniye sürecek ve kapatılamayacak.':
    'That is what it looks like. The real one lasts 20 seconds and cannot be closed.',
  'Bu sayaç yalnızca uygulama açıkken işler. Ayarlardan "Cihaz etkinliğini izle"yi açarsan arka planda da sayar.':
    'This counter only runs while the app is open. Turn on "Track device activity" in Settings to count in the background.',
  'Cihaz etkinliği izniyle ölçülüyor — sekme arka plandayken de sayar.':
    'Measured with device-activity permission — counts in the background too.',

  /* ---- Şifre ---- */
  'Şifre gerekli': 'PIN required',
  'Bu işlem kilitli. Devam etmek için şifreni gir.':
    'This action is locked. Enter your PIN to continue.',
  'Şifremi unuttum': 'I forgot my PIN',
  'Programı kapatmak için şifreni gir.': 'Enter your PIN to close the app.',
  'Şifreyi değiştirmek için önce mevcut şifreni gir.':
    'Enter your current PIN to change it.',
  'Kilidi kaldırmak için şifreni gir.': 'Enter your PIN to remove the lock.',
  'Verileri silmek için şifre gerekli.': 'A PIN is required to erase data.',
  'Şifre 4–8 rakam olmalı.': 'The PIN must be 4–8 digits.',

  /* ---- Kurulum ---- */
  'Ana ekrana ekle': 'Add to home screen',
  'Ana ekranına ekle, internetsiz de çalışsın':
    'Add it to your home screen and use it offline',
  'Artık normal bir uygulama gibi açılır, internet olmadan da çalışır ve tarayıcı çubuğu görünmez.':
    'It opens like a normal app, works offline, and hides the browser bar.',
  'Sağ üstten': 'From the top right',
  'düğmesine bas': 'tap the button',
  '“Ana Ekrana Ekle”': '“Add to Home Screen”',
  'Listeyi aşağı kaydır,': 'Scroll down the list,',
  "Safari'nin altındaki": 'At the bottom of Safari,',
  '(kare içinde yukarı ok)': '(square with an up arrow)',

  /* ---- Alt bilgi ---- */
  'Göz sağlığı rehberi': 'Eye health guide',
  'Windows sürümü': 'Windows version',
  'Web sürümü mü, Windows sürümü mü? Farkları':
    'Web version or Windows version? The differences',
  'İkisi de ücretsiz ve aynı işi yapıyor. Fark, tarayıcının yapabildikleriyle ilgili:':
    'Both are free and do the same job. The difference is what a browser is able to do:',
  'tarayıcı, sekmesi kapalıyken hiçbir şey ölçemez':
    'a browser cannot measure anything while its tab is closed',
  '— bu bir ayar değil, teknik bir sınır. Hiçbir izin bunu değiştirmiyor.':
    '— that is not a setting but a technical limit. No permission changes it.',
  'Kurulum': 'Installation',
  'yok': 'none',
  'indir, çalıştır': 'download and run',
  'Sekme kapalıyken ölçer mi': 'Measures while the tab is closed',
  'Bilgisayar açılışında başlar mı': 'Starts when the computer starts',
  'Hangi programda ne kadar durduğun': 'Time spent in each program',
  'Şifreyle kapanma koruması': 'PIN lock against closing',
  'Telefonda çalışır mı': 'Works on phones',
  'Kendiliğinden güncellenir mi': 'Updates itself',
  'evet': 'yes',
  'hayır': 'no',
  'yeniden indirilir': 'download again',
  'Zararlı olduğu anlamına gelmez —': 'That does not mean it is harmful —',
  'Ek bilgi': 'More info',
  'Yine de çalıştır': 'Run anyway',
  'ile açılır. Kaynak kodun tamamı açık, istersen kendin derleyebilirsin.':
    'opens it. The full source is public; you can build it yourself.',
  'Windows sürümü imzalı olmadığı için ilk açılışta':
    'Because the Windows version is unsigned, the first launch shows',
  '“Windows bilgisayarınızı korudu”': '“Windows protected your PC”',
  'uyarısı çıkar.': '.',
  '⬇ Windows sürümünü indir': '⬇ Download the Windows version',
  'Tarayıcı, sekmesi kapalıyken hiçbir şey ölçemez — hiçbir izin bunu değiştirmiyor. Bilgisayarın açık olduğu her an ölçüm yapılmasını istiyorsan':
    'A browser cannot measure anything while its tab is closed — no permission changes that. If you want measurement whenever your computer is on, use the',
  'kullan: açılışta başlar, tepside durur, cihazın tamamını ölçer.':
    'instead: it starts with Windows, lives in the tray, and measures the whole device.',
  '📖 Ayrıntılı rehberi oku': '📖 Read the full guide',
  'Gizlilik politikası': 'Privacy policy',
  'Kaynak kod': 'Source code',
  'Kısayollar:': 'Shortcuts:',
  'başlat/duraklat ·': 'start/pause ·',
  'hemen mola ·': 'break now ·',
  'pencereyi kapat.': 'close the dialog.',
  'Boşluk': 'Space',
  'Not:': 'Note:',
  'Şifre hakkında:': 'About the PIN:',
  've': 'and',
  'de': 'also',
  'Reklam': 'Ad',
  'Bu sayaç yalnızca uygulama açıkken işler.':
    'This counter only runs while the app is open.',
  'Bu uygulama tıbbi tavsiye değildir. Gözünde sürekli ağrı, bulanık görme veya baş ağrısı varsa göz hekimine görün. · Tüm veriler yalnızca bu cihazda saklanır, hiçbir yere gönderilmez.':
    'This app is not medical advice. See an eye doctor if you have persistent eye pain, blurred vision or headaches. · All data stays on this device and is never sent anywhere.',
  'Tarayıcı, işletim sistemi ekranını kilitleyemez. Bu uygulama sekmenin tamamını kapatır. Sekme kapalıyken hatırlatma gelmesi için uygulamayı ana ekrana ekleyip açık bırak.':
    'A browser cannot lock the operating system screen. This app covers the whole tab instead. To get reminders while the tab is closed, add the app to your home screen and leave it open.',
  'şifrenin kendisini değiştirmeyi': 'changing the PIN itself',
  'tüm verileri silmeyi': 'erasing all data',
  'korur. Ayarlar, duraklatma ve molayı atlama serbesttir. Masaüstü sürümünde şifre ayrıca programın kapatılmasını engeller — tarayıcıda böyle bir şey mümkün değil, sekmeyi kapatan herkes kilidi aşar.':
    'only. Settings, pausing and skipping breaks are free. In the desktop version the PIN also prevents the app from being closed — a browser cannot do that; anyone who closes the tab bypasses the lock.',
  /* ---- Diğer uygulamalar köprüsü ---- */
  'Diğer ücretsiz uygulamalarım': 'My other free apps',
  'Net maaş, kredi, kira, KDV — 35 araç':
    'Salary, loan, rent, VAT — 35 calculators (Turkish)',
  'Saatlik ve 7 günlük': 'Hourly and 7-day',
  'Döviz, altın ve tahmin': 'Currencies, gold and forecasts',
  'Haftalık Planlayıcı': 'Weekly Planner',
  'Ders ve iş programı': 'Study and work schedule',
  'Muhasebe': 'Bookkeeping',
  'Gelir, gider, kasa ve cari': 'Income, expenses, cash and accounts',
  'Hava Durumu': 'Weather',
  'Türkiye geneli, saatlik ve 7 günlük': 'All of Türkiye, hourly and 7-day',
  'Döviz, altın ve kur tahmini': 'Currencies, gold and rate forecasts',
};


/* ---- Dil seçimi ---- */
function dilOku() {
  try {
    const kayitli = localStorage.getItem(DIL_ANAHTAR);
    if (kayitli === 'tr' || kayitli === 'en') return kayitli;
  } catch {}
  // Tarayıcı Türkçe değilse İngilizce göster — uygulama global.
  const t = (navigator.language || 'tr').toLowerCase();
  return t.startsWith('tr') ? 'tr' : 'en';
}

function dilYaz(d) {
  try { localStorage.setItem(DIL_ANAHTAR, d); } catch {}
}

let AKTIF_DIL = dilOku();

/** Saati kullanıcının bölgesine göre yazar.

    NEDEN VAR: saatler elle `getHours()` + `padStart(2,'0')` ile
    yazılıyordu, yani HER dilde 24 saat. Ölçüldü (test-dil.html):
    İngilizce kipte ekranda "00:25" görünüyordu, AM/PM hiç yoktu.
    Dili çevirip saat biçimini çevirmemek yarım yerelleştirmedir;
    "resumes at 14:30" bir Amerikalı için okunaklı değil.

    "İngilizce = 12 saat" DEMİYORUZ: en-GB de 24 saat kullanır.
    Karar tarayıcının bölgesine bırakılıyor — varsayım değil, bilgi.
    Türkçe seçilmişse tr-TR (24 saat) sabit. */
function saatYaz(tarih) {
  const yerel = AKTIF_DIL === 'tr' ? 'tr-TR' : (navigator.language || 'en');
  try {
    return tarih.toLocaleTimeString(yerel, { hour: '2-digit', minute: '2-digit' });
  } catch {
    return String(tarih.getHours()).padStart(2, '0') + ':' +
           String(tarih.getMinutes()).padStart(2, '0');
  }
}

/** Tek bir metni çevir. Sözlükte yoksa olduğu gibi döner —
    çevrilmemiş metin, boş metinden iyidir. */
function C(metin) {
  if (AKTIF_DIL === 'tr' || metin == null) return metin;
  const d = String(metin).trim();
  return SOZLUK[d] || SOZLUK[d.replace(/\s+/g, ' ')] || metin;
}

/** Sayı içeren metinler için: iki dilde ayrı kalıp.
    Sözlükte anahtar olarak tutulamazlar çünkü sayı her seferinde
    değişiyor. */
function CS(trKalip, enKalip) {
  return AKTIF_DIL === 'en' ? enKalip : trKalip;
}

/** Sayfadaki metin düğümlerini ve nitelikleri çevirir.
    TAM eşleşme arıyor: parça eşleştirmek içinde Türkçe geçen her
    yeri bozardı. */
function sayfayiCevir(kok = document.body) {
  if (AKTIF_DIL === 'tr') return;

  const gezgin = document.createTreeWalker(kok, NodeFilter.SHOW_TEXT, {
    acceptNode(d) {
      const ust = d.parentElement;
      if (!ust) return NodeFilter.FILTER_REJECT;
      const e = ust.tagName;
      if (e === 'SCRIPT' || e === 'STYLE') return NodeFilter.FILTER_REJECT;
      return d.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    },
  });
  const dugumler = [];
  while (gezgin.nextNode()) dugumler.push(gezgin.currentNode);
  for (const d of dugumler) {
    const ham = d.nodeValue;
    const kirp = ham.trim();
    // HTML'de satıra bölünmüş metinler tek boşluğa indirgenmeden
    // eşleşmiyordu (tanıtım kartı böyle kaçmıştı).
    const yeni = SOZLUK[kirp] || SOZLUK[kirp.replace(/\s+/g, ' ')];
    if (yeni) d.nodeValue = ham.replace(kirp, yeni);
  }

  for (const nit of ['placeholder', 'title', 'aria-label', 'label', 'alt']) {
    kok.querySelectorAll('[' + nit + ']').forEach((e) => {
      const yeni = SOZLUK[e.getAttribute(nit).trim()];
      if (yeni) e.setAttribute(nit, yeni);
    });
  }

  document.documentElement.lang = 'en';
  const b = SOZLUK[document.title.trim()];
  if (b) document.title = b;
}

/** Dili değiştir ve sayfayı yeniden yükle.
    Yeniden yükleme en güvenlisi: çeviri tek yönlü (tr → en), geri
    dönmek için sayfanın Türkçe hâlinin baştan kurulması gerekiyor. */
function diliDegistir(d) {
  dilYaz(d);
  location.reload();
}

if (typeof window !== 'undefined') {
  window.C = C;
  window.CS = CS;
  window.sayfayiCevir = sayfayiCevir;
  window.diliDegistir = diliDegistir;
  window.aktifDil = () => AKTIF_DIL;
}

if (typeof module !== 'undefined') {
  module.exports = { SOZLUK, C, CS, sayfayiCevir, dilOku, diliDegistir };
}
