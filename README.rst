Informatics Matters Data Manager Job Decoder
============================================

.. image:: https://badge.fury.io/py/im-data-manager-job-decoder.svg
   :target: https://badge.fury.io/py/im-data-manager-job-decoder
   :alt: PyPI package (latest)

A package that simplifies the decoding of encoded text strings.
Given an encoded string the ``decode()`` method
returns the decoded value or an error.

For example, given the following `jinja2`_ encoded string
``'{{ foo }}, bar={{ bar }}, baz={{ baz }}'`` and variable map
``{'foo': 1, 'bar': 2, 'baz': 3}`` the decoder returns
the string ``'foo=1, bar=2, baz=3'``.

The following encoding/decoding formats are supported: -

- jinja2 (3.0)

.. _jinja2: https://jinja.palletsprojects.com/en/3.0.x/

Installation (Python)
=====================

The Job decoder is published on `PyPI`_ and can be installed from
there::

    pip install im-data-manager-job-decoder

Once installed you can access the protocol buffers with:

>>> from decoder import decoder
>>> decoded, success = decoder.decode(text, variables, 'command', decoder.TextEncoding.JINJA2_3_0)

.. _PyPI: https://pypi.org/project/im-data-manager-job-decoder

Get in touch
============

- Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/informaticsmatters/data-manager-job-decoder
