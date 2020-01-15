import folium
from flask import Flask, render_template, request, sessions, session
import time
import os
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
                return render_template('index.html', message='* Please input a diameter of less than 50000 meters and make sure your input is a number *')
            checkvar = int(diameter)
        except:
            return render_template('index.html', message='* Diameter input cannot contain letters or decimals *')
        tooltip = 'Click for more information.'
        print(city)
        print('----')
        try:
            global lat_lon
            import geocoder
            g = geocoder.osm(str(city))
            lat_lon = [g.json['lat'], g.json['lng']]
            session['user_lat_lon'] = lat_lon
            print(session['user_lat_lon'], ' changed to \/')
            print(lat_lon)
        except:
            return render_template('index.html', message='* The City You Inputted Does Not Exist | Fix: Try waiting and reloading*')


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
            print('PRE CITY AND LAT LON BELOW \/')
            print(city)
            print(lat_lon)
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            session['user_lat_lon'] = lat_lon
            print('sesssion created \/')
            print('BEFORE MAP ', session['user_lat_lon'])
            if preset_diameter == False:
                return render_template('index2.html', pre_diameter=str(of_diameter), word_one=word_one, word_two = word_two, word_three = word_three)
            else:
                return render_template('index2.html', word_one=word_one, word_two=word_two, word_three = word_three)
        except:
            return render_template('index.html', pre_diameter=str(of_diameter), pre_city = city)
    except:
        return render_template('index.html', message='* Required input fields are empty. Please complete them and try again. *')
