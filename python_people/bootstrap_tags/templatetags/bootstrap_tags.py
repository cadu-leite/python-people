from django import template
import django

register = template.Library()

@register.simple_tag
def bootstrap_form(obj, required=False):
    '''
    the required param, is only used when obj = Field for optional required fields.
    '''
    
    if isinstance(obj, django.forms.BaseForm):
        return form(obj)
    elif isinstance(obj, django.forms.forms.BoundField):
        return form_field(obj)
    else:
        raise Exception, 'Bootstrap template tag recieved a non form or field object'



def form_field(field, required=False):
    t = template.loader.get_template('bootstrap_tags/form_field.html')
    return t.render(template.Context({'field': field, 'required': required}))


def form(form):
    form_html = ''
    t = template.loader.get_template('bootstrap_tags/form_field.html')
    
 
    for fld in form.visible_fields():
        row = t.render(template.Context({'field': fld,}))
        #form_html += u'<div class="clearfix"> {field_html} </div>'.format(field_html=row)  
        form_html += '<div class="clearfix"> %s </div>' %(row) #meet python 2.5
    
    for fld in form.hidden_fields():
        row = unicode(fld)
        form_html += u'<div style="display:none;"> %s </div>' %(row)  
    
    
    return form_html
