#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import app, db, Venue, Artist, Show
from serializers import serialize_show, serialize_artist, serialize_venue


def format_datetime(value, format='medium'):
    """
    Format datetime util.

    :param value:
    :param format='medium':
    """
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
def index():
    """
    Controller to show homepage.
    """
    return render_template('pages/home.html')


@app.route('/venues')
def venues():
    """
    Controller to list all venues.
    """
    data = {}
    for venue in serialize_venue(Venue.query.all(), many=True, summarized=False):
        if venue['city'] not in data:
            data[venue['city']] = {
                'state': venue['state'],
                'venues': [venue]
            }
        else:
            data[venue['city']]['venues'].append(venue)

    data = [{'city': city, 'state': data[city]['state'], 'venues': data[city]['venues']} for city in data.keys()]

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Controller to search venues.
    """
    search_term = request.form.get('search_term')
    venues = serialize_venue(Venue.query.filter(Venue.name.ilike(f'%{search_term}%')), many=True)
    response={
        "count": len(venues), "data": venues
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    Controller to retrieve venue by id.

    :param venue_id:
    """
    venue = serialize_venue(Venue.query.get(venue_id), summarized=False)
    return render_template('pages/show_venue.html', venue=venue)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """
    Controller to render new venue form.
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    Controller to handle venue creation.
    """
    try:
        request_data = { **request.form }
        request_data['seeking_talent'] = request_data.get('seeking_talent') == 'y'
        venue = Venue(**request_data)
        db.session.add(venue)
        db.session.commit()
        flash(f'Venue `{request_data.get("name")}` was successfully listed.')
    except Exception as ex:
        db.session.rollback()
        print(ex)
        flash(f'Venue `{request_data.get("name")}` couldn\'t be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """
    Controller to delete venue based on venue_id.

    :param venue_id:
    """
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/artists')
def artists():
    """
    Controller to list all the artists.
    """
    artists = serialize_artist(Artist.query.all(), many=True)
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Controller to search artists.
    """
    search_term = request.form.get('search_term', '')
    artists = serialize_artist(Artist.query.filter(Artist.name.ilike(f'%{search_term}%')), many=True)
    response={
        "count": len(artists), "data": artists
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Controller to retrieve artist by id.

    :param artist_id:
    """
    artist = serialize_artist(Artist.query.get(artist_id), summarized=False)
    return render_template('pages/show_artist.html', artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Controller to render edit artist form.

    :param artist_id:
    """
    artist = Artist.query.get(artist_id)
    serialized_artist = serialize_artist(artist, summarized=False)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=serialized_artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    Controller to edit artist.

    :param artist_id:
    """
    artist = Artist.query.get(artist_id)
    for field in [
        "name", "city", "state", "phone", "website", "facebook_link",
        "seeking_description", "image_link", "genres"
    ]:
        setattr(artist, field, request.form.get(field))
    artist.seeking_venue = request.form.get('seeking_venue') == 'y'

    try:
        db.session.commit()
        flash(f'Artist {artist.name} was successfully updated.')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f'Artist `{artist.name}` couldn\'t be updated.')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Controller to render edit venue form.

    :param venue_id:
    """
    venue = Venue.query.get(venue_id)
    serialized_venue = serialize_venue(venue, summarized=False)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=serialized_venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    for field in [
        "name", "city", "state", "phone", "website", "facebook_link",
        "seeking_description", "image_link", "genres"
    ]:
        setattr(venue, field, request.form.get(field))
    venue.seeking_talent = request.form.get('seeking_talent', False)

    try:
        db.session.commit()
        flash(f'Venue {venue.name} was successfully updated.')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f'Venue `{venue.name}` couldn\'t be updated.')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """
    Controller to render artist form.
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    Controller to handle artist creation.
    """
    try:
        request_data = { **request.form }
        request_data['seeking_venue'] = request_data.get('seeking_venue') == 'y'
        artist = Artist()
        db.session.add(artist)
        db.session.commit()
        flash(f'Artist `{request_data.get("name")}` was successfully listed.')
    except Exception as ex:
        db.session.rollback()
        print(ex)
        flash(f'Artist `{request_data.get("name")}` couldn\'t be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/shows')
def shows():
    """
    Controller to display all shows.
    """
    shows = serialize_show(Show.query.all(), many=True)
    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    """
    Controller to render shows form.
    """
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    Controller to handle show scheduling.
    """
    try:
        show = Show(**request.form)
        db.session.add(show)
        db.session.commit()
        flash(f'Show was successfully listed.')
    except Exception as ex:
        db.session.rollback()
        print(ex)
        flash(f'Show couldn\'t be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    """
    404 error handler.

    :param error:
    """
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """
    500 error handler.

    :param error:
    """
    return render_template('errors/500.html'), 500
