import redis
import const

conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)