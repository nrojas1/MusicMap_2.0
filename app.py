import os
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory, flash
import psycopg2 as psql
from datetime import date

app = Flask(__name__)
db = psql.connect("dbname=geovis2 user=postgres password=uuuu")

def strCleanUp(d):
    d = d.replace('[','')
    d = d.replace(']','')
    d = d.replace('"','')
    d = d.replace("'",'')
    d = d.split(',')
    return d

@app.route('/')
def index():
    return render_template('start.html')

# @app.route('/srch')
# def dashboard():
#     return render_template('child.html')

# ---- form blocks ---- OK
@app.route('/concert')
def concert():
    return render_template('frm_concert.html')

@app.route('/rec')
def rec():
    return render_template('frm_rec.html')

@app.route('/event')
def event():
    return render_template('frm_event.html')

@app.route('/project')
def project():
    return render_template('frm_project.html')

# ---- form to db ---- OK
@app.route('/concert-db', methods = ['POST', 'GET'])
def db_concert():
    r = request.form.to_dict(flat=False)
    point = r['latitude'], r['longitude']
    pt = 'SRID=3857;POINT'+str(point)
    pt = pt.replace(',','')

    if len(r)!=11 :
        d = '%s,%s,%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['name'], r['date'], pt, r['t_0'], r['t_1'], r['pay_opt'], r['description'], r['email'])
        d = strCleanUp(d)
        c = db.cursor()
        c.execute("""
            INSERT INTO posts
            (type, talent_type, child_type, name, date, pt, t_0, t_1, pay_opt, description, email)
            VALUES
            ('concert',%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (d[0] ,d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8]))

        c.close()
        db.commit()
    else:
        d = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['child_type'], r['name'], r['date'], pt, r['t_0'], r['t_1'], r['pay_opt'], r['description'], r['email'])
        d = strCleanUp(d)
        c = db.cursor()
        c.execute("""
            INSERT INTO posts
            (type, talent_type, child_type, name, date, pt, t_0, t_1, pay_opt, description, email)
            VALUES
            ('concert',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9]))
        c.close()
        db.commit()
    #return render_template('form.html', results = r, d=d)
    return redirect('/listposts')

@app.route('/rec-db', methods = ['POST', 'GET'])
def db_rec():
    r = request.form.to_dict(flat=False)
    point = r['latitude'], r['longitude']
    pt = 'SRID=3857;POINT'+str(point)
    pt = pt.replace(',','')
    if len(r)!=9:
        d = '%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['date'], pt, r['t_0'], r['pay_opt'], r['description'], r['email'])
        d = strCleanUp(d)
        c = db.cursor()
        c.execute("""
            INSERT INTO posts
            (type, talent_type, child_type, name, date, pt, t_0, t_1, pay_opt, description, email)
            VALUES
            ('recording',%s,NULL,NULL,%s,%s,%s,NULL,%s,%s,%s);
        """, (d[0] ,d[1], d[2], d[3], d[4], d[5], d[6]))

        c.close()
        db.commit()
    else:
        d = '%s,%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['child_type'], r['date'], pt, r['t_0'], r['pay_opt'], r['description'], r['email'])
        d = strCleanUp(d)
        c = db.cursor()
        c.execute("""
            INSERT INTO posts
            (type, talent_type, child_type, name, date, pt, t_0, t_1, pay_opt, description, email)
            VALUES
            ('recording',%s,%s,NULL,%s,%s,%s,NULL,%s,%s,%s);
        """, (d[0] ,d[1], d[2], d[3], d[4], d[5], d[6], d[7]))

        c.close()
        db.commit()
    #return render_template('form.html', results = r)
    #return render_template('post_list.html')
    return redirect('/listposts')

@app.route('/event-db', methods = ['POST', 'GET'])
def db_event():
    r = request.form.to_dict(flat=False)
    point = r["latitude"], r["longitude"]
    pt = 'SRID=3857;POINT'+str(point)
    pt = pt.replace(',','')
    if len(r)!=11:
        d = '%s,%s,%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['name'], r['date'], pt, r['t_0'], r['t_1'], r['pay_opt'], r['description'], r['email'])
        d = strCleanUp(d)
        c = db.cursor()
        c.execute("""
            INSERT INTO posts
            (type, talent_type, child_type, name, date, pt, t_0, t_1, pay_opt, description, email)
            VALUES
            ('event',%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8]))
        c.close()
        db.commit()
    else:
        d = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['child_type'], r['name'], r['date'], pt, r['t_0'], r['t_1'], r['pay_opt'], r['description'], r['email'])
        d = strCleanUp(d)
        c = db.cursor()
        c.execute("""
            INSERT INTO posts
            (type, talent_type, child_type, name, date, pt, t_0, t_1, pay_opt, description, email)
            VALUES
            ('event',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9]))
        c.close()
        db.commit()
    #return render_template('form.html', results = r)
    #return render_template('list_posts.html')
    return redirect('/listposts')

