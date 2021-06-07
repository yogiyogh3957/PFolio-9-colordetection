from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename
from PIL import Image
from collections import defaultdict
from collections import Counter
import requests
import itertools
import math

STOCK_ENDPOINT = "http://thecolorapi.com/id?"

PEOPLE_FOLDER = os.path.join('static', 'uploads')

UPLOAD_FOLDER = '/Users/yogianantaputra'
FOLDER = "/Users/yogianantaputra/PycharmProjects/PFolio-9-colordetection/static/img"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
Bootstrap(app)

# all Flask routes below
@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("home")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('display_image', filename=filename))
    return render_template("index.html")


@app.route('/display_image/<filename>', methods=['POST', 'GET'])
def display_image(filename):
    if request.method == 'POST':
        print("yogi")
        return redirect(url_for('process_image', filename=filename))
    return render_template("showimage.html", image=f"uploads/{filename}")

@app.route('/process_image/<filename>', methods=['POST', 'GET'])
def process_image(filename):
    top5color = []
    rgbcode = []
    print("process showing color begin")
    im = Image.open(f'static/uploads/{filename}')
    by_color = defaultdict(int)

    #pixel counter each rgb code color
    for pixel in im.getdata():
        by_color[pixel] += 1

    #shorting by color with most pixel
    c = Counter(by_color)
    most_common = c.most_common(len(by_color))
    print(f"jumlah variasi warna = {len(by_color)}")

    #data cleaner, separating pixel count
    for data in range(len(most_common)):
        a = most_common[data][0] # datanya = ((255,255,255), 13456), diambil ke - 0
        a_list = list(a) #jadikan list
        try :
            a_list.pop(3)
        except IndexError :
            pass
        top5color.append(a_list)
    # print(top5color)

    #convert list to tupple,
    for x in range(len(top5color)):
        a = tuple(top5color[x])
        b = str(a)
        rgbcode.append(b)

    #rgb code is str tupple, converting into INT
    int_rgbcode = []
    for key in rgbcode:
        res = tuple(int(num) for num in key.replace('(', '').replace(')', '').replace('...', '').split(', '))
        int_rgbcode.append(res)

    #separated R G B from int_rgbcode
    red = []
    green = []
    blue = []

    def get_blue(correction, col_index):
        for num in range(len(int_rgbcode)):
            if int_rgbcode[num][2] > int_rgbcode[num][1]+correction and int_rgbcode[num][2] > int_rgbcode[num][0]+correction:
                blue.append(int_rgbcode[num])
        return blue[col_index]

    def get_green(correction, col_index):
        for num in range(len(int_rgbcode)):
            if int_rgbcode[num][1] > int_rgbcode[num][0]+correction and int_rgbcode[num][1] > int_rgbcode[num][2]+correction:
                green.append(int_rgbcode[num])
        return green[col_index]

    def get_red(correction, col_index):
        for num in range(len(int_rgbcode)):
            if int_rgbcode[num][0] > int_rgbcode[num][1]+correction and int_rgbcode[num][0] > int_rgbcode[num][2]+correction:
                red.append(int_rgbcode[num])
        return red[col_index]

    try :
        red_html = get_red(50, 0)
        green_html = get_green(50, 0)
        blue_html = get_blue(50, 0)
    except IndexError :
        try:
            red_html = get_red(30, 0)
            green_html = get_green(30, 0)
            blue_html = get_blue(30, 0)
        except IndexError:
            try:
                red_html = get_red(20, 0)
                green_html = get_green(20, 0)
                blue_html = get_blue(20, 0)
            except IndexError:
                try:
                    red_html = get_red(15, 0)
                    green_html = get_green(15, 0)
                    blue_html = get_blue(15, 0)
                except IndexError:
                    try:
                        red_html = get_red(10, 0)
                        green_html = get_green(10, 0)
                        blue_html = get_blue(10, 0)
                    except IndexError :
                        try:
                            red_html = get_red(30, 0)
                            green_html = get_red(30, 2)
                            blue_html = get_red(30, 4)
                        except IndexError:
                            try :
                                red_html = get_green(30, 2)
                                green_html = get_green(30, 0)
                                blue_html = get_green(30, 4)
                            except IndexError :
                                try :
                                    red_html = get_blue(30, 0)
                                    green_html = get_blue(30, 2)
                                    blue_html = get_blue(30, 4)
                                except IndexError :
                                    red_html = int_rgbcode[0]
                                    green_html = int_rgbcode[1]
                                    blue_html = int_rgbcode[2]



    print(red[:3])
    print(green[:3])
    print(blue[:3])
    print(int_rgbcode[:3])


    # #Compare each RGB, nilai maksimal 1, jika hasil perbandingan (p) makin mendekati 1 makin jauh warnanya, jika mendekati 0 mirip2
    # new_rgb = []
    # for x, y in itertools.combinations(int_rgbcode, 2):
    #     (r1, g1, b1) = x
    #     (r2, g2, b2) = y
    #     d = math.sqrt(((r2 - r1) * (r2 - r1)) + ((g2 - g1) * (g2 - g1)) + ((b2 - b1) * (b2 - b1)))
    #     p = d / math.sqrt(((255) * (255)) + ((255) * (255)) + ((255) * (255)))
    #
    #     # print(x, y, p)
    #     if p > 0.1:
    #         new_rgb.append(y)
    #         new_rgb.append(x)

        #API nama warna(belum sesuai dg nama warna HTML, dan lambat)
        # params = {
        #     "rgb": f"rgb{b}"
        # }
        # response = requests.get(STOCK_ENDPOINT, params=params)
        # data = response.json()
        # print(data['name']['value'])
        # colors.append(data['name']['value'])

    ## nama warna : code RGB inside dict.
    # color_dict = {}
    # for x in range(len(rgbcode)):
    #     color_dict[colors[x]] = rgbcode[x]
    #
    # new_color_dict = {}
    #
    # for key in color_dict:
    #     if key not in new_color_dict :
    #         new_color_dict[key] = color_dict[key]
    #
    # color_to_html = []
    # # print(new_color_dict)
    # for key in new_color_dict :
    #     color_to_html.append(new_color_dict[key])
    #
    # print(color_to_html)

    return render_template("showimage.html", image=f"uploads/{filename}", coloring=True, red=red_html, green=green_html, blue=blue_html, most=int_rgbcode[0])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 8930)), debug=True)

# if __name__=="__main__":
#     app.run(host='0.0.0.0', port=5000)



