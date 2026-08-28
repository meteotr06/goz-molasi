# -*- coding: utf-8 -*-
"""ÜRETİLMİŞ DOSYA — degisiklikler.js'ten.

ELLE DÜZENLEME. Değişiklik metnini `degisiklikler.js` içinde
değiştir, sonra `python masaustu/degisiklikler_uret.py` çalıştır.
"""

DEGISIKLIKLER = [
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
