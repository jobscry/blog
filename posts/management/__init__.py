
from socket import gethostname

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import models as auth_app
from django.contrib.sites.models import Site
from django.contrib.sites.management import create_default_site
from django.contrib.sites import models as sites_app
from django.core.management import call_command
from django.db.models.signals import post_syncdb


def create_user(app, created_models, verbosity, interactive, **kwargs):
    if settings.DEBUG and User in created_models and not interactive:
        if User.objects.count() > 0:
            return
        if verbosity >= 1:
            print
            print ("Creating default account "
                   "(username: admin / password: default) ...")
            print
        args = "admin", "example@example.com", "default"
        User.objects.create_superuser(*args)


def create_site(app, created_models, verbosity, interactive, **kwargs):
    if Site in created_models:
        domain = "127.0.0.1:8000" if settings.DEBUG else gethostname()
        if interactive:
            entered = raw_input("\nA site record is required. Please enter "
                                "the domain and optional port in the format "
                                "'domain:port'. For example 'localhost:8000' "
                                "or 'www.example.com'. Hit enter to use the "
                                "default (%s): " % domain)
            if entered:
                domain = entered.strip("': ")
        if verbosity >= 1:
            print
            print "Creating default Site %s ... " % domain
            print
        Site.objects.create(name="Default", domain=domain)
