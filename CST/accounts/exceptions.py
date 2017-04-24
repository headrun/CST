from common_exceptions.common import CommonBaseException


class InvalidUserNameOrPasswordError(CommonBaseException):
    message = 'Username or password provided are in correct'
    error_code = 'invalidUserNameOrPassword'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class AccountDisabledError(CommonBaseException):
    message = 'Account is disabled, contact support'
    error_code = 'accountDisabled'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class AnauthorizedEmailIdError(CommonBaseException):
    message = 'Email id not authorized'
    error_code = 'anauthorizedEmailId'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class UsernameAlreadyExistError(CommonBaseException):
    message = 'Username already exist'
    error_code = 'usernameAlreadyExist'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class EmailAlreadyExistError(CommonBaseException):
    message = 'Email already exist'
    error_code = 'emailAlreadyExist'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)


class UserAlreadyLoggedInError(CommonBaseException):
    message = 'The user is already logged in'
    error_code = 'userAlreadyLoggedIn'

    def __init__(self):
        CommonBaseException.__init__(self, self.message, self.error_code)
