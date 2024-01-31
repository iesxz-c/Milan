from discord import create_app,skt

app = create_app


if __name__ == "__main__":
    skt.run(app,host='0.0.0.0', port=5000, debug=True)


