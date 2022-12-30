########################################################################################
#  REFERENCES
#
#  Title: cal/utils.py
#  Author: Hui Wen
#  Date: 7/24/2018
#  URL: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
#
#  Title: cal/utils.py
#  Author: Hui Wen
#  Date: 7/29/2018
#  URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
########################################################################################

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
	def __init__(self, user_profile, year=None, month=None):
		self.year = year
		self.month = month
		self.user_profile = user_profile
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day, users=self.user_profile)
		d = ''
		for event in events_per_day:
			d += f'<li style="color:black; font-weight:bold; font-size: 1vw;"> {event.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, users=self.user_profile)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal