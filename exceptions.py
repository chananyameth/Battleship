class SubmarineGameError(Exception):
    pass


class InvalidVersionError(SubmarineGameError):
    pass


class InvalidMessageCodeError(SubmarineGameError):
    pass


class InvalidMessageError(SubmarineGameError):
    pass


class UnexpectedMessageError(SubmarineGameError):
    pass
