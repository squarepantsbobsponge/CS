from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '20241030'

# 模拟数据
mock_students = [
    {"sid": "12345", "sname": "Alice", "password": "password123", "status": 0},
    {"sid": "67890", "sname": "Bob", "password": "password456", "status": 1},
]

mock_seats = {
    "101": {"floor": 1, "isAvailable": "Y"},
    "102": {"floor": 1, "isAvailable": "N"},
    "201": {"floor": 2, "isAvailable": "Y"},
    "203": {"floor": 2, "isAvailable": "Y"},
}

mock_book_slots = {
    "101": {1: "Y", 2: "N", 3: "N", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "102": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "201": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "203": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
}

mock_signin_records = [
    {"id": "101", "sid": "12345", "start_time": "2023-10-01 08:00:00", "sign_in_time": "2023-10-01 08:05:00", "isSingIn": "Y"},
    {"id": "201", "sid": "67890", "start_time": "2023-10-01 09:00:00", "sign_in_time": None, "isSingIn": "N"},
]

mock_blacklist_records = [
    {"sid": "67890", "sname": "Bob", "status": 1},
]

# 表单定义
class LoginForm(FlaskForm):
    userid = StringField('Userid', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('none', '请选择用户类型'), ('student', 'Student'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    choice1 = SelectField('选择楼层', choices=[(1, '一楼'), (2, '二楼')], validators=[DataRequired()])
    choice2 = StringField('座位号')
    submit = SubmitField('Search')

class AppointmentForm(FlaskForm):
    start_time = SelectField('Start Time', choices=[
        (1, '08:00 AM'),
        (2, '09:00 AM'),
        (3, '10:00 AM'),
        (4, '11:00 AM'),
    ], validators=[DataRequired()])
    end_time = SelectField('End Time', choices=[
        (1, '08:00 AM'),
        (2, '09:00 AM'),
        (3, '10:00 AM'),
        (4, '11:00 AM'),
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Appointment')

class SignInForm(FlaskForm):
    id = StringField("座位号", validators=[DataRequired()])
    sid = StringField("学号", validators=[DataRequired()])
    sign_time = StringField('签到时间', validators=[DataRequired()])
    submit = SubmitField('签到')

class BlackListForm(FlaskForm):
    choice = SelectField('功能', choices=[(1, '查询'), (2, '添加/修改')], validators=[DataRequired()])
    sid = StringField('学号')
    status = StringField('冷冻时间')
    submit = SubmitField('确认')

# 路由定义
@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 获取表单数据
        userid = form.userid.data
        password = form.password.data
        role = form.role.data

        # 检查角色是否为 "none"
        if role == 'none':
            # 弹出提示窗口
            flash('请选择角色', 'error')
            return redirect(url_for('login'))

        # 模拟登录逻辑
        if role == 'student':
            session['userid'] = userid
            return redirect(url_for('individual_information'))
        elif role == 'admin':
            session['userid'] = userid
            return redirect(url_for('admin_page'))
        else:
            flash('用户名/密码不正确', 'error')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In', form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if 'userid' not in session:
        return redirect(url_for('login'))
    userid = session['userid']
    status = session['status']
    form = SearchForm()
    pivot_table = {}
    results = []

    if form.validate_on_submit():
        floor = form.choice1.data
        seat_id = form.choice2.data

        if seat_id == '':
            # 如果座位号为空，返回该楼层的所有座位信息
            for seat_id, seat_info in mock_seats.items():
                if seat_info["floor"] == int(floor) and seat_info["isAvailable"] == "Y":
                    pivot_table[seat_id] = mock_book_slots[seat_id]
        else:
            # 如果座位号不为空，返回指定座位号的信息
            if seat_id in mock_book_slots and mock_seats[seat_id]["floor"] == int(floor) and mock_seats[seat_id]["isAvailable"] == "Y":
                pivot_table[seat_id] = mock_book_slots[seat_id]

    return render_template('search.html', title='Search', form=form, results=pivot_table)

@app.route('/book_seat', methods=['GET', 'POST'])
def book_seat():
    if 'userid' not in session:
        return redirect(url_for('login'))
    userid = session['userid']
    status = session['status']
    if status != 0:
        return redirect('/individual_information')

    seat_id = request.args.get('seatId')
    form = AppointmentForm()

    if form.validate_on_submit():
        start_time = int(form.start_time.data)
        end_time = int(form.end_time.data)

        # 模拟预约逻辑
        if start_time >= end_time:
            flash('时间错误，请重新检查')
            return render_template('book_seat.html', form=form)

        if end_time - start_time > 4:
            flash('一次最大预约时间为4个小时，超过最大预约时间')
            return render_template('book_seat.html', form=form)

        for i in range(start_time, end_time):
            if mock_book_slots[seat_id][i] == 'Y':
                flash('预约时间段已被预约')
                return render_template('book_seat.html', form=form)

        for i in range(start_time, end_time):
            mock_book_slots[seat_id][i] = 'Y'

        flash('预约成功')
        return redirect(url_for('individual_information'))

    return render_template('book_seat.html', form=form)

@app.route('/individual_information', methods=['GET', 'POST'])
def individual_information():
    if 'userid' not in session:
        flash('You must be logged in to view your information.', 'error')
        return redirect(url_for('login'))
    userid = session['userid']
    status = session.get('status', 0) 

    if status == 0:
        status_message = "账号可用"
    else:
        status_message = f"账号锁定中，{status}天后解封"

    # 模拟获取预约记录
    results = [record for record in mock_signin_records if record["sid"] == userid]

    unsubscribe_message = request.args.get('unsubscribe_message', '')
    return render_template('individual_information.html', title='Individual Information', results=results, userid=userid, status=status_message, unsubscribe_message=unsubscribe_message)

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if 'userid' not in session:
        flash('You must be logged in to view your information.', 'error')
        return redirect(url_for('login'))
    userid = session['userid']
    unsubscribe_message = ''

    # 模拟取消订阅逻辑
    for record in mock_signin_records:
        if record["sid"] == userid:
            mock_signin_records.remove(record)
            unsubscribe_message = "删除成功!"
            break

    if not unsubscribe_message:
        unsubscribe_message = "删除失败，没有待预约记录或者超过取消预约时间(至少早于开始时间的30min)"

    return redirect(url_for('individual_information', unsubscribe_message=unsubscribe_message))

@app.route('/exit_login', methods=['GET'])
def exit_login():
    session.pop('userid', None)
    session.pop('status', None)
    return redirect(url_for('login'))

@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    if 'userid' not in session:
        flash('you must be restart to log in admin_page!', 'error')
        return redirect(url_for('login'))
    return render_template('admin_page.html', title='admin_page')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    results = []
    result = (False, None)

    if form.validate_on_submit():
        id = form.id.data
        sid = form.sid.data
        sign_time = form.sign_time.data

        # 模拟签到逻辑
        for record in mock_signin_records:
            if record["id"] == id and record["sid"] == sid:
                result = (True, [record])
                mock_signin_records.remove(record)
                break

    return render_template('signin.html', form=form, results=result, mock_signin_records=mock_signin_records)

@app.route('/blacklist', methods=['GET', 'POST'])
def blacklist():
    form = BlackListForm()
    results = []
    result = (1, None)

    if form.validate_on_submit():
        choice = form.choice.data
        sid = form.sid.data
        status = form.status.data

        # 模拟黑名单逻辑
        if choice == '1':
            if sid == '':
                results = mock_blacklist_records
            else:
                results = [record for record in mock_blacklist_records if record["sid"] == sid]
            result = (1, results)
        elif choice == '2':
            if sid and status:
                for record in mock_blacklist_records:
                    if record["sid"] == sid:
                        record["status"] = int(status)
                        break
                else:
                    mock_blacklist_records.append({"sid": sid, "sname": "New Student", "status": int(status)})
                results = [record for record in mock_blacklist_records if record["sid"] == sid]
                result = (2, results)

    return render_template('blacklist.html', form=form, results=result)

@app.route('/search_signin', methods=['GET'])
def search_signin():
    sid = request.args.get('sid')
    results = [record for record in mock_signin_records if record["sid"] == sid]
    return jsonify(results)

@app.route('/appointment_info', methods=['GET'])
def appointment_info():
    if 'userid' not in session:
        flash('You must be logged in to view your information.', 'error')
        return redirect(url_for('login'))
    userid = session['userid']

    # 模拟获取预约记录
    results = [record for record in mock_signin_records if record["sid"] == userid]

    return render_template('appointment_info.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)