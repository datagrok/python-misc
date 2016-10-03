class STFUAdminIsPopupMiddleware(object):
    """Silence complaints about is_popup variable in admin templates.

    Django 1.9 adds a django.template logger, with a DEBUG level
    message for missing context variables. This is helpful to track down
    possibly misspelled variable names in templates, etc.:
    https://docs.djangoproject.com/en/1.10/releases/1.9/#templates

    The Django admin uses a check against a variable 'is_popup' in the
    base.html template and several other places. But as of 1.9 and 1.10
    that variable being undefined is a completely expected situation;
    the template logic relies on undefined variables evaluating false
    without throwing errors!

    This middleware sets it to a default of False when it is not
    defined, so we don't see these three tracebacks and 100 lines of
    garbage on every single admin pageview!

        Traceback (most recent call last):
        File "...lib/python3.5/site-packages/django/template/base.py", line 889, in _resolve_lookup
            if isinstance(current, BaseContext) and getattr(type(current), bit):
        AttributeError: type object 'RequestContext' has no attribute 'is_popup'

        During handling of the above exception, another exception occurred:

        Traceback (most recent call last):
        File "...lib/python3.5/site-packages/django/template/base.py", line 898, in _resolve_lookup
            current = current[int(bit)]
        ValueError: invalid literal for int() with base 10: 'is_popup'

        During handling of the above exception, another exception occurred:

        Traceback (most recent call last):
        File "...lib/python3.5/site-packages/django/template/base.py", line 905, in _resolve_lookup
            (bit, current))  # missing attribute
        django.template.base.VariableDoesNotExist: Failed lookup for key
        [is_popup] in "[{'True': True, 'None': None, 'False': False}, {'messages':
        ...
        <50 lines of junk>
        ...

    Related: https://github.com/tomchristie/django-rest-framework/issues/3736

    """
    def process_template_response(self, request, response):
        for key in ['is_popup', 'errors']:
            response.context_data.setdefault(key, None)
        return response
