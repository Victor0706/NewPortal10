from django import template


register = template.Library()

@register.filter()
def censor1(title):
   if title[1:].islower() == True:
      return(title)
   else:
      return(title.replace(title[1:], '*'))


@register.filter()
def censor2(text):
   if text[1:].islower() == True:
      return(text)
   else:
      return(text.replace(text[1:], '*'))
