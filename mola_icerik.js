/* ============================================================
   MOLA İÇERİĞİ — her molada farklı bir kart

   Amaç: 20 saniye boyunca hep aynı "göz kırpmayı unutuyorsun"
   yazısını okumak sıkıcı. Molalar arasında içerik TÜRÜ de
   değişsin. Şu an dört tür var:

     1) bilgi  — göz sağlığı bilgisi (bilgiler.js, kaynaklı)
     2) hava   — dışarıdaki hava (Open-Meteo, ücretsiz, anahtarsız)
     3) ozet   — kişinin kendi geçmişi (kaç mola, kaç günlük seri)
     4) ipucu  — kısa pratik öneri

   Sıra: bilgi → hava → bilgi → ozet → bilgi → ipucu → ...
   Göz bilgisi baskın kalıyor, çünkü uygulamanın asıl işi o.
   Kullanılamayan tür (ör. konum yoksa hava) sessizce atlanır.

   Neden hava durumu? "6 metre uzağa bak" demenin en kolay yolu
   pencereden dışarı bakmak. Dışarısı nasıl, hava aydınlık mı,
   gün batımına ne kadar var — bunu bilmek molayı somutlaştırıyor.
   Ayrıca gün ışığına çıkmak miyopi ilerlemesini yavaşlatıyor
   (Xiong ve ark., Acta Ophthalmologica, 2017).
   ============================================================ */

