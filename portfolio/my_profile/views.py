from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.views.generic.base import View

from my_profile.backend import get_client_ip
from my_profile.forms import SendEmailForm
from my_profile.models import MyProfile, Visitors, IpAddress


# Create your views here.

class Index(View):
    template_name = "profile/profile.html"

    def get(self, request):
        if request.session.get('new', True):
            request.session['new'] = False
            visitor = Visitors.objects.create()
            visitor.count += 1
            visitor.save()
            request.session['user_code'] = visitor.code
            ip = get_client_ip(request)
            IpAddress.objects.create(visitor=visitor, address=ip)
        else:
            code = request.session.get('user_code', 0)
            try:
                visitor = Visitors.objects.get(code=code)
                visitor.count += 1
                visitor.save()
                ip = get_client_ip(request)
                IpAddress.objects.create(visitor=visitor, address=ip)
            except Visitors.DoesNotExist:
                pass

        profile = MyProfile.objects.all().first()
        links = profile.links_set.all()
        stacks = profile.stack_set.all()
        experiences = profile.workexperience_set.order_by('-start')
        educations = profile.education_set.order_by('-start')
        applications = profile.application_set.all()
        services = profile.service_set.all()

        context = {
            'profile': profile,
            'links': links,
            'stacks': stacks,
            'experiences': experiences,
            'educations': educations,
            'applications': applications,
            'services': services
        }

        return render(request, self.template_name, context)


class SendEmail(View):
    template_name = "profile/profile.html"

    def post(self, request):
        form = SendEmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile:index")

        return redirect("profile:index")
