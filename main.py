import subprocess
import os

import tornado.web
import tornado.ioloop
import sqlite3
import logging
logging.basicConfig(level=logging.DEBUG)

connection = sqlite3.connect("files/database.db")
c = connection.cursor()


class downloadRequestHandler(tornado.web.RequestHandler):
    def get(self, location):

        url = self.get_argument("url")
        logging.debug(f"Request Recieved: url: {url}")
        location = list(c.execute("SELECT location FROM managed_locations WHERE name = ?",(location,)).fetchone())[0]
        logging.debug(location)

        if bool(self.get_argument("direct_link")) is True:
            subprocess.Popen(["/usr/bin/wget", "-o", os.path.join(location, "TBF", url.strip("/")[-1], url])

        else:
            subprocess.Popen(["/home/tristan/.local/bin/youtube-dl", "-o", os.path.join(location,"TBF","%(title)s.%(ext)s"), url])

        self.write("successful")
            
class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        import json
        self.write(json.dumps([item[0] for item in c.execute("SELECT name FROM managed_locations").fetchall()]))

if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/download/(\w+)', downloadRequestHandler),
        (r'/list', listRequestHandler),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
