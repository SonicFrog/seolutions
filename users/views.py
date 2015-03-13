from django.views import generic
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **inikwargs):
        view = super(LoginRequiredMixin, cls).as_view(inikwargs)
        return login_required(view)


class UserLoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = "login.html"

    redirection_key = 'redirection'
    default_redirection = '/'

    def get(self, request, *args, **kwargs):
        destination = None
        if self.redirection_key in request.GET.keys():
            destination = request.GET['redirection']
        else:
            destination = self.default_redirection

        if request.user.is_authenticated():
            return HttpResponseRedirect(destination)

        if request.user.is_authenticated():
            return HttpResponseRedirect("/")
        else:
            context = self.get_context_data(*args)
            context[self.redirection_key] = destination
            context['form'] = self.get_form(self.form_class).as_table()
            return self.render_to_response(context, **kwargs)


class UserLogoutView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.get_redirect_url(self, args, kwargs))

    def get_redirect_url(self, *args, **kwargs):
        return "/"


class UserLoginCheckView(generic.edit.ProcessFormView):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if request.user.is_authenticated():
            return HttpResponse()

        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_to = None
                if "redirect" not in request.POST.keys():
                    redirect_to = "/"
                else:
                    redirect_to = request.POST['redirect']
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponseNotAllowed(redirect_to)
        else:
            return HttpResponseNotAllowed()
