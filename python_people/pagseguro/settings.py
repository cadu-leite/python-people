PAGSEGURO_API_URL = "https://ws.pagseguro.uol.com.br/v2/checkout"
PAGSEGURO_API_RETURN_URL = "https://ws.pagseguro.uol.com.br/v2/checkout"
PAGSEGURO_API_TOKEN=""

try:
    from pag_seg_settings_local import *
except ImportError:
    pass