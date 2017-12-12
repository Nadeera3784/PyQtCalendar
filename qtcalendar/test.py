from holder.minimal import MinimalHolder
from views import EventInCalendar

ui = MinimalHolder()

# Create an event label
label = EventInCalendar()
ui.getMainLayout().addWidget(label)

ui()
