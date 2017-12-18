from example.secrets import CREDENTIALS
import datetime as dt
import requests


class HolidayDownloader:
    '''
        Class for parsing holidays of a given country using the google api
    '''
    instance = None

    @staticmethod
    def getInstance():
        if HolidayDownloader.instance is None:
            HolidayDownloader.instance = HolidayDownloader()
        return HolidayDownloader.instance

    def __init__(self):
        self.holidays = None
        self.country = 'co'
        self.language = 'es'
        self.key = CREDENTIALS

        self.holidays = self._parseHolidays()

    def _parseHolidays(self):
        url = ('https://www.googleapis.com/calendar/v3/calendars/',
               self.country, '__', self.language,
               '%40holiday.calendar.google.com/events?key=',
               self.key)
        url = ''.join(url)

        holidays = requests.get(url).json()['items']

        holidays_dates = list()
        for h in holidays:
            holidays_dates.append((h['start']['date'], h['end']['date']))

        holidays_dates = list(set(holidays_dates))
        holidays_dates.sort(key=lambda x: dt.datetime.strptime(x[0], '%Y-%m-%d'))
        holidays_dates = [start for start, end in holidays_dates]

        return holidays_dates

    def getHolidayDates(self):
        return [dt.datetime.strptime(i, '%Y-%m-%d').date() for i in self.holidays]


if __name__ == '__main__':
    c = HolidayDownloader()
    for i in c.getHolidayDates():
        print(i)
