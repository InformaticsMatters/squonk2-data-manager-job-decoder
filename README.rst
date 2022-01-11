Informatics Matters Data Manager Job Decoder
============================================

.. image:: https://badge.fury.io/py/im-data-manager-job-decoder.svg
   :target: https://badge.fury.io/py/im-data-manager-job-decoder
   :alt: PyPI package (latest)

Installation (Python)
=====================

The Job decoder is published on `PyPI`_ and can be installed from
there::

    pip install im-data-manager-job-decoder

Once installed you can access the protocol buffers with:

>>> from decoder import decoder
>>> decoder.decode(text, variables, 'command', decoder.TextEncoding.JINJA2_3_0)

.. _PyPI: https://pypi.org/project/im-data-manager-job-decoder

Get in touch
============

- Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/informaticsmatters/data-manager-job-decoder
