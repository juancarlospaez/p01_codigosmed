from .ium import ium_pipe, ium_unique, ium_tuple
__all__ = ["ium_pipe", "ium_unique", "ium_tuple"]

# Eliminar el módulo 'ium' del espacio de nombres
import sys
if 'medkode.ium' in sys.modules:
    del sys.modules['medkode.ium']