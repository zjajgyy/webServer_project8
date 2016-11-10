import PIL.Image
import imghdr
from io import BytesIO
from flask import Flask,render_template,request,Response
import consul
import json


APP = Flask(__name__)

c = consul.Consul(host="192.168.1.1", port=8500)
c.agent.service.register('consul_image',service_id='100',address='192.168.1.3',port=8082)

@APP.route('/image_service',methods=["POST","GET"])
def image_service():
    """this is for picture"""
    if (request.method == 'POST'):
        print("dabaiiiiiiiiiiiiiiiiiiiiiii")
        scale = request.form.get('scale')
        print("image_service scale :" + scale)
        files = request.files['file']
        file_type = imghdr.what(files)
        code = 200
        byte_io = BytesIO()
        if (scale == None):
            scale = '1'
        if (file_type != None):
            try:
                im = PIL.Image.open(files)
            except Exception:
                code = 600
            (x, y) = im.size
            x_s = x * float(scale)
            y_s = y * float(scale)
            print(x)
            print(x_s)
            out = im.resize((int(x_s), int(y_s)), PIL.Image.ANTIALIAS)
            out.save(byte_io, file_type)
            byte_io.seek(0)
        else:
            code = 600
        if code == 200:
            return Response(byte_io,mimetype=file_type,status=code)
        elif code == 600:
            return Response(json.dumps('image.html'),status=code)
    else:
        return Response(json.dumps('image.html'))


@APP.route('/scale_service',methods=['post'])
def judge_scale():
    scale = request.form.get('scale')
    print("dabaiiiiii scale : " + scale)
    scale_temp = scale.replace('.', '')
    if(scale_temp.isdigit()):
        if(scale == '0'):
            return Response(json.dumps("NO"))
        else:
            return Response(json.dumps("Yes"))
    else:
        return Response(json.dumps("No"))

if __name__ == '__main__':
    APP.run(host="0.0.0.0",port=8082)
