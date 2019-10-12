from flask import Flask, jsonify, request, render_template,redirect, send_from_directory
import numpy as np
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import sys
from collections import OrderedDict
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize

app= Flask(__name__)

with open('database_user.json') as dataku:
    data_user = json.load(dataku)

rekomendasi=[]
resep_bahan=[]
cara_masak=[]

db_user=[]

current_user=[]

@app.route('/file/<path:path>')
def aksesfile(path):
    return send_from_directory('file', path)

@app.route('/', methods=['GET','POST'])
def beranda():
    if request.method == "GET":
        if len(current_user)!=0:
            signout='Sign Out'
            user=current_user[0]
            return render_template('welcome_nologin.html',signout=signout,user=user)
        else:
            return render_template('welcome.html')
    else:
        data = request.form
        nama=data['username'].lower()
        pwd=data['password']

        for i in range(len(data_user)):
            if nama==data_user[i]['username']: 
                if pwd==data_user[i]['password']:
                    current_user.append(nama)
                    return redirect('/recommendation')
                else:
                    message='Wrong Password'
                    return render_template('error_login.html',message=message)
            elif i == len(data_user) - 1:
                message="Please Register Your Account First"
                return render_template('error_login.html',message=message)
            else:
                continue

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="GET":
        return render_template('signup.html')
    else:
        logup = request.form
        nama_up=logup['user_input']
        pwd_up=logup['pass_input']
        for i in range(len(data_user)):
            db_user.append(data_user[i]['username'])
        if nama_up in db_user:
            message='Your Username Already Exist'
            return render_template('error_login.html', message=message)
        else:
            data_user.append({'username': nama_up, 'password': pwd_up})
            data_user_full = json.dumps(data_user)
            data_user_json = open('database_user.json', 'w')
            data_user_json.write(data_user_full)
            current_user.append(nama_up)
            return redirect('/recommendation')

@app.route('/signout',methods=['GET','POST'])
def signout():
    current_user.clear()
    return render_template('welcome.html')

@app.route('/about')
def about():
    if len(current_user)!=0:
        signout='Sign Out'
        user=current_user[0]
        return render_template('about.html',signout=signout,user=user)
    else:
        return render_template('about.html')

@app.route('/visualization')
def visualization():
    if len(current_user)!=0:
        signout='Sign Out'
        user=current_user[0]
        return render_template('visualization.html',signout=signout,user=user)
    else:
        return render_template('visualization.html')

@app.route('/recommendation',methods=['POST','GET'])
def recommendation():
    rekomendasi.clear()
    resep_bahan.clear()
    cara_masak.clear()
    if request.method=='POST':
        return render_template('recommendation.html')
    else:
        if len(current_user)!=0:
            signout='Sign Out'
            user=current_user[0]
            return render_template('recommendation.html',signout=signout,user=user)
        else:
            message='Please Login First'
            return render_template('error_login.html',message=message)
        
@app.route('/hasil',methods=['POST'])
def hasil():
    if request.method == "POST":
        data_input=request.form
        ingredients=data_input['ingredients'].lower()
        selected_dish = request.form.get("dish")
        if selected_dish=='ayam':
            dataresep=df[df['category']=='ayam']
        elif selected_dish=='ikan':
            dataresep=df[df['category']=='ikan']
        elif selected_dish=='telur':
            dataresep=df[df['category']=='telur']
        elif selected_dish=='tahu':
            dataresep=df[df['category']=='tahu']
        elif selected_dish=='tempe':
            dataresep=df[df['category']=='tempe']
        elif selected_dish=='sapi':
            dataresep=df[df['category']=='sapi']
        else:
            message='Input Your Main Dish'
            return render_template('error_login.html',message=message)
        
        dataresep=dataresep[dataresep['Title']!='Data Input']
        dataresep=dataresep.append({'Title':'Data Input','Ingredients':ingredients}, ignore_index=True)

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(dataresep['Ingredients'])
        cosine_sim= cosine_similarity(count_matrix)
        indexinput=dataresep[dataresep['Title']== 'Data Input'].index.values[0]
        food=list(enumerate(cosine_sim[indexinput]))
        sortfood=sorted(food, key=lambda i:i[1], reverse=True)
        
        for i in sortfood[:6]:
            if dataresep.iloc[i[0]]['Title']!='Data Input':
                rekomendasi.append(dataresep.iloc[i[0]]['Title'])

        for i in rekomendasi:
            resep_bahan.append(data['Ingredients'][data['Title']==i].values[0])
            cara_masak.append(data['Steps'][data['Title']==i].values[0])
        signout='Sign Out'
        user=current_user[0]
    return render_template('result_alter.html',rekomendasi=rekomendasi, resep_bahan=resep_bahan, cara_masak=cara_masak,signout=signout,user=user)

@app.route('/resep',methods=['POST','GET'])
def resep():
    resep_klik = request.form.get("resep")
    if resep_klik=='0':
        rekomen=rekomendasi[0]
        resep=resep_bahan[0].split('--')
        cara=cara_masak[0].split('--')
    elif resep_klik=='1':
        rekomen=rekomendasi[1]
        resep=resep_bahan[1].split('--')
        cara=cara_masak[1].split('--')
    elif resep_klik=='2':
        rekomen=rekomendasi[2]
        resep=resep_bahan[2].split('--')
        cara=cara_masak[2].split('--')
    elif resep_klik=='3':
        rekomen=rekomendasi[3]
        resep=resep_bahan[3].split('--')
        cara=cara_masak[3].split('--')
    elif resep_klik=='4':
        rekomen=rekomendasi[4]
        resep=resep_bahan[4].split('--')
        cara=cara_masak[4].split('--')
    signout='Sign Out'
    user=current_user[0]
    return render_template('full_receipt.html',rekomendasi=rekomen, resep_bahan=resep, cara_masak=cara,signout=signout,user=user)

if __name__=='__main__':
    #Data
    data=pd.read_csv('datasets/data_full.csv')
    df=data[['Title','category']]

    Ingredients=[]
    for i in data['Ingredients']:
        lower=i.lower()
        number=re.sub("\d"," ",lower)
        punct=re.sub(r"[^\w\s]"," ",number)
        space=re.sub(r"\s+"," ",punct)
        Ingredients.append(space)

    df['Ingredients']=Ingredients

    #Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    datastemmed = map(lambda x: stemmer.stem(x),
    Ingredients)
    datastemmed = list(Ingredients)
    df['Ingredients']=datastemmed
    
    #Sinonim Kata
    sinonim = {}
    with open("synonim.txt") as file:
        for line in file:
            (key, val) = line.split(":")
            sinonim[key] = val.replace("\n","")

    stopwords=open('stopwords_id.txt','r').read()
    
    def replace_all(data, dic):
        for i, j in dic.items():
            data = data.replace(i, j)
        return data
    dic = OrderedDict(sinonim)

    datachange = []
    for line in df['Ingredients']:
        result = replace_all(line, dic)
        datachange.append(result)
        
    df['Ingredients']=datachange

    resepfinal=[]
    for line in datachange:
        word_token = word_tokenize(line)
        word_token = [word for word in word_token if not word in stopwords and not word[0].isdigit()]
        resepfinal.append(" ".join(word_token))
    df['Ingredients']=resepfinal
    app.run(debug=True)