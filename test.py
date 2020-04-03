def timer(func):
    import time

    def wrapper(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)
        time_diff = time.time() - time_start
        print('{} func. ran in {} sec.'.format(func.__name__, time_diff))
    return wrapper


