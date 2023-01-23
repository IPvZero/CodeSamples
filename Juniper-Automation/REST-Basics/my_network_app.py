from flask import Flask, jsonify, request

app = Flask(__name__)
networks = [
    {"id": 1, "name": "Net1", "subnets": ["10.0.0.0/8", "192.168.1.0/24"]},
    {
        "id": 2,
        "name": "Net2",
        "subnets": ["2.2.2.2/32", "192.168.2.0/24", "172.16.0.0/16"],
    },
]


@app.route("/networks", methods=["GET"])
def get_networks():
    return jsonify({"networks": networks})


@app.route("/network/<int:id>", methods=["GET"])
def get_network(id):
    for net in networks:
        if net["id"] == id:
            return jsonify({"network": net})
    return jsonify({"error": "Network ID was not found"}), 404


@app.route("/network", methods=["POST"])
def create_network():
    data = request.get_json()
    if not data or not ("name" in data and "subnets" in data):
        return jsonify({"error": "The data is not valid"}), 400
    new_network = {
        "id": len(networks) + 1,
        "name": data["name"],
        "subnets": data["subnets"],
    }
    networks.append(new_network)
    return jsonify({"network": new_network}), 201


@app.route("/network/<int:id>", methods=["PUT"])
def update_network(id):
    for net in networks:
        if net["id"] == id:
            data = request.get_json()
            if not data or not ("name" in data and "subnets" in data):
                return jsonify({"error": "The data is not valid"}), 400
            net.update(data)
            return jsonify({"network": net}), 200
    return jsonify({"error": "Network ID was not found"}), 404


@app.route("/network/<int:id>", methods=["DELETE"])
def delete_network(id):
    for net in networks:
        if net["id"] == id:
            networks.remove(net)
            return jsonify({"info": "Network successfully deleted"}), 200
    return jsonify({"error": "Network ID was not found"}), 404


if __name__ == "__main__":
    app.run(host="192.168.4.63", port=5050, debug=True)
