from redis import Redis, StrictRedis

r0 = StrictRedis.from_url('redis://localhost/0')
r1 = StrictRedis.from_url('redis://localhost/0', socket_timeout=10)
r2 = StrictRedis.from_url('redis://localhost/0?socket_timeout=10')
r3 = StrictRedis()

url1 = 'redis://localhost/0'
r4 = StrictRedis.from_url(url1)
r5 = StrictRedis.from_url(url1, socket_timeout=10)


def t():
    StrictRedis.from_url('redis://localhost/0')
    Redis()
