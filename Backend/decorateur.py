from django.http import HttpResponseForbidden


def permission_requise(intitule_permission):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            utilisateur = request.user
            if utilisateur.is_authenticated and utilisateur.role:
                permissions = utilisateur.role.permission.values_list('permission', flat=True)
                if intitule_permission in permissions:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Accès refusé : permission insuffisante.")
        return _wrapped_view
    return decorator
