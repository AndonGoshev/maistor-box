from django import template

register = template.Library()

# This tag returns a list of True and False values. All the True values will represent
# a given star.
@register.simple_tag
def rating_stars(given_stars):
    MAX_NUMBER_OF_STARS = 5

    rating_stars = []

    for i in range(1, MAX_NUMBER_OF_STARS+1):
        if i <= given_stars:
            rating_stars.append(True)
        else:
            rating_stars.append(False)

    return rating_stars


