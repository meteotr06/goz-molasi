/* KÖPRÜ (tarayıcı tarafı) — Windows sürümünün sayacını dinler.
 *
 * SORUN
 *   İki sürüm iki ayrı yere yazıyordu:
 *     Windows  -> %APPDATA%\GozMolasi\durum.json
 *     Tarayıcı -> localStorage
 *   Biri 8 dakikadayken öbürü 20:00 gösteriyordu. Kullanıcının sözüyle:
 *   "süre başa sarmasın".
 *
 * NASIL
 *   Tarayıcı bilgisayardaki dosyayı okuyamaz — bu bir izin meselesi
 *   değil, aşılabilecek bir duvar değil. O yüzden Windows sürümü
 *   127.0.0.1:8452 üzerinde küçük bir OKUMA ucu açıyor; burası ona
 *   soruyor.
 *
 * ÖLÇÜLDÜ (27.08.2026) — SÖZ VERİLMEYEN KISIM
 *     sayfa http://localhost:8455    -> köprü OKUNDU
 *     sayfa https://meteotr06.github.io -> ERR_BLOCKED_BY_CLIENT
 *   Yayındaki sayfa, en az bir makinede yerel uca ulaşamıyor (tarayıcı
 *   eklentisi kesiyor). Bu yüzden köprü BİR KOLAYLIKTIR, bir güvence
 *   değil. Ulaşılamazsa uygulama bugünkü gibi çalışır ve kullanıcıya
 *   hata gösterilmez — olmayan bir şeyin eksikliği hata değildir.
 *
 * YÖN
 *   Tek yönlü: Windows -> tarayıcı. Windows sürümü sürekli açık ve
 *   ekran süresini gerçekten ölçebiliyor; sekme ise kapanıp açılıyor.
 *   Hangisi daha çok şey biliyorsa doğru olan odur.
 */
(() => {
  'use strict';

  const ADRES = 'http://127.0.0.1:8452/durum';
  const ILK_ZAMAN_ASIMI = 1200;   // açılışı geciktirmemeli
  const SORGU_ARALIGI = 5000;

  // Köprü yoksa her 5 saniyede bir boşuna denemenin anlamı yok; arka
  // arkaya başarısızlıkta aralık açılıyor. Sekme açık kalınca saatlerce
  // gereksiz istek atmasın.
  const EN_UZUN_ARALIK = 60000;

  async function sor(zamanAsimi = ILK_ZAMAN_ASIMI) {
    // AbortController şart: köprü yokken fetch'in kendi zaman aşımını
    // beklemek açılışı kilitler.
    const kes = new AbortController();
    const sayac = setTimeout(() => kes.abort(), zamanAsimi);
    try {
      const yanit = await fetch(ADRES, { cache: 'no-store', signal: kes.signal });
      if (!yanit.ok) return null;
      const veri = await yanit.json();
      // Beklediğimiz şey mi? Portu başka bir program tutuyor olabilir;
      // rastgele bir JSON'u sayaç sanıp süreyi bozmayalım.
      if (!veri || veri.kaynak !== 'windows') return null;
      if (!Number.isFinite(+veri.kalan_sn)) return null;
      return veri;
    } catch {
      return null;                 // köprü yok: normal ve sessiz durum
    } finally {
      clearTimeout(sayac);
    }
  }

  window.Kopru = {
    sor,

    /** Açılışta bir kez sorar; Windows sürümü açıksa durumunu döndürür. */
    async ilkDurum() {
      return sor(ILK_ZAMAN_ASIMI);
    },

    /**
     * Sekme açık kaldığı sürece dinler ve her değişiklikte `geri`yi çağırır.
     * `geri(veri)` -> Windows açık, `geri(null)` -> bağlantı koptu.
     */
    dinle(geri) {
      let aralik = SORGU_ARALIGI;
      let sonDurumVarMi = null;
      let durduruldu = false;

      const tur = async () => {
        if (durduruldu) return;
        // Sekme arka plandayken sormanın anlamı yok: kullanıcı bakmıyor,
        // hem pil hem istek boşa gidiyor. Öne gelince zaten sorulacak.
        if (document.hidden) {
          zamanlayici = setTimeout(tur, aralik);
          return;
        }
        const veri = await sor(ILK_ZAMAN_ASIMI);
        const varMi = veri !== null;
        if (varMi !== sonDurumVarMi) {
          sonDurumVarMi = varMi;
          geri(veri);
        } else if (varMi) {
          geri(veri);
        }
        aralik = varMi ? SORGU_ARALIGI
                       : Math.min(EN_UZUN_ARALIK, aralik * 2);
        zamanlayici = setTimeout(tur, aralik);
      };

      // TEK ZİNCİR. Eskiden `visibilitychange` bekleyen zamanlayıcıyı
      // İPTAL ETMEDEN `tur()` çağırıyordu: her gizle→göster çevrimi bir
      // zincir daha ekliyordu. Bir iş gününde 200 sekme geçişi = 200
      // eşzamanlı zincir, saniyede onlarca istek, boşa giden pil.
      // Ayrıca paylaşılan `aralik` zincirler arasında eziliyor ve geri
      // çekilme mantığı bozuluyordu.
      let zamanlayici = setTimeout(tur, SORGU_ARALIGI);
      const tazele = () => {
        if (durduruldu || document.hidden) return;
        clearTimeout(zamanlayici);          // bekleyeni İPTAL ET
        aralik = SORGU_ARALIGI;
        tur();
      };
      document.addEventListener('visibilitychange', tazele);
      return () => {
        durduruldu = true;
        clearTimeout(zamanlayici);
        document.removeEventListener('visibilitychange', tazele);
      };
    },
  };
})();
