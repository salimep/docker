from flask import Flask
app= Flask(__name__)
@app.route("/<name>")

def first(name):
    return "hello {}".format(name)



if __name__ == '__main__':
    app.run()