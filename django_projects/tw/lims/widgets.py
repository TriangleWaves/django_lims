from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):
    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            url = value.url
            output.append("<img src='%s' alt='' /><br/>" % (url[:url.rfind('/')+1] + "tmb_" + url[url.rfind('/')+1:],))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class AdminStatusWidget(AdminFileWidget):
    def __init__(self, attrs={}):
        super(AdminStatusWidget, self).__init__(attrs)


