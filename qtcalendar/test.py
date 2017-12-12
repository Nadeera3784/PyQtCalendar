from holder.minimal import MinimalHolder
from calendar import EventInCalendar

ui = MinimalHolder()

# Create an event label
event = EventInCalendar()
event.getView().setText('Hello, world!')
event.getView().updateStatus()
ui.getMainLayout().addWidget(event.getView())

ui()
