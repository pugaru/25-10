from SGU.models import Grupos, Permissions

def header(request):
    perm = Permissions.objects.filter(usuario_id__username=request.user)
    grupo = Grupos.objects.all()
    contexto = {'perm':perm, 'grupo': grupo}
    return contexto