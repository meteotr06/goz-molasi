/* NELER DEĞİŞTİ — kullanıcıya yaptığımız işi söyle (K-44).
 *
 * NEDEN VAR
 *   Bugüne kadar sessizce yayınladık. Web şeridi "Yeni sürüm hazır"
 *   diyordu, masaüstü kartı "düzeltmeler ve yeni özellikler var" —
 *   ikisi de doğru ve ikisi de bilgisiz. Kullanıcı neyin düzeldiğini
 *   öğrenemiyordu.
 *
 *   Aile kipinde bu daha ağır: bir ebeveyn, korumanın çalıştığını
 *   sanarak kurmuş olabilir. Düzelttiğimiz açıklar tam da bu sınıftı.
 *   Ona "ayarlarını bir kez daha gözden geçir" demek zorundayız.
 *
 * TEK KAYNAK
 *   Bu dosya. `masaustu/degisiklikler.py` buradan ÜRETİLİR
 *   (`python masaustu/degisiklikler_uret.py`) — elle düzenleme.
 *   Projede aynı desen `dunya.js` → `dunya.py` için zaten kurulu;
 *   sebebi de yazılı: elle ikiz tutulan iki dosya kayıyor.
 *
 * `surum` NE DEMEK
 *   Bu değişikliklerin ÇIKTIĞI damga. Güncel damgaya eşit olmak
 *   ZORUNDA DEĞİL ve olmaya çalışma. Damga her yayında artıyor (bir
 *   yazım düzeltmesi bile artırıyor), bu liste ise yalnızca
 *   anlatılacak bir şey olunca büyüyor.
 *
 *   Şerit "damgaya eşit kayıt" değil, "kullanıcının en son gördüğü
 *   sürümden BÜYÜK kayıt" arıyor. Eşitlik arayan ilk sürüm sessizce
 *   hiç çıkmadı (damga 94, kayıt 93) — bu projede aynı sınıf üç kez
 *   yakalandı. Sayıları elle eşitleme; tuzağı bir sonraki yayına
 *   ertelemiş olursun.
 */
