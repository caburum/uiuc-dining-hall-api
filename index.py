from typing import TypedDict, List
import requests
from datetime import datetime, timedelta
import re

API_BASE = 'https://web.housing.illinois.edu/MobileAppWS/api'

API_LOCATIONS = f'{API_BASE}/LocationSchedules'
class DiningHall(TypedDict):
	DiningOptionID: int
	DiningOptionName: str
	Type: str
	DiningLocation: str

DINING_HALLS = {
	'IKE': 1,
	'PAR': 2,
	'ISR': 3,
	'LAR': 5,
	'FOG': 12
}

API_MENU = f'{API_BASE}/Menu/%s/%s' # location_id, date (YYYY-MM-DD)
class FoodItem(TypedDict):
	Category: str
	Course: str # meal category
	CourseSort: int
	DiningMenuID: int
	DiningOptionID: int
	EventDate: str # day
	EventDateGMT: int
	FormalName: str # name
	ItemID: int
	Meal: str # time period
	ScheduleID: int
	ServingUnit: str # station
	Traits: str
	
yummy = re.compile(r'chicken carnitas|^chicken tenders', re.IGNORECASE)

def get_menu(location_id: int, date: str) -> List[FoodItem]:
	url = API_MENU % (location_id, date)
	resp = requests.get(url)
	if resp.status_code != 200:
		raise Exception(f'Error fetching menu: {resp.status_code}')
	data = resp.json()
	if isinstance(data, dict) and 'Items' in data:
		items = data['Items']
	else:
		items = data
	return items  # type: ignore

today = datetime.now().date()

for i in range(14):
	for hall, hall_id in DINING_HALLS.items():
		day = today + timedelta(days=i)
		day_str = day.strftime('%Y-%m-%d')

		menu = get_menu(hall_id, day_str)
		for item in menu:
			if yummy.search(item['FormalName']):
				print(f"{day_str} {hall} {item['Meal']}: {item['FormalName']} ({item['ServingUnit']})")