@app.route('/map')
def map():
    if 1 == 1:
        session.modified = True
        if 'user_lat_lon' not in session:
            try:
                diameter = of_diameter
                crater_diameter = int(diameter) * 21.5
                print(crater_diameter)
            except:
                return render_template('index.html', message='* The diameter you inputted contains letters *')
            print('NOT IN SESSION!!!!!!!')
            lat_lon_session = lat_lon
        else:
            print('SESSION FIRST: ', session['user_lat_lon'])
            print('ASDF ', lat_lon, ' ', city)
            diameter = of_diameter
            try:
                crater_diameter = int(diameter) * 21.5
                print(crater_diameter)
            except:
                return render_template('index.html', message='* The diameter you inputted contains letters *')
            lat_lon2 = lat_lon
            print('lat_lon2 ', lat_lon2)
            print(lat_lon)
            print('map city: ', city)
            lat_lon_session = session['user_lat_lon']
            print('SESSION: ', lat_lon_session)
            print(lat_lon)
        print(lat_lon_session, ' latlon')
        if int(crater_diameter) > 60000:
            m = folium.Map(location=lat_lon, zoom_start=5)
            folium.Circle(location=lat_lon, radius=crater_diameter * 51,
                          tooltip="Dust and Ash causes fallout around the world. Living animals and plants begin dieing because of lack of sunlight and the ability to get nutrition.",
                          color='white', fill=True,
                          fill_color='', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 19,
                          tooltip="Asteroid would cause fallout around the world because of dust and ash thrown into the atmosphere | All people are aware of the situation either by hearing or sight | Unbearable Heat",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 9,
                          tooltip="Unbearable Fatal Heat Felt | Sound Shockwave | Buildings Likely Flattened | Heat & Shockwave Still Felt Farther Away",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 5,
                          tooltip="Buildings Destroyed | Certain Clothing may ignite | Debris and heat fatal to many ", color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 3,
                          tooltip="Human Skin May Burn | Infastructure destroyed | Flying Debris Fatal ", color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter*1.45, tooltip="All Buildings Knocked Over | Human Skin Burns | Most Perish ",color='yellow', fill=True,
                          fill_color='yellow', zoom_start=5).add_to(m)

            folium.Circle(location=lat_lon, radius=crater_diameter/1.5, tooltip="Crater Area | Anything Living Dies ", color='orange', fill=True,
                              fill_color='orange', zoom_start=5).add_to(m)
            folium.Circle(location=lat_lon , radius=int(diameter), tooltip="Original Size of Asteroid | Click", color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=5).add_to(m)
            print(diameter)

        elif int(crater_diameter) > 7000:
            m = folium.Map(location=lat_lon, zoom_start=10)
            folium.Circle(location=lat_lon, radius=crater_diameter * 14,
                          tooltip="Worldwide Fallout Possible From Dust & Ash | Almost all people are aware of the situation either by hearing or sight.",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Waves Felt (Fatal to those of old age or certain medical conditions) | Sound Shockwave | Most Buildings Stand | Heat & Shockwave Still Felt Farther Away",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed | Certain Clothing may ignite, debris and heat fatal to many ",
                          color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn and infastructure destroyed | Flying Debris Fatal ",

                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 1.2,
                          tooltip="Most Buildings Knocked Over | Human Skin Burns | Most Perish ",
                          color='yellow', fill=True,
                          fill_color='yellow', zoom_start=10).add_to(m)

            folium.Circle(location=lat_lon, radius=crater_diameter / 1.5,
                          tooltip="Crater Area | Anything Living Dies ",
                          color='orange',
                          fill=True,
                          fill_color='orange', zoom_start=10).add_to(m)
            folium.Circle(location=lat_lon, radius=int(diameter), tooltip="Original Size of Asteroid | Click",
                          popup='(Circle Sizes Are Enlarged or Understated)', color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=10).add_to(m)
            print(diameter)


        elif int(crater_diameter) > 3000:
            m = folium.Map(location=lat_lon, zoom_start=11)
            folium.Circle(location=lat_lon, radius=crater_diameter * 14,
                          tooltip="Some Fallout Could Occur from dust & ash | Almost all people are aware of the situation either by hearing or sight.",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Waves Felt (Fatal to people of older age or certain medical conditions)| Sound Shockwave | Buildings Probably Stand | Heat & Shockwave Still Felt Farther Away",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed | Certain Clothing may ignite, debris and heat fatal to many ",
                          color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn and infastructure destroyed | Flying Debris Fatal ",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 1.2,
                          tooltip="All Buildings Knocked Over | Human Skin Burns | Most Perish ",
                          color='yellow', fill=True,
                          fill_color='yellow', zoom_start=11).add_to(m)

            folium.Circle(location=lat_lon, radius=crater_diameter / 1.5,
                          tooltip="Crater Area | Anything Living Dies ",
                          color='orange', fill=True,
                          fill_color='orange', zoom_start=11).add_to(m)
            folium.Circle(location=lat_lon, radius=int(diameter), tooltip="Original Size of Asteroid | Click",
                          color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=11).add_to(m)
            print(diameter)

        elif int(crater_diameter) > 1743:
            m = folium.Map(location=lat_lon, zoom_start=12)
            folium.Circle(location=lat_lon, radius=crater_diameter * 14,
                          tooltip="Ash & Dust is kicked up from the collision, but not enough to cause fallout | Some heat felt",
                          popup='Heat is felt, everyone is aware of the situation either by hearing or sight.',
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Felt (Could Be Fatal To Certain People with Certain Medical Conditions) | Sound Shockwave | Buildings Probably Stand | Heat & Shockwave Still Felt Farther Away",
                          popup='Buildings still stand because they have distance from the point of impact.',
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed | Certain Clothing may ignite, debris and heat fatal to many ",
                          popup='Fatal heat and debris causes casualties', color='limegreen', fill=True,
                          fill_color='limegreen', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn and infastructure destroyed | Flying Debris Fatal ",
                          popup='Most bridges/houses flattened. Casualties occur from debris, earthquake and heat.',
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 1.2,
                          tooltip="All Buildings Knocked Over | Human Skin Burns | Most Perish ",
                          popup='Cities flattened by intense ground shaking.', color='yellow', fill=True,
                          fill_color='yellow', zoom_start=12).add_to(m)

            folium.Circle(location=lat_lon, radius=crater_diameter / 1.5,
                          tooltip="Crater Area | Anything Living Dies ",
                          popup='Crater Area | Hole in Ground', color='orange', fill=True,
                          fill_color='orange', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=int(diameter), tooltip="Original Size of Asteroid | Click",
                          popup='(Circle Sizes Are Enlarged or Understated)', color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)
            print(diameter)

        elif int(crater_diameter) > 400:
            m = folium.Map(location=lat_lon, zoom_start=12)
            folium.Circle(location=lat_lon, radius=crater_diameter * 14,
                          tooltip="Ash & Dust is kicked up from the collision, fallout is very unlikely but possible for the region | Heat Felt",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Felt (Fatal to those of older age or have certain medical conditions)| Sound Shockwave | Buildings Probably Stand | Heat & Shockwave Still Felt Farther Away",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 4,
                          tooltip="Buildings Destroyed | Certain Clothing may ignite, debris and heat fatal to many ", color='limegreen',
                          fill=True,
                          fill_color='limegreen', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 2,
                          tooltip="Human Skin May Burn and infastructure destroyed | Flying Debris Fatal ",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 1.2,
                          tooltip="Most Buildings Knocked Over | Human Skin Burns | Most Perish ", color='yellow', fill=True,
                          fill_color='yellow', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter / 1.5,
                          tooltip="Crater Area | Anything Living Dies ",
                          color='orange', fill=True,
                          fill_color='orange', zoom_start=12).add_to(m)
            folium.Circle(location=lat_lon, radius=int(diameter), tooltip="Original Size of Asteroid | Click",
                          color='grey',
                          fill=True,
                          fill_color='grey', zoom_start=12).add_to(m)

        else:
            m = folium.Map(location=lat_lon, zoom_start=17)
            folium.Circle(location=lat_lon, radius=crater_diameter * 14,
                          tooltip="Some heat may be/is felt | Almost all people are aware of the situation either by hearing or sight.",
                          color='purple', fill=True,
                          fill_color='lightgrey', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 8,
                          tooltip="Unbearable Heat Felt | Sound Shockwave | Buildings Probably Stand | Heat & Shockwave Still Felt Farther Away",
                          color='grey', fill=True,
                          fill_color='grey', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 4.5,
                          tooltip="Buildings Destroyed | Certain Clothing may ignite, debris and heat fatal to many",
                          fill=True,
                          color='limegreen',
                          fill_color='limegreen', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 3,
                          tooltip="Human Skin May Burn and infastructure destroyed | Flying Debris Fatal",
                          color='#ff6666', fill=True,
                          fill_color='#ff6666', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lon, radius=crater_diameter * 1.6,
                          tooltip="Most Buildings Knocked Over | Human Skin Burns | Most Perish ",
                        color='yellow', fill=True,
                          fill_color='yellow', zoom_start=17).add_to(m)

            folium.Circle(location=lat_lon, radius=crater_diameter / 1.5,
                          tooltip="Crater Area | Anything Living Dies",
                          color='orange', fill=True,
                          fill_color='orange', zoom_start=17).add_to(m)
            folium.Circle(location=lat_lon, radius=int(diameter), tooltip="Original Size of Asteroid",
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
if __name__ == "__main__":
    app.run(debug=False)
