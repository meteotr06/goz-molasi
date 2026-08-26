# Yayma — bu üç şey diğer uygulamalara nasıl taşınır

Göz Molası'nda kurulan üç şeyin başka projede uygulanma kılavuzu.
Kodu buradan kopyalamak yerine **neyin neden öyle olduğunu** anlat;
her projenin kendi şekli var.

Sıra önemli: **1'i her projede yap**, 2 ve 3 uygulamaya bağlı.

---

## 1. Otomatik sınama zinciri

**Ne çözüyor:** "Derledim, çalışıyor herhalde" diyip bozuk sürüm
yayınlamayı. Göz Molası'nda bir kere "başarıyla derlendi" diyen bir
sürüm çalıştırıldığında hiç açılmadı — derleme çıktısına bakılıp
geçilmişti.

### Kurulum

Her sınama **ayrı bir dosya**, çıkış kodu 0 = geçti. Bir koşucu hepsini
sırayla çalıştırır. Ucuzdan pahalıya diz: veri hatası varsa 2 dakikalık
derlemeyi hiç başlatma.

```python
# sinama.py
SINAMALAR = [
    ("veri",     "sinama_veri.py",     "İçerik tutarlılığı"),
    ("yerlesim", "sinama_yerlesim.py", "Çakışma ve taşma"),
    ("acilis",   "sinama_acilis.py",   "Derlenen exe açılıyor mu"),
]
EXE_GEREKENLER = {"acilis"}      # "hizli" kipinde atlanır

for ad, dosya, aciklama in SINAMALAR:
    kod = subprocess.call([sys.executable, dosya], cwd=BURASI)
```

### Derlemeye bağlama — kritik kısım

Sınama varsa ama derleme onu çağırmıyorsa, sınama yok demektir.

```bat
echo [1/4] Kaynak sinamalari...
python "%~dp0masaustu\sinama.py" hizli
if errorlevel 1 (
  echo SINAMA BASARISIZ - DERLEME YAPILMADI.
  pause & exit /b 1
)
... derle ...
echo [4/4] Acilis sinamasi...
python "%~dp0masaustu\sinama_acilis.py"
if errorlevel 1 (
  echo EXE DERLENDI AMA ACILMIYOR. Bu surumu kimseye verme.
  pause & exit /b 1
)
start "" "%~dp0Uygulama.exe"      && uygulama YALNIZCA burada aciliyor
```

### Açılış sınaması nasıl yazılır

Süreci gerçekten başlat, penceresinin geldiğini gör, sonra kapat:

```python
surec = subprocess.Popen([EXE], cwd=KOK)
time.sleep(4)
if surec.poll() is not None:
    hatalar.append("program açılır açılmaz kapandı")
# EnumWindows ile başlığı eşleşen görünür pencereyi ara
# DwmGetWindowAttribute(9) ile gerçek kutusunu ölç
# calisma_alani() dışına taşıyor mu bak
```

**Sınama kullanıcının programını öldürmüş halde bırakmaz.** Başlarken
açık mıydı diye bak, bitince geri aç. Bir kere böyle oldu: sınama
programı kapattı, kimse geri açmadı, kullanıcı saatlerce korumasız
çalıştı.

### Üç ders

**a) Gizli içerik = denetlenmemiş içerik.**
Sınama "yatay taşma yok" diyordu ve 31/31 geçiyordu. Ama sekme
varsayılan olarak gizliydi, içeriği hiç ölçülmüyordu — telefonda 123
piksel taşıyordu. Gizli olan ne varsa sınama **açıp** ölçmeli:

```js
const oncedenAcikti = !panel.hidden;
dugme.click();
await new Promise((z) => setTimeout(z, 1500));   // içerik kurulsun
... ölç ...
if (!oncedenAcikti) kapat();                     // durumu geri kur
```

