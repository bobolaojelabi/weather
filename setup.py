import requests
from flask import Flask, request,redirect,render_template, flash,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        city = "lagos"
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4ca1f940926b2812ff0af5d35d325d6c'
        r = requests.get(url.format(city)).json()
        print(r)
        #creating a dictionary to store the infomation we need
        weather ={
            'city': city,
            'country':r['sys']['country'],
            'temperature':r['main']['temp'],
            'humidity':r['main']['humidity'],
            'pressure':r['main']['pressure'],
            'wind':r['wind']['speed'],
            'icon':r['weather'][0]['icon'],
            'description':r['weather'][0]['description'],
            'main':r['weather'][0]['main']
        }
        load = 'https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=4ca1f940926b2812ff0af5d35d325d6c'
        rsq = requests.get(load.format(city)).json()
        days = []
        for item in rsq['list']:
            timestamp = item['dt']
            days.append({
                'date':datetime.utcfromtimestamp(timestamp).strftime('%A'),
                'time':datetime.utcfromtimestamp(timestamp).strftime('%H:%M'),
                'temp':item['main']['temp'],
                'pressure':item['main']['pressure'],
                'wind':item['wind']['speed'],
                'main':item['weather'][0]['main'],
                'icon':item['weather'][0]['icon'],
                'description':item['weather'][0]['description']
            })
        return render_template('index.html',weather=weather,days=days)
    else:
        city = request.form.get('city')
        if city != '':
            url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&exclude=hourly,daily&appid=4ca1f940926b2812ff0af5d35d325d6c'
            r = requests.get(url.format(city)).json()
            #creating a dictionary to store the infomation we need
            weather ={
                'city': city,
                'country':r['sys']['country'],
                'temperature':r['main']['temp'],
                'humidity':r['main']['humidity'],
                'pressure':r['main']['pressure'],
                'wind':r['wind']['speed'],
                'icon':r['weather'][0]['icon'],
                'description':r['weather'][0]['description'],
                'main':r['weather'][0]['main']
            }
            load = 'https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=4ca1f940926b2812ff0af5d35d325d6c'
            rsq = requests.get(load.format(city)).json()
            days = []
            for item in rsq['list']:
                timestamp = item['dt']
                days.append({
                    'date':datetime.utcfromtimestamp(timestamp).strftime('%A'),
                    'time':datetime.utcfromtimestamp(timestamp).strftime('%H:%M'),
                    'temp':item['main']['temp'],
                    'pressure':item['main']['pressure'],
                    'wind':item['wind']['speed'],
                    'main':item['weather'][0]['main'],
                    'icon':item['weather'][0]['icon'],
                    'description':item['weather'][0]['description']
                })
            return render_template('index.html',weather=weather,days=days)
        else:
            return redirect('/')


if(__name__)=='__main__':
   app.run(debug=True)
