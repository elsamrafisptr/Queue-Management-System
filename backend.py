from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

Base = declarative_base()

class Antrean(Base):
    __tablename__ = 'antrean'
    id = Column(Integer, primary_key=True)
    nomor_antrean = Column(Integer)
    estimasi_waktu = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class AntreanServer:
    def __init__(self):
        self.counter = 1
        self.engine = create_engine('sqlite:///antrean.db')  # SQLite for simplicity
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.antrean_data = {}

    def get_antrean(self):
        with self.Session() as session:
            antrean = session.query(Antrean).order_by(Antrean.timestamp.desc()).first()
            if antrean:
                antrean_data = {
                    "nomor_antrean": antrean.nomor_antrean,
                    "estimasi_waktu": antrean.estimasi_waktu
                }
                return json.dumps(antrean_data)
            else:
                return json.dumps({})

    def update_antrean(self):
        antrean_data = {
            "nomor_antrean": self.counter,
            "estimasi_waktu": "30 menit"
        }
        with self.Session() as session:
            new_antrean = Antrean(**antrean_data)
            session.add(new_antrean)
            session.commit()
        self.antrean_data = antrean_data
        self.counter += 1
        return "Antrean berhasil diperbarui"

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler, logRequests=True, allow_none=True)
    server.register_instance(AntreanServer())

    print("Server Antrean Medis berjalan di port 8000...")
    server.serve_forever()
