from dns.exception import DNSException
from flask import Flask, request, jsonify
from netaddr import IPNetwork
import dns.resolver
from datetime import datetime
import validators
import re

app = Flask(__name__)


def resolve_dns(dom):
    try:
        resolver = dns.resolver.Resolver()
        answer = resolver.resolve(dom, "A")
        return answer
    except DNSException:
        return None


lst_regitser = []


@app.route('/dns/<dominio>', methods=['GET'])
def get_resolucion(dominio):
    """ devuelve un json con la resolución DNS de tipo A del dominio """
    if request.method == "GET":
        result_dns = resolve_dns(dominio)
        if result_dns:
            data = {
                "name": dominio,
                "resolution_dns": [],
                "created_at": datetime.now(),

            }
            for item in result_dns:
                print(item)
                data["resolution_dns"].append(str(item))

            print(dominio)
            lst_regitser.append(data)
            print(lst_regitser)
            return jsonify(data), 200
        else:
            return jsonify({"message": "No valid domain name"}), 400
    else:
        return "Se recibió un POST"


@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(lst_regitser), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
