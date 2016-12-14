import redis, ast

currency_cache = redis.StrictRedis(host='172.31.13.183', port=6379, db=0)
exist = currency_cache.get('currencies')
conversions = ast.literal_eval(exist)
print conversions

