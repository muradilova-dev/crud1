# diary/utils.py — САМЫЙ ПРОСТОЙ И РАБОЧИЙ PDF В МИРЕ (reportlab)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Image, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from django.http import HttpResponse
from django.conf import settings
import os

def render_to_pdf(template_src, context_dict={}):
    entry = context_dict['entry']
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{entry.dish}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()

    # Русский стиль
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=36,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#5e35b1')
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=20,
        leading=22,
        alignment=TA_JUSTIFY
    )

    # Заголовок
    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width/2, height - 3*cm, entry.dish)

    # Страна
    p.setFont("Helvetica", 28)
    p.drawCentredString(width/2, height - 6*cm, entry.get_country_display())

    # Фото
    if entry.photo:
        photo_path = os.path.join(settings.MEDIA_ROOT, str(entry.photo))
        if os.path.exists(photo_path):
            img = Image(photo_path, width=16*cm, height=12*cm)
            img.hAlign = 'CENTER'
            img.drawOn(p, width/2 - 8*cm, height - 20*cm)

    # Рейтинг
    stars = "★" * entry.rating + "☆" * (5 - entry.rating)
    p.setFont("Helvetica-Bold", 48)
    p.setFillColor(colors.HexColor('#ffb300'))
    p.drawCentredString(width/2, height - 33*cm, stars)
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 24)
    p.drawCentredString(width/2, height - 36*cm, f"{entry.rating}/5")

    # Теги
    if entry.tags:
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(width/2, height - 40*cm, "Теги:")
        tag_list = entry.tag_list()
        x = width/2 - len(tag_list)*2*cm
        for tag in tag_list:
            p.setFillColor(colors.white)
            p.setStrokeColor(colors.HexColor('#667eea'))
            p.roundRect(x, height - 43*cm, 4*cm, 1*cm, 0.5*cm, fill=1)
            p.setFillColor(colors.HexColor('#667eea'))
            p.setFont("Helvetica-Bold", 16)
            p.drawCentredString(x + 2*cm, height - 42.3*cm, f"#{tag}")
            x += 5*cm

    # Описание
    p.setFont("Helvetica", 16)
    desc_y = height - 47*cm if entry.tags else height - 42*cm
    p.drawString(3*cm, desc_y, "Описание:")
    lines = entry.description.split('\n')
    y = desc_y - 1*cm
    for line in lines:
        if y < 5*cm:
            p.showPage()
            y = height - 5*cm
        p.drawString(3*cm, y, line.strip() or " ")
        y -= 0.7*cm

    # Футер
    p.setFont("Helvetica-Oblique", 12)
    p.setFillColor(colors.grey)
    p.drawCentredString(width/2, 2*cm, f"Записано {entry.created_at.strftime('%d %B %Y')} • Мой Кулинарный Дневник")

    p.showPage()
    p.save()
    return response