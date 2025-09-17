import tkinter as tk
from tkinter import font
import random

# Emoji icons for each move
ICONS = {
    "rock": "✊",
    "paper": "✋",
    "scissors": "✌️"
}
MOVES = list(ICONS.keys())

RESULT_TEXT = {
    "win": "🎉 Vyhrál jsi!",
    "lose": "😕 Prohrál jsi.",
    "draw": "🤝 Remíza!"
}

class RPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors")
        self.configure(bg="#222")

        self.history = []
        self.score = {"player": 0, "pc": 0, "draw": 0}

        self.setup_fonts()
        self.create_widgets()

    def setup_fonts(self):
        # Attempt to use a large emoji-compatible font, fallback if needed
        self.emoji_font = font.Font(family="Segoe UI Emoji", size=48)
        self.result_font = font.Font(family="Arial", size=22, weight="bold")
        self.score_font = font.Font(family="Arial", size=18, weight="bold")
        self.hist_font = font.Font(family="Consolas", size=12)

    def create_widgets(self):
        # Score label
        self.score_label = tk.Label(self, text=self.format_score(), bg="#222", fg="#eee", font=self.score_font)
        self.score_label.pack(pady=(15, 10))

        # Result label
        self.result_label = tk.Label(self, text="Hraj!", bg="#222", fg="#4ad991", font=self.result_font)
        self.result_label.pack(pady=(0, 20))

        # Icon buttons
        btn_frame = tk.Frame(self, bg="#222")
        btn_frame.pack(pady=(0, 20))

        self.buttons = {}
        for i, move in enumerate(MOVES):
            b = tk.Button(
                btn_frame, text=ICONS[move], font=self.emoji_font, width=4, height=2,
                command=lambda m=move: self.play(m),
                bg="#353d4c", fg="#fff", bd=0, activebackground="#65738a", activeforeground="#fff",
                highlightthickness=0, relief="flat", cursor="hand2"
            )
            b.grid(row=0, column=i, padx=15)
            self.buttons[move] = b

        # Game history
        self.hist_label = tk.Label(self, text="Historie:", bg="#222", fg="#ccc", font=self.hist_font, anchor="w")
        self.hist_label.pack(fill="x", padx=20, pady=(0, 5))
        self.hist_box = tk.Text(self, height=7, width=34, bg="#111", fg="#bbb", font=self.hist_font, state="disabled", wrap="none")
        self.hist_box.pack(padx=20, pady=(0, 12))

        # Reset button
        self.reset_btn = tk.Button(
            self, text="Reset", font=self.score_font, bg="#373", fg="#fff",
            command=self.reset_game, bd=0, highlightthickness=0, relief="flat", width=10, cursor="hand2"
        )
        self.reset_btn.pack(pady=(0, 12))

    def format_score(self):
        return f"Ty: {self.score['player']}   PC: {self.score['pc']}   Remíza: {self.score['draw']}"

    def play(self, player_move):
        pc_move = random.choice(MOVES)
        result = self.judge(player_move, pc_move)
        self.update_score(result)
        self.show_result(result, player_move, pc_move)
        self.add_history(player_move, pc_move, result)

    def judge(self, player, pc):
        if player == pc:
            return "draw"
        wins = [("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")]
        if (player, pc) in wins:
            return "win"
        return "lose"

    def update_score(self, result):
        if result == "win":
            self.score["player"] += 1
        elif result == "lose":
            self.score["pc"] += 1
        else:
            self.score["draw"] += 1
        self.score_label.config(text=self.format_score())

    def show_result(self, result, player_move, pc_move):
        msg = RESULT_TEXT[result]
        msg += f"\nTy: {ICONS[player_move]}  PC: {ICONS[pc_move]}"
        self.result_label.config(text=msg, fg=("#4ad991" if result=="win" else "#ed5a5a" if result=="lose" else "#ffa800"))

    def add_history(self, player_move, pc_move, result):
        entry = f"Ty: {ICONS[player_move]}  PC: {ICONS[pc_move]}  =>  {RESULT_TEXT[result].split(' ')[0]}"
        self.history.append(entry)
        self.hist_box.config(state="normal")
        self.hist_box.delete(1.0, tk.END)
        for i, line in enumerate(self.history[-7:]):
            self.hist_box.insert(tk.END, f"{len(self.history)-len(self.history[-7:])+i+1:2d}: {line}\n")
        self.hist_box.see(tk.END)
        self.hist_box.config(state="disabled")

    def reset_game(self):
        self.score = {"player": 0, "pc": 0, "draw": 0}
        self.history = []
        self.score_label.config(text=self.format_score())
        self.result_label.config(text="Hraj!", fg="#4ad991")
        self.hist_box.config(state="normal")
        self.hist_box.delete(1.0, tk.END)
        self.hist_box.config(state="disabled")

if __name__ == "__main__":
    app = RPSApp()
    app.resizable(False, False)
    app.mainloop()
