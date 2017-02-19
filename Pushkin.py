from flask import Flask, render_template
import requests



app = Flask(__name__)
app.debug = True

def get_data():
    url = "https://raw.githubusercontent.com/ischurov/dj-prog/master/pushkin1.json"  # получаю данные
    r = requests.get(url)
    data = r.json()
    poems = data['poems']

    for row in poems:
        row["title"] = row["title"][0]
        if row["title"] == '* * *':
            row["title"] = row['verses'][0].upper().replace('«','').replace('"','').replace(';','').replace(':','')
        if row["title"] == '':
            row["title"] = row['verses'][1].upper().replace('«','').replace('"','').replace(';','').replace(':','')

    return poems

def sort_titles():
    poems = get_data()
    titles = []
    for poem in poems:
        titles.append(poem['title'])
    titles.sort()
    return titles

@app.route('/')
def list_rows():
    return render_template("main.html",
                           data=sort_titles())

@app.route('/poem/<int:n>')
def show_poem(n):
    data = get_data()
    row = data[n-1]
    return render_template("show_poem.html",
                           table=row, n=n)

@app.route('/random')
def random():
    import random
    poems = get_data()
    random_poems = random.choice(poems)
    return render_template("random.html",
                           r_table=random_poems)

if __name__ == '__main__':
    app.run()