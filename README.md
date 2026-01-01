# HilAnchor Bot 🙂

בוט טלגרם אישי לעקוב אחרי התקדמות היום בצורה עדינה ותומכת.

## תכונות עיקריות

- ✅ **מעקב יומי** - צ'ק-אין אוטומטי ב-11:00, 14:00, 17:00
- 📊 **סיכומים יומיים** - סיכום של כל הפעילות והתקדמות
- 📓 **יומן אישי** - שמירת מחשבות והרגשות פרטיות
- 💬 **טקסט חופשי** - אפשרות לשלוח מחשבות בכל רגע
- 🎯 **ליווי תומך** - עזרה בפירוק משימות גדולות ומעקב אחר התקדמות
- 🔒 **פרטיות מלאה** - הבוט מוגבל למשתמש אחד בלבד (OWNER_USER_ID)

## סביבת הפיתוח

- **Python**: 3.9.7
- **מערכת הפעלה**: Windows
- **ספריות עיקריות**:
  - `python-telegram-bot` - ממשק עם Telegram API
  - `httpx` - בקשות HTTP (תומך proxy)
  - `python-dotenv` - ניהול משתני סביבה
  - `pytz` - ניהול אזורי זמן
  - `ollama` - אינטגרציה עם מודלי LLM (אופציונלי)

## התקנה

### 1. שכפול הפרויקט
```bash
git clone <repository-url>
cd HilAnchor_bot
```

### 2. יצירת סביבה וירטואלית
```bash
python -m venv .venv
.venv\Scripts\activate  # ב-Windows
```

### 3. התקנת תלויות
```bash
pip install -r requirements.txt
```

### 4. הגדרת קובץ .env
צור קובץ `.env` בתיקיית הפרויקט עם התוכן הבא:

```env
# חובה - מידע בסיסי
BOT_TOKEN=your_telegram_bot_token_here
OWNER_USER_ID=your_telegram_user_id_here

# אופציונלי - נתיבים מותאמים אישית
STATE_PATH=state.json
JOURNAL_PATH=personal_journal.txt

# אופציונלי - אינטגרציה עם LLM
USE_LLM=false
LLM_MODEL=llama3.2:3b

# אופציונלי - Proxy (אם הרשת חוסמת Telegram)
PROXY_URL=http://your-proxy:port
```

#### איך לקבל BOT_TOKEN?
1. פתח שיחה עם [@BotFather](https://t.me/botfather) בטלגרם
2. שלח `/newbot` וענה על השאלות
3. העתק את ה-TOKEN שתקבל

#### איך לקבל OWNER_USER_ID?
1. פתח שיחה עם [@userinfobot](https://t.me/userinfobot)
2. הבוט ישלח לך את ה-ID שלך

### 5. הרצת הבוט
```bash
python run.py
```

## פקודות זמינות

- `/start` - התחלת הבוט ובחירת מצב היום
- `/checkin` - צ'ק-אין ידני
- `/summary` - סיכום היום עד עכשיו
- `/journal` - קריאת היומן האישי
- `/journal_add` - הוספת רשומה ליומן האישי
- `/journal_info` - סטטיסטיקה על היומן

## יצירת קובץ EXE

### התקנת PyInstaller
```bash
pip install pyinstaller
```

### יצירת EXE עם אייקון
```bash
pyinstaller --onefile --icon=handshake.ico --name=HilAnchor run.py
```

#### פרמטרים:
- `--onefile` - יוצר קובץ EXE בודד
- `--noconsole` - מסתיר את חלון הקונסול (אופציונלי, תלוי אם רוצים לראות logs)
- `--icon=handshake.ico` - מגדיר את האייקון של ה-EXE
- `--name=HilAnchor` - שם הקובץ הסופי

הקובץ יישמר בתיקייה `dist\HilAnchor.exe`

### חשוב לשים לב:
1. **קובץ .env**: יש להעתיק את קובץ `.env` לאותה תיקייה שבה נמצא ה-EXE
2. **קבצי State**: הקבצים `state.json` ו-`personal_journal.txt` ייווצרו אוטומטית
3. **Ollama** (אם USE_LLM=true): צריך להיות מותקן ורץ במחשב

## מבנה הפרויקט

```
HilAnchor_bot/
├── run.py                    # נקודת כניסה ראשית
├── handshake.ico            # אייקון הבוט
├── requirements.txt         # תלויות Python
├── .env                     # משתני סביבה (לא ב-git)
├── state.json              # מצב הבוט (נוצר אוטומטית)
├── personal_journal.txt    # יומן אישי (נוצר אוטומטית)
└── hilanchor/
    ├── __init__.py
    ├── config.py           # הגדרות ומשתני סביבה
    ├── auth.py             # אימות משתמשים
    ├── state_store.py      # ניהול מצב הבוט
    ├── keyboards.py        # מקלדות אינטראקטיביות
    ├── messages.py         # כל הודעות הבוט
    ├── scheduler.py        # משימות מתוזמנות
    ├── summary.py          # יצירת סיכומים
    ├── journal.py          # ניהול היומן האישי
    ├── llm.py             # אינטגרציה עם LLM
    ├── nudges.py          # תזכורות
    ├── services/
    │   └── flow.py        # לוגיקת flow הבוט
    └── handlers/
        ├── __init__.py
        ├── commands.py    # מטפלי פקודות
        ├── free_text.py   # מטפל טקסט חופשי
        ├── patterns.py    # דפוסי callback
        └── callbacks/     # מטפלי כפתורים
            ├── mode.py
            ├── worked.py
            ├── noreason.py
            ├── bigaction.py
            ├── yesnext.py
            └── nudge.py
```

## Proxy Configuration

אם הרשת שלך חוסמת Telegram, תוכל להגדיר Proxy בקובץ `.env`:

```env
# HTTP Proxy
PROXY_URL=http://your-proxy-server:port

# או SOCKS5 Proxy
PROXY_URL=socks5://your-proxy-server:port
```

## פתרון בעיות נפוצות


### LLM לא עובד
- ודא ש-Ollama מותקן ורץ (`ollama serve`)
- בדוק שהמודל קיים (`ollama list`)
- אם לא צריך LLM, השאר `USE_LLM=false`

## רישיון

פרויקט פרטי לשימוש אישי.

## יצירת קשר

לשאלות ובעיות, פנה למפתח הפרויקט.
