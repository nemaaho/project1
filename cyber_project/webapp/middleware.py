from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if the session has expired
        if request.user.is_authenticated and request.session.get_expiry_age() <= 0:
             # Log the user out
            logout(request)
            return redirect('last/')  # Redirect to login page

        response = self.get_response(request)
        return response
