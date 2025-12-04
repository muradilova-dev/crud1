# diary/utils.py
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO

def render_to_pdf(template_src, context_dict={}):
    template = render_to_string(template_src, context_dict)
    buffer = BytesIO()
    
    # ВАЖНО: эта строка включает поддержку кириллицы и фото
    pisa_status = pisa.CreatePDF(
        src=template,
        dest=buffer,
        encoding='utf-8',
        link_callback=None
    )
    
    if pisa_status.err:
        return HttpResponse("Ошибка PDF", status=500)
        
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{context_dict["entry"].dish}.pdf"'
    return response