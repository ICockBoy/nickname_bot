import asyncio
import queue
import select
import socket

from DataBase import DataBaseJson
from session import Session

Sessions = {}
db = DataBaseJson("unrealskill.ueuo.com", "unrealskill.ueuo.com", "shluxa_111!")


async def stuff(data):
    _data = data.decode('utf-8').split("\r")
    if _data[0] == "code":
        request_js = _data[1].split("&")
        if request_js[0] not in Sessions:
            Sessions[request_js[0]] = Session()
        result = await Sessions[request_js[0]].send_code(request_js[1].strip(" "))
        if result:
            return b'1'
        else:
            return b'0'
    if _data[0] == "auth":
        request_js = _data[1].split("&")
        if request_js[0] not in Sessions:
            return b'0'
        else:
            result = await Sessions[request_js[0]].auth(request_js[1])
            if result:
                db.set_session(int(request_js[0]), Sessions[request_js[0]].import_to_dict())
                return b'1'
            else:
                return b'0'


async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(('localhost', 50000))
    server.listen(5)
    inputs = [server]
    outputs = []
    message_queues = {}
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    result = await stuff(data)
                    message_queues[s].put(result)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                s.send(next_msg)
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == "__main__":
    asyncio.run(main())
