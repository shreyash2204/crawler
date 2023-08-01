# import pymongo
import bcrypt
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask,render_template,request,send_file,url_for, redirect, session

app = Flask(__name__)

app.secret_key = 'keynotknown'


@app.route('/')
def ho():
    return render_template("/index.html")

@app.route('/',methods=['POST','GET'])
def output():
    if request.method == 'POST':
        ean = request.form["url"]

        uri = f"https://www.google.com/search?q={ean}"
        print(uri)
        browser = requests.get(uri)
        soup = BeautifulSoup(browser.text, 'html.parser')

        items = soup.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe")

        first_link_ean = None

        if len(items) > 0:
            div = items[0] 

            a_tags = div.find_all('a')
            title = div.find("div", class_="BNeawe vvjwJb AP7Wnd")

            if title:
                title_text = title.text.lower()
                for link in a_tags:
                    href = link.get('href')

                    first_link_ean = "https://www.google.com" + href
    return render_template("/index.html", data=first_link_ean)

@app.route('/upload', methods=['POST'])
def extract():
    data= []

    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        df = pd.read_excel(file)
        ean_list = df['Ean'].tolist()

    for ean_number in ean_list:
        uri = f"https://www.google.com/search?q={ean_number}"
        print(uri)
        browser = requests.get(uri)
        soup = BeautifulSoup(browser.text, 'html.parser')

        items = soup.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe")

        first_link_ean = None

        if len(items) > 0:
            div = items[0] 

            a_tags = div.find_all('a')
            title = div.find("div", class_="BNeawe vvjwJb AP7Wnd")

            if title:
                title_text = title.text.lower()
                for link in a_tags:
                    href = link.get('href')

                    first_link_ean = "https://www.google.com" + href
                    data.append({'EAN': ean_number, 'Link': first_link_ean})
                    break
    df = pd.DataFrame(data)
    df.to_excel('ean_links.xlsx', index=False)

    return render_template("/index.html")
@app.route('/download')    
def download_file():
    path="urlfile.csv"
    return send_file(path, as_attachment=True)

@app.route("/createaccount")
def createaccount():
    return render_template('createaccount.html')  
    

if __name__ == "__main__":
    app.run(debug=True)