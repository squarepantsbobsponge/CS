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
    {"sid": "67890", "sname": "Bob", "password": "password456", "status": 3},
]

mock_seats = {
    "101": {"floor": 1, "isAvailable": "Y"},
    "102": {"floor": 1, "isAvailable": "N"},
    "103": {"floor": 1, "isAvailable": "Y"},
    "104": {"floor": 1, "isAvailable": "Y"},
    "105": {"floor": 1, "isAvailable": "Y"},
    "201": {"floor": 2, "isAvailable": "Y"},
    "202": {"floor": 2, "isAvailable": "Y"},
    "203": {"floor": 2, "isAvailable": "Y"},
    "204": {"floor": 2, "isAvailable": "Y"},
    "205": {"floor": 2, "isAvailable": "Y"},
    "206": {"floor": 2, "isAvailable": "Y"},
    "207": {"floor": 2, "isAvailable": "Y"},
    "208": {"floor": 2, "isAvailable": "Y"},
    "209": {"floor": 2, "isAvailable": "Y"},
    "210": {"floor": 2, "isAvailable": "Y"},
    "211": {"floor": 2, "isAvailable": "Y"},
}

mock_book_slots = {
    "101": {1: "Y", 2: "N", 3: "N", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "102": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "103": {1: "Y", 2: "N", 3: "N", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "104": {1: "Y", 2: "N", 3: "N", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "105": {1: "Y", 2: "N", 3: "N", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "201": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "202": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "203": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "204": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "205": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "206": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "207": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "208": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "209": {1: "Y", 2: "Y", 3: "Y", 4: "Y", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "210": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
    "211": {1: "N", 2: "N", 3: "N", 4: "N", 5: "N", 6: "N", 7: "N", 8: "N", 9: "N", 10: "N", 11: "N", 12: "N", 13: "N", 14: "N"},
}

mock_signin_records = [
    {"id": "101", "sid": "12345", "start_time": "2023-10-01 08:00:00", "sign_in_time": "2023-10-01 08:05:00", "isSingIn": "Y"},
    {"id": "201", "sid": "67890", "start_time": "2023-10-01 09:00:00", "sign_in_time": None, "isSingIn": "N"},
    {"id": "207", "sid": "67891", "start_time": "2023-10-01 10:00:00", "sign_in_time": None, "isSingIn": "N"},
    {"id": "208", "sid": "67892", "start_time": "2023-10-01 11:00:00", "sign_in_time": None, "isSingIn": "N"},
    {"id": "209", "sid": "67893", "start_time": "2023-10-01 12:00:00", "sign_in_time": None, "isSingIn": "N"},
    {"id": "210", "sid": "67894", "start_time": "2023-10-01 13:00:00", "sign_in_time": None, "isSingIn": "N"},
]

mock_blacklist_records = [
    {"sid": "67890", "sname": "Bob", "status": 3},
    {"sid": "66666", "sname": "Bow", "status": 2},
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
    # status = session['status']
    status = session.get('status', 0)
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
    status = session.get('status', 0)
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
                record["isSingIn"] = "Y"  # 更新签到状态为 "Y"
                result = (True, [record])
                break

    # 处理前端通过 AJAX 请求签到
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        id = request.json.get('id')
        sid = request.json.get('sid')

        # 模拟签到逻辑
        for record in mock_signin_records:
            if record["id"] == id and record["sid"] == sid:
                record["isSingIn"] = "Y"  # 更新签到状态为 "Y"
                return jsonify({"status": "success", "message": "签到成功"})

        return jsonify({"status": "error", "message": "签到失败，未找到对应记录"})

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

        # 处理查询请求
        if choice == '1':
            if sid == '':  # 查询所有黑名单记录
                results = mock_blacklist_records
            else:  # 根据学号查询黑名单记录
                results = [record for record in mock_blacklist_records if record["sid"] == sid]
            result = (choice, results)

        # 处理修改请求
        elif choice == '2':
            if sid and status:  # 学号和冷冻时间都不为空
                for record in mock_blacklist_records:
                    if record["sid"] == sid:
                        record["status"] = int(status)
                        break
                else:
                    mock_blacklist_records.append({"sid": sid, "sname": "New Student", "status": int(status)})
                results = [record for record in mock_blacklist_records if record["sid"] == sid]
                result = (choice, results)
            else:
                flash('学号和冷冻时间不能为空', 'error')

    # 处理前端通过 AJAX 请求查询黑名单记录
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        sid = request.json.get('sid')
        new_status = request.json.get('status')

        if new_status is not None:  # 处理修改请求
            for record in mock_blacklist_records:
                if record["sid"] == sid:
                    record["status"] = int(new_status)
                    return jsonify({"status": "success", "message": "冷冻时间修改成功"})
            return jsonify({"status": "error", "message": "未找到对应学号"})

        else:  # 处理查询请求
            if sid:
                results = [record for record in mock_blacklist_records if record["sid"] == sid]
                if results:
                    return jsonify({"status": "success", "data": results})
                else:
                    return jsonify({"status": "error", "message": "此人不在黑名单中"})
            else:
                return jsonify({"status": "error", "message": "请输入学号"})

    return render_template('blacklist.html', form=form, results=result, mock_blacklist_records=mock_blacklist_records)


@app.route('/search_signin', methods=['GET'])
def search_signin():
    sid = request.args.get('sid')
    results = [record for record in mock_signin_records if record["sid"] == sid]
    print(results)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)