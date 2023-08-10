import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

N = 0

def stable_matching(senior, junior):

    students = {}

    for i in range(N):
        students[senior[i]['id']] = {
            'ans': senior[i]['ans'],
            'prefered_type': senior[i]['prefered_type'],
            'pref': senior[i]['pref'],
            'partner': 'free',
        } 
        students[junior[i]['id']] = {
            'ans': junior[i]['ans'],
            'prefered_type': junior[i]['prefered_type'],
            'pref': junior[i]['pref'],
            'partner': 'free',
        }

    free_count = N
    while free_count > 0:
        for s in senior:
            s_id = s['id']
            if students[s_id]['partner'] == 'free':
                for j in students[s_id]['pref']:
                    j_id = j[1]
                    if students[j_id]['partner'] == 'free':
                        students[j_id]['partner'] = s_id
                        students[s_id]['partner'] = j_id
                        free_count -= 1
                        break
                    else:
                        that_senior_id = students[j_id]['partner']
                        if j_prefers_this_morethan_that(students[j_id]['pref'], s_id, that_senior_id):
                            students[j_id]['partner'] = s_id
                            students[s_id]['partner'] = j_id
                            students[that_senior_id]['partner'] = 'free'
                            break

    return students
                            
def j_prefers_this_morethan_that(junior_preference_list, this_senior_id, that_senior_id):
    this_senior_rank = that_senior_rank = 999999
    n = len(junior_preference_list)
    for i in range(n):
        id = junior_preference_list[i][1]
        if id == this_senior_id:
            this_senior_rank = i
        elif id == that_senior_id:
            that_senior_rank = i

    return this_senior_rank < that_senior_rank
    
def get_preference_list(senior, junior):
    for i in range(N):
        senior[i]['pref'] = sorted(
            [[euclidean_distance(senior[i]['ans'], j['ans']), j['id']] for j in junior],
            reverse=True if senior[i]['prefered_type']=='different' else False
            )
        junior[i]['pref'] = sorted(
            [[euclidean_distance(junior[i]['ans'], s['ans']), s['id']] for s in senior],
            reverse=True if junior[i]['prefered_type']=='different' else False
            )

def euclidean_distance(p1, p2):
    n = len(p1)
    return sum([(p1[i]-p2[i])**2 for i in range(n)]) ** 0.5

def plot(results):
    data = []
    for k in results.keys():
        if k.startswith('65'):
            data.append(results[k]['ans'])
            k_partner = results[k]['partner']
            data.append(results[k_partner]['ans'])

    pca = PCA(3)
    df = pca.fit_transform(np.array(data))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    cnames = ['tab:brown', 'tab:orange', 'tab:olive', 'tab:green', 'tab:cyan', 'tab:blue', 'tab:purple', 'tab:pink', 'tab:red']
    n_cnames = len(cnames)

    for i in range(0, N*2, 2):
        c = cnames[i//2%n_cnames]
        ax.scatter(df[i , 0] , df[i , 1], df[i , 2], color=c, marker='X')
        ax.scatter(df[i+1 , 0] , df[i+1 , 1], df[i+1 , 2], color=c, marker='*')
        ax.plot(df[i:i+2 , 0] , df[i:i+2 , 1], df[i:i+2 , 2], color='black')

    plt.show()

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

    with open('result_20230810_1230.csv', 'r') as f:
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

    students = {k:v for k, v in students.items() if v['join_matching']}
    senior = [v for v in students.values() if v['id'].startswith('65')]
    junior = [v for v in students.values() if v['id'].startswith('66')]
    
    n_senior = len(senior)
    n_junior = len(junior)

    print(f'จำนวนรุ่นพี่: {n_senior}')
    print(f'จำนวนรุ่นน้อง: {n_junior}')
    print(f'\nrandom รุ่นพี่ที่จะมีสายรหัส 2 คนทั้งหมด {n_junior-n_senior} คน ดังนี้')

    if input('\ntype y to continue: ') != 'y':
        print('force quit.')
        return
    print()

    # duplicate senior
    lucky_senior = random.sample(senior, n_junior-n_senior)
    print('\n'.join(f"{i+1}. {each['nickname']} ({each['id']})" for i, each in enumerate(lucky_senior)))
    duplicate_senior = []
    for each in lucky_senior:
        copy = each.copy()
        copy['id'] += '_dup'
        duplicate_senior.append(copy)
    senior += duplicate_senior

    global N
    N = n_junior

    if input('\ntype y to continue: ') != 'y':
        print('force quit.')
        return

    get_preference_list(senior, junior)
    results = stable_matching(senior, junior)

    hints = {} # key: senior_id, value: hint<str>
    with open('hint_20230810_1130.csv', 'r') as f:
        records = [row for row in csv.reader(f, delimiter=',')]
        body = records[1:]

        for each in body:
            id = each[2]
            hint1 = each[3]
            if id in hints:
                print('wow', id)
            else:
                hints[id] = hint1


    matching_results = []
    gen_hint_dict = []
    gen_point_dict_idlist = []
    gen_point_dict_pointlist = []

    for k, v in results.items():
        if k.startswith('65'):
            senior_id = k[:-4] if k.endswith('_dup') else k
            junior_id = v['partner']

            matching_results.append(f"{students[senior_id]['nickname']} ({senior_id}) <แมทช์กับ> น้อง{students[junior_id]['nickname']} ({junior_id})")
            
            gen_hint_dict.append(f"'{junior_id}': ['{hints[senior_id]}'],")
            
            gen_point_dict_idlist.append(junior_id)
            gen_point_dict_idlist.append(senior_id)
            gen_point_dict_pointlist.append(students[junior_id]['ans'])
            gen_point_dict_pointlist.append(students[senior_id]['ans'])



    print('\nผลการจับคู่ด้วย Gale-Shapley stable matching:')
    print('\n'.join(matching_results))

    print('\ngenerate hint_dict:')
    print('\n'.join(gen_hint_dict))

    pca = PCA(3)
    df = pca.fit_transform(np.array(gen_point_dict_pointlist))

    gen_point_dict = []
    for i in range(0, df.shape[0], 2):
        gen_point_dict.append(f"'{gen_point_dict_idlist[i]}': [[{df[i , 0]:.4f}, {df[i , 1]:.4f}, {df[i , 2]:.4f}], [{df[i+1 , 0]:.4f}, {df[i+1 , 1]:.4f}, {df[i+1 , 2]:.4f}]],")

    print('\ngenerate point_dict:')
    print('\n'.join(gen_point_dict))

    plot(results)

main()
