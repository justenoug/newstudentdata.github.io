from flask import Flask, flash, render_template, request, redirect, session
from flask.helpers import get_flashed_messages
from flask_session import Session

import db

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# map the specific URL
    
@app.route("/")
def get_holdings():
    print(session.get('user_name'))
    if not session.get('user_name'):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    try:
        db_obj = db.Database()
        #value returned by get_holdings is assigned to a variable (holdings)
        holdings =db_obj.get_holdings(session['user_name'])
        #
        return render_template('holding.html', holdings=holdings,name=session['user_name'])
    except Exception as e:
        print(str(e))
        return "Oops, something failed"

@app.route("/stock", methods=['GET','POST'])
def stock():
    #templates to render HTML which will display in the user's browser
    if session.get('user_name'):
        if(request.method=='GET'):
            return render_template('stock.html',username = session['user_name'])
        elif(request.method=='POST'):
            try:
                #instance (object) of our database class
                db_obj = db.Database()

                holdings = db_obj.get_holding(request.form["symbol"],session['user_name'])

                if len(holdings) > 0:
                    return "Cannot add holding since it already exists"

                #calling add_holding function with request.form(current request on http) as parameters
                #else:
                db_obj.add_holding(request.form["symbol"], request.form["quantity"], request.form["price"], request.form["date"], request.form["notes"],session['user_name'])
                #redirecting to the given url
                return redirect("/")
            except:
                return "Oops, something failed"    
    return redirect('/login')    


@app.route("/signup", methods=['POST','GET'])
def signup():
    session.pop('user_name', None)
    try :
        if(request.method=='GET'):
            
            message=get_flashed_messages()
            #print(message)
            if(len(message)>0):
                m=message[0]
                session.pop('_flashes', None)
                return render_template('signup.html', message=m)
            return render_template('signup.html')

        elif(request.method=='POST'):
            
            username = request.form['name']
            password = request.form['pass']
            email = request.form['email']    
            #print(username, email, password)

            db_obj=db.Database()
            user = db_obj.get_user(username,email)
            print(len(user))

            if(len(user)==0):
                db_obj.register(username,email,password)
                session['user_name'] = username
                return redirect("/")
            else  : 
                print("username or email already exists")
                flash("username or email already exists")
                return redirect("signup")

                

    except Exception as e:
        print(str(e))
        
        return "oops, something failed"        

@app.route("/logout")

def logout():
    session.pop('user_name')
    return redirect("/")

@app.route("/login",methods=['POST','GET'])
def login():
    session.pop('user_name', None)
    try :
        if(request.method=='GET'):
            return render_template('login.html')
        elif(request.method=='POST'):
            session.pop('user_id', None)
            username = request.form['name']
            password = request.form['pass']
            db_obj=db.Database()
            user=db_obj.fetch_user(username,password)
            if(len(user)==1):
                #print("I AM HERE ")
                session['user_name']=username
                
                return redirect("/")

            #print("I AM HERE ")
            flash("Wrong username or password!")
            return redirect("/login")
    except Exception as e:
        print(e)    

    
@app.route("/delete")
def delete_holdings():
    if not session.get('user_name'):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    #fetch data of query parameter in url 
    symbol = request.args.get('symbol')

    try:
        db_obj = db.Database()
        db_obj.delete_holding(symbol)
        return redirect("/")
    except:
        return "Oops, something failed"

@app.route("/update-stock", methods=['POST'])
def update_holding():
    if not session.get('user_name'):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    try:
        db_obj = db.Database()
        #value returned by get_holdings is assigned to a variable (holdings)
        holdings = db_obj.get_holding(request.form["symbol"],session['user_name'])

        if len(holdings) == 0:
            return "Cannot update holding since it doesn't exists"
        db_obj.update_holding(request.form["symbol"], request.form["quantity"], request.form["price"], request.form["date"], request.form["notes"])
        return redirect("/")
    except Exception as e:
        print(str(e))
        return "Oops, something failed"

@app.route("/update")
def fetch_holdings1():
    #getting the data 
    symbol = request.args.get('symbol')
    db_obj = db.Database()
    holdings = db_obj.get_holding(symbol,session['user_name'])
    #assigning the value of holdings[0] in holding
    holding = holdings[0]

    print(holding[0])
    return render_template('update.html', holding=holdings[0])



