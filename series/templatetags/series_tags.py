from django import template

register = template.Library()

@register.filter
def filter_by_episode(history_queryset, episode_id):
    """Returns the watch history for a specific episode"""
    try:
        return history_queryset.get(episode_id=episode_id)
    except:
        return None 