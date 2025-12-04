# diary/models.py
from django.db import models
from django.contrib.auth.models import User

# Список стран (ISO код + название)
COUNTRIES = [
    ('AF', 'Афганистан'), ('AX', 'Аландские острова'), ('AL', 'Албания'), ('DZ', 'Алжир'),
    ('AR', 'Аргентина'), ('AM', 'Армения'), ('AU', 'Австралия'), ('AT', 'Австрия'),
    ('AZ', 'Азербайджан'), ('BH', 'Бахрейн'), ('BD', 'Бангладеш'), ('BY', 'Беларусь'),
    ('BE', 'Бельгия'), ('BR', 'Бразилия'), ('BG', 'Болгария'), ('CA', 'Канада'),
    ('CN', 'Китай'), ('CO', 'Колумбия'), ('HR', 'Хорватия'), ('CU', 'Куба'),
    ('CZ', 'Чехия'), ('DK', 'Дания'), ('EG', 'Египет'), ('EE', 'Эстония'),
    ('FI', 'Финляндия'), ('FR', 'Франция'), ('GE', 'Грузия'), ('DE', 'Германия'),
    ('GR', 'Греция'), ('HU', 'Венгрия'), ('IS', 'Исландия'), ('IN', 'Индия'),
    ('ID', 'Индонезия'), ('IR', 'Иран'), ('IQ', 'Ирак'), ('IE', 'Ирландия'),
    ('IL', 'Израиль'), ('IT', 'Италия'), ('JP', 'Япония'), ('JO', 'Иордания'),
    ('KZ', 'Казахстан'), ('KG', 'Кыргызстан'), ('KR', 'Южная Корея'), ('KW', 'Кувейт'),
    ('LV', 'Латвия'), ('LB', 'Ливан'), ('LT', 'Литва'), ('MY', 'Малайзия'),
    ('MX', 'Мексика'), ('MA', 'Марокко'), ('NL', 'Нидерланды'), ('NZ', 'Новая Зеландия'),
    ('NO', 'Норвегия'), ('PK', 'Пакистан'), ('PE', 'Перу'), ('PH', 'Филиппины'),
    ('PL', 'Польша'), ('PT', 'Португалия'), ('QA', 'Катар'), ('RO', 'Румыния'),
    ('RU', 'Россия'), ('SA', 'Саудовская Аравия'), ('RS', 'Сербия'), ('SG', 'Сингапур'),
    ('SK', 'Словакия'), ('SI', 'Словения'), ('ES', 'Испания'), ('SE', 'Швеция'),
    ('CH', 'Швейцария'), ('SY', 'Сирия'), ('TW', 'Тайвань'), ('TH', 'Таиланд'),
    ('TR', 'Турция'), ('UA', 'Украина'), ('AE', 'ОАЭ'), ('GB', 'Великобритания'),
    ('US', 'США'), ('UY', 'Уругвай'), ('UZ', 'Узбекистан'), ('VN', 'Вьетнам'),
    # Добавь ещё, если нужно
]

RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.CharField(max_length=200, verbose_name="Название блюда")
    country = models.CharField(max_length=2, choices=COUNTRIES, verbose_name="Страна")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг")
    description = models.TextField(verbose_name="Впечатления")
    photo = models.ImageField(upload_to='dishes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    
    # ← НОВОЕ ПОЛЕ ДЛЯ ТЕГОВ
    tags = models.CharField(max_length=300, blank=True, verbose_name="Теги (через запятую)")

    def __str__(self):
        return f"{self.dish} — {self.get_country_display()}"

    # ← МЕТОД ДЛЯ РАБОТЫ С ТЕГАМИ
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]