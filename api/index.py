from flask import Flask, render_template, request, redirect
import os
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

def getHtml(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def downloadHandler(link_id):
    url = f"https://files.jntufastupdates.com/download/{link_id}"
    sp = getHtml(url)
    return sp.find("a", class_="wpdm-download-link download-on-click btn btn-primary")["data-downloadurl"]


def homepageHandler(yy, sem):
    url = f"https://www.jntufastupdates.com/jntuk-{yy}-{sem}-question-papers/"
    sp = getHtml(url)
    div = sp.find("figure", class_="wp-block-table")
    a_tag_links = div.find_all("a", attrs={"data-wpel-link" : "internal"})
    links = [{"text" : a_tag.text, "id" : a_tag["href"].split("/")[-2]} for a_tag in a_tag_links]
    return links

def listerHandler(lister_id):
    url = f"https://www.jntufastupdates.com/{lister_id}"
    soup = getHtml(url)
    div = soup.find("div", attrs = {"class": "td-post-content tagdiv-type"})
    p_tags = div.find_all(lambda tag : tag.name=="p" and (tag.find("a") or tag.find("strong")) and not tag.find("img") and not tag.has_attr("class") and not tag.has_attr("style"))
    filtered_ptags = []
    
    for tg in p_tags:
        if(tg.find("strong")):
            filtered_ptags.append(tg)
        a_tag = tg.find("a")
        if(a_tag):
            a_tag_link = a_tag["href"]

            x = a_tag_link.split("/", 3)[-1]
            a_tag["href"] = "/"+x
            filtered_ptags.append(tg)

    return filtered_ptags

@app.route('/')
def home():
    return render_template('first.html')


@app.route('/sem', methods=['POST'])
def lister():
    year = request.form['year']
    sem = request.form['sem']
    data = homepageHandler(year, sem)
    return render_template('second.html', data = data)


@app.route('/show/<ID>', methods=['GET'])
def show(ID):
    data = listerHandler(ID)
    return render_template('third.html', data = data)



@app.route('/download/<ID>/', methods=['GET'])
def download(ID):
    print(ID)
    data = downloadHandler(ID)
    return redirect(data)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)