#!/usr/bin/env python

import web
import xmlrpclib
import utils


urls = (
    '/(.*)', 'index'
)


old_version = False
proxy = xmlrpclib.ServerProxy("http://localhost:8123/RPC2/")


def fetch_data():
    methods = {
        "hash": "d.get_hash",
        "name": "d.get_name",

        "raw_down_rate": "d.get_down_rate",
        "raw_up_rate": "d.get_up_rate",

        "raw_completed_bytes": "d.get_completed_bytes",
        "raw_total_bytes": "d.get_size_bytes",
        "raw_left_bytes": "d.get_left_bytes",

        "active": "d.is_active",
        "hashing": "d.is_hash_checking",

        "connection_current": "d.get_connection_current",
        "connection_leech": "d.get_connection_leech",
        "connection_seed": "d.get_connection_seed",

        "raw_ratio": "d.get_ratio",
    }

    call_keys = list()
    call_methods = list()

    for key, val in methods.iteritems():
        call_keys.append(key)
        call_methods.append("%s=" % val)

    raw_torrents = proxy.d.multicall("started", *call_methods)
    torrents = list()

    for raw_torrent in raw_torrents:
        torrent = dict()

        for key, val in zip(call_keys, raw_torrent):
            torrent[key] = val

        torrents.append(torrent)

    return torrents


def format_data(data):
    data["completed_bytes"] = utils.format_size(data["raw_completed_bytes"])
    data["total_bytes"] = utils.format_size(data["raw_total_bytes"])
    data["percentage"] = "%.2f" % (data["raw_completed_bytes"] / float(data["raw_total_bytes"]) * 100)
    data["state"] = get_state(data)
    data["ratio"] = "%.2f" % (float(data["raw_ratio"]) / 1000)
    data["down_rate"] = utils.format_speed(data["raw_down_rate"])
    data["time_remaining"] = utils.time_remaining(data["raw_down_rate"], data["raw_left_bytes"])

    return data


def get_state(data):
    if not data["active"]:
        return "hashing" if data["hashing"] else "stopped"

    return "leeching" if data["connection_current"] == "leech" else "seeding"


class index:
    def GET(self, name):
        torrents = fetch_data()
        unfinished_torrents = list()
        finished_torrents = list()

        for t in torrents:
            t = format_data(t)
            if t['state'] == "leeching":
                unfinished_torrents.append(t)
            else:
                finished_torrents.append(t)

        finished_torrents = sorted(finished_torrents, key=lambda x: x['name'])
        unfinished_torrents = sorted(unfinished_torrents, key=lambda x: x['name'])

        context = {
            'torrentlists': (
                {"torrents": unfinished_torrents, "type": "unfinished"},
                {"torrents": finished_torrents, "type": "finished"},
            )
        }

        return utils.render("index.html", context)


app = web.application(urls, globals())


if __name__ == "__main__":
    app.run()