**b) Sınırı değil niyeti sına.**
Eşik 1200 sn iken testi tam 1200 sn'ye kurdum; aradan geçen birkaç
milisaniye eşiği aştı ve sınama rastgele kalmaya başladı. 1080 sn yaz —
sınanan şey "normal bir kapat-aç sayacı sıfırlamamalı".

**c) Sınama yanlışsa sınamayı düzelt, kodu değil.**
Dokunma hedefi denetimim alt bilgideki metin içi düğmeyi işaretledi.
Kod doğruydu: WCAG 2.5.8'in "inline" istisnası cümle içindeki hedefleri
kuralın dışında tutuyor. Kuralı yumuşatmak değil, istisnayı öğretmek
gerekiyordu.

---

## 2. İki dillilik (`dil.js` yöntemi)

**Yöntem:** Sözlüğün anahtarı **Türkçe metnin kendisi**. HTML'e hiç
dokunulmuyor; sayfa kurulduktan sonra DOM gezilip metin düğümleri
değiştiriliyor.

```js
const SOZLUK = { 'Şimdi mola ver': 'Take a break now', ... };

function sayfayiCevir(kok = document.body) {
  if (AKTIF_DIL === 'tr') return;
  const gezgin = document.createTreeWalker(kok, NodeFilter.SHOW_TEXT, {
    acceptNode(d) {
      const e = d.parentElement?.tagName;
      if (e === 'SCRIPT' || e === 'STYLE') return NodeFilter.FILTER_REJECT;
      return d.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT
                                : NodeFilter.FILTER_REJECT;
    },
  });
  // ... eşleşenleri değiştir
  for (const nit of ['placeholder', 'title', 'aria-label', 'alt']) { ... }
}
```

### Neden `data-c="dugme.mola"` değil

Denendi, vazgeçildi:

- **Her öğeye nitelik eklemek gerekiyor.** Yüzlerce öğe, hepsi elle.
  Biri unutulunca sessizce çevrilmiyor ve bunu kimse fark etmiyor.
- **Anahtar ile metin iki ayrı yerde durur.** Türkçe metni değiştiren
  kişi sözlüğü unutur; anahtar `dugme.mola` ama içerik başka bir şey
  yazar. Anahtar metnin kendisi olunca bu ayrışma **imkânsız**.
- **Çevrilmemiş metin boş kalmaz.** Sözlükte yoksa Türkçesi görünür.
  Anahtar yönteminde `dugme.mola` yazısı görünür — kullanıcıya çöp.

Bedeli: tam eşleşme gerekiyor. Kabul edilebilir, çünkü:

### Tuzaklar

1. **HTML'de satıra bölünmüş metin eşleşmez.** `Ana ekranına ekle,\n
   internetsiz de çalışsın` sözlükteki tek satırla tutmuyordu.
   Çözüm: karşılaştırmadan önce boşlukları tek boşluğa indir.
   ```js
   const yeni = SOZLUK[kirp] || SOZLUK[kirp.replace(/\s+/g, ' ')];
   ```
2. **Sayı içeren metin anahtar olamaz** — sayı her seferinde değişiyor.
   İki dilde ayrı kalıp veren bir yardımcı yaz:
   ```js
   CS(`${dk} dakika kapalıydı`, `closed for ${dk} minutes`)
   ```
3. **Çeviri tek yönlü (tr → en).** Dili geri almak için sayfayı yeniden
   yükle; DOM'u geri çevirmeye çalışma.
4. **Sonradan eklenen içeriği ayrıca çevir.** JS ile kurulan her
   bölümden sonra `sayfayiCevir(kap)` çağır — yoksa o kısım Türkçe kalır.
5. **Uzun metinleri çevirme, ÇEKME.** Rehber gibi sayfalar için ayrı
   dosya tut (`rehber.html` / `guide.html`) ve dile göre olanı getir.
   Bin kelimeyi sözlüğe koymak sürdürülemez.

---

## 3. Bilgiler sekmesi

**Ne çözüyor:** İçerik uygulamanın içine dağılmış ve tek tek çıkıyorsa,
merak eden kişinin hepsini görebileceği bir yer yoktur.

### Sekme çubuğu

```html
<nav class="sekme-cubugu" role="tablist">
  <button class="sekme secili" id="sekmeDugmeSayac"
          role="tab" aria-selected="true" aria-controls="sekmeSayac">Sayaç</button>
  <button class="sekme" id="sekmeDugmeBilgiler"
          role="tab" aria-selected="false" aria-controls="sekmeBilgiler">Bilgiler</button>
