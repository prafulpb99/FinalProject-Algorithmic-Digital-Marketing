
from flask import Flask,render_template,url_for,request, flash
import pandas as pd 
import numpy as np
import re
import pickle
import datetime
from flask_mail import Mail,Message
from datetime import date




user_df = pd.read_csv('demo_new.csv')
#print(user_df.head())
model = pickle.load(open('xgb_reg.pkl','rb'))



app = Flask(__name__)
app.config['DEBUG']= True
app.config['TESTING']= False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USE_TLS']= False
app.config['MAIL_USE_SSL']= True
# app.config['MAIL_DEBUG']= True
app.config['MAIL_USERNAME']= 'adm.sps2020@gmail.com'
app.config['MAIL_PASSWORD']= '2020sps.adm'
app.config['MAIL_DEFAULT_SENDER']= 'adm.sps2020@gmail.com'
app.config['MAIL_MAX_EMAILS']=None
# app.config['MAIL_SUPPRESS_SEND']
app.config['MAIL_ASCII_ATTACHMENT']= False

#app.config['MAIL_USERNAME']= 'adm.sps2020@gmail.com'
#app.config['MAIL_PASSWORD']= '2020sps.adm'
mail= Mail(app)
today = date.today()
#tlitle = request.form['message']

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/promotion',methods=['GET'])
def promotion():
    return render_template('promotion.html')

@app.route('/customerdash',methods=['GET'])
def customerdash():
    return render_template('dashboard.html')

@app.route('/insightsdash',methods=['GET'])
def insightsdash():
    return render_template('insights.html')

@app.route('/AddToCart',methods=['POST'])

def AddToCart():
    print('11112222')

    if request.method == 'POST':
        #print('11111')
        userid = int(request.form['userid'])
        #print(userid)
        #print(user_df.user_id.tolist())

        
        if userid in user_df.user_id.tolist():

            #print('here')
            index = int(user_df[user_df['user_id'] == userid].index[0])
            age_range=int(user_df.get_value(index, 'age_range'))
            marital_status=int(user_df.get_value(index, 'marital_status'))
            gender=int(user_df.get_value(index, 'gender'))
            city=int(user_df.get_value(index, 'city'))
            state=int(user_df.get_value(index, 'state'))
            job=int(user_df.get_value(index, 'job'))
            event_weekday = int(datetime.datetime.today().weekday())
            #brand= request.args.get('myList1')
            category_code_level1= request.args.get('myList2')
            category_code_level2= request.args.get('myList3')
            brand = request.form.get('brandList')

           
            #category_code_level1 = request.form['myList2']
            #category_code_level2 = request.form['myList3']
            price = float(request.form['price'])
            #print(gender)
            print(city)
            print(state)
            print(job)
            print(brand)
            #result=model.predict([[brand, price,event_weekday, category_code_level1,category_code_level2, 4 , age_range, marital_status,gender, city, state, job]])
            values= [3, price,event_weekday, category_code_level1,category_code_level2, 4 , age_range, marital_status,gender, city, state, job]
            headers = ['brand', 'price','event_weekday', 'category_code_level1','category_code_level2', 'activity_count' , 'age_range', 'marital_status','gender', 'city', 'state', 'job']
            
            input_variables = pd.DataFrame([values],
                                columns=headers, 
                                dtype=float,
                                index=['input'])
            result = model.predict(input_variables)
            #prediction = (prediction_proba[0])[1]
            #print(prediction)
            if int(result) == 0:
                #print(str(brand))
                

                pred_text = "You have just unlocked a coupon. Please check your registered mail id to redeem your coupon.\n\nProduct is added to the cart!"
                
                msg = Message(subject="Today Only: Save 30% on "+ str(brand),
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=['prafulpb99@gmail.com'
                                      #,'sekhar.s@husky.neu.edu'
                                      ]) # replace with your email for testing
                msg.body= "Hi,\n\nSave 30% on all " + str(brand) + " products TODAY. (" + str(today) + ").\nUse code 30"+ str(brand) + " for upto 30% OFF.\n\nThank you for shopping with us!."
                          
                #print(str(model_prediction))
                mail.send(msg)
            else:

                pred_text = "Product is added to the cart"
            
 
        else:
            pred_text = "Please try a correct user-id!"
            

            

    return render_template('promotion.html',prediction_text = pred_text)



if __name__ == '__main__':
	app.run(debug=True)