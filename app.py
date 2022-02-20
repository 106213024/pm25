from flask import Flask, request,send_file
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.support.ui import Select
from PIL import Image
import shutil
import io
app = Flask(__name__)
@app.route('/health', methods=['GET'])
def health():
    return 'ok'
# @app.route('/makeGif/<inputstart>/<inputend>/<inputzoom>/<inputlat>/<inputlon>/<inputspeed>', methods=['GET'])
@app.route('/makeGif', methods=['GET'])
def makeGif():
# def makeGif(inputstart,inputend,inputzoom,inputlat,inputlon,inputspeed):
    token = token
    chrome_options = Options() 
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(f"https://www.taichuangaiot.org/")
    elem = driver.find_element_by_id("id")
    elem.send_keys('penny2')
    elem = driver.find_element_by_id("pwd")
    elem.send_keys('-.048?LSZhij') #++048BKM[lrv')        
    time.sleep(1)
    button = driver.find_element_by_class_name('btn.btn-primary') # 登入
    button.click()  
    time.sleep(1)
    now = datetime.now()
    url = 'https://www.taichuangaiot.org/history?'
    endtime = ''
    starttime = ''
    empty= [" ","", "　","\n","None"," None "]
    needAnd = 0
    pathTest = r"./tmp/"
    # if os.path.isfile(pathTest):
    shutil.rmtree(pathTest)
    if needAnd == 0:
        inputstart = str(request.args.get('inputstart')) ##
        inputend = str(request.args.get('inputend'))
        inputzoom = str(request.args.get('inputzoom'))
        inputlat = str(request.args.get('inputlat'))
        inputlon = str(request.args.get('inputlon'))
        inputspeed = str(request.args.get('inputspeed'))
        print("111",inputstart,"222")
        if inputstart not in empty:
            url = url + "start='"+ inputstart + "'"
            starttime = inputstart.split(" ")[1]
            needAnd = 1
        if inputend not in empty:
            if needAnd == 1:
                url = url + "&"
            url = url + "end='"+ inputend + "'"
            endtime = inputend.split(" ")[1]
            needAnd = 1
        if inputzoom not in empty:
            if needAnd == 1:
                url = url + "&"
            url = url + "zoom='"+ inputzoom + "'"
            needAnd = 1
        if inputlat not in empty:
            if needAnd == 1:
                url = url + "&"
            url = url + "lat='"+ inputlat + "'"
            needAnd = 1
        if inputlon not in empty:
            if needAnd == 1:
                url = url + "&"
            url = url + "lon='"+ inputlon + "'"
            needAnd = 1
        if inputspeed not in empty:
            if needAnd == 1:
                url = url + "&"
            url = url + "speed='"+ inputspeed + "'"
        driver.get(url)
        time.sleep(2)
        button4 = driver.find_element_by_id("search")
        button4.click()
        button9 = driver.find_element_by_id("daterange")
        button9.click()
        button8 = driver.find_elements_by_class_name('calendar-time')
        s1 = Select(driver.find_elements_by_class_name('hourselect')[1])
        s2 = Select(driver.find_elements_by_class_name('minuteselect')[1])
        buttonLoop = driver.find_element_by_class_name('leaflet-control-timecontrol.timecontrol-loop.looped')
        h = 0
        print(s1.first_selected_option.text,"      111111")
        if endtime in empty: # == '' or endtime != '':
            print("9")
            if (int(s1.first_selected_option.text) >= 12):
                print("8")
                h = int(s1.first_selected_option.text) - 12
                print(h,s1.first_selected_option.text,"222222222")
            else: 
                if s1.first_selected_option.text =='0':
                    h = '12'
                else:
                    h = s1.first_selected_option.text
            endtime = str(h) + ":" +s2.first_selected_option.text+":00"
        if endtime[0] == '0' and endtime[1] != ":":
            endtime = endtime[1:]
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")  #下滾
        time.sleep(2)
        # action.click(chartsmap).drag_and_drop_by_offset(chartsmap,-500,-100).perform()      #  @@@@@@@@@@@@@@@@@@@@@
        bottonFull = driver.find_element_by_class_name('leaflet-control-fullscreen-button.leaflet-bar-part')#leaflet-control-zoom-in')
        bottonFull.click() 
        dt_string = now.strftime("%d%m%Y_%H.%M.%S")
        time.sleep(2)
        tlist = []
        os.mkdir('./tmp/')
        while True :
            t = driver.find_element_by_class_name('leaflet-control-timecontrol.timecontrol-date') 
            print(t.text,endtime)
            if t.text != '尚未載入數據':
                i = 1
                while True:
                    t = driver.find_element_by_class_name('leaflet-control-timecontrol.timecontrol-date') 
                    if endtime not in t.text :
                        tlist.append(t)
                        driver.get_screenshot_as_file(f"./tmp/%s.png" %i)
                        print(i,t.text)
                        i = i +1
                        if i == 2:
                            buttonLoop.click()
                    else:
                        if i > 1:
                            print('end',i,tlist,t.text)
                            break
                break
            else:
                print("loadong data")
        img_dir = './tmp'
        img_list = os.listdir(img_dir)  # 列出目錄所有圖片
        img_list.sort(key=lambda x: int(x[:-4]))  # 排序
        first_img = Image.open(os.path.join(img_dir, img_list[0]))  # 第一張圖片物件
        else_imgs = [Image.open(os.path.join(img_dir, img)) for img in img_list[1:]]  # 剩餘圖片物件
        first_img.save("./tmp.gif" , append_images=else_imgs,duration=300,  # 每張圖片的過過渡時間
        save_all=True) # 拼接儲存，如果想要迴圈播放可以加上loop=0
    driver.quit()
    # return send_file('tmp.gif', mimetype='image/gif')
    with open("tmp.gif", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/gif'
        )



# @app.route("/")
# def hello():
#     return "Hello, World!"
if __name__ == '__main__':
    app.run(debug=True)
    # 設定 token
