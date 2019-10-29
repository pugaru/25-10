from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from SGU.forms import form_usuario, LoginForm
from SGU.models import Grupos, Usuario, Permissions
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.views import login
from src.usuario import Gerencia_usuario, Gerencia_permissao
from django.urls import reverse

# Create your views here.

User_model = get_user_model()

def erro_acesso(request):
    return render(request, "erro_acesso.html")

def checa_sgu(request):
    return 'SGU' in Gerencia_permissao.Pega_grupo(request)

@login_required(login_url='sgu:login')
@user_passes_test(checa_sgu, login_url='sgu:erro_acesso', redirect_field_name=None)
def sgu(request):
    contexto = {
        "users" : Usuario.objects.all()
    } 
    delete = request.POST.get("delete")
    if delete:
        Gerencia_usuario.Deleta_usuario(delete)
    return render(request, "sgu.html", contexto)

'''
class View_Registro(CreateView):
    @method_decorator(user_passes_test(checa_sgu, login_url='sgu:erro_acesso', redirect_field_name=None))
    @method_decorator(login_required(login_url='sgu:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)    
    form_class = form_usuario
    template_name = 'cadastro_usuario.html'
    model = User_model
    success_url = reverse_lazy('sgu:sgu')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grupos'] = Grupos.objects.all()
        return context

registro_usuario = View_Registro.as_view()
'''
@login_required(login_url='sgu:login')
@user_passes_test(checa_sgu, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_usuario(request):    
    if request.method == 'POST':
        form = form_usuario(request.POST)
        if form.is_valid():
            Gerencia_usuario.Cria_usuario(request, form)
            return HttpResponseRedirect(reverse('sgu:sgu'))
        else:
            return HttpResponseRedirect(reverse('sgu:cadastro_usuario'))
    else:
        contexto = {
            "form" : form_usuario(),
            "grupos" : Grupos.objects.all(),
        }            
        return render(request, "cadastro_usuario.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(checa_sgu, login_url='sgu:erro_acesso', redirect_field_name=None)
def detalhes(request, username):
    if request.method == 'POST':
        button = request.POST.get("button")
        contexto = Gerencia_usuario.Atualiza_usuario(request, username)
        if button == "update_continue":
            return HttpResponseRedirect(reverse('sgu:detalhes', kwargs={'username':username}))
        elif button == "update":
            return HttpResponseRedirect(reverse('sgu:sgu'))
    else:
        perms = []
        grupo = []
        detalhes = Usuario.objects.get(username=username)
        perm = Permissions.objects.filter(usuario_id__id=detalhes.id)
        for i in Grupos.objects.all():
            i = str(i)
            grupo.append(i)
        for i in perm:
            i = str(i)
            perms.append(i)
        contexto = {
            "detalhes" : detalhes,
            "grupos" : grupo,
            "perms" : perms,
        }
    return render(request, "detalhes.html", contexto)

@login_required(login_url='sgu:login')
def chg_pass(request):
    if request.method == 'POST':
        pass_old = request.POST.get("pass_old")
        new_pass = request.POST.get("password")
        if User.check_password(request.user, pass_old):
            user = Usuario.objects.get(username=request.user)
            user.set_password(new_pass)
            user.save()
            return HttpResponseRedirect(reverse('sgu:logout'))
        else:
            print ("Senha incorreta")
    return render(request, "chg_pass.html")

def loginAdminPanel(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = Usuario.objects.get(username=username)
            if usuario.tipo == 'E':
                account = authenticate(username=username, password=password)
                if account is not None:
                    login(request, account)
                    return HttpResponseRedirect(reverse('principal'))
                else:
                    messages.error(request, 'Usuário ou senha Incorretos!')
            else:
                messages.warning(request, 'Você não tem permissões administrativas!')
        else:
            messages.error(request, 'Formulário inválido!')
    else:
        form = LoginForm()
        context = {'form':form}
    return render(request, "login_admin.html", context)