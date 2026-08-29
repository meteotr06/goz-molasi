# -*- coding: utf-8 -*-
"""ÜRETİLMİŞ DOSYA — degisiklikler.js'ten.

ELLE DÜZENLEME. Değişiklik metnini `degisiklikler.js` içinde
değiştir, sonra `python masaustu/degisiklikler_uret.py` çalıştır.
"""

DEGISIKLIKLER = [
    {
        'surum': 147,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Sayılar artık Türkçe yazımıyla: “6,7” ve “1.433 dk”.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Haftalık özette “günde ortalama <b>6.7</b>” yazıyordu — Türkçede ondalık ayırıcı virgüldür. Artık <b>6,7</b>.',
            'Uzun süreler ayırıcısız yazılıyordu (“1433 dk”). Artık <b>1.433 dk</b>. İngilizce arayüzde de kendi yazımıyla: “1,433 min”.',
            'Sayı doğruydu, <b>yazımı yanlıştı</b> — ve yanlış okunan doğru sayı, yanlış sayıdır.',
        ],
    },
    {
        'surum': 146,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Kayıtlı verin bozulursa ekranda anlamsız sayılar görünebiliyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Tarayıcının sakladığı veri bozulursa (yarım yazma, eski sürüm, elle kurcalama) mola sayın <b>“cok”</b> ya da <b>“-3”</b> gibi görünebiliyordu. Artık bozuk değerler <b>0</b> olarak gösteriliyor — uygulama açılıyor ve doğru saymaya devam ediyor.',
            'Ayarlar bu süzgeçten zaten geçiyordu; <b>sayaçlar geçmiyordu</b>. İkisi de aynı korumayı kullanıyor artık.',
        ],
    },
    {
        'surum': 144,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': '“Hepsini sil”, uygulama başka bir sekmede de açıkken tutmuyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Uygulamayı <b>iki sekmede birden</b> açtıysan ve birinde “hepsini sil” dediysen, veriler siliniyor ama <b>öteki sekme kendi belleğindekini geri yazıyordu</b>. Sayaçların ve bütün ayarların birkaç saniye içinde geri geliyordu.',
            'Artık silme, açık olan bütün sekmelere bildiriliyor: hepsi yazmayı durdurup temiz başlıyor. <b>Sildiğin gerçekten siliniyor.</b>',
        ],
    },
    {
        'surum': 142,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Uzun molada ayağa kalkmaya davet, ve oturmak üzerine kaynaklı bir bilgi kartı.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            '<b>Uzun molada</b> (iki saat aralıksız çalıştıktan sonra) tek satır ekledik: “istersen ayağa kalk, biraz hareket et.” Bir davet — <b>zorunluluk değil</b>, süre şartı yok.',
            '<b>20 dakikalık molalar değişmedi.</b> Onların işi gözünü dinlendirmek; oraya ikinci bir amaç koymak asıl işi zayıflatırdı.',
            'Yeni bilgi kartı: <b>oturmakla ilgili sayılar</b>. NHS 30 dakikada bir kalkmayı öneriyor ama aynı sayfada “sınır koyacak kadar kanıt yok” diyor; Dünya Sağlık Örgütü hiç süre vermiyor. Kartta ikisi de yazıyor — <b>öneriyi kural gibi göstermiyoruz</b>.',
        ],
    },
    {
        'surum': 141,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Ekrandaki bir sağlık bilgisi, dayandığı kaynağın söylediğinden farklıydı.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            '“2 saat eşiği” bilgi kartı, Amerikan Optometri Birliği’ne dayandırılıyordu ama <b>Birliğin söylediğinden farklı bir şey</b> yazıyordu. Kaynak “en yüksek risk <b>iki saat ve üzeri</b> kesintisiz kullananlarda” diyor; kart ise “risk 2 saati <b>aşınca başlıyor</b>” diyordu. Kartın metni kaynağa uyduruldu.',
            'Kaynağın <b>adını yazıyorsak</b>, söylediğini de doğru aktarmamız gerekir. Bu yazı Türkçe, İngilizce ve Windows sürümünde ayrı ayrı duruyordu; üçü de düzeltildi.',
        ],
    },
    {
        'surum': 140,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Türkçe arayüzde yazıyı büyütünce sayfa yana kayıyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            '<b>Türkçe kullanıyorsan ve yazıları büyüttüysen</b>, sayfa yana kayıyor ve içerik ekranın dışına taşıyordu. Küçük telefonlarda daha belirgindi. Artık taşma yok.',
            'Sebep, Türkçe yazıların daha uzun olmasıydı — aynı ekran İngilizcede sorunsuz görünüyordu. Bundan sonra dar ekran <b>iki dilde birden</b> ölçülüyor.',
        ],
    },
    {
        'surum': 139,
        'tarih': '29 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Yazıyı büyütenlerde “ekran birazdan kararacak” uyarısı ekranın dışına taşıyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Yazıları büyüttüysen, molaya az kala çıkan <b>“ekran birazdan kararacak”</b> uyarısı balonun ve ekranın dışına taşıyor, yani <b>tam okunamıyordu</b>. Yazı artık satır atlayarak balonun içinde kalıyor.',
            'Bu uyarı, uygulamanın asıl işi. Yazıyı büyüten kişi çoğu zaman tam da <b>görmekte zorlanan</b> kişi — o yüzden bunu bir görünüm ayrıntısı değil, <b>işlev</b> olarak ele aldık.',
        ],
    },
    {
        'surum': 137,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Telefonun “yazıları büyüt” ayarı artık uygulamayı da büyütüyor.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Telefonunda ya da bilgisayarında <b>yazıları büyüttüysen</b>, bu uygulama onu <b>dinlemiyordu</b>: yazılar sabit boyuttaydı. Göz için yapılmış bir uygulamada bu ters bir durumdu. Artık bütün yazılar senin ayarınla birlikte büyüyor.',
            'Görünüm <b>aynı kaldı</b>: normal boyutta ekrandaki her ögenin yazı boyu, genişliği, yüksekliği ve yeri tek tek ölçülüp karşılaştırıldı — hiçbiri değişmedi.',
        ],
    },
    {
        'surum': 136,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Konum izni reddedilince çıkan yazı İngilizce arayüzde Türkçe kalıyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'İngilizce kullananlar için: <b>konum izni reddedildiğinde</b> çıkan yazı Türkçe kalıyordu — hem de tam kafa karıştıran anda. Konum ve hava durumuyla ilgili bütün yazılar çevrildi.',
            'O yazı artık <b>iki yolu birden</b> söylüyor: aşağıdan şehir arayabilirsin, ya da adres çubuğundaki kilit simgesinden konuma izin verebilirsin.',
        ],
    },
    {
        'surum': 135,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'İngilizce arayüzde Türkçe kalan dört yazı daha; paylaşımın son çaresi artık sessizce kaybolmuyor.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'İngilizce kullananlar için: <b>cihaz etkinliği izninin üç durumu</b> ve tanıtımdaki örnek mola yazısı Türkçe kalıyordu. Dördü de çevrildi.',
            '<b>Paylaş</b> düğmesi: telefon paylaşım penceresi yoksa ve panoya kopyalama da engellenmişse, uygulama tarayıcının küçük penceresine düşüyordu. Tarayıcılar o pencereyi çoğu zaman <b>engelliyor</b> ve o zaman ekranda hiçbir şey olmuyordu. Artık link <b>uygulamanın kendi kutusunda</b> görünüyor, seçili hâlde.',
            'Cihaz etkinliği izni reddedildiğinde artık <b>ne kaybettiğin</b> de yazıyor — eskiden yalnızca nasıl geri açılacağı yazıyordu.',
        ],
    },
    {
        'surum': 134,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': '“Hepsini sil” geçmişi silmiyordu — silindikten sonra ekranda eski sayılar duruyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            '<b>“Verileri sıfırla”</b> yalnızca ayarları ve bugünün sayaçlarını siliyordu; <b>7 günlük geçmiş ve seri cihazda kalıyordu</b>. Silme sonrası sayaç 0 gösteriyor ama ekranda hâlâ “8 mola bugün” yazıyor, grafikte çubuk duruyor ve seri rozeti görünüyordu. Artık gerçekten hepsi siliniyor.',
            'Silme artık <b>tek tek anahtar saymıyor</b>: uygulamanın bütün kayıtları kuralla temizleniyor, yani sonradan eklenen bir kayıt da kendiliğinden kapsanıyor.',
        ],
    },
    {
        'surum': 133,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Uygulamayı iki sekmede açtığında iki sayaç birden işliyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Uygulamayı <b>iki sekmede</b> açtığında ikinci sekme “burada devam et” yazısını gösteriyor ama <b>kendi sayacını da işletiyordu</b>. İki pencere <b>farklı süreler</b> gösteriyor, ikisi de ayrı ayrı mola veriyordu. Artık yalnızca bir sekme sayar; ötekinin sayacı durur.',
            'Sayan sekmeyi kapatırsan ya da öteki sekmede <b>“burada devam et”</b> dersen, sayaç <b>kaldığı yerden</b> orada sürer.',
        ],
    },
    {
        'surum': 132,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Erken uyarı ayarı, belirli bir kombinasyonda sessizce kapanıyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Çalışma aralığını <b>1 dakikaya</b>, erken uyarıyı <b>en yükseğe (60 sn)</b> alırsan uyarı sessizce <b>kapanıyordu</b>: ayar ekranı 60 gösteriyor, ama hiç uyarı gelmiyordu. Artık uyarı kapanmıyor, çalışma aralığının hemen altına çekiliyor.',
            'Uyarıyı <b>kendin sıfıra çektiysen</b> ya da Toplantı / Film kipindeysen sıfır olduğu gibi kalır — orada sıfır zaten “uyarma” demek.',
        ],
    },
    {
        'surum': 131,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'İngilizce arayüzde Türkçe kalan altı yazı çevrildi.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'İngilizce kullananlar için: uygulamanın <b>altı yazısı Türkçe kalıyordu</b> — titreşim ve canlılık desteklenmediğinde çıkan uyarılar, rehber yüklenemediğinde çıkan not, kurulum ipucu ve egzersiz bölümünün açıklaması. Hepsi çevrildi.',
            'Bunlar göze çarpmıyordu çünkü her biri <b>yalnızca belirli bir durumda</b> ekrana geliyor. Artık bir denetim, çevrilmesi gereken her yazının sözlükte olduğunu <b>tek tek değil topluca</b> ölçüyor.',
        ],
    },
    {
        'surum': 130,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Yan yana duran iki sayı birbirini yalanlıyordu; sebebi artık ekranda yazıyor. Bir de yanlış cümle düzeltildi.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            '“Tamamlanan mola” ile “bu sekmede geçen süre” <b>aynı şeyi ölçmüyor</b>: molalar saate göre gelir (uygulama kapalıyken de süre işler), süre ise yalnız uygulama açıkken sayılır. Yan yana durunca “3 mola ama 9 dakika” gibi <b>imkânsız görünen</b> bir tablo çıkıyordu. Artık fark büyüdüğünde sebebi ekranda yazıyor.',
            'Mola ekranı açıkken uygulamadan ayrılınca çıkan yazı “o molayı verilmiş saydık” diyordu. <b>Doğru değildi</b> — o mola sayılmıyor. Yazı artık ne olduğunu doğru söylüyor.',
            'Bilgi ekranı “5 egzersiz” yazıp beşini listeliyordu; molalarda <b>yalnızca dördü çıkabiliyordu</b>. Liste artık gerçekten çıkanlardan üretiliyor.',
        ],
    },
    {
        'surum': 126,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.3',
        'ozet': 'Telefonda sayacın hâlâ sıfırlanmasına yol açan hata düzeltildi — önceki düzeltme yalnızca yeni kurulumlara ulaşıyordu.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Telefonda sayaç sıfırlanmasın diye getirdiğimiz ayar, <b>zaten uygulamayı kullananlara ulaşmıyordu</b>: ayar bir kez cihazına kaydedildiği için yeni varsayılan onu değiştiremiyordu. Artık telefonda bir kereye mahsus yeni davranışa geçiliyor.',
            'Bu ayarı <b>kendin değiştirdiysen dokunulmuyor</b> — seçimin korunuyor. “Uzun süre uzak kalınca sayacı sıfırla” ayarından her zaman geri alabilirsin.',
            'Mola ekranının alt kenarı telefonda tarayıcı mesajı ve gezinti çubuğu tarafından örtülüyordu; kaynak satırı okunmuyordu. Artık altta yer bırakılıyor.',
            'Sayfanın altında artık <b>sürüm numarası</b> yazıyor — bir sorun bildirirken hangi sürümde olduğunu söyleyebilirsin.',
            'Kayıt yapılamadığında (depolama doluysa) uygulama artık bunu söylüyor. Eskiden sessizce kaydetmiyordu.',
        ],
    },
    {
        'surum': 111,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.2',
        'ozet': 'Telefonda sayaç artık her dönüşte baştan başlamıyor ve mola geri tuşuyla kazayla kapanmıyor.',
        'ayar_gozden_gecir': False,
        'maddeler': [
            'Telefonda başka uygulamaya geçip dönünce sayaç <b>baştan başlıyordu</b>. Molanın düştüğü andan sonra bir dakika içinde dönmediysen sayaç sıfırlanıyordu — telefonda bu neredeyse hiç tutmaz. Artık molan seni bekliyor.',
            '<b>Yeni ayar:</b> “Uzun süre uzak kalınca sayacı sıfırla”. <b>Telefonda kapalı</b>, bilgisayarda açık geliyor. Sebebi: telefonda başka uygulamaya geçmek ekrandan kalkmak değildir, hâlâ ekrana bakıyorsundur. İstediğin gibi değiştirebilirsin.',
            '<b>Yeni ayar:</b> “Molada kazayla çıkmayı önle”. Açık geliyor. Mola sürerken geri tuşu molayı bitirmiyor. Seni kilitlemez: Esc her zaman çıkarır ve molayı yine atlayabilirsin.',
            'Sayaç sıfırlandığında artık <b>nedenini söylüyor</b>. Eskiden sessizce başa dönüyordu ve bozuk gibi duruyordu.',
            'Cihazın saati değişince (yaz saati ya da elle ayar) uygulama “kapalıydın” diyordu — oysa hiç ayrılmamış olabilirsin. Artık saat değişimini ayırt ediyor.',
            'Bildirime izin verilmediğinde ekran artık <b>ne kaybettiğini ve nasıl geri alacağını</b> yazıyor.',
            'Arka planda çalışma sözü <b>küçültüldü</b>: telefonda tarayıcı sayfayı uyutabilir ve mola uyarısı gelmeyebilir. Gelmeyecek bir uyarıyı vaat etmektense sınırı yazmayı seçtik.',
            'Gizli sekmede uygulamanın <b>hiç açılmamasına</b> yol açabilecek bir hata kapatıldı.',
        ],
    },
    {
        'surum': 93,
        'tarih': '28 Ağustos 2026',
        'masaustu_surum': '1.1',
        'ozet': 'Aile kipinde korumanın sessizce devre dışı kalabildiği yedi durum düzeltildi.',
        'ayar_gozden_gecir': True,
        'maddeler': [
            'Aile kipi: çocuğun kayıt dosyasını düzenleyerek günlük süre sınırını kaldırabildiği yol kapatıldı. Süre artık gün içinde geri gidemiyor; denenirse ekranda yazıyor.',
            'Aile kipi: “kip açık ama şifre yok”, “sınır negatif”, “ek süre çok ileri bir tarihe kurulmuş” gibi durumlarda koruma sessizce kalkıyordu. Artık uyarı çıkıyor.',
            'Aile kipi: ayar ekranında artık neyin garanti olduğu VE neyin olmadığı yazıyor — ayar dosyası silinirse kipin kalkacağı dahil.',
            'Windows ile tarayıcı sürümü aynı sayacı paylaşıyor: birinde 8 dakika kalmışken diğerini açınca süre baştan başlamıyor.',
            'Bilgisayardan kalktığınızda tarayıcı sürümünün sahte mola vermesine yol açan hata düzeltildi.',
            'Uzun mola: iki saat aralıksız çalışınca öneri geliyor. Ayar açıktı ama çalışmıyordu.',
            '“5 dakika duraklat” gerçekten 5 dakika: sekmeyi kapatıp dönseniz de süre işliyor. Önceden kalıcı olarak duraklıyordu.',
            'İngilizce sürümde Türkçe kalan metinler çevrildi — mola ekranındaki egzersiz yönergesi dahil.',
            'Panelde “koruma uygulanmıyor” uyarıları artık ekrana sığıyor; bir kısmı kenardan taşıyordu.',
        ],
    },
]


def son(surum=None):
    """Verilen sürümün kaydını döndürür; yoksa None."""
    for k in DEGISIKLIKLER:
        if surum is None or k.get('masaustu_surum') == surum:
            return k
    return None
