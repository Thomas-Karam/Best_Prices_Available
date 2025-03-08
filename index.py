import requests
from bs4 import BeautifulSoup
from wtforms import *
from wtforms.validators import *
from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for


class class_search(FlaskForm):
    inp=StringField(validators=[DataRequired()])
    sub=SubmitField()

class class_message(FlaskForm):
    name=StringField(validators=[DataRequired()])
    email=StringField(validators=[DataRequired()])
    message=StringField(validators=[DataRequired()])
    send=SubmitField()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def Scraping_for_search(u):
    result_jumia=[]
    result_amazon=[]
    url_jumia=f"http://www.jumia.com.eg/catalog/?q={u.replace(' ','+')}"
    code_jumia = requests.get(url_jumia, headers=headers)
    soup_jumia = BeautifulSoup(code_jumia.content, "lxml")
    image = soup_jumia.find("img", {"class": "img"})
    if image:
        image = image['data-src']
    else:
        image = 'No image available'
    description_jumia = soup_jumia.find("h3", {"class": "name"})
    price_j = soup_jumia.find("div", {"class": "prc"})
    if price_j:
        price_jumia =float(price_j.text.replace(',', '').replace('EGP', '').strip())
    else:
        price_jumia = 0.0
    rate_jumia =soup_jumia.find("div", {"class", "stars _s"})
    link_jumia = soup_jumia.find("a", {"class": "core"})['href']
    result_jumia.append({
        'description':description_jumia.text,
        'price':price_jumia,
        'rate':rate_jumia,
        'link':f"http://www.jumia.com.eg{link_jumia}",
        'from':'Jumia'
    })

    url_amazon=f"http://www.amazon.eg/s?k={description_jumia.text.replace(' ','+')}&language=en_AE"
    code_amazon = requests.get(url_amazon, headers=headers)
    soup_amazon = BeautifulSoup(code_amazon.content, "lxml")
    description_amazon = soup_amazon.find("h2", {"class": "a-size-base-plus"})
    price_a = soup_amazon.find("span", {"class": "a-price-whole"})
    if price_a:
        price_amazon = float(price_a.text.replace(',', '').replace('EGP', '').strip())
    else:
        price_amazon = 0.0
    rate_amazon = soup_amazon.find("span", {"class": "a-icon-alt"})
    link_amazon = soup_amazon.find("a", {"class": "a-link-normal"})['href']
    result_amazon.append({
        'description':description_amazon.text, 
        'price':price_amazon,
        'rate':rate_amazon, 
        'link':f"http://www.amazon.eg{link_amazon}",
        'from':'Amazon'
    })
    Search = sorted((result_amazon + result_jumia), key=lambda x: x['price'], reverse=False)
    return Search, image


app = Flask(__name__)
app.config['SECRET_KEY']='2dbbf715b836ebab5a3420222be54177bea4848ea1800b0e81fe1a6424825439'

@app.route('/', methods=['Get', 'POST'])
def en():
    search=class_search()
    messages=class_message()
    total_results=[]
    image =''
    if search.inp.data:
        total_results, image = Scraping_for_search(search.inp.data)
    return render_template('BP-e.html',
                           css="BP-e",
                           link_a="/ar",
                           search=search,
                           message=messages,
                           results=total_results,
                           name=search.inp.data,
                           image= image ) 

@app.route('/ar', methods=['Get', 'POST'])
def ar():
    search=class_search()
    messages=class_message()
    total_results=[]
    image =''
    if search.inp.data:
        total_results, image = Scraping_for_search(search.inp.data)
    return render_template(
        'BP-a.html',
        css="BP-a",
        link_e="/",
        title="ar",
        search=search,
        message=messages,
        results=total_results,
        name=search.inp.data,
        image= image 
        )
