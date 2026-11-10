
from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Snake and Ladder</title>
<style>
body {
    background: linear-gradient(135deg, #141e30, #243b55);
    color: white;
    font-family: Arial;
    text-align: center;
}
h1 { color: #ffcc00; }

.board {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    max-width: 600px;
    margin: 20px auto;
    gap: 3px;
}
.cell {
    background: #fff;
    color: #222;
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 13px;
    border-radius: 5px;
    position: relative;
}
.snake { background: #ff7675; }
.ladder { background: #55efc4; }
.player1 { border: 4px solid #0984e3; }
.player2 { box-shadow: inset 0 0 0 4px #e17055; }

button {
    padding: 12px 25px;
    background: #ffcc00;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    font-size: 16px;
}
.info {
    background: white;
    color: #222;
    padding: 15px;
    max-width: 400px;
    margin: 20px auto;
    border-radius: 10px;
}
</style>
</head>
<body>

<h1>🐍 SNAKE AND LADDER 🪜</h1>
<h3>First player to reach 100 wins!</h3>

<div class="info">
    <h3>🔵 Player 1: {{ p1 }}</h3>
    <h3>🔴 Player 2: {{ p2 }}</h3>
    <h3>🎲 Dice: {{ dice }}</h3>
    <h3>{{ message }}</h3>

    {% if not winner %}
    <form method="POST">
        <button type="submit">🎲 Roll Dice</button>
    </form>
    {% else %}
    <h2>🏆 {{ winner }} WINS!</h2>
    {% endif %}

    <form method="POST" action="/reset">
        <button type="submit">🔄 New Game</button>
    </form>
</div>

<div class="board">
{% for n in cells %}
    <div class="cell
    {% if n in snakes %}snake{% elif n in ladders %}ladder{% endif %}
    {% if n == p1 %} player1{% endif %}
    {% if n == p2 %} player2{% endif %}">
        {{ n }}
        {% if n == p1 %}🔵{% endif %}
        {% if n == p2 %}🔴{% endif %}
        {% if n in snakes %}🐍{{ snakes[n] }}{% endif %}
        {% if n in ladders %}🪜{{ ladders[n] }}{% endif %}
    </div>
{% endfor %}
</div>

<p>🔵 Player 1 | 🔴 Player 2</p>
<p>🐍 Red = Snake | 🪜 Green = Ladder</p>

</body>
</html>
"""

snakes = {
    99: 54, 70: 55, 52: 42, 25: 2, 95: 72
}

ladders = {
    6: 25, 11: 40, 60: 85, 46: 90, 17: 69
}

@app.route("/", methods=["GET", "POST"])
def home():
    if "p1" not in globals():
        reset_game()

    global p1, p2, turn, dice, message, winner

    if request.method == "POST" and not winner:
        dice = random.randint(1, 6)

        if turn == 1:
            position = p1 + dice
            if position <= 100:
                p1 = snakes.get(position, ladders.get(position, position))
            message = "Player 1 rolled " + str(dice)
            if p1 == 100:
                winner = "Player 1"
            turn = 2

        else:
            position = p2 + dice
            if position <= 100:
                p2 = snakes.get(position, ladders.get(position, position))
            message = "Player 2 rolled " + str(dice)
            if p2 == 100:
                winner = "Player 2"
            turn = 1

    cells = []
    for row in range(9, -1, -1):
        nums = list(range(row * 10 + 1, row * 10 + 11))
        if row % 2 == 1:
            nums.reverse()
        cells.extend(nums)

    return render_template_string(
        HTML, p1=p1, p2=p2, turn=turn, dice=dice,
        message=message, winner=winner,
        cells=cells, snakes=snakes, ladders=ladders
    )

def reset_game():
    global p1, p2, turn, dice, message, winner
    p1 = 0
    p2 = 0
    turn = 1
    dice = "-"
    message = "Player 1 starts!"
    winner = None

@app.route("/reset", methods=["POST"])
def reset():
    reset_game()
    return home()

reset_game()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

