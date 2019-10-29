from SGU.models import Usuario, Permissions, Grupos

class Gerencia_usuario():
    def Deleta_usuario(delete):
        Permissions.objects.filter(usuario_id=delete).delete()
        Usuario.objects.filter(id=delete).delete()
    
    def Cria_usuario(request, form):
        nomes = request.POST.getlist("grupo")
        form.save()
        username = request.POST.get("username")
        pessoa = Usuario.objects.get(username=username)
        for nome in nomes:
            done = Permissions.objects.create(groups=nome, usuario_id=pessoa.id)
            done.save()


    def Atualiza_usuario(request, username):
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        perm_update = request.POST.getlist("grupo")
        is_active = request.POST.get("is_active")
        pessoa = Usuario.objects.get(username=username)
        perms = []
        grupo = []
        for i in Permissions.objects.filter(usuario_id__id=pessoa.id):
            i = str(i)
            perms.append(i)
        for i in perms:
            if i not in perm_update:
                Permissions.objects.filter(usuario_id__id=pessoa.id, groups=i).delete()
        for i in perm_update:
            if i not in perms:
                Permissions.objects.create(groups=i, usuario_id=pessoa.id)
        for i in Grupos.objects.all():
            i = str(i)
            grupo.append(i)
        for i in Permissions.objects.filter(usuario_id__id=pessoa.id):
            i = str(i)
            perms.append(i)
        if is_active == "on":
            pessoa.is_active = 1
        elif is_active is None:
            pessoa.is_active = 0
        pessoa.nome = nome
        pessoa.email = email
        pessoa.save()
        contexto = {
            "detalhes" : pessoa,
            "grupos" : grupo,
            "perms" : perms,
        }

        return contexto


class Gerencia_permissao():
    def Pega_grupo(request):
        perm = Permissions.objects.filter(usuario_id__username=request.username)
        grupos = []
        for i in perm:
            i = str(i)
            grupos.append(i)
        return grupos