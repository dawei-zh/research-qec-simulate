r"""
Introduction
------------
qecsim is a Python 3 package for simulating quantum error correction using stabilizer codes.
It is lightweight, modular and extensible, allowing additional codes, error models and decoders to be plugged in.

Components
----------
qecsim includes three key abstract classes: :class:`qecsim.model.StabilizerCode`, :class:`qecsim.model.ErrorModel` and
:class:`qecsim.model.Decoder`.

+-----------------------------+
| Decoder                     |
+=============================+
| | decode(syndrome):recovery |
+-----------------------------+

Execution

"""