const MolaIcerik = (() => {
  const KONUM_ANAHTAR = 'goz-molasi-konum';
  const HAVA_ANAHTAR = 'goz-molasi-hava';
  const HAVA_TAZELIK = 30 * 60 * 1000;      // 30 dk — daha sık sormaya gerek yok

  /* ---------- Kısa pratik ipuçları ---------- */
  const IPUCLARI = [
    { baslik: 'Ekranı biraz aşağı al',
      metin: 'Ekranın üst kenarı göz hizanın ALTINDA olsun. Yukarı bakarak çalışmak ' +
             'göz kapağını daha çok açar, gözyaşı daha hızlı buharlaşır.',
      kaynak: 'American Optometric Association' },
    { baslik: 'Bir kol boyu uzakta dursun',
      metin: 'Ekranla aran 50–70 cm olsun — yaklaşık bir kol boyu. Daha yakını ' +
             'odaklama kasını sürekli kasılı tutar.',
      kaynak: 'American Academy of Ophthalmology' },
    { baslik: 'Parlaklığı odana uydur',
      metin: 'Ekran, arkasındaki duvardan belirgin şekilde parlak olmamalı. ' +
             'Gece karanlık odada tam parlaklık gözü zorlar.',
      kaynak: 'AOA — bilgisayar görme sendromu önerileri' },
    { baslik: 'Klimanın önünde oturma',
      metin: 'Doğrudan üzerine gelen hava akımı gözyaşı tabakasını kurutur. ' +
             'Vantilatör ve klimayı yüzünden başka yöne çevir.',
      kaynak: 'Tear Film & Ocular Surface Society, DEWS II' },
    { baslik: 'Bilerek üç kez tam kırp',
      metin: 'Ekrana bakarken çoğu göz kırpma yarım kalır, kapaklar tam kapanmaz. ' +
             'Şimdi üç kez, kapaklar tamamen birleşecek şekilde yavaşça kırp.',
      kaynak: 'Ophthalmology & Therapy, 2023' },
    { baslik: 'Su iç',
      metin: 'Vücut susuz kaldığında gözyaşı üretimi de düşer. Molayı bir bardak ' +
             'su içmek için kullan — hem kalkmış olursun.',
      kaynak: 'Journal of Clinical Medicine, 2021' },
  ];

  /* ================= KONUM ================= */

  function konumOku() {
    try { return JSON.parse(localStorage.getItem(KONUM_ANAHTAR) || 'null'); }
    catch { return null; }
  }
  function konumYaz(k) {
    try { localStorage.setItem(KONUM_ANAHTAR, JSON.stringify(k)); } catch {}
  }
  function konumSil() {
    try {
      localStorage.removeItem(KONUM_ANAHTAR);
      localStorage.removeItem(HAVA_ANAHTAR);
      localStorage.removeItem(KALITE_ANAHTAR);
    } catch {}
  }

  /** Tarayıcının konumunu ister. Tarayıcılar bunu yalnızca bir
      tıklamanın ardından güvenilir şekilde soruyor — bu yüzden
      ayarlardaki düğmeden çağrılıyor, molanın ortasında değil. */
  function konumuBul() {
    return new Promise((coz) => {
      if (!navigator.geolocation) { coz({ hata: 'Cihazın konum desteklemiyor.' }); return; }
      navigator.geolocation.getCurrentPosition(
        async (p) => {
          const k = {
            enlem: +p.coords.latitude.toFixed(3),
            boylam: +p.coords.longitude.toFixed(3),
            ad: await yerAdiBul(p.coords.latitude, p.coords.longitude),
          };
          konumYaz(k);
          coz({ konum: k });
        },
        (e) => coz({
          hata: e.code === 1 ? 'Konum izni verilmedi. Aşağıdan şehir arayabilirsin.'
                             : 'Konum alınamadı. Aşağıdan şehir arayabilirsin.',
        }),
        { timeout: 10000, maximumAge: 10 * 60 * 1000 }
      );
    });
  }

  /** Koordinattan şehir adı. Bulunamazsa boş döner — kritik değil. */
  async function yerAdiBul(enlem, boylam) {
    try {
      const u = `https://geocoding-api.open-meteo.com/v1/search?latitude=${enlem}` +
                `&longitude=${boylam}&count=1&language=tr&format=json`;
      const c = await fetch(u);
      const d = await c.json();
      return (d.results && d.results[0] && d.results[0].name) || '';
    } catch { return ''; }
  }

  /** Şehir araması — dünya çapında çalışır, anahtar istemez. */
  async function sehirAra(metin) {
    const q = (metin || '').trim();
    if (q.length < 2) return [];
    try {
      const u = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(q)}` +
                `&count=6&language=tr&format=json`;
      const c = await fetch(u);
      const d = await c.json();
      return (d.results || []).map((r) => ({
        ad: r.name,
        alt: [r.admin1, r.country].filter(Boolean).join(', '),
        enlem: +r.latitude.toFixed(3),
        boylam: +r.longitude.toFixed(3),
      }));
    } catch { return []; }
  }

  function sehirSec(y) {
    konumYaz({ enlem: y.enlem, boylam: y.boylam, ad: y.ad });
    try {
      localStorage.removeItem(HAVA_ANAHTAR);
      localStorage.removeItem(KALITE_ANAHTAR);
    } catch {}
  }

  /* ================= HAVA ================= */

  /* Open-Meteo hava kodu → kısa Türkçe karşılık.
     Kaynak: WMO 4677 hava kodu tablosu. */
  const HAVA_ADI = {
    0: ['Açık', '☀️'], 1: ['Az bulutlu', '🌤️'], 2: ['Parçalı bulutlu', '⛅'],
    3: ['Kapalı', '☁️'], 45: ['Sisli', '🌫️'], 48: ['Kırağılı sis', '🌫️'],
    51: ['Hafif çisenti', '🌦️'], 53: ['Çisenti', '🌦️'], 55: ['Yoğun çisenti', '🌦️'],
    61: ['Hafif yağmur', '🌧️'], 63: ['Yağmurlu', '🌧️'], 65: ['Kuvvetli yağmur', '🌧️'],
    71: ['Hafif kar', '🌨️'], 73: ['Kar yağışlı', '🌨️'], 75: ['Yoğun kar', '❄️'],
    80: ['Sağanak', '🌦️'], 81: ['Sağanak yağmur', '🌧️'], 82: ['Kuvvetli sağanak', '⛈️'],
    95: ['Gök gürültülü', '⛈️'], 96: ['Dolulu fırtına', '⛈️'], 99: ['Şiddetli fırtına', '⛈️'],
  };

  async function havaGetir() {
    const konum = konumOku();
    if (!konum) return null;

    // Taze önbellek varsa ağa hiç çıkma
    try {
      const eski = JSON.parse(localStorage.getItem(HAVA_ANAHTAR) || 'null');
      if (eski && Date.now() - eski.an < HAVA_TAZELIK) return eski.veri;
    } catch {}

    try {
      const u = `https://api.open-meteo.com/v1/forecast?latitude=${konum.enlem}` +
                `&longitude=${konum.boylam}` +
                `&current=temperature_2m,apparent_temperature,weather_code,is_day` +
                `&daily=sunset,sunrise,uv_index_max&timezone=auto&forecast_days=1`;
      const c = await fetch(u);
      if (!c.ok) return null;
      const d = await c.json();
      const veri = {
        ad: konum.ad || '',
        sicaklik: Math.round(d.current.temperature_2m),
        hissedilen: Math.round(d.current.apparent_temperature),
        kod: d.current.weather_code,
        gunduz: !!d.current.is_day,
        batis: d.daily.sunset && d.daily.sunset[0],
        dogus: d.daily.sunrise && d.daily.sunrise[0],
        uv: d.daily.uv_index_max && d.daily.uv_index_max[0],
      };
      try { localStorage.setItem(HAVA_ANAHTAR, JSON.stringify({ an: Date.now(), veri })); } catch {}
      return veri;
    } catch { return null; }
  }

  /* ---------- HAVA KALİTESİ ----------
     Neden göz uygulamasında? Hava kirliliği ile kuru göz arasında
     ölçülmüş bir bağ var: PM2.5 ve ozon yükseldiğinde kuru göz
     şikâyetiyle başvuru artıyor. Ekran başındaki az kırpma zaten
     gözyaşını inceltiyor; kirli havada ikisi üst üste biniyor. */
  const KALITE_ANAHTAR = 'goz-molasi-hava-kalite';

  async function kaliteGetir() {
    const konum = konumOku();
    if (!konum) return null;
    try {
      const eski = JSON.parse(localStorage.getItem(KALITE_ANAHTAR) || 'null');
      if (eski && Date.now() - eski.an < HAVA_TAZELIK) return eski.veri;
    } catch {}
    try {
      const u = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${konum.enlem}` +
                `&longitude=${konum.boylam}&current=european_aqi,pm2_5,pm10&timezone=auto&forecast_days=1`;
      const c = await fetch(u);
      if (!c.ok) return null;
      const d = await c.json();
      if (d.current == null || d.current.european_aqi == null) return null;
      const veri = {
        ad: konum.ad || '',
        aqi: Math.round(d.current.european_aqi),
        pm25: d.current.pm2_5,
        pm10: d.current.pm10,
      };
      try { localStorage.setItem(KALITE_ANAHTAR, JSON.stringify({ an: Date.now(), veri })); } catch {}
      return veri;
    } catch { return null; }
  }

  /* Avrupa Hava Kalitesi İndeksi (EAQI) eşikleri — Avrupa Çevre Ajansı */
  function aqiSeviye(a) {
    if (a <= 20) return ['çok iyi', '🟢'];
    if (a <= 40) return ['iyi', '🟢'];
    if (a <= 60) return ['orta', '🟡'];
    if (a <= 80) return ['kötü', '🟠'];
    if (a <= 100) return ['çok kötü', '🔴'];
    return ['aşırı kötü', '🟣'];
  }

  function kaliteKarti(k) {
    if (!k) return null;
    const [ad, simge] = aqiSeviye(k.aqi);
    const yer = k.ad ? `${k.ad} · ` : '';
    const parcalar = [`Hava kalitesi indeksi ${k.aqi} — ${ad}.`];
    if (k.pm25 != null) parcalar.push(`PM2.5: ${Math.round(k.pm25)} µg/m³.`);

    if (k.aqi <= 40) {
      parcalar.push('Hava temiz — pencereyi açıp uzağa bakmak için iyi bir an.');
    } else if (k.aqi <= 60) {
      parcalar.push('Hava orta düzeyde. Gözün batıyorsa suni gözyaşı işe yarayabilir.');
    } else {
      parcalar.push('Hava kirli. Pencereyi kapalı tut; kirli havada kuru göz şikâyeti ' +
                    'belirgin şekilde artıyor. Yine de gözünü ekrandan ayır — ' +
                    'odanın en uzak köşesine bak.');
    }
    return {
      baslik: `${simge} ${ad} (indeks ${k.aqi})`,
      metin: yer + parcalar.join(' '),
      kaynak: 'Open-Meteo (EAQI) · JAMA Ophthalmology, 2018 — kirlilik ve kuru göz',
    };
  }

  function kalanSure(isoZaman) {
    if (!isoZaman) return null;
    const fark = new Date(isoZaman).getTime() - Date.now();
    if (fark <= 0) return null;
    const dk = Math.round(fark / 60000);
    if (dk < 60) return `${dk} dakika`;
    return `${Math.floor(dk / 60)} saat ${dk % 60} dakika`;
  }

  function havaKarti(h) {
    if (!h) return null;
    const [ad, simge] = HAVA_ADI[h.kod] || ['—', '🌡️'];
    const yer = h.ad ? `${h.ad} · ` : '';
    const baslik = `${simge} ${h.sicaklik}° · ${ad}`;

    const parcalar = [];
    if (Math.abs(h.hissedilen - h.sicaklik) >= 2) {
      parcalar.push(`Hissedilen ${h.hissedilen}°.`);
    }
    if (h.gunduz) {
      const kalan = kalanSure(h.batis);
      parcalar.push('Pencereden dışarı bak — uzağa odaklanmanın en kolay yolu bu.');
      if (kalan) parcalar.push(`Gün batımına ${kalan} var.`);
      parcalar.push('Gün ışığında geçirilen zaman, özellikle çocuklarda miyopi ilerlemesini yavaşlatıyor.');
    } else {
      const kalan = kalanSure(h.dogus);
      parcalar.push('Hava karanlık; yine de gözünü ekrandan ayır ve odanın en uzak köşesine bak.');
      if (kalan) parcalar.push(`Gün doğumuna ${kalan} var.`);
      parcalar.push('Gece ekran parlaklığını düşürmek gözü belirgin şekilde rahatlatır.');
    }

    return { baslik, metin: yer + parcalar.join(' '), kaynak: 'Open-Meteo · Acta Ophthalmologica, 2017' };
  }

  /* ================= KİŞİSEL ÖZET ================= */

  function ozetKarti(istatistik) {
    if (typeof Gecmis === 'undefined') return null;
    const bugun = (istatistik && istatistik.tamamlananMola) | 0;
    const hafta = Gecmis.sonGunler(7, istatistik).reduce((t, g) => t + g.sayi, 0);
    const seri = Gecmis.seri(istatistik);

    // İlk gün hiç veri yokken "0 mola verdin" demek moral bozar
    if (bugun === 0 && hafta === 0) return null;

    const parcalar = [];
    parcalar.push(`Bugün ${bugun} mola tamamladın.`);
    if (hafta > bugun) parcalar.push(`Son yedi günde toplam ${hafta} mola.`);
    if (seri >= 2) parcalar.push(`${seri} gündür üst üste günlük hedefi tutturuyorsun.`);
    const dk = Math.round((hafta * 20) / 60);
    if (dk >= 1) parcalar.push(`Bu, yaklaşık ${dk} dakikalık toplam göz dinlenmesi demek.`);

    return {
      baslik: `bugün ${bugun}. molan`,
      metin: parcalar.join(' '),
      kaynak: 'Kendi geçmişin · yalnızca bu cihazda saklanır',
    };
  }

  /* ================= SIRA ================= */

  const SIRA = ['bilgi', 'hava', 'bilgi', 'ozet', 'bilgi', 'ipucu', 'bilgi', 'kalite'];
  let havaIzin = true;                 // ayarlardan kapatılabilir
  function havaAyarla(acik) { havaIzin = !!acik; }
  let adim = 0;
  let bilgiNo = Math.floor(Math.random() * 1000);
  let ipucuNo = Math.floor(Math.random() * 1000);

  function bilgiKarti() {
    if (typeof BILGILER === 'undefined' || !BILGILER.length) return null;
    return BILGILER[bilgiNo++ % BILGILER.length];
  }
  function ipucuKarti() {
    return IPUCLARI[ipucuNo++ % IPUCLARI.length];
  }

  /** Sıradaki kartı döndürür. Üretilemeyen tür atlanır,
      en kötü ihtimalle göz bilgisine düşer — kart hep dolu gelir. */
  async function sonraki(istatistik) {
    for (let deneme = 0; deneme < SIRA.length; deneme++) {
      const tur = SIRA[adim++ % SIRA.length];
      let k = null;
      if (tur === 'bilgi') k = bilgiKarti();
      else if (tur === 'ipucu') k = ipucuKarti();
      else if (tur === 'ozet') k = ozetKarti(istatistik);
      else if (tur === 'hava') k = havaIzin ? havaKarti(await havaGetir()) : null;
      else if (tur === 'kalite') k = havaIzin ? kaliteKarti(await kaliteGetir()) : null;
      if (k) return { tur, ...k };
    }
    const y = bilgiKarti();
    return y ? { tur: 'bilgi', ...y } : null;
  }

  /** Türe göre kartın üstündeki etiket. */
  const ETIKET = { bilgi: 'Neden?', hava: 'Dışarısı', ozet: 'Senin durumun',
                   ipucu: 'İpucu', kalite: 'Hava kalitesi' };

  return {
    sonraki, ETIKET, havaAyarla,
    konumuBul, konumOku, konumSil, sehirAra, sehirSec,
    havaGetir, havaKarti, kaliteGetir, kaliteKarti, ozetKarti,
  };
})();

if (typeof module !== 'undefined') module.exports = { MolaIcerik };
