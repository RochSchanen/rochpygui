# "visa.py"
# content; VISA interface
# author; Roch schanen
# created; 2020 April 23
# repository; https://github.com/RochSchanen/rochpygui

# todo: check platform and libraries to define the VISA backend to be used
# todo: send email to "pyvisa-py" gihub project about closing error

# gpib_ctypes: https://gpib-ctypes.readthedocs.io/en/latest/index.html
from gpib_ctypes import make_default_gpib as _gpibSetup
_gpibSetup() # set gpib_ctypes as pyvisa-py backend for GPIB communication

# pyvisa: https://pyvisa.readthedocs.io/en/latest/
from pyvisa import ResourceManager as visaSetup
VISA = visaSetup('@py') # set pyvisa-py as backend for VISA communication

