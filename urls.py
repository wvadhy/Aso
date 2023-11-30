"""Relevant URLS"""

URLS = {
    "villager": 'https://obufilsoc.com/imgs/villager-r.png',
    "creeper": 'https://obufilsoc.com/imgs/creeper-r.png',
    "wave_1": 'https://obufilsoc.com/imgs/wave.png',
    "wave_3": 'https://obufilsoc.com/imgs/wave_3.png',
    "kanye": 'https://api.kanye.rest/'
}


def u_get(key: str) -> str:
    return URLS.get(key, "Error, invalid key")