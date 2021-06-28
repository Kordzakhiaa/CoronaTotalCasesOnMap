import requests
import folium
from bs4 import BeautifulSoup
import pandas


# წრეების რადიუსის გენერირება
def radius_gen(tcases):
    tcases = int(tcases.replace(',', ''))

    return tcases ** 0.25


# წრეების ფერების გენერირება
def color_gen(tcases):
    tcases = int(tcases.replace(',', ''))

    if tcases < 3000:
        return "blue"
    elif tcases < 9000:
       return "green"
    elif tcases < 35000:
        return "purple"
    elif tcases < 90000:
        return "pink"
    elif tcases < 200000:
        return "yellow"
    elif tcases < 250000:
        return "orange"
    else:
        return "red"


r = requests.get('https://www.worldometers.info/coronavirus/')

c = r.content

soup = BeautifulSoup(c, 'html.parser')

data = soup.find('tbody')

rows = data.find_all('tr', {'style': ''})

dictionary = {}


for item in rows:
    tcases = item.find_all('td')[2].text.strip()
    dictionary[item.find_all('td')[1].text.strip()] = tcases    # ვწერთ ლექსიკონში სახელის და ინფიცირების რაოდენობის მიხედვით (name: cases)


# ვკითხულობთ country_data ფაილიდან ქვეყნების მონაცემებს და ვინახავთ country_data ცვლადში
country_data = pandas.read_csv('countries.csv')

# country_data ცვლადიდან ვიღებთ ქვეყნების განედებს და ვინახავთ latitude ცვლადში
latitude = list(country_data['latitude'])

# country_data ცვლადიდან ვიღებთ ქვეყნების გრძედებს და ვინახავთ longitude ცვლადში
longitude = list(country_data['longitude'])

# country_data ცვლადიდან ვიღებთ ქვეყნების დასახელებებს და ვინახავთ country_name ცვლადში
country_name = list(country_data['name'])

# საწყისი პარამეტრები: ლოკაცია(საქართველო/თბილისი)...
MAP = folium.Map(location=[41.69411, 44.83368], zoom_start=5, tile="Stamen Terrain")


fg = folium.FeatureGroup(name="Countries")

# ციკლი განედის, გრძედის და სახელის მიხედვით 
for latitude, longitude, country_name in zip(latitude, longitude, country_name):

    if country_name in dictionary.keys():
        try:
            fg.add_child(folium.CircleMarker(location=[latitude, longitude],
                                            popup=str(country_name) + '\n' +
                                            str(dictionary[country_name]),
                                            radius=radius_gen(dictionary[country_name]), fill_color=color_gen(dictionary[country_name]), color='#666666', fill_opacity=0.7))
        except:
            pass


MAP.add_child(fg)

MAP.save('CoronaMap.html')
