from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def la_permission(context, intitule_permission):
    user = context['request'].user
    if user.is_authenticated and hasattr(user, 'role') and user.role:
        return user.role.permission.filter(permission=intitule_permission).exists()
    return False
