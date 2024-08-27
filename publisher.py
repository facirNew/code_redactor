import redis


def main():
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True,
    )

    r.publish('channel_1', '1')  # pass
    r.publish('channel_2', '2')  # pass
    r.publish('channel_3', '3')  # syntax error
    r.publish('channel_1', '4')  # time limit
    r.publish('channel_2', '5')  # wrong answer


if __name__ == '__main__':
    main()