@app.route('/project-db', methods = ['POST', 'GET']) # TO DO WITH POLYGONS -> geom table in db -> foreighn key to main table
def db_project():
    r = request.form.to_dict(flat=False)
    reg = r['region']
    c = db.cursor()

    # d = '%s,%s,%s,%s,%s,%s,%s,%s'%(r['talent_type'], r['child_type'], r['name'], r['date'], pt, r['t_0'], r['t_1'], r['description'])
    # d = strCleanUp(d)
    return render_template('form.html', results = r)

# @app.route('/form', methods = ['POST', 'GET'])
# def db_update():
#     results = request.form.to_dict(flat=False)
#     point = results['latitude'], results['longitude']
#     pt = 'SRID=3857;POINT'+str(point)
#     pt = pt.replace(',','')
#     d = '%s,%s,%s'%(results['name'] , results['date'], pt)
#     d = strCleanUp(d)
#     c = db.cursor()
#
#     c.execute("""
#         INSERT INTO evenements
#         (nom, date, pt)
#         VALUES
#         (%s, %s, %s);
#     """, (d[0], d[1], d[2],))
#
#     c.close()
#     db.commit()
#     #return render_template('form.html', results = results, d=d)
#     return render_template('child_list.html')

# ---- display posts in dashboard ----
@app.route('/listposts')
def posts():
    c = db.cursor()
    c.execute("""
        SELECT
         id, type, talent_type, child_type, name, ST_X(pt), ST_Y(pt), date, t_0::varchar,
         t_1::varchar, pay_opt, description, email, geom_id, __date
        FROM posts;
    """)
    rows = [{
    'id': l[0], 'type': l[1], 'talent_type': l[2], 'child_type': l[3],
    'name': l[4], 'x': l[5], 'y': l[6], 'date': l[7], 't_0': l[8], 't_1': l[9],
    'pay_opt': l[10], 'description': l[11], 'email': l[12], 'geom_id': l[13], 'DATESTAMP': l[14]
    } for l in c]
    c.close()
    return render_template('list_posts.html',
        posts=rows)

# @app.route('/liste')
# def evenements():
#     c = db.cursor()
#     c.execute("""
#         SELECT *
#         FROM evenements;
#     """)
#     rows = [{
#         'nom': l[0], 'x': l[1], 'y': l[2], 'pt':l[3]
#     } for l in c]
#     c.close()
#     return render_template('child_list.html',
#         evenements=rows)

# @app.route('/cabanes.json')
# def cabanes_json():
#     c = db.cursor()
#     c.execute("""
#         SELECT
#          nom,
#          ST_X(ST_Transform(pt,4326))::integer,
#          ST_Y(ST_Transform(pt,4326))::integer
#         FROM cabanes
#     """)
#     rows = [{
#         'nom': l[0], 'x': l[1], 'y': l[2]
#     } for l in c]
#     c.close()
#     return jsonify(rows)

# @app.route('/evenements.json')
# def evenements_json():
#     c = db.cursor()
#     c.execute("""
#         SELECT
#          id,
#          nom,
#          date,
#          ST_X(st_pointfromtext(pt, 3857)),
#          ST_Y(st_pointfromtext(pt, 3857))
#         FROM evenements
#         ORDER BY id DESC;
#
#     """)
#     rows = [{
#         'id': l[0], 'nom': l[1], 'date': l[2], 'x': l[4], 'y': l[3]
#     } for l in c]
#     c.close()
#     return jsonify(rows)

# ---- json ----
@app.route('/posts.json')
def posts_json():
    c = db.cursor()
    c.execute("""
        SELECT
         id, type, talent_type, child_type, name, ST_X(pt), ST_Y(pt), date, t_0::varchar,
         t_1::varchar, pay_opt, description, email, geom_id, __date
        FROM posts
        ORDER BY id DESC;
    """)
    rows = [{
    'id': l[0], 'type': l[1], 'talent_type': l[2], 'child_type': l[3],
    'name': l[4], 'x': l[5], 'y': l[6], 'date': l[7], 't_0': l[8], 't_1': l[9],
    'pay_opt': l[10], 'description': l[11], 'email': l[12], 'geom_id': l[13], 'DATESTAMP': l[14]
    } for l in c]
    c.close()
    return jsonify(rows)

# @app.route('/regions.json')
# def regions_json():
#     c = db.cursor()
#     c.execute("""
#         SELECT jsonb_build_object(
#             'type',     'FeatureCollection',
#             'features', jsonb_agg(features.feature)
#         )
#         FROM (
#           SELECT jsonb_build_object(
#             'type',       'Feature',
#             'id',         id,
#             'geometry',   ST_AsGeoJSON(geom)::jsonb,
#             'properties', to_jsonb(inputs) - 'id' - 'geom'
#           ) AS feature
#           FROM (SELECT * FROM regions) inputs) features;
#     """)
#     rows = c.fetchall()
#     c.close()
#     return jsonify(rows)

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True)
