from django import template

register = template.Library()

@register.simple_tag
def unread_noti(request):
    user = request.user
    unread = user.notification_set.filter(noti_type="Unread")
    if unread.count() == 0:
        unread = 0
    else:
        unread = unread.count()
    return unread