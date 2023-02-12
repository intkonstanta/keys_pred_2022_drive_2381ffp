import sqlite3
from sqlite3 import Error
import re
import pick
from pick import pick
import os
import sys


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_competition_id(conn):
    counter = -1
    id = conn.cursor().execute("SELECT id FROM competitions").fetchall()

    result = []
    for i in id:
        result.append(list(map(int, filter(str.isdigit, (str(id[counter])).split()))))
        counter += 1
    #print(int(re.findall(r'\d+', (str(id[counter])))[0]))
    return ((int(re.findall(r'\d+', (str(id[counter])))[0])))
    #list(str(id[0]))[1]


def start_a_competition(conn, name=None, date=None, organizer=None, location=None):
    sql_create_compt = ' INSERT INTO competitions (name, begin_date, organizer, location) VALUES ("{}", "{}", "{}",' \
                       ' "{}")'.format(name, date, organizer, location)
    c = conn.cursor()
    c.execute(sql_create_compt)
    sql = "CREATE TABLE IF NOT EXISTS competition_{} (id INTEGER PRIMARY KEY AUTOINCREMENT, ride_type text," \
          " pilots_involved text, begin_time text, end_time text, name text);".format(get_competition_id(conn))
    print(sql)
    c.execute(sql)
    conn.commit()


def get_ride_id(conn, competition_id):
    counter = -1
    id = conn.cursor().execute("SELECT id FROM competition_{}".format(competition_id)).fetchall()
    if id:
        result = []
        for i in id:
            result.append(list(map(int, filter(str.isdigit, (str(id[counter])).split()))))
            counter += 1
        #print(int(re.findall(r'\d+', (str(id[counter])))[0]))
        return ((int(re.findall(r'\d+', (str(id[counter])))[0])))
    else:
        return '0'


def add_telemetric_data(conn, ride_id='1.1', pilot='None', angle='0', velocity='0', trajectory='0'):
    sql_create_ride = ' INSERT INTO "{}" (pilot, angle, velocity, trajectory) VALUES ("{}", "{}", "{}", "{}")'.format\
        (ride_id, pilot, angle, velocity, trajectory)

    c = conn.cursor()
    c.execute(sql_create_ride)
    conn.commit()


def start_a_ride(conn, competition_index='1', ride_type='64', pilots=[], begin_time='00:00', end_time='00:30'):
    types = {'64':'qualifying', '32':'top 32', '16':'top 16', '8':'top 8', '4':'semifinal', '2':'final'}
    sql_create_ride = ' INSERT INTO competition_{} (ride_type, pilots_involved, begin_time, end_time, name) ' \
                      'VALUES ("{}", "{}", "{}", "{}", "{}")'.format(competition_index, types[ride_type], pilots,
                                                                     begin_time, end_time, (str(competition_index)+'.'+
                                                                                            str(get_ride_id(conn, competition_index))))

    c = conn.cursor()
    c.execute(sql_create_ride)
    sqlt = 'CREATE TABLE IF NOT EXISTS "{}.{}" (id INTEGER PRIMARY KEY AUTOINCREMENT, pilot text, angle text,' \
           ' velocity text, trajectory text);'.format(competition_index, get_ride_id(conn, competition_index))
    print(sqlt)
    c.execute(sqlt)
    conn.commit()


def get_competitions(conn):
    sqll = "SELECT * FROM competitions"
    table = conn.cursor().execute(sqll).fetchall()
    return table


def get_rides(conn, competition_index):
    sqll = "SELECT * FROM competition_{}".format(competition_index)
    table = conn.cursor().execute(sqll).fetchall()
    print(table)
    return table


def get_ride(conn, ride_index):
    sqll = "SELECT * FROM '{}'".format(ride_index)
    table = conn.cursor().execute(sqll).fetchall()
    print(table)
    return table


def interface(conn):
    def create_menu(title, options):
        choice = option, index = pick(options, title, indicator='=>', default_index=0)
        os.system('cls')
        return choice
    def competition_creation_interface():
        name_c = input("Enter the name of competition: ")
        date_c = input("Enter the date: ")
        organizer_c = input("Enter the name of organizer: ")
        location_c = input("Enter the location: ")
        start_a_competition(conn, name_c, date_c, organizer_c, location_c)
    def ride_creation_interface(competition_index):
        type = input("Enter the number of players (64 - qualifying, 32 - top 32 etc.): ")
        pilots = input("Enter the numbers of involved pilots: ")
        begin_t = input("Enter the time of start: ")
        end_t = input("Enter the time of end: ")
        start_a_ride(conn, competition_index, type, pilots, begin_t, end_t)
    def telemetric_data_creation_interface(ride_id):
        pilot = input("Enter the number/name of pilot: ")
        angle = input("Enter the angle: ")
        velocity = input("Enter the velocity: ")
        trajectory = input("Enter the trajectory: ")
        add_telemetric_data(conn, ride_id, pilot, angle, velocity, trajectory)
    def show_competitions():
        compts = get_competitions(conn)
        arr = ['Back\n']
        for i in compts:
            arr.append(''.join(str(i)))
        return create_menu('Table of competitions', arr)
    def show_rides(competition_index):
        rides = get_rides(conn, competition_index)
        arr = ['Back\n', 'Add\n']
        for i in rides:
            arr.append(''.join(str(i)))
        return create_menu('Table of rides', arr)
    def show_the_ride(ride_id):
        rides = get_ride(conn, ride_id)
        arr = ['Back\n', 'Add\n']
        for i in rides:
            arr.append(''.join(str(i)))
        return create_menu('Table of telemetric data', arr)

    choice = create_menu('Welcome to my ugly console-interface! ', ['Select a competition', 'Create a competition'])
    if choice[1] == 1:
        competition_creation_interface()
    elif choice[1] == 0:
        local_choice = show_competitions()
        if local_choice[1] != 0:
            local_local_choice = show_rides(local_choice[1])
            if local_local_choice[1] == 1:
                ride_creation_interface(local_choice[1])
            elif local_local_choice[1] != 0:
                local_ride_index = str(local_choice[1])+'.'+str(local_local_choice[1]-1)
                local_local_local_choice = show_the_ride(local_ride_index)
                if local_local_local_choice[1] == 1:
                    telemetric_data_creation_interface(local_ride_index)


def main():
    database = "pythonsqlite.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS competitions (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name text,
                                        begin_date text,
                                        organizer text,
                                        location text,
                                        id_key TEXT AS (substr(('competition' || '_' || id), 0, 40)) STORED
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:

        create_table(conn, sql_create_projects_table)
        #start_a_competition(conn, "Grand_Championship", "08.02.06", "Me.", "Moscow")
        #start_a_competition(conn, "Grand_Championship", "08.02.06", "Me.", "Moscow")
        #start_a_competition(conn, "Grand_Championship", "08.02.06", "Me.", "Moscow")
        interface(conn)
        #start_a_ride(conn, pilots = ['34', '56', '34'])
        # create tasks table
        #create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()