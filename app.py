import folium
from flask import Flask, render_template, request, sessions, session, make_response
import time
import os, ast
import pandas as pd
from folium.plugins import MarkerCluster
app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def calculate():
    try:
        global of_diameter
        global city
        city = request.form['city']
        if len(city) > 30:
            return render_template('index.html', message='* Please shorten the length of the city name input *')
        diameter = request.form['diameter']
        diameter2 = request.form['otherdiameter']
        of_diameter = None
        if len(diameter2) == 0:
            preset_diameter = True
            of_diameter = diameter
        else:
            preset_diameter = False
            of_diameter = diameter2

        if len(city) == 0:
            return render_template('index.html', message='* You have not inputted an area or diameter *')
        try:
            if int(of_diameter) > 20000:
                return render_template('index.html', message='* Please input a diameter of less than 20000 meters and make sure your input is a number *')
            checkvar = int(diameter)
        except:
            return render_template('index.html', message='* Diameter input cannot contain letters or decimals *')

        try:
            global lat_lon
            import geocoder
            g = geocoder.osm(str(city))
            lat_lon = [g.json['lat'], g.json['lng']]
            session['user_lat_lon'] = lat_lon
        except:
            import pandas as pd

            df = pd.read_csv("static/worldcities.csv")

            for index, row in df.iterrows():
                if str(row['city']).lower() == str(city).lower():
                    lat_lon = [row['lat'], row['lng']]
                    session['user_lat_lon'] = lat_lon
                    break
                else:
                    lat_lon = ""
            if len(lat_lon) == 0:
                return render_template('index.html', message='* The City You Inputted Does Not Exist   Fix: Try waiting and reloading*')


        try:
            word_one = ""
            word_two = ""
            word_three = ""
            after_space = False
            for char in str(city):
                if char == " ":
                    after_space = True
                if char == " " and after_space == True:
                    after_space = None
                if after_space== False:
                    word_one += str(char)
                elif after_space==True:
                    word_two += str(char)
                else:
                    word_three += str(char)
            resp1 = make_response(render_template('index2.html', pre_diameter=str(of_diameter), word_one=word_one, word_two = word_two, word_three = word_three))
            resp2 = make_response(render_template('index2.html', word_one=word_one, word_two = word_two, word_three = word_three))

            resp1.set_cookie('latitude_longitude', str(lat_lon))
            resp2.set_cookie('latitude_longitude', str(lat_lon))

            resp1.set_cookie('diameters', str(of_diameter))
            resp2.set_cookie('diameters', str(of_diameter))

            if preset_diameter == False:
                return resp1
            else:
                return resp2
        except:
            return render_template('index.html', pre_diameter=str(of_diameter), pre_city = city)
    except:
        return render_template('index.html', message='* Required input fields are empty. Please complete them and try again. *')
