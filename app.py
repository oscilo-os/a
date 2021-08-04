import base64
import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TKAgg")
from io import BytesIO
from flask import *

from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/',methods =["GET", "POST"])
def hello():
    return render_template("form.html")

@app.route('/plot',methods =["GET", "POST"])
def pl():
    if request.method == "POST":
        N = float(request.form.get("N"))
        a = float(request.form.get("a"))
        b = float(request.form.get("b"))
        c = float(request.form.get("c"))
        d = float(request.form.get("d"))
        epsilon = float(request.form.get("epsilon"))
        maxperiod = float(request.form.get("maxperiod"))
        initial_proportion = float(request.form.get("initial_proportion"))

        qstar = (b - c) / (a - d + b - c)
        print(qstar)
        choise_history = []
        for i in range(int(N)):
            rand = random.random()
            if rand < initial_proportion:
                choise_history.append(1)
            else:
                choise_history.append(0)

        k0 = sum(choise_history)
        kt = [k0]
        for i in range(int(maxperiod)):

            q = []
            for j in range(int(N) - 1):
                q.append((choise_history[j - 1] + choise_history[j + 1]) / 2)
                q.append((choise_history[0] + choise_history[int(N) - 2]) / 2)

            I = []
            for j in range(int(N)):
                if q[j] >= qstar:
                    I.append(1)
                else:
                    I.append(0)

            new_choice_history = []
            for j in range(int(N)):
                rand1 = random.random()
                rand2 = random.random()

                if rand1 < 1 - 2 * epsilon:
                    new_choice_history.append(I[j])
                elif rand2 < 0.5:
                    new_choice_history.append(1)
                else:
                    new_choice_history.append(0)

            kt.append(sum(new_choice_history))
            choise_history = new_choice_history
        ktprint = [i / N for i in kt]
        plt.plot(ktprint)
        plt.ylim(0, 1)
        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"

if __name__=='__main__':
    app.run()
