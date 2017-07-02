from redis import Redis, StrictRedis

r0 = StrictRedis.from_url('redis://localhost/0')
r1 = StrictRedis.from_url('redis://localhost/0', socket_timeout=10)
r2 = StrictRedis.from_url('redis://localhost/0?socket_timeout=10')
r3 = StrictRedis()


def t():
    StrictRedis.from_url('redis://localhost/0')
    Redis()