@app.route('/map')
def map():
    if 1 == 1: # IF ONE = ONE GO BACK
        session.modified = True
        if 'user_lat_lon' not in session:
            print('NOT IN SESSION!!!!!!!')
            lat_lons = request.cookies.get('latitude_longitude')
            # try:
            #     lat_lons = ast.literal_eval(lat_lons)
            # except:
            try:
                lat_lons = lat_lons.strip('][').split(', ')
            except:
                lat_lons = [40.7128, 74.0060]
                print('DevNote: Occ Strip Failed Set to NYC Lat Lon')
            print(lat_lons)
            print(type(lat_lons))
            diameter = request.cookies.get('diameters')
            print(diameter)
        else:
            print('SESSION FIRST: ', session['user_lat_lon'])
            print('ASDF ', lat_lon, ' ', city)
            diameter = of_diameter
            lat_lon_session = session['user_lat_lon']
            print('SESSION: ', lat_lon_session)
            print(lat_lon)
            lat_lons = lat_lon
        print('LATLONS: FINAL BEFORE SUBMITION: ', lat_lons)
        print(diameter)
        print(type(diameter))
        try:
            crater_diameter = int(diameter) * 21.5
        except:
            return render_template('map.html')
        print(crater_diameter)
        if int(crater_diameter) > 60000:
            m = folium.Map(location=lat_lons, zoom_start=5)
            folium.Circle(location=lat_lons, radius=crater_diameter * 51,
                          tooltip="Dust and Ash causes fallout <br> Living animals and plants begin dieing because of lack of sunlight and the ability to get nutrition.",
                          color='white', fill=True,
                          fill_color='', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 19,
                          tooltip="Asteroid would cause fallout because of dust and ash thrown into the atmosphere <br> >All people are aware of the situation either by hearing or sight<br>   Unbearable Heat",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 9,
                          tooltip="Unbearable Fatal Heat Felt   <br>Sound Shockwave   <br>Buildings Likely Flattened   <br>Heat & Shockwave ",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 5,
                          tooltip="Buildings Destroyed   <br>Certain Clothing may ignite   <br>Debris and heat fatal to many ", color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 3,
                          tooltip="Human Skin May Burn  <br> Infastructure destroyed<br>   Flying Debris Fatal ", color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter*1.45, tooltip="All Buildings Knocked Over  <br> Human Skin Burns  <br> Most Perish ",color='yellow', fill=True,
                          fill_color='yellow', zoom_start=5).add_to(m)

            folium.Circle(location=lat_lons, radius=crater_diameter/1.5, tooltip="Crater Area  <br> Anything Living Dies ", color='orange', fill=True,
                              fill_color='orange', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lons , radius=int(diameter), tooltip="Original Size of Asteroid", color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=5).add_to(m)
            print(diameter)

        elif int(crater_diameter) > 7000:
            m = folium.Map(location=lat_lons, zoom_start=10)
            folium.Circle(location=lat_lons, radius=crater_diameter * 14,
                          tooltip="Worldwide Fallout Possible From Dust & Ash   <br>All people are aware of the situation either by hearing or sight.",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Waves Felt (Fatal to those of old age or certain medical conditions)  <br> Sound Shockwave  <br> Most Buildings Stand  <br> Heat & Shockwave ",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed  <br> Certain Clothing may ignite  <br> Debris and heat fatal to many ",
                          color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn  <br> Infastructure destroyed  <br> Flying Debris Fatal ",

                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 1.2,
                          tooltip="Most Buildings Knocked Over  <br> Human Skin Burns  <br> Most Perish ",
                          color='yellow', fill=True,
                          fill_color='yellow', zoom_start=10).add_to(m)

            folium.Circle(location=lat_lons, radius=crater_diameter / 1.5,
                          tooltip="Crater Area  <br> Anything Living Dies ",
                          color='orange',
                          fill=True,
                          fill_color='orange', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lons, radius=int(diameter), tooltip="Original Size of Asteroid",
                          popup='(Circle Sizes Are Enlarged or Understated)', color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=10).add_to(m)
            print(diameter)


        elif int(crater_diameter) > 3000:
            m = folium.Map(location=lat_lons, zoom_start=11)
            folium.Circle(location=lat_lons, radius=crater_diameter * 14,
                          tooltip="Some Fallout Could Occur from dust & ash  <br> All people are aware of the situation either by hearing or sight.",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Waves Felt (Fatal to people of older age or certain medical conditions) <br> Sound Shockwave  <br> Buildings Probably Stand  <br> Heat & Shockwave ",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed  <br> Certain Clothing may ignite  <br> Debris and heat fatal to many ",
                          color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn  <br> Infastructure destroyed  <br> Flying Debris Fatal ",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 1.2,
                          tooltip="All Buildings Knocked Over  <br> Human Skin Burns  <br> Most Perish ",
                          color='yellow', fill=True,
                          fill_color='yellow', zoom_start=11).add_to(m)

            folium.Circle(location=lat_lons, radius=crater_diameter / 1.5,
                          tooltip="Crater Area  <br> Anything Living Dies ",
                          color='orange', fill=True,
                          fill_color='orange', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lons, radius=int(diameter), tooltip="Original Size of Asteroid",
                          color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=11).add_to(m)
            print(diameter)

        elif int(crater_diameter) > 1743:
            m = folium.Map(location=lat_lons, zoom_start=12)
            folium.Circle(location=lat_lons, radius=crater_diameter * 14,
                          tooltip="Ash & Dust is kicked up from the collision, but not enough to cause fallout  <br> Some heat felt",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Felt  <br> (Could Be Fatal To Certain People with Certain Medical Conditions)  <br> Sound Shockwave   Buildings Probably Stand   Heat & Shockwave ",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed  <br> Certain Clothing may ignite  <br> Debris and heat fatal to many ",
                          color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn and infastructure destroyed  <br> Flying Debris Fatal ",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 1.2,
                          tooltip="All Buildings Knocked Over  <br> Human Skin Burns  <br> Most Perish ",
                          color='yellow', fill=True,
                          fill_color='yellow', zoom_start=12).add_to(m)

            folium.Circle(location=lat_lons, radius=crater_diameter / 1.5,
                          tooltip="Crater Area  <br> Anything Living Dies ",
                          popup='Crater Area  <br> Hole in Ground', color='orange', fill=True,
                          fill_color='orange', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=int(diameter), tooltip="Original Size of Asteroid  <br> Click",
                          popup='(Circle Sizes Are Enlarged or Understated)', color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)
            print(diameter)

        elif int(crater_diameter) > 400:
            m = folium.Map(location=lat_lons, zoom_start=12)
            folium.Circle(location=lat_lons, radius=crater_diameter * 14,
                          tooltip="Ash & Dust is kicked up from the collision  <br> Fallout is extremely unlikely but possible for the region  <br> Heat Felt",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Felt  <br> (Fatal to those of older age or have certain medical conditions) <br> Sound Shockwave  <br> Buildings Probably Stand  <br> Heat & Shockwave ",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed  <br> Certain Clothing may ignite  <br> Debris and heat fatal to many ", color='limegreen',
                          fill=True,
                          fill_color='limegreen', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn and infastructure destroyed  <br> Flying Debris Fatal ",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 1.2,
                          tooltip="Most Buildings Knocked Over  <br> Human Skin Burns  <br> Most Perish ", color='yellow', fill=True,
                          fill_color='yellow', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter / 1.5,
                          tooltip="Crater Area  <br> Anything Living Dies ",
                          color='orange', fill=True,
                          fill_color='orange', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lons, radius=int(diameter), tooltip="Original Size of Asteroid  <br> Click",
                          color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)

        else:
            m = folium.Map(location=lat_lons, zoom_start=17)
            folium.Circle(location=lat_lons, radius=crater_diameter * 14,
                          tooltip="Some heat may be/is felt  <br> Almost all people are aware of the situation either by hearing or sight.",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Felt  <br> Sound Shockwave  <br> Buildings Probably Stand  <br> Heat & Shockwave ",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 4.5,
                          tooltip="Buildings Destroyed  <br> Certain Clothing may ignite  <br> Debris and heat fatal to many",
                          fill=True,
                          color='limegreen',
                          fill_color='limegreen', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 3,
                          tooltip="Human Skin May Burn and infastructure destroyed  <br> Flying Debris Fatal",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lons, radius=crater_diameter * 1.6,
                          tooltip="Most Buildings Knocked Over  <br> Human Skin Burns  <br> Most Perish ",
                        color='yellow', fill=True,
                          fill_color='yellow', zoom_start=17).add_to(m)

            folium.Circle(location=lat_lons, radius=crater_diameter / 1.5,
                          tooltip="Crater Area  <br> Anything Living Dies",
                          color='orange', fill=True,
                          fill_color='orange', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lons, radius=int(diameter), tooltip="Original Size of Asteroid",
                          popup='(Circle Sizes Are Enlarged or Understated)', color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=17).add_to(m)
            print(diameter)
        print('Process Finished!')

        return m.get_root().render()
    else:
        return render_template('map.html')
