from flask import Flask,render_template,request,redirect,url_for,session,flash,jsonify
import sqlite3
from flask import session


app = Flask(__name__)
app.secret_key='your_secret_key'

con=sqlite3.connect("hotelproject.db",check_same_thread=False)
cur=con.cursor()

#create a table
cur.execute("create table if not exists hotel(id integer primary key AUTOINCREMENT,Firstname text,Lastname text,Create_Password text,Confirm_Password text)")
con.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Welcome')
def Register():
    return render_template('Register.html')




@app.route('/Sign_In',methods=["POST","GET"])
def Sign_In():
    return render_template('Sign_In.html')
    

@app.route('/Sign Up',methods=["POST","GET"])
def Sign_Up():
    if request.method =="POST":
        try:

            Firstname=request.form.get('Firstname')
            Lastname=request.form.get('Lastname')
            Create_Password=request.form.get('Create_Password')
            Confirm_Password=request.form.get('Confirm_Password')

            con=sqlite3.connect("hotelproject.db")
            cur=con.cursor()
            cur.execute("insert into hotel(Firstname,Lastname,Create_Password,Confirm_Password) values(?,?,?,?)",(Firstname,Lastname,Create_Password,Confirm_Password))
            con.commit()
            session['user_full_name']=f"{Firstname} {Lastname}"
            flash("User registered successfully","success")
            return redirect('/Sign_In')
        
        except:
            flash("Error in insert operation","danger")
        finally:
            return render_template('Sign_In.html',Firstname=Firstname,Lastname=Lastname,Create_Password=Create_Password,Confirm_Password=Confirm_Password)    
            con.close()
    return render_template('Sign_Up.html')

@app.route('/index/<int:id>',methods=["GET","POST"])
def index(id):
    if request.method =='POST':
        username_or_email=request.form.get('username_or_email')
        password=request.form.get('password')

        #query the database to check if the user exists and the password matches
        con=sqlite3.connect("hotelproject.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM hotel WHERE id = ?", (id,))

        # cur.execute("select * from hotel where Firstname=? and Create_Password=?",(username_or_email,password))
        print(cur)
        user=cur.fetchone()
        print(user)

        if user:
            if password==user[4] and username_or_email==user[1]:
                 print("your login is successful")
                 return render_template("main.html")

            # session["Firstname"] = user["Firstname"]
            # session["Create_Password"] = user["Create_Password"]
            # return redirect(url_for('index'))
            else:
                flash ("Invalid username or password","danger")
    return render_template('Sign_In.html')


@app.route('/Added_items')
def Added_items():
    return render_template("Added_items.html")

@app.route('/add_to_card',methods=["POST"])
def add_to_card():
    item_id=request.json.get('item_id')

    if 'cart' not in session:
        session['cart']=[]
    session['cart'].append(item_id)
    session.modified=True
    return jsonify(cartCount=len(session['cart']))

@app.route('/order')
def order():
    return render_template("order.html")

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/Thankyou")
def Thankyou():
    return render_template("Thankyou.html")

if __name__=='__main__':
    app.run(debug=True)
