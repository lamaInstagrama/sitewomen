from django.contrib.auth.models import Group


def new_users_handler(backend, user, response, *args, **kwargs):
    social = Group.objects.filter(name='social')
    if len(social):
        user.groups.add(social[0])
