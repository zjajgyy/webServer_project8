from flask import Flask,render_template,request,Response,make_response
import requests
import consul
import json
from functools import wraps

URL = "http://localhost:8500/v1/catalog/service/"
app = Flask(__name__)


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


def find_service(service_name):
    print("find_service")
    c = consul.Consul(host="192.168.1.1", port=8500)
    (service_id, service_content) = c.catalog.service(service_name)
    ip = service_content[0]["ServiceAddress"]
    port = service_content[0]["ServicePort"]
    return ip, str(port)


@app.route('/index')
@allow_cross_domain
def index():
    return render_template('register.html')


@app.route('/toLogin')
@allow_cross_domain
def to_login():
    return render_template('login.html')


@app.route('/register',methods=['POST','GET'])
@allow_cross_domain
def register():
    ip, port = find_service("consul_database")
    print("data: ", ip)
    url = "http://" + ip + ":" + port + "/register_service"
    email = request.form.get('email')
    password = request.form.get('password')
    data = {'username': email, 'password': password}
    r = requests.post(url, data)
    result = r.text
    print("result: " + json.loads(result))
    return json.loads(result)


@app.route('/judge_email',methods=['POST'])
@allow_cross_domain
def judge_email():
    ip, port = find_service("consul_database")
    url = "http://" + ip + ":" + port + "/judgeEmail_service"
    email = request.form.get('email')
    data = {'username': email}
    r = requests.post(url, data)
    result = r.text
    return json.loads(result)


@app.route('/login',methods=["POST"])
@allow_cross_domain
def login():
    ip, port = find_service("consul_database")
    #print("data: ", ip)
    url = "http://" + ip + ":" + port + "/login_service"
    email = request.form.get('email')
    password = request.form.get('password')
    data = {'username': email, 'password': password}
    print(data)
    r = requests.post(url, data)
    result = r.text
    print("result: " + json.loads(result))
    return json.loads(result)


@app.route('/main_page')
@allow_cross_domain
def main_page():
    return render_template('mainpage.html')


@app.route('/image_resize',methods=["POST","GET"])
@allow_cross_domain
def image_resize():
    ip, port = find_service("consul_image")
    print("data: ", ip)
    url = "http://" + ip + ":" + port + "/image_service"
    if request.method == 'POST':
        scale ={'scale':request.form.get('scale')}
        image_file ={'file': request.files['file']}
        r = requests.post(url,scale,files=image_file)
        print("image_resize status :" + str(r.status_code))
        print("content-type: " + r.headers['Content-Type'])
        if r.status_code == 200 :
            print("valid picture file")
            result = r.content
            return Response(result,mimetype=r.headers['Content-Type'],status=str(r.status_code))
        elif r.status_code == 600:
            result = r.text
            print("600 error : " + result + "status :" + str(r.status_code))
            return render_template(json.loads(result), title=str(r.status_code))
    else:
        r = requests.get(url)
        result = r.text
        print("image_resize result:"+result)
        return render_template(json.loads(result))


@app.route('/judge_scale',methods=["POST","GET"])
@allow_cross_domain
def judge_scale():
    ip, port = find_service("consul_image")
    print("data: ", ip)
    url = "http://" + ip + ":" + port + "/scale_service"
    print("judge_scale url : " + url)
    scale = {'scale': request.form.get('scale')}
    r = requests.post(url, data=scale)
    result = r.text
    print("r result : " + json.loads(result))
    return json.loads(result)


@app.route('/get_info', methods=["POST"])
@allow_cross_domain
def get_info():
    ip, port = find_service("consul_resource")
    print("data: ", ip)
    url = "http://" + ip + ":" + port + "/resource_service"
    r = requests.post(url)
    result = r.text
    print("info url :"+url)
    print("GETINFO: " + json.loads(result))
    return json.loads(result)


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8888)
