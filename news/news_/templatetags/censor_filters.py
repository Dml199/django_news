import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

BAD_WORDS = ['редиска', 'дурень', 'глупец']  # список запрещённых слов

@register.filter
@stringfilter
def censor(value):
    def censor_word(match):
        word = match.group(0)
        for bad in BAD_WORDS:
            if (word.lower() == bad and
                (word[0].isupper() or word[0].islower()) and
                (len(word) == 1 or word[1:].islower())):
                return word[0] + '*' * (len(word) - 1)
        return word

    pattern = r'\b[А-Яа-яA-Za-z][а-яa-z]*\b'
    return re.sub(pattern, censor_word, value)