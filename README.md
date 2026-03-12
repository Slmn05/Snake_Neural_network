# Snake_Neural_network
# 🐍 Snake Game with Neural Network AI

This project is a classic **Snake game** implemented in Python, with a **trainable neural network AI** that can learn to play the game.

You can either play the game manually or train/watch an AI learn how to play.

## 🎮 Play the Game Yourself

To play Snake manually, run:

```bash
python SNAKE.py
```

---

## 🤖 Watch the Trained AI Play

To watch the neural network that I trained play the game, run:

```bash
python Play_AI.py
```

---

## 🧠 Continue Training the Existing AI

If you want to continue training the existing AI, open **Play_AI.py** and uncomment the following line:

```python
# V3.train(1000, 100, [w1, w2])
```

This will train the AI for **100 generations** with a **population size of 1000**, starting from the current trained weights.

---

## 🧪 Train Your Own AI From Scratch

To train a completely new neural network, uncomment the following line in **Play_AI.py**:

```python
V3.train(1000, 200)  # train(population_size, generations)
```

⚠️ This will **overwrite the existing training logs and weights**.

---
## 🎮 Training Data

<p align="center">
  <img src="training_logs\pop_size_1000_number_of_gens_200.png" width="500">
</p>
---

## 📦 Installation

Install the required libraries using:

```bash
pip install -r requirements.txt
```

---

## 🛠 Technologies Used

* **Python**
* **Pygame** (game engine)
* **NumPy** (neural network computations)
* **Matplotlib** (training visualization)
