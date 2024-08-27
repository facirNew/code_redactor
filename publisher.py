import redis

r = redis.Redis(
  host='localhost',
  port=6379,
  decode_responses=True,
)

r.publish('channel_1', '5')
r.publish('channel_2', '2')
r.publish('channel_3', '3')
