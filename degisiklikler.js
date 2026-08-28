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
