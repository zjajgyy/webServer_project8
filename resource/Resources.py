import consul
from flask import Flask,Response
import psutil
import json

app = Flask(__name__)
c = consul.Consul(host="192.168.1.1", port=8500)
c.agent.service.register('consul_resource',service_id='resource_id',address='192.168.1.2',port=8081)
@app.route('/resource_service',methods=['POST','GET'])
def getRescourse():
    print("INTORESOURCE")
    mem = psutil.virtual_memory()
    cpu = str(psutil.cpu_percent())
    ram = str(mem.used/mem.total)
    info = cpu+":"+ram
    print(info)
    resp = Response(json.dumps(info))
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
