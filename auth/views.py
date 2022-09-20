import contextlib
from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
import msal
from django.core.cache import cache as django_cache
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login


User = get_user_model()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        settings.CLIENT_ID,
        authority=authority or settings.AUTHORITY,
        client_credential=settings.CLIENT_SECRET,
        token_cache=cache,
    )


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [], redirect_uri="http://localhost:5000/getAToken", state="hello"
    )


def index(request, *args, **kwargs):
    button = (
        f"<h3>Hello {request.user.first_name}</h3>"
        if request.user.is_authenticated
        else f"""<button><a href='{reverse("login")}' blank=True>Sign In</a></button>"""
    )

    html = f"""
    <h1>Azure AD Auth</h1>
    {button}
    """
    return HttpResponse(html)


def login(request, *args, **kwargs):
    auth_url = _build_auth_code_flow(scopes=settings.SCOPE)
    django_cache.set("flow", auth_url)
    return HttpResponseRedirect(auth_url.get("auth_uri"))


def ad_callback(request, *args, **kwargs):
    result = _build_msal_app().acquire_token_by_auth_code_flow(django_cache.get("flow", {}), request.GET)
    if "error" in result:
        return HttpResponse(f"<h1>{result.get('error')}</h1><p>{result.get('error_description')}</p>")
    # create user
    email = result.get("id_token_claims").get("preferred_username")
    profile_info = {
        "username": email.rsplit("@", 1)[0],
        "email": email,
        "first_name": result.get("id_token_claims").get("name"),
    }
    extra_fields = {"is_staff": False, "is_superuser": False}

    user = User(**profile_info, **extra_fields)
    user.set_unusable_password()
    user.full_clean()
    user.save()
    django_login(request, user)
    user.refresh_from_db()
    return HttpResponseRedirect(reverse("index"))
