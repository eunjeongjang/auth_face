from flask import Flask, render_template, request, redirect, url_for, Response
import mysql.connector
import csv

app = Flask(__name__)

# MySQL 연결 설정
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # MySQL 호스트 (일반적으로 localhost)
        user="root",       # MySQL 사용자 이름
        password="lee1108!!", # MySQL 비밀번호
        database="face_recgnition"   # 사용할 데이터베이스 이름
    )

# 데이터 조회
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from face_rec_reg")  # 'items'는 예시 테이블 이름
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', rows=rows)

# 데이터 삭제
@app.route('/delete', methods=['POST'])
def delete():
    ids_to_delete = request.form.getlist('item_ids')  # 체크된 항목들 가져오기
    if ids_to_delete:
        connection = get_db_connection()
        cursor = connection.cursor()
        # 선택된 항목들을 삭제
        cursor.execute('delete from face_rec_reg where id in ({})'.format(','.join(ids_to_delete)))
        connection.commit()
        cursor.close()
        connection.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # init_db()  # 앱 실행 시 데이터베이스 초기화
    app.run(debug=True)
