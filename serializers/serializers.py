"""Module for serializing querysets."""

from .utils import (
    serialize_detailed_artist_instance, serialize_detailed_venue_instance,
    serialize_summarized_artist_instance, serialize_summarized_venue_instance,
    serialize_show_instance
)


def serialize_show(shows, many=False):
    """
    Serializer for show.

    :param artists:
    :param many=False:
    :param summarized=True:
    """
    return [ serialize_show_instance(show) for show in shows ] if many else serialize_show_instance(shows)


def serialize_artist(artists, many=False, summarized=True):
    """
    Serializer for artist.

    :param artists:
    :param many=False:
    :param summarized=True:
    """
    serializer_func = serialize_summarized_artist_instance if summarized else serialize_detailed_artist_instance
    return [ serializer_func(artist) for artist in artists ] if many else serializer_func(artists)


def serialize_venue(venues, many=False, summarized=True):
    """
    Serializer for venue.

    :param artists:
    :param many=False:
    :param summarized=True:
    """
    serializer_func = serialize_summarized_venue_instance if summarized else serialize_detailed_venue_instance
    return [ serializer_func(venue) for venue in venues ] if many else serializer_func(venues)
