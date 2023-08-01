#!/usr/bin/python

from flask import Flask, jsonify, request
import json
import requests
from flask_cors import CORS 
import pymysql


db_config = {
    'host': '43.202.54.126',  ## 실제 데이터베이스 주소 
    'user': 'gasida',
    'password': 'qwe123',
    'db': 'products',
}

def get_db():
    return pymysql.connect(**db_config)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
@app.route("/api/order", methods=["GET"])
def get_orders():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # 딕셔너리 형태로 변환하여 JSON으로 반환
        orders = []
        for row in rows:
            order = {
                'id': row[0],
                'name': row[1],
                'store': row[2],
                'storeId': row[3],
                'price': row[4],
                'img': row[5]
            }
            orders.append(order)

        return jsonify(orders), 200

    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


@app.route("/api/order/<oid>", methods=["GET"])
def order(oid):
    try:
        # 주문 데이터 조회
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # 주문 데이터를 딕셔너리 형태로 변환하여 JSON으로 반환
        orders = []
        for row in rows:
            order = {
                'id': row[0],
                'name': row[1],
                'store': row[2],
                'storeId': row[3],
                'price': row[4],
                'img': row[5]
            }
            orders.append(order)

        # 주문 데이터를 JSON 형식으로 변환
        orders_json = json.dumps(orders)

        # JSON 형식의 데이터를 파싱하여 딕셔너리로 변환
        data = json.loads(orders_json)

        # 가게 정보 조회를 위해 주문 데이터에서 해당 가게의 storeId를 찾음
        sid = "0"
        for v in data:
            if v["id"] == oid:
                sid = v["storeId"]
                break

        # 가게 정보 조회
        response = requests.get("http://k8s-green-5ca3ac43a6-1240869498.ap-northeast-2.elb.amazonaws.com/api/store/" + sid)
        store_status = response.json()

        return store_status

    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500


def get_product_info(order_id):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # products 테이블에서 해당 주문에 해당하는 가격, 상품명, 상점명 조회
            sql = "SELECT price, name, store FROM products WHERE id = %s"
            cursor.execute(sql, (order_id,))
            product_info = cursor.fetchone()
            return product_info
    finally:
        conn.close()

# orders 테이블에 주문 정보 저장하는 함수
def save_order(order_id, name, store, price):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # orders 테이블에 주문 정보와 상품 정보 저장
            sql = "INSERT INTO orders (order_id, name, store, price) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (order_id, name, store, price))
        conn.commit()
    finally:
        conn.close()

@app.route('/api/order/complete/<int:orderId>', methods=['POST','GET'])
def complete_order(orderId):
    data = request.get_json()
    order_id = data.get('orderId')  # 주문 ID를 받아옴
    product_info = get_product_info(order_id)
    if product_info:
        # Extract necessary values from product_info tuple
        price, name, store = product_info

        # orders 테이블에 주문 정보와 상품 정보 저장
        save_order(order_id, name, store, price)
        return jsonify({'message': '주문이 완료되었습니다.'}), 200
    else:
        return jsonify({'message': '상품 정보를 가져오는 데에 실패했습니다'}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9001,
        debug=True
    )


