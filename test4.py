import random
import cv2
import numpy as np
import sqlite3 as sq
import pandas as pd

def find_image():
    conn = sq.connect('game.db')
    cc = conn.cursor()

    a=['pic1.jpeg','pic2.jpeg','pic3.jpg','pic4.jpg','pic5.jpg']
    b=['rabbit.png','mouse.jpg','star.JPG']
    x=random.randint(1,600)
    y=random.randint(1,830)
    filename = 'saveimage.jpg'

    img1 = cv2.imread(random.choice(a))
    overlay_img1 = np.ones(img1.shape,np.uint8)*255
    img2 = cv2.imread(random.choice(b))
    rows,cols,channels = img2.shape
    overlay_img1[x:rows+x, y:cols+y] = img2
    img2gray = cv2.cvtColor(overlay_img1,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray,100,10,cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    final1 = cv2.bitwise_and(img1,img1,mask = mask_inv)
    final2 = cv2.bitwise_and(overlay_img1,overlay_img1, mask = mask)
    result = cv2.add(final1,final2)
    cv2.imwrite(filename, result)

    blur = cv2.GaussianBlur(img2gray, (5, 5), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchies = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    blank = np.zeros(thresh.shape[:2], dtype='uint8')
    cv2.drawContours(blank, contours, -1,(255, 0, 0), 1)
    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
    print(cx,cy)
    centroid_coordinate = [cx,cy]
    #Create for the first time the SQL table :
    #cc.execute("CREATE TABLE IF NOT EXISTS centroid (cx int, cy int)")
    #conn.commit()
    cc.execute('INSERT OR REPLACE into centroid (cx,cy) VALUES (?,?)', centroid_coordinate)
    conn.commit()

    def click_event(event, c, d, flag, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates.
            print(c,d)
            mouse_coor=[c,d]
            cc.execute('INSERT OR REPLACE into mousecoordinate (mouse_c, mouse_d) VALUES (?,?)', mouse_coor)
            #cc.execute("CREATE TABLE IF NOT EXISTS mousecoordinate (mouse_c int, mouse_d int)")
            conn.commit()

    img = cv2.imread('saveimage.jpg', 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    query = '''SELECT * from centroid INNER JOIN mousecoordinate on centroid.rowid=mousecoordinate.rowid'''
    result1 =cc.fetchall()
    data = pd.read_sql(query,conn)
    df = pd.DataFrame(data)
    df.to_csv('export.csv', index=False)
    df2 = pd.read_csv('export.csv', index_col=False)
    conn = sq.connect('game.db')
    cc = conn.cursor()
    df2.to_sql('summarycoordinates', conn, if_exists='replace', index = False)
    conn.commit()

    query2 = '''SELECT cx, cy  from  summarycoordinates WHERE rowid = (select max(rowid) from summarycoordinates)'''
    query3 = '''SELECT mouse_c, mouse_d  from  summarycoordinates WHERE rowid = (select max(rowid) from summarycoordinates)'''
    result2 = cc.execute(query2)
    conn.commit()
    result2 = cc.fetchone()
    result3 = cc.execute(query3)
    conn.commit()
    result3 = cc.fetchone()
    #print(result2)
    #print(result3)

    diff_x = abs(result2[0]-result3[0])
    diff_y = abs(result2[1]-result3[1])
    print(diff_x)
    print(diff_y)

    if diff_x<=50 and diff_y<=50:
        print('You successfully detected the picture')
    else:
        print('You failed to detect the picture')

if __name__=='__main__':
    find_image()