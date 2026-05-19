import queue

event_bus = queue.Queue()

def publish(event):
    event_bus.put(event)

def consume():
    events = []
    while not event_bus.empty():
        events.append(event_bus.get())
    return events
