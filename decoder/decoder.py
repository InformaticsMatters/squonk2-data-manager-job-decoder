"""A module to decode text strings based on an encoding.

This is typically used by the Data Manager's API instance methods
when launching applications (and Jobs) where text requires decoding,
given a 'template' string and a 'dictionary' of parameters and values.
"""
import enum
from typing import Dict, Optional, Tuple

# The decoding engine implementations.
# The modules are expected to be called 'decode_<TextEncoding.lower()>'
from . import decode_jinja2_3_0


class TextEncoding(enum.Enum):
    """A general text encoding format, used initially for Job text fields.
    """
    JINJA2_3_0 = 1      # Encoding that complies with Jinja2 v3.0.x


def decode(template_text: str,
           variable_map: Optional[Dict[str, str]],
           subject: str,
           template_engine: TextEncoding) -> Tuple[str, bool]:
    """Given some text and a 'variable map' (a dictionary of keys and values)
    this returns the decoded text (using the named engine) as a string
    and a boolean set to True. On failure the boolean is False and the returned
    string is an error message.

    The 'subject' is a symbolic reference to the text
    used for error reporting so the client understands what text is
    in error. i.e. if the text is for a 'command'
    the subject might be 'command'.
    """
    assert template_text
    assert subject
    assert template_engine

    # If there are no variables just return the template text
    if variable_map is None:
        return template_text, True

    if template_engine.name.lower() == 'jinja2_3_0':
        return decode_jinja2_3_0.decode(template_text, variable_map, subject)

    # Unsupported engine if we get here!
    return f'Unsupported template engine: {template_engine}', False
