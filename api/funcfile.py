import csv
import re
from database_driver import db, Users, Temperature
import logging
from datetime import datetime
from sqlalchemy import desc, asc

logging.basicConfig(filename='rfid_barcode.log', level=logging.DEBUG)

def db_list():
    user_list = []
    #db_list2 = Users.query.all()
    db_list2 = Users.query.order_by(asc(Users.name)).all()
    for user in db_list2:
        try:
            owner = user.id
            search = Temperature.query.filter_by(owner_id=owner).order_by(desc(Temperature.id)).first()
            last_temp = search.temp
            if last_temp >= 100.4:
                user_list.append({'id': user.id, 'Name': user.name, 'RFID': user.rfid, 'Barcode': user.barcode, 'HighTemp':True})
            else:
                user_list.append({'id': user.id, 'Name': user.name, 'RFID': user.rfid, 'Barcode': user.barcode, 'HighTemp':False})
        except:
            user_list.append({'id': user.id, 'Name': user.name, 'RFID': user.rfid, 'Barcode': user.barcode, 'HighTemp':False})
    return user_list

def delete_user_entry(id):
    try:
        search = Users.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
        return ({'Success': True, 'Deleted': search.name})
    except:
        return ({'Success': False})

def edit_user_entry(id, user_name, user_rfid, user_barcode):
    errors = []
    search = Users.query.filter_by(id=id).first()
    if search.name != user_name:
        if csv_checker_name(user_name) is False:
            search.name = user_name
        else:
            errors.append(f'Name Exists: {user_name}')
            logging.info(f'Error Code: 102 (Name Exists: {user_name}) (Datetime: {str(datetime.now())})')
    if search.rfid != user_rfid:
        if csv_checker_rfid(user_rfid) is False:
            search.rfid = user_rfid
        else:
            errors.append(f'RFID Exists: {user_rfid}')
            logging.info(f'Error Code: 101 (RFID Exists: {user_rfid}) (Datetime: {str(datetime.now())})')
    if search.barcode != user_barcode:
        if csv_checker_barcode(user_barcode) is False:
            search.barcode = user_barcode
        else:
            errors.append(f'Barcode Exists: {user_barcode}')
            logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')
    db.session.commit()
    if len(errors) == 0:
        return ({'Success': True, 'Errors': errors})
    else:
        return ({'Success': False, 'Errors': errors})

def edit_temp_entry(id, temp):
    search = Temperature.query.filter_by(id=id).first()
    try:
        temp = float(temp)
    except:
        return ({'Success':False, 'Error':'Temperature must be a number'})
    check_int = isinstance(temp, int)
    check_flt = isinstance(temp, float)
    if check_int or check_flt:
        if search.temp != temp:
            search.temp = temp
            db.session.commit()
        return ({'Success':True})
    else:
        return ({'Success':False, 'Error':'Temperature must be a number'})

def delete_temp_entry(id):
    try:
        search = Temperature.query.filter_by(id=id).first()
        db.session.delete(search)
        db.session.commit()
        return ({'Success': True, 'Date': search.date, 'Temperature': search.temp})
    except:
        return ({'Success': False})

def query_by_name(name):
    try:
        search = Users.query.filter_by(name=name).first()
        return ({'ID': search.id, 'Name':search.name,'RFID':search.rfid,'Barcode':search.barcode,'Success':True})
    except:
        return ({'Success':False})

def query_by_rfid(rfid):
    try:
        search = Users.query.filter_by(rfid=rfid).first()
        return ({'ID': search.id, 'Name':search.name,'RFID':search.rfid,'Barcode':search.barcode,'Success':True})
    except:
        return ({'Success':False})

def query_by_barcode(barcode):
    try:
        search = Users.query.filter_by(barcode=barcode).first()
        return ({'ID': search.id, 'Name':search.name,'RFID':search.rfid,'Barcode':search.barcode,'Success':True})
    except:
        return ({'Success':False})

def query_search(value):
    try:
        search = Users.query.filter_by(barcode=value).first()
        if value == search.barcode:
            return ({'ID': search.id, 'Name':search.name,'RFID':search.rfid,'Barcode':search.barcode, 'Temperatures':temp_14_days(search.id)})
    except:
        pass
    try:
        search = Users.query.filter_by(rfid=value).first()
        if value == search.rfid:
            return ({'ID': search.id, 'Name':search.name,'RFID':search.rfid,'Barcode':search.barcode, 'Temperatures':temp_14_days(search.id)})
    except:
        pass
    return ({'Success':False})


def view_profile(id):
    try:
        search = Users.query.filter_by(id=id).first()
        return ({'ID': search.id, 'Name':search.name,'RFID':search.rfid,'Barcode':search.barcode,'Highest_Temp':highest_temp(id),'Lowest_Temp':lowest_temp(id),'Average_Temp':avg_temp(id),'All_Temperatures':get_temps(id),'Chart_Temperatures':temp_14_days(id),'Success':True})
    except:
        return ({'Success':False})

def temp_14_days(owner):
    try:
        temp_list = []
        search = Temperature.query.filter_by(owner_id=owner).order_by(desc(Temperature.id)).all()
        if len(search) >= 14:
            search2 = search[0:14]
        elif len(search) < 14:
            search2 = search
        x = range(len(search2))
        for y in x:
            temp_list.append(search2[y].temp)
        if len(search2) < 14:
            x = range(14-len(search2))
            for y in x:
                temp_list.append(0)
        return temp_list
    except:
        temp_list = []
        return temp_list

def highest_temp(owner):
    try:
        search = Temperature.query.filter_by(owner_id=owner).order_by(desc(Temperature.temp)).first()
        return ({'Success':True, 'Date':search.date, 'Temperature':search.temp})
    except:
        return ({'Success':False})

