from flask import render_template, flash, redirect, url_for, request, jsonify
from app import db
from app.main.forms import EditProfileForm, UploadForm
from flask_login import current_user, login_required
from app.models import Users
from app.main import bp

from os.path import dirname, join
import geopandas as gpd
import pandas as pd
import json

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import GeoJSONDataSource, Label, Slider
from bokeh.models.glyphs import Patches
from bokeh.layouts import WidgetBox, row, column, layout, gridplot

resources = INLINE
js_resources = resources.render_js()
css_resources = resources.render_css()

import psycopg2
from flask import current_app
import base64

DATABASE_URL = 'crewasis'

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                            title='Home Page',
                            posts=posts,
                            js_resources=INLINE.render_js(),
                            css_resources=INLINE.render_css())

@bp.route('/data', methods=['GET', 'POST'])
@login_required
def data_post():
    data = request.get_json()
    state = data.get('id')
    year = data.get('year')
    if year is not None:
        year = int(float(year))
    else:
        year = 2019


    print(state)
    print(year)
    con = psycopg2.connect(database=DATABASE_URL)
    sql = "select * from geodata where code = '%s'"%state
    df = gpd.GeoDataFrame.from_postgis(sql, con, geom_col='geom')
    slider = Slider(title = 'Year',start = 2014, end = 2019, step = 1, value = year)
    adults = get_data("select percent from population where code = '%s'"%state)
    name = get_data("select state from population where code = '%s'"%state)
    total_med = get_data("select january + february + march + april + may + june + july + august + september + october + november + december from colorado where category = 'medical' and year = '%s' and code = '%s'"%(year, state))
    total_ret = get_data("select january + february + march + april + may + june + july + august + september + october + november + december from colorado where category = 'retail' and year = '%s' and code = '%s'"%(year, state))

    print(total_med)
    name = name[0][0]
    adults = adults[0][0]
    if len(total_med) > 0:
        total_med = total_med[0][0]
    else:
        total_med = 0
    if len(total_ret) > 0:
        total_ret = total_ret[0][0]
    else:
        total_ret = 0
    print(adults)
    adults = round(float(adults)*100,2)
    print(adults)
    df_json = json.loads(df.to_json())
    json_data = json.dumps(df_json)
    splot = figure(plot_width=320, plot_height=300, match_aspect=True, title=None, toolbar_location=None)
    tplot = figure(plot_width=320, plot_height=300, title=None, toolbar_location=None, tools='')
    geosource = GeoJSONDataSource(geojson = json_data)
    splot.patches('xs','ys', source = geosource, fill_color = '#131E3A', line_color = 'black', line_width = 0.25, fill_alpha = 1)
    text_year = Label(x=250, y=250, x_units='screen', y_units='screen',text=str(year), text_color='#131E3A',  text_font_size='16pt', text_font_style = 'bold')
    text_state = Label(x=0, y=250, x_units='screen', y_units='screen',text=name,text_color='#131E3A',  text_font_size='16pt', text_font_style = 'bold')
    text_med = Label(x=145, y=220, x_units='screen', y_units='screen',text=str(f"{total_med:,d}")+'$',text_color='#013240',  text_font_size='18pt', text_font_style = 'bold', text_font = 'Roboto', text_baseline = 'middle', text_align='right', x_offset=25)
    text_val1 = Label(x=175, y=210, x_units='screen', y_units='screen',text='Medical Marijuana',text_color='#013220',  text_font_size='11pt', text_font_style = 'normal', text_font = 'Roboto')
    text_ret = Label(x=145, y=180, x_units='screen', y_units='screen',text=str(f"{total_ret:,d}")+'$',text_color='#013240',  text_font_size='18pt', text_font_style = 'bold', text_font = 'Roboto', text_baseline = 'middle', text_align='right', x_offset=25)
    text_val2 = Label(x=175, y=170, x_units='screen', y_units='screen',text='Retail Marijuana',text_color='#013220',  text_font_size='11pt', text_font_style = 'normal', text_font = 'Roboto')
    text_adults = Label(x=145, y=60, x_units='screen', y_units='screen',text=str(adults)+'%', text_color='#013240',  text_font_size='18pt', text_font_style = 'bold', text_font = 'Roboto', text_baseline = 'middle', text_align='right', x_offset=25)
    text_val9 = Label(x=175, y=50, x_units='screen', y_units='screen',text='21+ Adults in state',text_color='#013220',  text_font_size='11pt', text_font_style = 'normal', text_font = 'Roboto')



    tplot.add_layout(text_year)
    tplot.add_layout(text_state)
    tplot.add_layout(text_med)
    tplot.add_layout(text_val1)
    tplot.add_layout(text_ret)
    tplot.add_layout(text_val2)

    tplot.add_layout(text_adults)
    tplot.add_layout(text_val9)


    splot.axis.visible = False
    splot.grid.visible = False
    splot.outline_line_width = 0
    tplot.outline_line_width = 0
    #l = gridplot([[splot], [tplot]], sizing_mode='scale_width')
    s = layout(tplot, sizing_mode='fixed')
    layout1 = row([splot, s], sizing_mode='stretch_width')
    layout2 = column(slider, layout1, sizing_mode='stretch_both')
    #layout2 = grid([[slider], [splot, s],], sizing_mode='stretch_both')

    script, div = components(layout2, INLINE)
    return jsonify(script=script,
                    div=div)

