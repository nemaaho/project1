from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordValidator1():
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!\#\%\&\+\:\;\*\@]"
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': self.min_length})

    def get_help_text(self):
        return "Your password must contain at least one special character (~\!\#\%\&\+\:\;\*\@)."

class PasswordValidator2():
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if str(password).islower():
            raise ValidationError (_('Password must contain at least 1 upper letter.') % {'min_length':self.min_length})

    def get_help_text(self):
        return "Your password must contain at least one upper letter."