const DEGISIKLIKLER = [
  {
    surum: 140,
    masaustuSurum: '1.3',
    tarih: '29 Ağustos 2026',
    ozet: 'Türkçe arayüzde yazıyı büyütünce sayfa yana kayıyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      '<b>Türkçe kullanıyorsan ve yazıları büyüttüysen</b>, sayfa yana '
        + 'kayıyor ve içerik ekranın dışına taşıyordu. Küçük telefonlarda '
        + 'daha belirgindi. Artık taşma yok.',
      'Sebep, Türkçe yazıların daha uzun olmasıydı — aynı ekran '
        + 'İngilizcede sorunsuz görünüyordu. Bundan sonra dar ekran '
        + '<b>iki dilde birden</b> ölçülüyor.',
    ],
    ozetEn: 'With the Turkish interface and larger text, the page '
        + 'scrolled sideways.',
    tarihEn: '29 August 2026',
    maddelerEn: [
      '<b>If you use Turkish and have made text larger</b>, the page '
        + 'scrolled sideways and content ran off the screen — more so on '
        + 'small phones. That is fixed.',
      'The cause was that Turkish text is longer: the same screen looked '
        + 'fine in English. Narrow screens are now measured in <b>both '
        + 'languages</b>.',
    ],
  },
  {
    surum: 139,
    masaustuSurum: '1.3',
    tarih: '29 Ağustos 2026',
    ozet: 'Yazıyı büyütenlerde “ekran birazdan kararacak” uyarısı '
        + 'ekranın dışına taşıyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      'Yazıları büyüttüysen, molaya az kala çıkan <b>“ekran birazdan '
        + 'kararacak”</b> uyarısı balonun ve ekranın dışına taşıyor, '
        + 'yani <b>tam okunamıyordu</b>. Yazı artık satır atlayarak '
        + 'balonun içinde kalıyor.',
      'Bu uyarı, uygulamanın asıl işi. Yazıyı büyüten kişi çoğu zaman '
        + 'tam da <b>görmekte zorlanan</b> kişi — o yüzden bunu bir '
        + 'görünüm ayrıntısı değil, <b>işlev</b> olarak ele aldık.',
    ],
    ozetEn: 'For people using larger text, the “the screen is about to '
        + 'go dark” warning ran off the screen.',
    tarihEn: '29 August 2026',
    maddelerEn: [
      'If you use larger text, the <b>“the screen is about to go '
        + 'dark”</b> warning shown shortly before a break ran outside '
        + 'the bubble and off the screen, so it <b>could not be read in '
        + 'full</b>. The text now wraps and stays inside the bubble.',
      'That warning is the app\u2019s core job. Someone who enlarges '
        + 'text is often exactly the person who <b>has trouble '
        + 'seeing</b> — so we treated this as <b>function</b>, not as a '
        + 'visual detail.',
    ],
  },
  {
    surum: 137,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'Telefonun “yazıları büyüt” ayarı artık uygulamayı da büyütüyor.',
    ayarGozdenGecir: false,
    maddeler: [
      'Telefonunda ya da bilgisayarında <b>yazıları büyüttüysen</b>, bu '
        + 'uygulama onu <b>dinlemiyordu</b>: yazılar sabit boyuttaydı. '
        + 'Göz için yapılmış bir uygulamada bu ters bir durumdu. Artık '
        + 'bütün yazılar senin ayarınla birlikte büyüyor.',
      'Görünüm <b>aynı kaldı</b>: normal boyutta ekrandaki her ögenin '
        + 'yazı boyu, genişliği, yüksekliği ve yeri tek tek ölçülüp '
        + 'karşılaştırıldı — hiçbiri değişmedi.',
    ],
    ozetEn: 'Your device\u2019s “larger text” setting now enlarges the app '
        + 'as well.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'If you have made <b>text larger</b> on your phone or computer, this '
        + 'app <b>was not listening</b>: its text stayed at a fixed size. '
        + 'That was backwards for an app made for your eyes. All text now '
        + 'grows together with your setting.',
      'The appearance is <b>unchanged</b>: at normal size, every element '
        + 'on screen had its text size, width, height and position '
        + 'measured and compared one by one — none of them moved.',
    ],
  },
  {
    surum: 136,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'Konum izni reddedilince çıkan yazı İngilizce arayüzde Türkçe '
        + 'kalıyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      'İngilizce kullananlar için: <b>konum izni reddedildiğinde</b> çıkan '
        + 'yazı Türkçe kalıyordu — hem de tam kafa karıştıran anda. '
        + 'Konum ve hava durumuyla ilgili bütün yazılar çevrildi.',
      'O yazı artık <b>iki yolu birden</b> söylüyor: aşağıdan şehir '
        + 'arayabilirsin, ya da adres çubuğundaki kilit simgesinden konuma '
        + 'izin verebilirsin.',
    ],
    ozetEn: 'The message shown when location permission is denied stayed '
        + 'in Turkish in the English interface.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'For people using English: the message shown when <b>location '
        + 'permission is denied</b> stayed in Turkish — at exactly the '
        + 'confusing moment. All location and weather texts are now '
        + 'translated.',
      'That message now offers <b>both ways out</b>: search for a city '
        + 'below, or allow location from the padlock icon in the address '
        + 'bar.',
    ],
  },
  {
    surum: 135,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'İngilizce arayüzde Türkçe kalan dört yazı daha; paylaşımın '
        + 'son çaresi artık sessizce kaybolmuyor.',
    ayarGozdenGecir: false,
    maddeler: [
      'İngilizce kullananlar için: <b>cihaz etkinliği izninin üç '
        + 'durumu</b> ve tanıtımdaki örnek mola yazısı Türkçe kalıyordu. '
        + 'Dördü de çevrildi.',
      '<b>Paylaş</b> düğmesi: telefon paylaşım penceresi yoksa ve panoya '
        + 'kopyalama da engellenmişse, uygulama tarayıcının küçük '
        + 'penceresine düşüyordu. Tarayıcılar o pencereyi çoğu zaman '
        + '<b>engelliyor</b> ve o zaman ekranda hiçbir şey olmuyordu. '
        + 'Artık link <b>uygulamanın kendi kutusunda</b> görünüyor, '
        + 'seçili hâlde.',
      'Cihaz etkinliği izni reddedildiğinde artık <b>ne kaybettiğin</b> '
        + 'de yazıyor — eskiden yalnızca nasıl geri açılacağı yazıyordu.',
    ],
    ozetEn: 'Four more texts that stayed in Turkish in the English '
        + 'interface; the share fallback no longer disappears silently.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'For people using English: the <b>three states of the device '
        + 'activity permission</b> and the sample-break text in the '
        + 'introduction stayed in Turkish. All four are now translated.',
      'The <b>Share</b> button: when the phone share sheet is missing and '
        + 'copying to the clipboard is blocked too, the app fell back to '
        + 'the browser\u2019s small dialog. Browsers <b>block</b> that '
        + 'dialog in many situations, and then nothing at all appeared. '
        + 'The link is now shown <b>inside the app</b>, already selected.',
      'When the device activity permission is denied, the app now also '
        + 'says <b>what you lose</b> — previously it only said how to '
        + 'turn it back on.',
    ],
  },
  {
    surum: 134,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: '“Hepsini sil” geçmişi silmiyordu — silindikten sonra ekranda '
        + 'eski sayılar duruyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      '<b>“Verileri sıfırla”</b> yalnızca ayarları ve bugünün sayaçlarını '
        + 'siliyordu; <b>7 günlük geçmiş ve seri cihazda kalıyordu</b>. '
        + 'Silme sonrası sayaç 0 gösteriyor ama ekranda hâlâ “8 mola '
        + 'bugün” yazıyor, grafikte çubuk duruyor ve seri rozeti '
        + 'görünüyordu. Artık gerçekten hepsi siliniyor.',
      'Silme artık <b>tek tek anahtar saymıyor</b>: uygulamanın bütün '
        + 'kayıtları kuralla temizleniyor, yani sonradan eklenen bir '
        + 'kayıt da kendiliğinden kapsanıyor.',
    ],
    ozetEn: '“Erase all data” did not erase the history — old numbers '
        + 'stayed on screen afterwards.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      '<b>“Reset all data”</b> only cleared the settings and today\u2019s '
        + 'counters; the <b>7-day history and streak stayed on the '
        + 'device</b>. After erasing, the counter showed 0 but the screen '
        + 'still said “8 breaks today”, the bar was still in the chart and '
        + 'the streak badge was still there. Everything is now really '
        + 'erased.',
      'Erasing no longer works from <b>a list of individual keys</b>: all '
        + 'of the app\u2019s records are cleared by rule, so anything '
        + 'added later is covered automatically.',
    ],
  },
  {
    surum: 133,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'Uygulamayı iki sekmede açtığında iki sayaç birden işliyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      'Uygulamayı <b>iki sekmede</b> açtığında ikinci sekme “burada '
        + 'devam et” yazısını gösteriyor ama <b>kendi sayacını da '
        + 'işletiyordu</b>. İki pencere <b>farklı süreler</b> gösteriyor, '
        + 'ikisi de ayrı ayrı mola veriyordu. Artık yalnızca bir sekme '
        + 'sayar; ötekinin sayacı durur.',
      'Sayan sekmeyi kapatırsan ya da öteki sekmede <b>“burada devam et”</b> '
        + 'dersen, sayaç <b>kaldığı yerden</b> orada sürer.',
    ],
    ozetEn: 'Opening the app in two tabs ran two timers at once.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'When the app was open in <b>two tabs</b>, the second tab showed the '
        + '“use here” notice but <b>also kept running its own timer</b>. '
        + 'The two windows showed <b>different times</b> and each gave its '
        + 'own breaks. Now only one tab counts; the other one stops.',
      'If you close the counting tab, or press <b>“Use here”</b> in the '
        + 'other one, the timer <b>carries on where it left off</b> there.',
    ],
  },
  {
    surum: 132,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'Erken uyarı ayarı, belirli bir kombinasyonda sessizce kapanıyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      'Çalışma aralığını <b>1 dakikaya</b>, erken uyarıyı <b>en yükseğe '
        + '(60 sn)</b> alırsan uyarı sessizce <b>kapanıyordu</b>: ayar '
        + 'ekranı 60 gösteriyor, ama hiç uyarı gelmiyordu. Artık uyarı '
        + 'kapanmıyor, çalışma aralığının hemen altına çekiliyor.',
      'Uyarıyı <b>kendin sıfıra çektiysen</b> ya da Toplantı / Film '
        + 'kipindeysen sıfır olduğu gibi kalır — orada sıfır zaten '
        + '“uyarma” demek.',
    ],
    ozetEn: 'The advance-warning setting switched itself off silently in '
        + 'one particular combination.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'If you set the work interval to <b>1 minute</b> and the advance '
        + 'warning to its <b>maximum (60 s)</b>, the warning was silently '
        + '<b>turned off</b>: the settings screen showed 60, but no '
        + 'warning ever came. The warning is no longer switched off; it '
        + 'is brought just under the work interval instead.',
      'If you set the warning to zero <b>yourself</b>, or you are in '
        + 'Meeting / Film mode, zero stays as it is — there zero already '
        + 'means “do not warn”.',
    ],
  },
  {
    surum: 131,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'İngilizce arayüzde Türkçe kalan altı yazı çevrildi.',
    ayarGozdenGecir: false,
    maddeler: [
      'İngilizce kullananlar için: uygulamanın <b>altı yazısı Türkçe '
        + 'kalıyordu</b> — titreşim ve canlılık desteklenmediğinde çıkan '
        + 'uyarılar, rehber yüklenemediğinde çıkan not, kurulum ipucu ve '
        + 'egzersiz bölümünün açıklaması. Hepsi çevrildi.',
      'Bunlar göze çarpmıyordu çünkü her biri <b>yalnızca belirli bir '
        + 'durumda</b> ekrana geliyor. Artık bir denetim, çevrilmesi '
        + 'gereken her yazının sözlükte olduğunu <b>tek tek değil '
        + 'topluca</b> ölçüyor.',
    ],
    ozetEn: 'Six pieces of text that stayed in Turkish in the English '
        + 'interface are now translated.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'For people using English: <b>six pieces of text stayed in '
        + 'Turkish</b> — the notices shown when vibration or the vividness '
        + 'setting is unsupported, the note shown when the guide fails to '
        + 'load, the install hint, and the description of the exercises '
        + 'section. All are now translated.',
      'These went unnoticed because each one only appears in <b>a '
        + 'particular state</b>. A check now verifies that every text '
        + 'needing translation is in the dictionary — <b>as a rule, not '
        + 'a list</b>.',
    ],
  },
  {
    surum: 130,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'Yan yana duran iki sayı birbirini yalanlıyordu; sebebi artık '
        + 'ekranda yazıyor. Bir de yanlış cümle düzeltildi.',
    ayarGozdenGecir: false,
    maddeler: [
      '“Tamamlanan mola” ile “bu sekmede geçen süre” <b>aynı şeyi '
        + 'ölçmüyor</b>: molalar saate göre gelir (uygulama kapalıyken de '
        + 'süre işler), süre ise yalnız uygulama açıkken sayılır. Yan yana '
        + 'durunca “3 mola ama 9 dakika” gibi <b>imkânsız görünen</b> bir '
        + 'tablo çıkıyordu. Artık fark büyüdüğünde sebebi ekranda yazıyor.',
      'Mola ekranı açıkken uygulamadan ayrılınca çıkan yazı “o molayı '
        + 'verilmiş saydık” diyordu. <b>Doğru değildi</b> — o mola '
        + 'sayılmıyor. Yazı artık ne olduğunu doğru söylüyor.',
      'Bilgi ekranı “5 egzersiz” yazıp beşini listeliyordu; molalarda '
        + '<b>yalnızca dördü çıkabiliyordu</b>. Liste artık gerçekten '
        + 'çıkanlardan üretiliyor.',
    ],
    ozetEn: 'Two numbers shown side by side contradicted each other; the '
        + 'reason is now stated on screen. A false message was also fixed.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      '“Breaks completed” and “time in this tab” <b>do not measure the '
        + 'same thing</b>: breaks are timed by the clock (time passes even '
        + 'while the app is closed), while the duration only counts while '
        + 'the app is open. Side by side this produced <b>impossible '
        + 'looking</b> figures such as “3 breaks but 9 minutes”. When the '
        + 'gap is large, the reason is now shown on screen.',
      'The message shown after leaving while the break screen was open '
        + 'said “we counted that break as taken”. That was <b>not true</b> '
        + '— the break is not counted. The message now says what actually '
        + 'happened.',
      'The info screen said “5 exercises” and listed five, but <b>only '
        + 'four could ever appear</b> in breaks. The list is now derived '
        + 'from the ones that actually appear.',
    ],
  },
  {
    surum: 126,
    masaustuSurum: '1.3',
    tarih: '28 Ağustos 2026',
    ozet: 'Telefonda sayacın hâlâ sıfırlanmasına yol açan hata düzeltildi — '
        + 'önceki düzeltme yalnızca yeni kurulumlara ulaşıyordu.',
    ayarGozdenGecir: false,
    maddeler: [
      'Telefonda sayaç sıfırlanmasın diye getirdiğimiz ayar, <b>zaten '
        + 'uygulamayı kullananlara ulaşmıyordu</b>: ayar bir kez cihazına '
        + 'kaydedildiği için yeni varsayılan onu değiştiremiyordu. Artık '
        + 'telefonda bir kereye mahsus yeni davranışa geçiliyor.',
      'Bu ayarı <b>kendin değiştirdiysen dokunulmuyor</b> — seçimin '
        + 'korunuyor. “Uzun süre uzak kalınca sayacı sıfırla” ayarından '
        + 'her zaman geri alabilirsin.',
      'Mola ekranının alt kenarı telefonda tarayıcı mesajı ve gezinti '
        + 'çubuğu tarafından örtülüyordu; kaynak satırı okunmuyordu. '
        + 'Artık altta yer bırakılıyor.',
      'Sayfanın altında artık <b>sürüm numarası</b> yazıyor — bir sorun '
        + 'bildirirken hangi sürümde olduğunu söyleyebilirsin.',
      'Kayıt yapılamadığında (depolama doluysa) uygulama artık bunu '
        + 'söylüyor. Eskiden sessizce kaydetmiyordu.',
    ],
    ozetEn: 'Fixed a fault that still reset the timer on phones — the '
        + 'earlier fix only reached fresh installations.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'The setting that stops the timer resetting on phones <b>was not '
        + 'reaching people who already used the app</b>: once saved to the '
        + 'device, the new default could not change it. Phones now switch '
        + 'over once.',
      'If you changed this setting yourself, it is <b>left alone</b> — your '
        + 'choice is kept. You can always change it back under “Reset the '
        + 'timer after a long absence”.',
      'The bottom of the break screen was covered by the browser message '
        + 'and the navigation bar on phones, hiding the source line. There '
        + 'is now room for them.',
      'The page footer now shows a <b>version number</b>, so you can say '
        + 'which version you are on when reporting a problem.',
      'When saving fails (for example if storage is full) the app now says '
        + 'so. It used to fail silently.',
    ],
  },
  {
    surum: 111,
    masaustuSurum: '1.2',
    tarih: '28 Ağustos 2026',
    ozet: 'Telefonda sayaç artık her dönüşte baştan başlamıyor ve mola '
        + 'geri tuşuyla kazayla kapanmıyor.',
    // İki yeni ayar AÇIK geliyor; davranış değiştiği için anlatılmalı.
    ayarGozdenGecir: false,
    maddeler: [
      'Telefonda başka uygulamaya geçip dönünce sayaç <b>baştan '
        + 'başlıyordu</b>. Molanın düştüğü andan sonra bir dakika içinde '
        + 'dönmediysen sayaç sıfırlanıyordu — telefonda bu neredeyse hiç '
        + 'tutmaz. Artık molan seni bekliyor.',
      '<b>Yeni ayar:</b> “Uzun süre uzak kalınca sayacı sıfırla”. '
        + '<b>Telefonda kapalı</b>, bilgisayarda açık geliyor. Sebebi: '
        + 'telefonda başka uygulamaya geçmek ekrandan kalkmak değildir, '
        + 'hâlâ ekrana bakıyorsundur. İstediğin gibi değiştirebilirsin.',
      '<b>Yeni ayar:</b> “Molada kazayla çıkmayı önle”. Açık geliyor. '
        + 'Mola sürerken geri tuşu molayı bitirmiyor. Seni kilitlemez: '
        + 'Esc her zaman çıkarır ve molayı yine atlayabilirsin.',
      'Sayaç sıfırlandığında artık <b>nedenini söylüyor</b>. Eskiden '
        + 'sessizce başa dönüyordu ve bozuk gibi duruyordu.',
      'Cihazın saati değişince (yaz saati ya da elle ayar) uygulama '
        + '“kapalıydın” diyordu — oysa hiç ayrılmamış olabilirsin. Artık '
        + 'saat değişimini ayırt ediyor.',
      'Bildirime izin verilmediğinde ekran artık <b>ne kaybettiğini ve '
        + 'nasıl geri alacağını</b> yazıyor.',
      'Arka planda çalışma sözü <b>küçültüldü</b>: telefonda tarayıcı '
        + 'sayfayı uyutabilir ve mola uyarısı gelmeyebilir. Gelmeyecek bir '
        + 'uyarıyı vaat etmektense sınırı yazmayı seçtik.',
      'Gizli sekmede uygulamanın <b>hiç açılmamasına</b> yol açabilecek '
        + 'bir hata kapatıldı.',
    ],
    ozetEn: 'On phones the timer no longer restarts every time you come '
        + 'back, and the back button no longer ends a break by accident.',
    tarihEn: '28 August 2026',
    maddelerEn: [
      'On phones, switching to another app and coming back <b>restarted '
        + 'the timer</b>. Unless you returned within one minute of the '
        + 'break falling due, it reset — which almost never happens on a '
        + 'phone. Your break now waits for you.',
      '<b>New setting:</b> “Reset the timer after a long absence”. '
        + '<b>Off by default on phones</b>, on by default on computers. '
        + 'The reason: on a phone, switching to another app is not the '
        + 'same as looking away from a screen. You can change it.',
      '<b>New setting:</b> “Prevent leaving the break by accident”. On by '
        + 'default. The back button no longer ends a break. It does not '
        + 'lock you in: Esc always exits and you can still skip the break.',
      'When the timer does reset, it now <b>says why</b>. It used to go '
        + 'back to the start silently, which looked like a fault.',
      'When the device clock changed (daylight saving or a manual '
        + 'adjustment) the app claimed you had been away. It now tells '
        + 'the difference.',
      'When notifications are refused, the screen now says <b>what you '
        + 'lose and how to allow them again</b>.',
      'The background promise was <b>made smaller</b>: on a phone the '
        + 'browser may suspend the page and the break alert may not '
        + 'arrive. We would rather state the limit than promise an alert '
        + 'that never comes.',
      'Fixed a fault that could stop the app opening at all in a private '
        + 'window.',
    ],
  },
  {
    surum: 93,
    /* Masaustu AYRI surumleniyor: web damga sayiyor (93), masaustu
       anlamli surum kullaniyor. Ikisi ayni artifakt degil, ayni anda
       da cikmiyorlar. Tek anahtar tutmak, birinde bildirimin SESSIZCE
       hic cikmamasi demekti - bu tam olarak boyle yakalandi:
       `son("1.1")` None donuyordu.
       v1.1 henuz yayinlanmadi; bugunku isler onun icinde cikacak. */
    masaustuSurum: '1.1',
    tarih: '28 Ağustos 2026',
    ozet: 'Aile kipinde korumanın sessizce devre dışı kalabildiği yedi durum düzeltildi.',
    ozetEn: 'Fixed seven cases where Family mode protection could switch off silently.',
    tarihEn: '28 August 2026',
    // Ebeveynin ayarını yeniden gözden geçirmesi gereken sürüm
    ayarGozdenGecir: true,
    maddeler: [
      'Aile kipi: çocuğun kayıt dosyasını düzenleyerek günlük süre ' +
        'sınırını kaldırabildiği yol kapatıldı. Süre artık gün içinde ' +
        'geri gidemiyor; denenirse ekranda yazıyor.',
      'Aile kipi: “kip açık ama şifre yok”, “sınır negatif”, “ek süre ' +
        'çok ileri bir tarihe kurulmuş” gibi durumlarda koruma sessizce ' +
        'kalkıyordu. Artık uyarı çıkıyor.',
      'Aile kipi: ayar ekranında artık neyin garanti olduğu VE neyin ' +
        'olmadığı yazıyor — ayar dosyası silinirse kipin kalkacağı dahil.',
      'Windows ile tarayıcı sürümü aynı sayacı paylaşıyor: birinde ' +
        '8 dakika kalmışken diğerini açınca süre baştan başlamıyor.',
      'Bilgisayardan kalktığınızda tarayıcı sürümünün sahte mola ' +
        'vermesine yol açan hata düzeltildi.',
      'Uzun mola: iki saat aralıksız çalışınca öneri geliyor. Ayar ' +
        'açıktı ama çalışmıyordu.',
      '“5 dakika duraklat” gerçekten 5 dakika: sekmeyi kapatıp ' +
        'dönseniz de süre işliyor. Önceden kalıcı olarak duraklıyordu.',
      'İngilizce sürümde Türkçe kalan metinler çevrildi — mola ' +
        'ekranındaki egzersiz yönergesi dahil.',
      'Panelde “koruma uygulanmıyor” uyarıları artık ekrana sığıyor; ' +
        'bir kısmı kenardan taşıyordu.',
    ],
maddelerEn: [
      'Family mode: closed a way a child could lift the daily time '
        + 'limit by editing the saved file. Time can no longer run '
        + 'backwards during the day; if it is attempted, the screen says so.',
      'Family mode: protection used to switch off silently in cases '
        + 'like “mode on but no password”, “negative limit”, or “extra '
        + 'time set to a date far in the future”. A warning now appears.',
      'Family mode: the settings screen now states what is guaranteed '
        + 'AND what is not — including that deleting the settings file '
        + 'turns the mode off.',
      'The Windows and browser versions share one timer: with 8 minutes '
        + 'left in one, opening the other no longer restarts the countdown.',
      'Fixed a bug that made the browser version fire false breaks after '
        + 'you stepped away from the computer.',
      'Long break: a suggestion now appears after two hours of '
        + 'uninterrupted work. The setting was on but did nothing.',
      '“Pause 5 minutes” really is 5 minutes: the clock keeps running '
        + 'even if you close the tab and come back. It used to pause forever.',
      'Text left in Turkish in the English version was translated — '
        + 'including the exercise instruction on the break screen.',
      'The “protection not applied” warnings in the panel now fit on '
        + 'screen; some were overflowing the edge.',
    ],
  },
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DEGISIKLIKLER };
}
