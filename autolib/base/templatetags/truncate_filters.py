from django import template  
register = template.Library()  
 
@register.filter("truncatechars")  
def truncate_chars(value, max_length):  
    if value is None or len(value) <= max_length:  
        return value  
  
    truncd_val = value[:max_length]  
    if value[max_length] != " ":  
        rightmost_space = truncd_val.rfind(" ")  
        if rightmost_space != -1:  
            truncd_val = truncd_val[:rightmost_space]  
  
    return truncd_val + "..."   