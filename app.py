from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

cnx = mysql.connector.connect(
    user='root', password='1234', host='localhost', database='dbms')
cursor = cnx.cursor()
app = Flask(__name__)


@app.route('/rooms', methods=['POST'])
def save_task():
    room_id = request.form.get('room_id')
    cost_room=request.form.get('cost_room')
    query = ("insert into rooms values({}, {})".format(room_id, cost_room))
    cursor.execute(query)
    cnx.commit()
    return redirect(url_for('get_rooms'))

@app.route('/rooms/insert')
def get_rooms():
    return render_template('index.html')

@app.route('/rooms/display')
def dis_rooms():
    rooms=[]
    query=("SELECT room_no,room_cost FROM rooms ")
    cursor.execute(query)
    for (room_no,room_cost) in cursor:
        room = {
            'num': room_no,
            'cost': room_cost
        }
        rooms.append(room)
        print(rooms)
    return render_template('dis_room.html',disprooms=rooms)

@app.route('/book/<num>', methods=['GET','POST'])
def book(num):
    # logic to insert booking details to booking table
    query = ("insert into book values({})".format(num))
    cursor.execute(query)
    cnx.commit()
    return render_template('success.html')
@app.route('/book/available')
def check_available():
    rooms=[]
    query=("select room_no,room_cost from rooms where room_no NOT IN (select * from book);")
    cursor.execute(query)
    for (room_no,room_cost) in cursor:
        room = {
            'num': room_no,
            'cost': room_cost
        }
        rooms.append(room)
        print(rooms)
    return render_template('dis_room.html',disprooms=rooms)
