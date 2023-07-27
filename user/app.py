#!/usr/bin/python

from flask import Flask, jsonify, session, request, redirect
import json
from flask_cors import CORS 
import pymysql

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)

db_config = {
    'host': '13.125.215.66',
    'user': 'gasida',
    'password': 'qwe123',
    'db': 'userinfo',
}

# MySQL 연결 함수
def get_db():
    return pymysql.connect(**db_config)

# 회원 로그인 API
@app.route('/api/user', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        # 사용자 정보 조회
        query = "SELECT * FROM userinfo WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = request.form['username']
            # 로그인 성공 시 리다이렉트 URL 반환
            return redirect("/w/login", code=302)
   
        else:
            return redirect("/w/loginfail", code=302)

    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


@app.route("/api/user", methods=["GET"])
def get():
    if "username" in session:
        print(session["username"])
        return ("session found:"+session["username"])
    else:
        return ("Session not found: ")

@app.route("/api/user/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/w/login", code=302)


# 회원가입 API
@app.route('/api/user/signup', methods=['POST'])
def signup():
    try:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        birthdate = request.form['birthdate']

        if password != confirm_password:
            return jsonify({'message': '비밀번호가 일치하지 않습니다.'}), 400

        # 데이터베이스에 회원 정보 저장
        conn = get_db()
        cursor = conn.cursor()

        query = "INSERT INTO userinfo (username, password, name, address, phone, email, birthdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, name, address, phone, email, birthdate))

        conn.commit()
        cursor.close()
        conn.close()

        return '''
        <script>
            alert('회원가입이 완료되었습니다.');
            window.location.href = "/"; // 회원가입 완료 후 로그인 페이지로 리다이렉트
        </script>
        '''


    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500

@app.route("/api/user/status", methods=["GET"])
def get_user_info():
    if "username" in session:
        return jsonify(session["username"]), 200
    else:
        return jsonify(""), 200



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9002,
        debug=True
    )
