from datetime import datetime

'''
This py file contains the General Functions that our project uses
Use this class for functions that do not need the variables of the Project class to run

These are separated from a parent class in order to increase testability
'''

def convert_to_datetime(date):
        """
        :param date: str
        :return: datatime type or str "NA"
        """
        try:
            res = datetime.strptime(date, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            res = "NA"
        return res

def combine_id_name(indi, name):
    return indi + " " + name

def dates_within(date1, date2, limit, unit):
    conversion = {'days': 1, 'months': 30.4, 'years': 365.25}
    """
    check the interval between two dates
    :param date1: first date in '%Y-%m-%d' format
    :param date2: second date in '%Y-%m-%d' format
    :param limit: int
    :param unit: str in ('days', 'months', 'years')
    :return: bool
    """
    dt1 = convert_to_datetime(date1)
    dt2 = convert_to_datetime(date2)
    if dt1 == "NA" or dt2 == "NA":
        return True
    if unit not in conversion:
        raise Exception("No such unit")
    return (abs((dt1 - dt2).days) / conversion[unit]) <= limit

def date_before(before, after):
    """
    before happens first
    after happens later
    :param before: the date should happen first
    :param after: the date should happen after
    :return: bool
    """
    dt1 = convert_to_datetime(before)
    dt2 = convert_to_datetime(after)
    if dt1 == "NA" or dt2 == "NA":
        return True
    return dt1 < dt2  # after should be greater than before

def before_today(date):
    dt = convert_to_datetime(date)
    if dt == "NA":
        return True
    return dt < datetime.today().date()