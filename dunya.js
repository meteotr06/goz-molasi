/* ============================================================
   DÜNYADAN — molalarda gösterilen genel kültür kartları

   NEDEN VAR
   Uygulamanın bütün bilgileri göz sağlığı üzerineydi ve hepsi aynı
   yöne bakıyordu: "ekran gözünü yoruyor". Günde 20-30 mola veren biri
   için bu bir süre sonra tekrara düşüyor ve okunmamaya başlıyor.

   Buradaki kartlar dünyanın her yerinden, her konudan. Amaç molayı
   birkaç saniyeliğine merak edilecek bir şeye çevirmek.

   KURAL — bu dosyaya bilgi eklerken:
     • Kaynağı olacak. Kaynaksız bilgi girilmez.
     • Doğruluğu tartışmalı olan "ilginç bilgi"ler girilmez
       (jilet eriten mide asidi, camın akması, beynin %10'u...).
     • Abartı yok. "İnanılmaz!" değil, ne olduğu yazılır.
     • Tek bir ülkeye/kültüre yığılmaz.

   Göz bilgileri bilgiler.js'te; onlar hâlâ baskın. Bu dosya
   çeşitlilik için, onların yerine geçmek için değil.
   ============================================================ */

const DUNYA = [
  {
    baslik: 'Venüs’te bir gün, bir yıldan uzun',
    metin: 'Venüs kendi ekseninde bir turu 243 Dünya gününde tamamlıyor, '
         + 'Güneş çevresindeki turu ise 225 günde. Yani orada gün, yıldan uzun.',
    kaynak: 'NASA — Venus Fact Sheet',
  },
  {
    baslik: 'Okyanus tabanının çoğu haritalanmadı',
    metin: 'Deniz tabanının modern çözünürlükle haritalanmış kısmı dörtte bir '
         + 'civarında. Ay’ın ve Mars’ın yüzeyini daha ayrıntılı biliyoruz.',
    kaynak: 'Seabed 2030 / NOAA',
  },
  {
    baslik: 'Ahtapotun üç kalbi var',
    metin: 'İkisi solungaçlara kan pompalar, biri vücuda. Yüzerken vücuda '
         + 'pompalayan kalp duruyor — bu yüzden ahtapotlar yüzmek yerine '
         + 'yürümeyi tercih ediyor.',
    kaynak: 'Wells, Journal of Experimental Biology',
  },
  {
    baslik: 'Sahra Çölü, Amazon’u besliyor',
    metin: 'Rüzgâr her yıl Sahra’dan Amazon’a milyonlarca ton toz taşıyor. '
         + 'Bu tozdaki fosfor, yağmurun toprakta yıkadığı besini yerine koyuyor.',
    kaynak: 'NASA Goddard, 2015 uydu ölçümleri',
  },
  {
    baslik: 'Oxford, Aztek İmparatorluğu’ndan eski',
    metin: 'Oxford’da 1096’dan beri ders veriliyor. Aztek İmparatorluğu ise '
         + '1428’de kuruldu. Oxford, Aztekler ortaya çıktığında üç yüz yıllıktı.',
    kaynak: 'University of Oxford — kurumsal tarihçe',
  },
  {
    baslik: 'Ay her yıl uzaklaşıyor',
    metin: 'Ay, Dünya’dan yılda yaklaşık 3,8 cm uzaklaşıyor. Bunu Apollo '
         + 'görevlerinin Ay’a bıraktığı aynalara lazer tutarak ölçüyoruz.',
    kaynak: 'Lunar Laser Ranging, NASA',
  },
  {
    baslik: 'Antarktika bir çöl',
    metin: 'Çölün tanımı sıcaklık değil, yağış: yılda 250 mm’den az. '
         + 'Antarktika bu ölçüte göre dünyanın en büyük çölü.',
    kaynak: 'British Antarctic Survey',
  },
  {
    baslik: 'Vücudundaki bakteri sayısı, hücrelerin kadar',
    metin: 'Uzun süre "10 kat fazla" denirdi. 2016’da yapılan dikkatli sayım '
         + 'oranı yaklaşık 1,3’e 1 buldu — yani neredeyse başa baş.',
    kaynak: 'Sender, Fuchs & Milo, PLOS Biology, 2016',
  },
  {
    baslik: 'Ağaçlar toprak altından haberleşiyor',
    metin: 'Mantar ipliklerinden oluşan ağ, ağaçlar arasında karbon ve besin '
         + 'taşıyor. Gölgede kalan bir fidan, komşusundan şeker alabiliyor.',
    kaynak: 'Simard ve ark., Nature, 1997',
  },
  {
    baslik: 'Yunuslar beyinlerinin yarısıyla uyur',
    metin: 'Bir yarı uyurken diğeri uyanık kalıyor; bir göz de açık kalıyor. '
         + 'Nefes almak için su yüzüne çıkmaları gerektiğinden başka çareleri yok.',
    kaynak: 'Mukhametov, Neuroscience Letters',
  },
  {
    baslik: 'Bal bozulmuyor',
    metin: 'Mısır piramitlerinde bulunan binlerce yıllık bal hâlâ yenebilir '
         + 'durumdaydı. Sebebi: çok az su, yüksek asit ve arıların kattığı '
         + 'hidrojen peroksit.',
    kaynak: 'Smithsonian Magazine / National Honey Board',
  },
  {
    baslik: 'Dünyada yaklaşık 7.000 dil konuşuluyor',
    metin: 'Ama bunların yarısına yakını tehlike altında. Ortalama iki haftada '
         + 'bir dil, son konuşanıyla birlikte kayboluyor.',
    kaynak: 'UNESCO Atlas of the World’s Languages in Danger',
  },
  {
    baslik: 'Güneş ışığı sana 8 dakika önce yola çıktı',
    metin: 'Işık Güneş’ten Dünya’ya 8 dakika 20 saniyede geliyor. Pencereden '
         + 'gördüğün ışık, Güneş’i sekiz dakika önceki hâliyle gösteriyor.',
    kaynak: 'NASA — Sun Fact Sheet',
  },
  {
    baslik: 'Nepal’in bayrağı dörtgen değil',
    metin: 'Dünyada dikdörtgen olmayan tek ulusal bayrak Nepal’inki. İki '
         + 'üçgenin üst üste binmesinden oluşuyor.',
    kaynak: 'Nepal Anayasası, Ek 1',
  },
  {
    baslik: 'Bir kitap yazan en eski isim bir kadın',
    metin: 'Adı bilinen en eski yazar, MÖ 2300’lerde yaşamış Akkadlı rahibe '
         + 'Enheduanna. Tabletlerine adını yazmış — imzalı en eski edebiyat.',
    kaynak: 'British Museum / Penn Museum koleksiyonları',
  },
  {
    baslik: 'Bulutlar hafif değil',
    metin: 'Orta boy bir kümülüs bulutu yaklaşık 500 ton su taşıyor. Havada '
         + 'durmasının sebebi hafiflik değil, damlaların çok küçük olması.',
    kaynak: 'USGS Water Science School',
  },
  {
    baslik: 'Dünyanın en uzun yer adı Yeni Zelanda’da',
    metin: 'Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronuku'
         + 'pokaiwhenuakitanatahu — 85 harf. Maori dilinde, bir tepeyi anlatıyor.',
    kaynak: 'Land Information New Zealand',
  },
  {
    baslik: 'Tuz Roma’da maaş değildi',
    metin: '"Salary" kelimesi tuz anlamına gelen sal’dan geliyor ama askerlerin '
         + 'tuzla ödendiğine dair sağlam bir kanıt yok. Yaygın anlatı, doğrulanmış '
         + 'bir tarih değil.',
    kaynak: 'Oxford English Dictionary — köken notu',
  },
];

if (typeof module !== 'undefined') module.exports = { DUNYA };
