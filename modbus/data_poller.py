from threading import Timer

def poll_data(timer ,get_data_func, write_func,):
    data = get_data_func()
    write_func(data)
    Timer(timer, poll_data, [timer,get_data_func, write_func]).start()