from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author_page.html'
    
class AboutTechView(TemplateView):
    template_name = 'about/tech_page.html'

class AboutContactView(TemplateView):
    template_name = 'about/contact_page.html'
