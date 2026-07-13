# 💬 Gemini Chatbot + SQLite (suhbatni saqlash va davom ettirish)

Terminal orqali ishlaydigan chatbot. Har bir xabar SQLite bazasiga yoziladi,
dastur qayta ishga tushirilganda oxirgi suhbat **avtomatik tiklanadi** —
bot nafaqat eski xabarlarni ko'rsatadi, balki `previous_interaction_id`
orqali oldingi kontekstni ham haqiqatan "eslaydi".

## ✅ Vazifa talablari qanday bajarildi

| Talab | Qayerda |
|---|---|
| Har bir xabar (session ID, matn, turi, vaqt) saqlanadi | `database.py` → `messages` jadvali |
| Jadval strukturasi | `database.py` → `init_db()` |
| SQLite | `sqlite3` (standart kutubxona) |
| Oxirgi sessiyani aniqlash va tiklash | `database.py` → `get_last_session_id()` |
| Terminal (CLI) orqali ishlash | `main.py` |
| Modul tarzida yozilgan kod | 4 ta alohida fayl: `config`, `database`, `chat_client`, `main` |
| Exception handling | har bir modulda maxsus exception klasslari + try/except |

## 🗂️ Fayl tuzilishi

```
chat-db-homework/
├── main.py           # CLI kirish nuqtasi — suhbat sikli shu yerda
├── database.py        # SQLite: sessiyalar va xabarlarni saqlash/o'qish
├── chat_client.py      # Gemini API wrapper (interactions.create)
├── config.py           # .env dan sozlamalarni o'qish
├── requirements.txt
├── .env.example        # qaysi environment o'zgaruvchilar kerakligi namunasi
├── .gitignore
└── README.md
```

## ⚙️ O'rnatish

```bash
# 1) Repo'ni klon qiling (yoki papkani oching)
cd chat-db-homework

# 2) Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3) Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 4) .env faylini yarating
cp .env.example .env
# keyin .env faylni oching va GOOGLE_API_KEY ni haqiqiy qiymatga almashtiring
```

## ▶️ Ishga tushirish

```bash
python main.py
```

- Birinchi marta ishga tushirganda — yangi sessiya yaratiladi.
- Dasturni to'xtatib (`exit` yozing yoki Ctrl+C), qayta ishga tushirsangiz —
  oldingi suhbat avtomatik tiklanadi.

## 🗄️ Baza sxemasi

**`sessions`** — har bir suhbat "seansi"

| ustun | tavsif |
|---|---|
| `id` | sessiya ID (PK) |
| `created_at` | yaratilgan vaqt |
| `updated_at` | oxirgi faollik vaqti (eng oxirgisini topish uchun) |
| `last_interaction_id` | Gemini'dagi oxirgi javob ID — kontekstni davom ettirish uchun |

**`messages`** — har bir xabar

| ustun | tavsif |
|---|---|
| `id` | xabar ID (PK) |
| `session_id` | qaysi sessiyaga tegishli (FK → sessions.id) |
| `role` | `'user'` yoki `'system'` |
| `content` | xabar matni |
| `created_at` | yuborilgan vaqt |

## 🧠 Qanday ishlaydi (resume mexanizmi)

```
Dastur ishga tushadi
        │
        ▼
sessions jadvalida yozuv bormi?
        │
   ┌────┴────┐
   yo'q      bor
   │           │
yangi       eski xabarlarni ekranga chiqar
session     + last_interaction_id ni o'qi
yaratiladi         │
   │               ▼
   └──────►  suhbat davom etadi
             (har javobdan keyin DB yangilanadi)
```

Muhim nozik joy: `previous_interaction_id`. Bu — Gemini'ning yangi
`interactions` API'sida har bir javobga biriktirilgan ID. Keyingi so'rovda
shuni yuborsak, model butun tarixni qayta yubormasdan ham oldingi
xabarlarni "eslaydi" (kontekst server tomonida saqlanadi). Biz bu ID ni
`sessions.last_interaction_id` ustunida saqlaymiz — shu sababli dastur
o'chib-yonganda ham bot xotirasini yo'qotmaydi, shunchaki eski log emas.

## 🚀 GitHub'ga joylash

```bash
git init
git add .
git commit -m "Homework: SQLite bilan suhbat tarixini saqlash va tiklash"

# GitHub saytida yangi (bo'sh!) repository yarating, keyin:
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

⚠️ **`.env` faylingiz hech qachon commit qilinmasin.** `.gitignore` buni
avtomatik oldini oladi, lekin push qilishdan oldin `git status` bilan
tekshirib ko'ring — agar `.env` ro'yxatda ko'rinsa, uni commit qilmang.

## 💡 Kengaytirish g'oyalari (o'zingiz sinab ko'rish uchun)

- `/new` buyrug'i — dasturni qayta ishga tushirmasdan yangi sessiya ochish
- Bir nechta parallel sessiyalarni boshqarish (sessiyalar ro'yxatini ko'rsatish)
- Suhbatni `.txt` yoki `.json` ga eksport qilish
- `SQLAlchemy` ga o'tish (katta loyihalarda ORM qulayroq bo'ladi)
