import redis

r = redis.Redis(
  host='localhost',
  port=6379,
  decode_responses=True,
)

r.publish('channel_1', '1')
r.publish('channel_2', '2')
r.publish('channel_3', '3')
r.publish('channel_1', '4')
r.publish('channel_2', '5')
