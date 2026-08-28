/* ============================================================
   FACTS (English) — the "why?" cards shown during breaks.

   Same content and same sources as bilgiler.js. Every claim is
   sourced; nothing invented. Where the evidence is weak, the card
   says so plainly.

   If you edit one file, edit the other.
   ============================================================ */

const BILGILER_EN = [
  {
    baslik: 'Your eyes forget to blink',
    metin: 'You normally blink about 15 times a minute. Staring at a screen drops that to 5–7. ' +
           'Blinking less dries out the tear film — that is where the burning, stinging and dryness come from.',
    kaynak: 'American Academy of Ophthalmology, 2024',
  },
  {
    baslik: 'How far does it actually drop?',
    metin: 'In a classic study of 104 office workers, blink rate fell from 22 per minute at rest to ' +
           '10 while reading a book, and 7 while looking at a screen.',
    kaynak: 'Tsubota & Nakamori, New England Journal of Medicine, 1993',
  },
  {
    baslik: 'You are not alone',
    metin: 'A review pooling 45 studies found that roughly 66% of screen workers report symptoms of ' +
           'digital eye strain. The three most common: blurred vision (34%), tired eyes (32%), watering (31%).',
    kaynak: 'Scientific Reports, 2023 (review of 45 studies)',
  },
  {
    baslik: 'Common everywhere',
    metin: 'Measurements during the pandemic put the prevalence of digital eye strain in Türkiye at ' +
           'about 48%. Health authorities in several countries recommend the 20-20-20 rule to the public.',
    kaynak: 'BMC Public Health, 2024',
  },
  {
    baslik: 'Why exactly 6 metres?',
    metin: 'In eye care, 6 metres counts as "optical infinity" — it is only 0.17 dioptres away from true ' +
           'infinity. Look that far and your focusing muscle (the ciliary muscle) relaxes essentially fully. ' +
           'Looking further brings no extra benefit.',
    kaynak: 'Standard optometric definition — the "far point"',
  },
  {
    baslik: 'The muscle stays tensed',
    metin: 'Focusing up close contracts the ciliary muscle. Hold that for hours and the muscle stays ' +
           'tensed — this is the second cause of eye strain, alongside reduced blinking.',
    kaynak: 'American Optometric Association',
  },
  {
    baslik: 'The two-hour threshold',
    metin: 'The American Optometric Association says those at greatest risk are people who spend ' +
           'two or more continuous hours at a screen every day. Once you are around that mark, ' +
           'a longer break is worth it.',
    kaynak: 'American Optometric Association',
  },
  {
    baslik: 'Let us be honest about the evidence',
    metin: 'The 20-20-20 rule is an expert recommendation, not a proven treatment. The specific numbers ' +
           'were chosen in the 1990s because they are memorable. What is well documented is the problem ' +
           'itself and the fact that regular breaks reduce symptoms.',
    kaynak: 'Johnson & Rosenfield, Optometry and Vision Science, 2023',
  },
  {
    baslik: 'Maybe 10 minutes is better',
    metin: 'In a small study, 20-second breaks every 20 minutes were not enough to relax the focusing ' +
           'muscle; breaks every 10 minutes performed better. The reminder itself matters more than the ' +
           'exact numbers.',
    kaynak: 'Johnson & Rosenfield, Optom Vis Sci, 2023',
  },
  {
    baslik: 'For children, what matters is being outdoors',
    metin: 'A meta-analysis of 12,922 children aged 6–16 found a clear dose-response: 7 hours outdoors ' +
           'a week cuts the risk of developing myopia by 20%, 16 hours by 53%, 27 hours by 69%. ' +
           'Screen time matters mainly because it displaces time outside.',
    kaynak: 'Cochrane, 2024 · Ophthalmic Research, 2024',
  },
  {
    baslik: 'Close work and myopia',
    metin: 'Sustained close work is associated with myopia progression in children, though the link is ' +
           'weaker than the protective effect of daylight. Distance breaks are a sensible habit either way.',
    kaynak: 'Ciuffreda & Vasudevan, Ophthalmic Physiol Opt, 2008',
  },
  {
    baslik: 'It is not only your eyes',
    metin: 'Sitting still at a screen also loads the neck, shoulders and lower back. Standing up during a ' +
           'break helps more than the eye exercise alone.',
    kaynak: 'Cochrane Database of Systematic Reviews, 2025',
  },
  {
    baslik: 'Screens do not permanently damage your eyes',
    metin: 'There is no evidence that screen use causes lasting damage to the eye. The symptoms are real ' +
           'but reversible — they ease once you rest.',
    kaynak: 'American Academy of Ophthalmology',
  },
  {
    baslik: 'Screen position matters too',
    metin: 'Keep the screen an arm’s length away (about 60 cm) and slightly below eye level. Looking ' +
           'slightly downward lets the eyelid cover more of the surface, which reduces drying.',
    kaynak: 'American Optometric Association',
  },
];

const IPUCLARI_EN = [
  {
    baslik: 'Lower the screen a little',
    metin: 'The top edge of the screen should sit BELOW eye level. Looking upward opens the eyelid wider, ' +
           'so tears evaporate faster.',
    kaynak: 'American Optometric Association',
  },
  {
    baslik: 'Keep it an arm’s length away',
    metin: 'Sit 50–70 cm from the screen — roughly an arm’s length. Any closer keeps the focusing ' +
           'muscle permanently contracted.',
    kaynak: 'American Academy of Ophthalmology',
  },
  {
    baslik: 'Match brightness to the room',
    metin: 'The screen should not be noticeably brighter than the wall behind it. Full brightness in a ' +
           'dark room strains the eyes.',
    kaynak: 'AOA — computer vision syndrome guidance',
  },
  {
    baslik: 'Do not sit in the airflow',
    metin: 'Air blowing straight at your face dries the tear film. Point fans and air conditioning away ' +
           'from you.',
    kaynak: 'Tear Film & Ocular Surface Society, DEWS II',
  },
  {
    baslik: 'Blink fully three times, on purpose',
    metin: 'Most blinks at a screen are incomplete — the lids never fully meet. Blink slowly three times ' +
           'now, letting them close completely. That is what empties the oil glands at the lid margin.',
    kaynak: 'Ophthalmology & Therapy, 2023',
  },
  {
    baslik: 'Drink some water',
    metin: 'When the body is short of water, tear production drops too. Use the break to drink a glass — ' +
           'and you get up while you are at it.',
    kaynak: 'Journal of Clinical Medicine, 2021',
  },
];

if (typeof module !== 'undefined') {
  module.exports = { BILGILER_EN, IPUCLARI_EN };
}