@app.route('/terms')
def terms():
    return render_template('termsofservice.html')
@app.route('/questions')
def more():
    return render_template('moreinfo.html')
@app.route('/home')
def home():
    print('GO HOME')
    return render_template('home.html')
@app.route('/asteroid-collision-location-map')
def globalasteroidlocationmap():
    return render_template('WorldwideAsteroidCollisionMap.html')
@app.route('/asteroid-collision-location-map', methods=["POST"])
def globalasteroidlocationmap2():
    return render_template('WorldwideAsteroidCollisionMap2.html')
@app.route('/earthquake-location-map')
def earthquakelocationmap():
    return render_template('WorldwideEarthquakeLocationMap.html')
@app.route('/earthquake-location-map', methods=['POST'])
def earthquakelocationmap2():
    return render_template('WorldwideEarthquakeLocationMap2.html')
@app.route('/nuke-detonation-location-map')
def nukedetonatinolocationmap():
    return render_template('WorldwideNukeDetonationLocationMap.html')
@app.route('/nuke-detonation-location-map', methods=['POST'])
def nukedetonatinolocationmap2():
    return render_template('WorldwideNukeDetonationLocationMap2.html')
@app.route('/volcano-location-map')
def vol():
    return render_template('volcanoeruptionlocationmap.html')
@app.route('/ret-map')
def retmap():
    return render_template('map.html')
@app.route('/ads.txt')
def ads():
    return render_template('ads.txt')
@app.route('/ret-asteroid-location')
def ast():
    return render_template('WorldwideAsteroidMap.html')
@app.route('/ret-earthquake')
def euake():
    return render_template('EarthquakeLocationMap.html')
@app.route('/ret-nuke-loc')
def nukeloc():
    return render_template('nukedetonationlocationmap.html')
@app.route('/coronavirus-location-map')
def corona():
    return render_template('CoronavirusLocation.html')
@app.route('/bad-links')
def badlinks():
    return render_template('badlinks.txt')
@app.route('/blog')
def astblog():
    return render_template('blog.html')
@app.route('/asteroid-hit-earth')
def ahe():
    return render_template('article1.html')
@app.route('/asteroid-earth')
def asteroidearth():
    return render_template('article2.html')
@app.route('/near-asteroids')
def nearasteroids():
    return render_template('article3.html')
@app.route('/asteroid-hit')
def asteroidhit():
    return render_template('article4.html')
@app.route('/testing')
def testing():
    return render_template('trackertemplate.html')
@app.route('/corona')
def coronatracking():
    return render_template('corona.html')
@app.route('/coronavirus-tracker')
def coronavirustracker():
    return render_template("JohnHopkinsMap.html")
@app.route('/telescope-review-celeston-powerseeker-127eq')
def celestonpowerseeker127eq():
    return render_template('1ARTICLE.html')
@app.route('/review-celestron-gc-4-german-equatorial-mount-and-tripod-telescope')
def gemeranequatorial():
    return render_template('2ARTICLEEquatorialMount.html')
@app.route('/maxusee-70mm-refractor-telescope-review')
def maxtelescope():
    return render_template('3ARTICLEMAXUSEE.html')
if __name__ == "__main__":
    of_diameter = 22
    app.run(debug=False)
