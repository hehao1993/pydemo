import traceback

from retrying import retry


def run2(r):
    return isinstance(r, int)


@retry(stop_max_attempt_number=3, retry_on_result=run2)
def run():
    print("开始重试")
    return 1/0


if __name__ == '__main__':
    try:
        run()
    except:
        traceback.print_exc()
    print(123)
