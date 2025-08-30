def pluralize(value, singular, plural=None):
    if plural is None:
        plural = singular + "s"
    return f"{value} {singular if value == 1 else plural}"
