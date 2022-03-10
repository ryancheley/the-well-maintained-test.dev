import subprocess
from django.views.generic import TemplateView
from allauth.socialaccount.models import SocialToken


class HomePageTemplateView(TemplateView):
    template_name = "twmt/index.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        search = request.GET.get('package')
        if search:
            batcmd= f'the-well-maintained-test package {search}'
        else:
            user_id = request.user.id
            try:
                gh_token = SocialToken.objects.filter(account__user=user_id).values()[0].get('token')
                batcmd= f'the-well-maintained-test check -s {gh_token}'
            except IndexError:
                batcmd= f'the-well-maintained-test check'
        try:
            result = subprocess.check_output(batcmd, shell=True).decode("utf-8") 
        except:
            result = "Package needs to be updated"
        context['result'] = result
        return self.render_to_response(context)
        