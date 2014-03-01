class BaseBox(object):
    """
    A base class for polymorphic boxes that wrap parser results. Simply use
    this as a base class for anything you return in a production function of a
    parser. This is necessary because RPython unlike Python expects functions
    to always return objects of the same type.
    """
    _attrs_ = []


class Token(BaseBox):
    """
    Represents a syntactically relevant piece of text.

    :param name: A string describing the kind of text represented.
    :param value: The actual text represented.
    :param source_pos: A :class:`SourcePosition` object representing the
                       position of the first character in the source from which
                       this token was generated.
    """
    def __init__(self, name, value, before_space="", after_space="", hidden_tokens_before=None, hidden_tokens_after=None):
        self.name = name
        self.value = value
        self.before_space = before_space
        self.after_space = after_space
        self.hidden_tokens_before = map(lambda x: Token(*x), hidden_tokens_before if hidden_tokens_before else [])
        self.hidden_tokens_after = map(lambda x: Token(*x), hidden_tokens_after if hidden_tokens_after else [])

    def __repr__(self):
        return "Token(%r, %r)" % (self.name, self.value)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def render(self):
        return self.before_space + self.value + self.after_space

    def gettokentype(self):
        """
        Returns the type or name of the token.
        """
        return self.name

    def getstr(self):
        """
        Returns the string represented by this token.
        """
        return self.value


class SourcePosition(object):
    """
    Represents the position of a character in some source string.

    :param idx: The index of the character in the source.
    :param lineno: The number of the line in which the character occurs.
    :param colno: The number of the column in which the character occurs.

    The values passed to this object can be retrieved using the identically
    named attributes.
    """
    def __init__(self, idx, lineno, colno):
        self.idx = idx
        self.lineno = lineno
        self.colno = colno
