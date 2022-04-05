"""
Global setting of the trading platform.
"""

from logging import CRITICAL
from typing import Dict, Any
from tzlocal import get_localzone

from .utility import load_json


SETTINGS: Dict[str, Any] = {
    "font.family": "微软雅黑",
    "font.size": 12,

    "log.active": True,
    "log.level": CRITICAL,
    "log.console": True,
    "log.file": True,

    "email.server": "smtp.qq.com",
    "email.port": 465,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",

    "datafeed.name": "rqdata",
    "datafeed.username": "license",
    "datafeed.password": "BvbpH1ERB5FGM2dcINbeX57u154o97k9wxQJG4sABGmEm6ZJ7BoGOwJlZRKeae9J2Ru6ea7-p5YIbkvIEJKnlDLVvFVExjkfp7PjMIUysMGPZXnd-JojscyvXVIlJ3j4R6-bdua9_oOiIydsaTIv1X3qZuRwaXMV5kTueR18eu8=X4wfWTiBCve64fXLlWT9IV0pzKBNpXK7mbKAFKHTkk1HPLw1RQTBE6X68nTTtS1j0qEQUqx3c-aT7alACF3DEipmyH-vVcGZLAjvOMDneydQCoySYejEhwcvCQ0RjoT53oq4XDaY4igCuwgcCGFqVOrv87_H7cuyUkdEPemp73k=",

    "database.timezone": get_localzone().zone,
    "database.name": "sqlite",
    "database.database": "database.db",
    "database.host": "",
    "database.port": 0,
    "database.user": "",
    "database.password": ""
}


# Load global setting from json file.
SETTING_FILENAME: str = "vt_setting.json"
SETTINGS.update(load_json(SETTING_FILENAME))


def get_settings(prefix: str = "") -> Dict[str, Any]:
    prefix_length = len(prefix)
    return {k[prefix_length:]: v for k, v in SETTINGS.items() if k.startswith(prefix)}
