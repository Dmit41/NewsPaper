from django import template

register = template.Library()


@register.filter()
def censor(text, word=str):
    if word in text:
        reword = word[0] + ((len(word) - 2) * "*") + word[-1]
        text = text.replace(word, reword)
    return text
