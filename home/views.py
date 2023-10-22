from django.views import generic
from django.apps import apps
import os

class appdata():
    def __init__(self):
        self.link = None
        self.name = None

class IndexView(generic.ListView):
    template_name = "home/main.html"
    context_object_name = "applications"

    def get_queryset(self):
        """Return the last five published questions."""
        dirlist_parent = [dir for dir in os.listdir(".") if os.path.isdir(f"./{dir}")]
        applications = [app for app in dirlist_parent if "apps.py" in os.listdir(f"./{app}")]
        placeholder = []
        print(os.listdir(".."))
        for application in applications:
            application = apps.get_app_config(application)
            app = appdata()
            app.link = application.label+":index"
            app.name = application.verbose_name
            placeholder.append(app)
        return placeholder