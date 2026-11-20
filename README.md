# LeetNote

LeetCode masalalari yechimlari va algoritmik mavzular (Topics) uchun yaratilgan minimalist, tezkor statik konspekt-sayt.

Ushbu loyihada har bir masala chuqur tahlil qilinadi: g'oyasi, turli xil yechish usullari (masalan, Vertikal, Gorizontal, Ikkilik qidiruv, Trie), ularning vaqt va xotira murakkabligi hamda 3 xil tildagi (**Python**, **PHP**, **Go**) toza kodlari taqdim etiladi.

---

## 🚀 Sayt imkoniyatlari (Features)

- **Tezkor statik sayt:** Tashqi og'ir freymvorklarsiz, toza HTML, CSS va Vanilla JS asosida ishlaydi.
- **Ko'p usulli tahlil (Multi-approach):** Masalaning barcha yechim usullari orasida interaktiv almashish (ustiga borganda yoki bosganda faqat kerakli usul kodi ko'rinadi).
- **3 ta tilda yechim:** Har bir usul uchun Python, PHP va Go yechimlari mavjud.
- **Qidiruv va filtrlar:** Masalalarni nomi, raqami, darajasi (Easy / Medium / Hard) va mavzular (Topics) bo'yicha bir zumda saralash.
- **Mavzular ensiklopediyasi (Topics):** Array, String, Trie, Hash Map va Math kabi mavzular bo'yicha nazariy tushunchalar, amallar murakkabligi va kod namunalari.
- **Mavzu tanlash (Dark/Light mode):** Qorong'i va yorug' rejimni qo'llab-quvvatlaydi.

---

## 📁 Loyiha strukturasi

```text
LeetNote/
├── python/          # Python yechim fayllari (NNNN-problem-slug.py)
├── php/             # PHP yechim fayllari (NNNN-problem-slug.php)
├── go/              # Go yechim fayllari (NNNN-problem-slug.go)
├── topics/          # Mavzular bo'yicha tushuntirishlar (Markdown formatida)
├── assets/          # Sayt shablonlari: style.css va app.js
├── site/            # Generatsiya qilingan statik veb-sayt (HTML)
├── problems.json    # Masalalar ro'yxati, usullari, izohlar va metama'lumotlar
└── build.py         # Saytni yig'uvchi (build) generator skript
```

---

## 🛠️ Ishga tushirish (Build & Run)

Saytni yangilash yoki lokal ko'rish uchun:

1. **Saytni qayta yig'ish (Build):**
   ```bash
   python build.py
   ```
   *`problems.json` va `topics/*.md` dagi ma'lumotlar asosida `site/` papkasi to'liq yangilanadi.*

2. **Lokal serverda ko'rish:**
   ```bash
   python -m http.server --directory site 8000
   ```
   So'ng brauzerda `http://localhost:8000` manzilini oching (yoki to'g'ridan-to'g'ri `site/index.html` faylini ochish ham mumkin).

---

## ✍️ Yangi masala qo'shish tartibi

1. `problems.json` fayliga yangi masala ma'lumotlarini (id, slug, title, difficulty, topics, methods) qo'shing.
2. `python/`, `php/` yoki `go/` papkasiga mos nom bilan (masalan, `0015-3sum.py`) asosiy yechimni joylang.
3. `python build.py` buyrug'ini bering — sayt avtomatik yangilanadi.
