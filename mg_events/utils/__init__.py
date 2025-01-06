from . import *
from mcdreforged.utils.serializer import Serializable

class content(Serializable):
    lang: str
    advancement: str
    raw: str
    class death(Serializable):
        killer: str
        weapon: str