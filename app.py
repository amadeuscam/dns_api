from datetime import datetime
import dns.resolver
from dns.exception import DNSException
from flask import Flask, request, jsonify

app = Flask(__name__)


def resolve_dns(dom):
    """ devulve las ip asociadas al dominio """
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
                data["resolution_dns"].append(str(item))

            lst_regitser.append(data)
    
            return jsonify(data), 200
        else:
            return jsonify({"message": "No valid domain name"}), 400


@app.route('/history', methods=['GET'])
def get_history():
    """ devuelve el historial de las peticiones  """
    return jsonify(lst_regitser), 200
