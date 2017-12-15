# PyQtCalendar
### *Current version: 1.0 alpha*
The idea is to create a fully fledged calendar for Python using PyQt5 that support event scheduling and event state tracking. You can expect the following from this calendar:

* Basic calendar operations: change country, change month, selected date, weekend, holidays and special days highlighting, change leading day, etc.
* Schedule an event: An event is described by an initial datetime, an ending datetime, a place and a fulfillment status. The fulfillment status can be whatever you want it to be, but must be represented numerically in the range 0.0 to 1.0; the calendar colors the event depending on the fulfillment status.
* Date overloading: If a date has too many events, a +N label appears in the date, hovering it will display a floating widget with the rest of the events.
* Date availability: Hovering a date for more than 1.5 seconds (number can be changed) will display the available times in that date (substracts events durantion from working time at the given date).
* Dynamic event insertion via module implementation: The calendar does not provide event addition buttons (as of current prospects), events can be added programmatically and, upon doing so, the whole date distribution is recalculated and displayed again.

Below is a screen capture of the calendar state for version 1.0 alpha.
![calendar](https://raw.githubusercontent.com/asmateus/PyQtCalendar/master/extra/calendar_v01.PNG)
