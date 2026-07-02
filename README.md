# 🏢  Сайт D4 Technologies

## 📋 Требования

Установить [Docker Desktop](https://www.docker.com/products/docker-desktop/) и запусти его.

---

## 🚀 Запуск

Открыть терминал в папке `D4Site/` и выполнить:

```bash
cd d4_django
docker compose up -d --build
```

⏳ Подождать 30–60 секунд пока всё поднимется.

🌐 Сайт: http://localhost:8000

---

## 👤 Создание админ-панели

```bash
docker compose exec web python manage.py createsuperuser
```

- Ввести имя пользователя
- Ввести емейл (по желанию)
- Ввести надежный пароль


🔐 Админка: http://localhost:8000/admin/

---

## ⏹️ Остановка

```bash
docker compose down
```

---

## 🌍 Продакшен

В файле `.env` поменяй:

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=<новый ключ — см. ниже>
DB_PASSWORD=<надёжный пароль>
```

🔑 Сгенерировать новый `SECRET_KEY`:

```bash
docker compose exec web python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## 🔧 Просмотр логов

```bash
docker compose logs web -f
```
