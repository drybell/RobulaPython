from timeout import timeout
import time

# Timeout after 5 seconds
@timeout(5)
def long_running_function2():
    time.sleep(6)

for i in range(10):
    print(i)
    try: 
        long_running_function2()
        print("I'm here")
    except Exception: 
        continue
    print("I didn't reach here")