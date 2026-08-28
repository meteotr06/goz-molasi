/* ============================================================
   BİLGİLER — Mola sırasında gösterilen "neden?" kartları
   Her kartın kaynağı var. Uydurma bilgi yok.
   Abartılı sağlık iddiasından kaçınıldı: kanıtı zayıf olan
   yerlerde bunu açıkça yazdık.
   ============================================================ */

const BILGILER = [
  {
    baslik: 'Gözün kırpmayı unutuyor',
    metin: 'Normalde dakikada yaklaşık 15 kez göz kırparsın. Ekrana bakarken bu sayı 5–7’ye düşer. ' +
           'Az kırpmak gözyaşı tabakasını kurutur; yanma, batma ve kuruluk hissi buradan gelir.',
    kaynak: 'American Academy of Ophthalmology, 2024',
  },
  {
    baslik: 'Rakam ne kadar düşüyor?',
    metin: '104 ofis çalışanıyla yapılan klasik bir çalışmada göz kırpma sayısı dinlenirken dakikada 22, ' +
           'kitap okurken 10, ekrana bakarken 7’ye indi.',
    kaynak: 'Tsubota & Nakamori, New England Journal of Medicine, 1993',
  },
  {
    baslik: 'Yalnız değilsin',
    metin: '45 çalışmayı birleştiren bir derlemede, ekran başında çalışanların yaklaşık %66’sı ' +
           'dijital göz yorgunluğu belirtisi bildirdi. En sık üçü: bulanık görme (%34), ' +
           'göz yorgunluğu (%32), sulanma (%31).',
    kaynak: 'Scientific Reports, 2023 (45 çalışma derlemesi)',
  },
  {
    baslik: 'Türkiye’de de yaygın',
    metin: 'Pandemi dönemi ölçümlerinde Türkiye’de dijital göz yorgunluğu görülme oranı yaklaşık %48 çıktı. ' +
           'Sağlık Bakanlığına bağlı hastanelerin hasta bilgilendirme sayfalarında da bu kural öneriliyor.',
    kaynak: 'BMC Public Health, 2024 · T.C. Sağlık Bakanlığı — Diyarbakır Çocuk Hastalıkları Hastanesi hasta bilgilendirme sayfası, 24.08.2023 (Bakanlık genelgesi değil, bağlı bir hastanenin bilgilendirmesi)',
  },
  {
    baslik: 'Neden tam 6 metre?',
    metin: '6 metre, göz hekimliğinde "optik sonsuzluk" sayılır — gerçek sonsuzluktan sadece 0,17 diyoptri uzaktır. ' +
           'Yani oraya baktığında odaklama kasın (siliyer kas) pratikte tamamen gevşer. ' +
           'Daha uzağa bakman ek fayda getirmez.',
    kaynak: 'Standart optometri tanımı — "uzak nokta"',
  },
  {
    baslik: 'Kas kasılı kalıyor',
    metin: 'Yakına uzun süre odaklandığında merceği şekillendiren kas kasılı kalır ve sen uzağa baktığında ' +
           'hemen gevşeyemez. Buna "yakın işe bağlı geçici miyopi" denir: birkaç saniyeliğine uzağın bulanık ' +
           'görünmesinin sebebi budur.',
    kaynak: 'Ciuffreda & Vasudevan, Ophthalmic Physiol Opt, 2008',
  },
  {
    baslik: '2 saat eşiği',
    metin: 'Amerikan Optometri Birliği, en yüksek riskin günde iki saat ve üzeri kesintisiz ekran ' +
           'kullananlarda olduğunu söylüyor. Kuralın orijinal ifadesi: "Her 20 dakikada bir, ' +
           '20 saniye boyunca 20 fit (6 m) uzağa bak."',
    kaynak: 'American Optometric Association (AOA)',
  },
  {
    baslik: 'Dürüst olalım: kanıt ne durumda?',
    metin: '20-20-20 kuralı 1990’larda akılda kalsın diye uydurulmuş bir formül; büyük bir klinik çalışmayla ' +
           'kanıtlanmadı. 2023’teki bir çalışma, hatırlatıcılar çalışırken kuruluk şikâyetlerinin azaldığını ama ' +
           'hatırlatıcı kalkınca bir hafta içinde geri döndüğünü gösterdi. Yani asıl işe yarayan şey: düzenli hatırlatma.',
    kaynak: 'Talens-Estarelles ve ark., Cont Lens Anterior Eye, 2023',
  },
  {
    baslik: 'Belki 10 dakika daha iyi',
    metin: 'Küçük bir çalışmada 20 dakikada bir verilen 20 saniyelik molalar odaklanma kaslarını rahatlatmaya ' +
           'yetmedi; 10 dakikada bir veya kendi isteğine göre verilen molalar daha iyi sonuç verdi. ' +
           'Ayarlardan süreyi 10 dakikaya çekmeyi deneyebilirsin.',
    kaynak: 'Johnson & Rosenfield, Optom Vis Sci, 2023',
  },
  {
    baslik: 'Çocuklar için asıl mesele: dışarısı',
    metin: 'Guangzhou’da 1903 çocukla yapılan 3 yıllık randomize çalışmada, günde 40 dakika ekstra açık hava dersi ' +
           'yeni miyopi görülme oranını %39,5’ten %30,4’e düşürdü. Molalar miyopiyi yavaşlatmıyor — açık hava yavaşlatıyor.',
    kaynak: 'He ve ark., JAMA, 2015',
  },
  {
    baslik: 'Yakın iş ve miyopi',
    metin: '25 bin çocuğu kapsayan bir derlemede yakın iş arttıkça miyopi olasılığı da artıyordu ' +
           '(haftalık her ek "diyoptri-saat" için %2). Bu bir ilişki; tek başına neden-sonuç kanıtı değil.',
    kaynak: 'Huang ve ark., PLOS One, 2015',
  },
  {
    baslik: 'Sadece göz değil',
    metin: 'Cochrane’in 2025 derlemesi, ek molaların bel ağrısı şiddetini azaltabileceğini söylüyor (kanıt düzeyi düşük). ' +
           'Güzel haber: molalar verimini düşürmüyor — daha az süre çalışsan da üretim aynı kalıyor.',
    kaynak: 'Cochrane Database of Systematic Reviews, 2025',
  },
  {
    baslik: 'Ekran gözünü kalıcı bozmaz',
    metin: 'Amerikan Göz Hekimleri Akademisi net: uzun ekran kullanımı gözde kalıcı hasar bırakmıyor. ' +
           'Yaşadığın şey yorgunluk ve kuruluk — rahatsız edici ama geri dönüşlü. Bu yüzden mola işe yarıyor.',
    kaynak: 'American Academy of Ophthalmology, 2024',
  },
  {
    baslik: 'Ekranın konumu da önemli',
    metin: 'Ekranı bir kol boyu uzakta (yaklaşık 60 cm) ve göz hizasının biraz altında tut. ' +
           'Hafif aşağı bakmak göz kapağının yüzeyi daha çok örtmesini sağlar, bu da kurumayı azaltır.',
    kaynak: 'American Academy of Ophthalmology, 2024',
  },
];

/* Mola ekranında gösterilen kısa yönlendirme cümleleri.
   Her molada değişir ki ezber olup görünmez hale gelmesin. */
const MOLA_CUMLELERI = [
  'Pencereden dışarı bak. Uzaktaki bir ağaç, bina ya da gökyüzü.',
  'Odanın en uzak köşesine bak ve birkaç kez göz kırp.',
  'Gözünü kapat, yavaşça nefes al. Kapalı göz de dinlenmedir.',
  'Omuzlarını geriye at, boynunu yavaşça sağa sola çevir.',
  'Bilinçli olarak 10 kez tam göz kırp — kapağı tamamen kapat.',
  'Ayağa kalk. 20 saniye ayakta durmak da sayılır.',
  'Uzaktaki bir noktaya odaklan, sonra parmağına, sonra tekrar uzağa.',
  'Bir yudum su iç. Vücudun susuzken göz de kurur.',
];

if (typeof module !== 'undefined') module.exports = { BILGILER, MOLA_CUMLELERI };
