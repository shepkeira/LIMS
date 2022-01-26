from django import template

register = template.Library()


# Takes a user and group name and returns a boolean whether the user is in the group
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
