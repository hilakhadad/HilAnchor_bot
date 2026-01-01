# 🧪 טסטים לבוט HilAnchor

קובץ זה מסביר איך להריץ את הטסטים עבור הבוט.

## 📋 מה נבדק?

### `test_messages.py` - טסטים להודעות
- ✅ כל ההודעות קיימות ולא ריקות
- ✅ הודעות דינמיות (פונקציות) עובדות נכון
- ✅ כפתורים לא ארוכים מדי
- ✅ הודעות מכילות תוכן בעברית
- ✅ עקביות בין הודעות שונות

### `test_bot_functionality.py` - טסטים לפונקציונליות
- ✅ מבנה של keyboards (כפתורים)
- ✅ callback data נכון
- ✅ ניהול state (מצב)
- ✅ יצירת סיכום יומי
- ✅ אינטגרציה עם LLM
- ✅ סוגי events בסיכום

## 🚀 איך להריץ?

### התקנת pytest (פעם ראשונה)

```bash
pip install pytest pytest-asyncio
```

### הרצת כל הטסטים

```bash
# מהתיקייה הראשית של הפרויקט
pytest tests/

# או עם פירוט מלא
pytest tests/ -v
```

### הרצת טסט ספציפי

```bash
# רק טסטים להודעות
pytest tests/test_messages.py -v

# רק טסטים לפונקציונליות
pytest tests/test_bot_functionality.py -v

# טסט ספציפי אחד
pytest tests/test_messages.py::TestCommandMessages::test_start_message_exists -v
```

### הרצה עם כיסוי (coverage)

```bash
# התקנה
pip install pytest-cov

# הרצה
pytest tests/ --cov=hilanchor --cov-report=html

# הדו"ח יישמר ב-htmlcov/index.html
```

## 📊 פלט מצופה

```
================================ test session starts ================================
collected 87 items

tests/test_messages.py ................................................. [ 52%]
tests/test_bot_functionality.py ..................................       [100%]

================================ 87 passed in 2.35s =================================
```

## 🔧 מה לעשות אם טסט נכשל?

אם טסט נכשל, זה אומר שמשהו השתנה בקוד שעלול לשבור את הבוט:

1. **קרא את הודעת השגיאה** - pytest יראה בדיוק מה נכשל
2. **בדקי אם השינוי היה מכוון** - אם שינית משהו ב-messages.py, אולי צריך לעדכן את הטסט
3. **תקני את הקוד או הטסט** - תלוי אם השינוי היה מכוון או טעות

### דוגמה לשגיאה

```
FAILED tests/test_messages.py::TestCommandMessages::test_start_message_exists
AssertionError: assert '/checkin' in ''
```

זה אומר שההודעה START_MESSAGE לא מכילה את `/checkin` - צריך לבדוק אם זה נמחק בטעות.

## 🎯 למה חשוב להריץ טסטים?

- 🛡️ **מגן מפני שגיאות** - אם שינית משהו ושברת משהו אחר, תדעי מיד
- 📝 **תיעוד** - הטסטים מראים איך הקוד אמור לעבוד
- 🔄 **שינויים בטוחים** - אפשר לשנות הודעות בביטחון שלא נשבר דבר
- 🚀 **פיתוח מהיר** - גילוי בעיות מהר לפני שהבוט רץ

## 💡 טיפים

1. **הריצי טסטים לפני כל שינוי גדול** - וודאי שהכל עובד
2. **הריצי טסטים אחרי שינוי** - וודאי שלא שברת משהו
3. **אם הוספת הודעה חדשה** - הוסיפי לה טסט ב-test_messages.py
4. **אם שינית פונקציונליות** - עדכני את הטסט המתאים

## 📚 מידע נוסף על pytest

- [תיעוד pytest](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - לטסטים async
- [Coverage.py](https://coverage.readthedocs.io/) - מדידת כיסוי טסטים
