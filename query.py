import pymysql.cursors
from flask import flash


def connect_to_db():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='Lch561101',
                                 database='platform',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_all_img_ids():
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM images')
            res = cursor.fetchall()
    return res


def get_all_unconfirmed_img_ids():
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM images WHERE is_confirmed IS FALSE AND is_vehicle IS NOT NULL")
            res = cursor.fetchall()
    return res


def get_info_by_id(image_id):
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM images WHERE id=%s', image_id)
            res = cursor.fetchall()
    return res


def get_name_by_id(image_id):
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT name FROM images WHERE id=%s', image_id)
            res = cursor.fetchall()
    return res[0]['name']


def get_name_by_id(image_id):
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT name FROM images WHERE id=%s', image_id)
            res = cursor.fetchall()
    return res[0]['name']


def save_img(name, path, is_vehicle=None, is_confirmed=False, correct=None):
    connection = connect_to_db()
    error = False
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO images (name, path, is_vehicle, is_confirmed, correct)'
                               'VALUES (%s, %s, %s, %s, %s)', (name, path, is_vehicle, is_confirmed, correct))
                connection.commit()
    except:
        connection.rollback()
        error = True
    finally:
        pass


def get_image_by_name(name):
    connection = connect_to_db()
    res = None
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM images WHERE name = %s', name)
            res = cursor.fetchall()
    return res


def update_image_by_name(name, path=None, is_vehicle=None, is_confirmed=None, correct=None):
    connection = connect_to_db()
    error = False
    query = "UPDATE images SET "
    params = []

    try:
        with connection:
            with connection.cursor() as cursor:
                if path:
                    query += 'path=%s '
                    params.append(path)
                if is_vehicle:
                    if len(params) != 0:
                        query += ","
                    query += " is_vehicle=%s "
                    params.append(is_vehicle)
                if is_confirmed:
                    if len(params) != 0:
                        query += ","
                    query += " is_confirmed=%s "
                    params.append(is_confirmed)
                if correct:
                    if len(params) != 0:
                        query += ","
                    query += " correct=%s "
                    params.append(correct)
                query += 'WHERE name=%s'
                params.append(name)
                cursor.execute(query, tuple(params))
                connection.commit()
    except:
        connection.rollback()
        error = True
    finally:
        pass


def check_predicted(image_name):
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT is_vehicle FROM images WHERE name=%s', image_name)
            result = cursor.fetchone()
    return result['is_vehicle']


def get_table_data():
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, path, is_vehicle, is_confirmed, correct FROM images')
            result = cursor.fetchall()
    table = []
    for image in result:
        ret = [image['id'], image['path']]
        if image['is_vehicle'] == 1:
            ret.append('Yes')
        elif image['is_vehicle'] == 0:
            ret.append('No')
        else:
            ret.append('')

        if image['is_confirmed'] == 1:
            ret.append('Yes')
        elif image['is_confirmed'] == 0:
            ret.append('No')
        else:
            ret.append('')

        if image['correct'] == 1:
            ret.append('Yes')
        elif image['correct'] == 0:
            ret.append('No')
        else:
            ret.append('')
        table.append(ret)
    return table


def get_accuracy():
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT correct FROM images WHERE correct IS NOT NULL')
            results = cursor.fetchall()
    if not len(results):
        return '0/0, accuracy: N/A'
    else:
        count = {1: 0, 0: 0}
        for item in results:
            count[item['correct']] += 1
        accuracy = '{:.2f}'.format(count[1] / len(results) * 100)
        return f"{count[1]}/{len(results)}, accuracy: {accuracy}%"


def get_training_status():
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT is_training FROM training_status')
            result = cursor.fetchone()
    return result['is_training']


def set_training_status(training):
    connection = connect_to_db()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE training_status SET is_training=%s WHERE id=%s', (training, 1))
            connection.commit()