</nav>
<div id="sekmeSayac" role="tabpanel"> ... mevcut içerik ... </div>
<section id="sekmeBilgiler" role="tabpanel" hidden>
  <div id="bilgilerIcerik"></div>
</section>
```

Düğme en az **44×44** olmalı. `aria-selected` ile `hidden` birlikte
güncellenmezse ekran okuyucu yanlış bilgi verir.

### İçeriği VERİDEN kur, HTML'e yazma

Elle yazmak aynı metnin ikinci kopyası demek. Göz Molası'nda
`bilgiler.py` ile `bilgiler.js` elle ikiz tutuluyordu ve ayrıştılar —
biri düz kesme işareti, öbürü tipografik.

```js
let kuruldu = false;
async function bilgileriKur() {
  if (kuruldu) return;        // tembel kurulum: sekme açılmadan çalışma
  kuruldu = true;
  const parcalar = BILGILER.map((b) => bilgiOgesi(b.baslik, b.metin, b.kaynak));
  kap.innerHTML = parcalar.join('');
  sayfayiCevir(kap);          // 2. bölümün 4. tuzağı
}
```

### Uzun metni çek, kopyalama

```js
const yanit = await fetch(aktifDil() === 'en' ? 'guide.html' : 'rehber.html');
const belge = new DOMParser().parseFromString(await yanit.text(), 'text/html');
const yazi = belge.querySelector('main.yazi');
yazi.querySelectorAll('script, .reklam-alani, nav.icindekiler').forEach((o) => o.remove());
govde.innerHTML = yazi.innerHTML;
```

Böylece sayfa hem arama motorları için ayrı adres olarak duruyor hem de
sekmede görünüyor. **Tek kaynak, iki gösterim.** Çevrimdışıyken servis
işçisinin önbelleğinden gelir; gelmezse bağlantı bırak, boş bırakma.

### İki zorunlu detay

**a) Uzun kelime bölünebilmeli.** 85 harflik bir yer adı 375 px ekranda
kabı zorla genişletip bütün sayfayı yatay kaydırıyordu. Uzun adresler ve
kaynak künyeleri de aynı sorunu çıkarır:

```css
.bilgi-oge b, .bilgi-oge p, .bilgi-oge .kaynak {
  overflow-wrap: anywhere;
  word-break: break-word;
}
.rehber-govde table { display: block; overflow-x: auto; max-width: 100%; }
```

**b) `innerHTML` kullanıyorsan kaçır.** Veri senin olsa bile alışkanlık
olsun:

```js
const kacis = (m) => String(m ?? '').replace(/[&<>"]/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
```

### Sınamaya ekle

```js
ekle('bilgiler', 'kartlar kuruldu', oge >= 20, `${oge} kart`);
ekle('bilgiler', 'her iddianın kaynağı var', kaynaksiz <= yonergeAdet, ...);
ekle('bilgiler', 'sekme içeriği taşmıyor', tasan.length === 0, ...);
```

---

## Uygularken

- **Önce sınama zinciri.** Diğer ikisini sınamasız eklersen aynı
  hataları yeniden bulursun.
- Her adımdan sonra sınamayı koştur; toplu uygulayıp sonunda bakma.
- Bir şey uymuyorsa **uydurmaya çalışma** — neden uymadığını o projenin
  `ILERLEME.md` dosyasına yaz.
