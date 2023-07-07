import threading
import time
import tkinter

def wait_for_event(e):
    while True:
        # print('\tTHREAD: This is the thread speaking, we are Waiting for event to start..')
        print("Thread sedang menunggu.")
        event_is_set = e.wait()
        # print('\tTHREAD:  WHOOOOOO HOOOO WE GOT A SIGNAL  : %s' % event_is_set)
        print("Thread menerima sebuah sinyal dan mengerjakannya.")
        time.sleep(20)
        e.clear()
        print("Thread sudah selesai mengerjakan perintah.")

# Main code
window = tkinter.Tk()
frame1 = tkinter.Frame(window)
button1 = tkinter.Button(frame1, text="test")

e = threading.Event()
t = threading.Thread(name='pausable_thread',
                     target=wait_for_event,
                     args=(e,))
t.start()
window.mainloop()



# while True:
#     print('MAIN LOOP: di main loop.')
#     time.sleep(4)
#     print('MAIN LOOP: memberikan sebuah sinyal.')
#     e.set()
#     print('MAIN LOOP: mengerjakan sesuatu')
#     time.sleep(4)
#     print('MAIN LOOP: masih mengerjakan sesuatu')
#     time.sleep(4)
#     print('MAIN LOOP: proses terakhir sebelum loop')
#     time.sleep(2)
