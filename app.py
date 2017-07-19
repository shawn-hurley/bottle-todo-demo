"""The TODO application for demoing the bind and unbind of a apb."""
from bottle import request, redirect, route, run, template, view
from seed_database import load_database
import psycopg2
import os
__author__ = 'shawn-hurley'


@route('/todo')
def todo_list():
    """List the all the pending task."""
    try:
        conn = __get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, task FROM todo where status=1")
        result = c.fetchall()
        output = template('make_table', rows=result)
        return output
    except (TypeError, psycopg2.Error) as e:
        print e
        output = template('no_database')
        # attempt to create database
        try:
            load_database(__get_db_connection())
            return redirect('/todo')
        except Exception, e:
            # if you cant create, no worries, just means DB is not bound.
            print e
            pass
        return output
    finally:
        c.close()


@route('/new', method='GET')
@view('new_task')
def new_item():
    """Show the task creation screen."""
    return


@route('/new', method='POST')
def save_new_item():
    """Save the new task and redirect to list."""
    if request.POST.save:
        new = request.POST.task.strip()
        conn = __get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO todo(task,status) VALUES(%s,%s)", (new, 1))
        conn.commit()
        c.close()
        return redirect('/todo')
    else:
        return redirect('/new')


@route('/edit/<no:int>', method='GET')
def edit_task(no):
    """Edit a task."""
    conn = __get_db_connection()
    c = conn.cursor()
    c.execute("SELECT task from todo WHERE id=%s", str(no))
    cur_data = c.fetchone()
    return template('edit_task', old=cur_data, no=no)


@route('/edit/<no:int>', method='POST')
def save_edit_task(no):
    """Save the edit on a task."""
    if request.POST.save:
        edit = request.POST.task.strip()
        status = request.POST.status.strip()
        if status == 'open':
            status = 1
        else:
            status = 0
        conn = __get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE todo SET task = %s, status = %s WHERE id = %s ",
                  (edit, status, str(no)))
        conn.commit()
        return redirect('/todo')
    else:
        return redirect('/edit/'+str(no))


def __get_db_connection():
    """Will return the database connection."""
    return psycopg2.connect(user=os.environ.get('POSTGRES_USER'),
                            host=os.environ.get('POSTGRES_HOST'),
                            password=os.environ.get('POSTGRES_PASSWORD'),
                            database=os.environ.get('POSTGRES_DB'))


run()