def get_data(query):
  """Return data from the database."""
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute(query)
  return c.fetchall()
  db.close()


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = UploadForm()
    if request.method == 'POST'and form.validate_on_submit():
        file = request.files['input_file']
        data = file.read()
        title = request.form['title']
        add_pdf(title, data)
        flash('Document upload successfully')
        return redirect(request.url)

    user = Users.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/pdf')
@login_required
def pdf():
    data = get_data("select pdf from pdf where id = 1")[0][0]
    pdfdict = get_data("select json_agg(json_build_object(id,title)) from pdf")[0][0]
    encoded_data = base64.b64encode(data).decode('utf-8')
    return render_template('pdf/pdf.html', title='PDF', encoded_data=encoded_data, pdfdict=pdfdict)

@bp.route('/pdf/<id>')
@login_required
def show_pdf(id):
    data = get_data("select pdf from pdf where id = '%s'"%id)[0][0]
    encoded_data = base64.b64encode(data).decode('utf-8')
    pdfdict = get_data("select json_agg(json_build_object(id,title)) from pdf")[0][0]
    return render_template('pdf/pdf.html', title=id, encoded_data=encoded_data, pdfdict=pdfdict)

def add_pdf(title, pdf):
  db = psycopg2.connect(database = DATABASE_URL)
  c = db.cursor()
  c.execute("insert into pdf (title, pdf) values (%s, %s)", (title, pdf))
  db.commit()
  db.close()

@bp.route('/california')
@login_required
def california():
    query_california = "select * \
                    from california"
    df_cali = pd.DataFrame(get_data(query_california), columns =['lic_num', 'lic_type', 'owner', 'contact', 'e-mail', 'phone', 'website', 'structure', 'adress', 'status', 'issue', 'exp', 'activities', 'use'])
    california_data = df_cali.to_html(index = False, classes="display compact", table_id="example")
    return render_template('california.html', california_data=california_data)

@bp.route('/colorado')
@login_required
def colorado():
    query_colorado = "select * \
                    from colorado_bis"
    df_colo = pd.DataFrame(get_data(query_colorado), columns =['bus_file_num', 'lic_type', 'entity_name', 'trade_name', 'status', 'exp_data', 'adress', 'city', 'zip_code'])
    df_colo.drop_duplicates(keep=False, inplace=True)
    df_colo['zip_code'] = df_colo['zip_code'].astype(str).str[:-2]
    colorado_data = df_colo.to_html(index = False, classes="display compact", table_id="example")
#    print (colorado_data)
    return render_template('colorado.html', colorado_data=colorado_data)

@bp.route('/oregon')
@login_required
def oregon():
    query_oregon = "select * \
                    from oregon_bis"
    df_oreg = pd.DataFrame(get_data(query_oregon), columns =['lic_num', 'lic_name', 'bus_name', 'lic_type', 'active', 'county', 'retail', 'medical', 'hemp'])
    oregon_data = df_oreg.to_html(index = False, classes="display compact", table_id="example")
#    print (colorado_data)
    return render_template('oregon.html', oregon_data=oregon_data)
