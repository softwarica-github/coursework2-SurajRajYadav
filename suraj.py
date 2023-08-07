import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
import string
from random import random


class VotingSystem:
    def __init__(self, candidates):
        self.candidates = candidates
        self.vote_counts = {candidate: 0 for candidate in candidates}
        self.db_conn = sqlite3.connect("voting_system.db")
        self.create_table()

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS voters (reference_id TEXT PRIMARY KEY)")
        self.db_conn.commit()

    def vote(self, candidate, name, reference_id):
        if name.strip() != "" and reference_id.strip() != "":
            if candidate in self.candidates and not self.has_voted(reference_id):
                self.vote_counts[candidate] += 1
                self.db_conn.execute("INSERT INTO voters (reference_id) VALUES (?)", (reference_id,))
                self.db_conn.commit()
                self.store_vote_information(name, reference_id, candidate)
                messagebox.showinfo("Voting System", "Thank you for voting!")

    def has_voted(self, reference_id):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT reference_id FROM voters WHERE reference_id=?", (reference_id,))
        result = cursor.fetchone()
        return result is not None

    def get_results(self):
        return self.vote_counts
    
    def store_vote_information(self, name, reference_id, candidate):
        with open("voting_information.txt", "a") as file:
            file.write(f"Name: {name}\nReference ID: {reference_id}\nCandidate: {candidate}\n\n")




class VotingApp:
    def __init__(self, voting_system):
        self.voting_system = voting_system

        self.root = tk.Tk()
        self.root.title("The Ultimate Voting System")
        self.root.geometry("800x600")
        self.root.configure(bg="skyblue")
        self.root.resizable(False,False)

        self.name_entry = None
        self.reference_id_entry = None
        self.captcha_label_entry=None
        self.candidate_labels = []
        self.vote_buttons = []
        self.results_label = None

    def setup_ui(self):
        name_label = tk.Label(self.root, text="Name:", font=("Arial", 12), bg="skyblue")
        name_label.pack(pady=10)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack()

        reference_id_label = tk.Label(self.root, text="Reference ID:", font=("Arial", 12), bg="skyblue")
        reference_id_label.pack(pady=10)
        self.reference_id_entry = tk.Entry(self.root, font=("Arial", 12))
        self.reference_id_entry.pack()




        for i, candidate in enumerate(self.voting_system.candidates):
            label = tk.Label(self.root, text=candidate, font=("Arial", 12), bg="skyblue")
            label.pack(pady=10)
            self.candidate_labels.append(label)

            button = tk.Button(self.root, text="Vote", font=("Arial", 12), bg="white",
                               command=lambda c=candidate: self.vote(c))
            button.pack()
            self.vote_buttons.append(button)

        results_label = tk.Label(self.root, text="Results:", font=("Arial", 14, "bold"), bg="skyblue")
        results_label.pack(pady=20)
        self.results_label = results_label



    def vote(self, candidate):
        name = self.name_entry.get()
        reference_id = self.reference_id_entry.get()


        self.voting_system.vote(candidate, name, reference_id)

        self.name_entry.delete(0, tk.END)
        self.reference_id_entry.delete(0, tk.END)


        self.display_results()

    def display_results(self):
        results = self.voting_system.get_results()
        self.results_label.config(text="Results:\n" + "\n".join(f"{c}: {results[c]}" for c in results))

    def run(self):
        self.setup_ui()
        self.root.mainloop()



def main():
    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    voting_system = VotingSystem(candidates)
    app = VotingApp(voting_system)
    app.run()

if __name__ == "__main__":
    main()