def lowest_temp(owner):
    try:
        search = Temperature.query.filter_by(owner_id=owner).order_by(asc(Temperature.temp)).first()
        return ({'Success':True, 'Date':search.date, 'Temperature':search.temp})
    except:
        return ({'Success':False})

def avg_temp(owner):
    try:
        temp_list = []
        total = 0
        search = Temperature.query.filter_by(owner_id=owner).all()
        x = range(len(search))
        for y in x:
            temp_list.append(search[y].temp)
        for x in temp_list:
            total += x
        average = total / len(search)
        format_avg = "{:.1f}".format(average)
        return ({'Success':True, 'Average':format_avg})
    except:
        return ({'Success':False})


def csv_checker_name(user_name):
    try:
        search = Users.query.filter_by(name=user_name).first()
        results = search.name
        if str(results) == str(user_name):
            return True
        else:
            return False
    except:
        return False

def csv_checker_rfid(user_rfid):
    try:
        search = Users.query.filter_by(rfid=user_rfid).first()
        results = search.rfid
        if str(results) == str(user_rfid):
            return True
        else:
            return False
    except:
        return False

def csv_checker_barcode(user_barcode):
    try:
        search = Users.query.filter_by(barcode=user_barcode).first()
        results = search.barcode
        if str(results) == str(user_barcode):
            return True
        else:
            return False
    except:
        return False

def csv_db_write(user_name, user_rfid, user_barcode):
    new_user = Users(
            name=user_name,
            rfid=user_rfid,
            barcode=user_barcode
        )
    db.session.add(new_user)
    db.session.commit()

def temp_write(owner, tempdata):
    try:
        tempdata = float(tempdata)
    except:
        return ({'Success':False, 'Error':['Temperature must be a number']})
    check_int = isinstance(tempdata, int)
    check_flt = isinstance(tempdata, float)
    if check_int or check_flt:
        ownerid = Users.query.filter_by(id=owner).first()
        new_temp = Temperature(
                temp=tempdata,
                owner=ownerid
            )
        db.session.add(new_temp)
        db.session.commit()
        return ({'Success':True})
    else:
        return ({'Success':False, 'Error':['Temperature must be a number']})

def get_temps(owner):
    results = []
    search = Users.query.filter_by(id=owner).first()
    temp_list = search.temperatures
    x = range(len(temp_list))
    for y in x:
        if temp_list[y].temp >= 100.4:
            hightemp=True
        else:
            hightemp=False
        results.append({'id':temp_list[y].id, 'DateTime':temp_list[y].date, 'Temperature':temp_list[y].temp, 'HighTemp':hightemp})
    return results

def add_new_user(user_name, user_rfid, user_barcode):
    errors = []
    if csv_checker_name(user_name) is False:
        if csv_checker_rfid(user_rfid) is False:
            if csv_checker_barcode(user_barcode) is False:
                csv_db_write(user_name, user_rfid, user_barcode)
                return ({'Success': True, 'Errors': errors})
            else:
                errors.append(f'Barcode Exists: {user_barcode}')
                logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')
        else:
            errors.append(f'RFID Exists: {user_rfid}')
            logging.info(f'Error Code: 101 (RFID Exists: {user_rfid}) (Datetime: {str(datetime.now())})')
            if csv_checker_barcode(user_barcode) is True:
                errors.append(f'Barcode Exists: {user_barcode}')
                logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')
    else:
        errors.append(f'Name Exists: {user_name}')
        logging.info(f'Error Code: 102 (Name Exists: {user_name}) (Datetime: {str(datetime.now())})')
        if csv_checker_rfid(user_rfid) is True:
            errors.append(f'RFID Exists: {user_rfid}')
            logging.info(f'Error Code: 101 (RFID Exists: {user_rfid}) (Datetime: {str(datetime.now())})')
        if csv_checker_barcode(user_barcode) is True:
            errors.append(f'Barcode Exists: {user_barcode}')
            logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')
    return ({'Success': False, 'Errors': errors})
                        

def csv_analyze(file):
    errors = []
    with open(file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        
        for row in csv_reader:
            user_name = row[0]
            user_rfid = row[1]
            user_barcode = row[2]
            if csv_checker_name(user_name) is False:
                if csv_checker_rfid(user_rfid) is False:
                    if csv_checker_barcode(user_barcode) is False:
                        csv_db_write(user_name, user_rfid, user_barcode)
                    else:
                        errors.append(f'Barcode Exists: {user_barcode}')
                        logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')
                else:
                    errors.append(f'RFID Exists: {user_rfid}')
                    logging.info(f'Error Code: 101 (RFID Exists: {user_rfid}) (Datetime: {str(datetime.now())})')
                    if csv_checker_barcode(user_barcode) is True:
                        errors.append(f'Barcode Exists: {user_barcode}')
                        logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')
            else:
                errors.append(f'Name Exists: {user_name}')
                logging.info(f'Error Code: 102 (Name Exists: {user_name}) (Datetime: {str(datetime.now())})')
                if csv_checker_rfid(user_rfid) is True:
                    errors.append(f'RFID Exists: {user_rfid}')
                    logging.info(f'Error Code: 101 (RFID Exists: {user_rfid}) (Datetime: {str(datetime.now())})')
                if csv_checker_barcode(user_barcode) is True:
                    errors.append(f'Barcode Exists: {user_barcode}')
                    logging.info(f'Error Code: 100 (Barcode Exists: {user_barcode}) (Datetime: {str(datetime.now())})')

    return ({'Success': True, 'Errors': errors})