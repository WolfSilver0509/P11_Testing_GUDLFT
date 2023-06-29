import json
from flask import Flask,render_template,request,redirect,flash,url_for
import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    filtered_clubs = [club for club in clubs if club['email'] == email]
    if filtered_clubs:
        club = filtered_clubs[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return render_template('index.html', error_message=f"L'email {email} n'est pas enregistré sur le site.")


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        current_date = datetime.date.today()
        competition_date = datetime.datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S").date()

        if competition_date >= current_date:

                return render_template('booking.html', club=foundClub, competition=foundCompetition)

        else:
            flash("Ce concours a déjà eu lieu. / This competition has already taken place.")
    else:
        flash("Une erreur s'est produite. Veuillez réessayer / Something went wrong - please try again")

def updateClubs():
    with open('clubs.json', 'w') as c:
        # Convertit les valeurs en entiers avant de les stocker
        updated_clubs = [{'name': club['name'], 'points': int(club['points'])} for club in clubs]
        json.dump({'clubs': updated_clubs}, c, indent=4)

def updateCompetitions():
    with open('competitions.json', 'w') as c:
        json.dump({'competitions': competitions}, c, indent=4)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    competition_name = request.form['competition']
    club_name = request.form['club']
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    flash('Great-booking complete!')
    updateClubs()  # Appel de la fonction updateClubs pour mettre à jour le fichier JSON des clubs
    updateCompetitions() # Appel de la fonction updateCompetitions pour mettre à jour le fichier JSON des compétitions
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))