import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def preprocess_answer(answer):
    convert_table = [
        {'ไปก่อนเริ่มคาบ': 1,
         'ถึงห้องตอน 8 โมงพอดีเป๊ะ': 2,
         'เข้าห้องสาย... แต่ก็ยังเข้านะ': 3,
         'มีคาบเช้าด้วยหรอ': 4,
        }, # ^ quiz 1
        {'เลิกคลาสปุ๊ปนั่งทำโปรเจคเลย งานจะได้เสร็จไว ๆ': 1,
         'วางแผนทำโปรเจคอย่างดี รับรองเสร็จทันเวลา': 2,
         'เอาไว้ค่อยทำวันท้าย ๆ ก็ได้ งานนี้ชิล ๆ': 3,
         'คุณเชื่อใน one night miracle หรือไม่?': 4,
        }, # ^ quiz 2
        {'ไปหาไรกินกับเพื่อนดีกว่า หิวแล้ว~': 1,
         'กลับหอไปนอนแล้ว เหน่ย': 2,
         'ไปทบทวนที่ห้องสมุดต่อคับ ตึง ๆ': 3,
         'ไปดูหนังที่ฟิวเจอร์ต่อดีกว่า': 4,
        }, # ^ quiz 3
        {'ร้านไหนไปได้ ไปหมดคับ': 1,
         'ถ้าเพื่อนไปด้วย เราก็ไปด้วย': 2,
         'ไปพอเป็นพิธี รีบกินรีบกลับ': 3,
         'ปฏิเสธรุ่นพี่ไป พอดีไม่ค่อยถนัด': 4,
        }, # ^ quiz 4
        {'เข้าหาทุกคน เฟรนลี่ที่หนึ่ง': 1,
         'ส่องดูรอบ ๆ ว่ามีใครพอจะดูเป็นแฟนในอนาคตเราได้บ้าง': 2,
         'มองหาคนที่ดูเข้ากับเรา แล้วไปทำความรู้จักแบบเนียน ๆ': 3,
         'เงียบ ๆ ไม่ค่อยเข้าหาใครก่อน': 4,
        }, # ^ quiz 5
        {'ของขวัญทำมือที่ให้จากใจ': 1,
         'ซื้อของที่คิดว่าเพื่อนจะได้ใช้ในอนาคต': 2,
         'เลี้ยงเหล้าเพื่อนพอ จบ': 3,
         'ไม่มีเพื่อนคับ': 4,
        }, # ^ quiz 6
        {'รอคิวไปนะ เพราะเราฮ็อตมาก': 1,
         'มีแฟนแล้วคับ อดไปนะ': 2,
         'ถ้านิสัยเข้ากันได้ ลองดูก็ไม่เสียหายนะ': 3,
         'อย่ามายุ่งกับเรา อยากอยู่คนเดียว แหะ ๆ': 4,
        }, # ^ quiz 7
        {'Python': 1,
         'HTML': 4,
        }, # ^ quiz 8
        {'Physics': 1,
         'English': 4,
        }, # ^ quiz 9
        {'Non-Alcoholic': 1,
         'Alcoholic': 4,
        }, # ^ quiz 10
        {'Introvert': 1,
         'Extrovert': 4,
        }, # ^ quiz 11
        {'Morning Bird': 1,
         'Night Owl': 4,
        }, # ^ quiz 12
        {'K-POP / J-POP': 1,
         'T-POP / Inter': 4,
        }, # ^ quiz 13
        {'Skincare ~': 1,
         'Skingame ~': 4,
        }, # ^ quiz 14
    ]

    preprocessed_answer = []
    n = len(answer)
    for i in range(n):
        if answer[i] in convert_table[i]:
            preprocessed_answer.append(convert_table[i][answer[i]])
        else:
            return []

    return preprocessed_answer

def main():
    students = {}

    with open('result_20230810_0003.csv', 'r') as f:
        records = [row for row in csv.reader(f, delimiter=',')]
        body = records[1:]

        for each in body:
            timestamp, nickname, id, join_day1, join_day2, join_matching = each[:6]
            answer = each[6:-4]
            prefered_type = each[-4]
            social_media = each[-3]

            students[id] = {
                'id': id,
                'timestamp': timestamp,
                'nickname': nickname,
                'join_day1': join_day1,
                'join_day2': join_day2,
                'join_matching': join_matching=='เล่น',
                'ans': preprocess_answer(answer),
                'prefered_type': 'similar' if prefered_type=='คล้าย ๆ กับเรา' else 'different',
                'social_media': social_media,
            }


    print(f'จำนวนคนตอบแบบฟอร์ม: {len(students)}')

    day1 = [v for v in students.values() if v['join_day1']=='เข้าร่วม']
    n_all = len(day1)
    n_senior = sum(1 for e in day1 if e['id'].startswith('65'))
    print(f'กิจกรรม day 1: {n_all} คน (พี่ {n_senior} น้อง {n_all-n_senior})')

    day2 = [v for v in students.values() if v['join_day2']=='เข้าร่วม']
    n_all = len(day2)
    n_senior = sum(1 for e in day2 if e['id'].startswith('65'))
    print(f'กิจกรรม day 2: {n_all} คน (พี่ {n_senior} น้อง {n_all-n_senior})')

    matching = [v for v in students.values() if v['join_matching']]
    n_all = len(matching)
    n_senior = sum(1 for e in matching if e['id'].startswith('65'))
    print(f'เล่นสายรหัส: {n_all} คน (พี่ {n_senior} น้อง {n_all-n_senior})')
        
    students = {k:v for k, v in students.items() if v['join_matching']}
    senior = [v for v in students.values() if v['id'].startswith('65')]
    junior = [v for v in students.values() if v['id'].startswith('66')]

    # plotting
    data = [v['ans'] for v in senior+junior]
    pca = PCA(3)
    df = pca.fit_transform(np.array(data))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    cnames = ['tab:brown', 'tab:orange', 'tab:olive', 'tab:green', 'tab:cyan', 'tab:blue', 'tab:purple', 'tab:pink', 'tab:red']
    n_cnames = len(cnames)

    n_senior = len(senior)
    for i in range(n_senior):
        c = cnames[i%n_cnames]
        ax.scatter(df[i , 0] , df[i , 1], df[i , 2], color=c, marker='X')

    n_junior = len(junior)
    for i in range(n_senior, n_senior+n_junior):
        c = cnames[i%n_cnames]
        ax.scatter(df[i , 0] , df[i , 1], df[i , 2], color=c, marker='*')

    plt.show()

main()
