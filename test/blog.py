# coding=utf-8
# @File  : blog.py
# @Author: PuJi
# @Date  : 2018/4/3 0003
import json
import yaml


from flask import Flask, request
app = Flask(__name__)


@app.route('/test',methods=['POST'])
def recharge_wallet():

    original_data = request.json
    print(original_data)
    print type(original_data)
    # data = yaml.safe_load(json.dumps(original_data))
    data = original_data
    username = request.json.get('username')
    source = request.json.get('source')
    print(source)
    print(username)
    print(source)
    print(data)
    return "{'result':True}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)