from datetime import datetime

DATETIME_FORMAT = '%b %d %Y %H:%M:%S'


def serialize_show_instance(show):
    return {
        'id': show.id,
        'start_time': show.start_time.strftime(DATETIME_FORMAT),
        'venue_id': show.venue.id,
        'artist_id': show.artist.id,
        'venue_name': show.venue.name,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link
    }


def serialize_detailed_artist_instance(artist):
    serialized_data = {
        attr: getattr(artist, attr) for attr in [
            "id", "name", "city", "state", "phone", "website", "facebook_link",
            "seeking_venue", "seeking_description", "image_link", 'past_shows', 'upcoming_shows'
        ]
    }

    serialized_data['genres'] = artist.genres.split(',')
    serialized_data['past_shows_count'] = len(serialized_data['past_shows'])
    serialized_data['upcoming_shows_count'] = len(serialized_data['upcoming_shows'])

    return serialized_data


def serialize_summarized_artist_instance(artist):
    return {
        'id': artist.id, 'name': artist.name, 'num_upcoming_shows': len(artist.upcoming_shows)
    }


def serialize_detailed_venue_instance(venue):
    serialized_data = {
        attr: getattr(venue, attr) for attr in [
            "id", "name", "city", "state", "phone", "website", "facebook_link",
            "seeking_talent", "seeking_description", "image_link", 'past_shows', 'upcoming_shows'
        ]
    }

    serialized_data['genres'] = venue.genres.split(',')
    serialized_data['past_shows_count'] = len(serialized_data['past_shows'])
    serialized_data['upcoming_shows_count'] = len(serialized_data['upcoming_shows'])

    return serialized_data


def serialize_summarized_venue_instance(venue):
    return {
        'id': venue.id, 'name': venue.name, 'num_upcoming_shows': len(venue.upcoming_shows)
    }
