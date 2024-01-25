import customtkinter as ctk
from tkinter import ttk
from tkcalendar import Calendar
import csv
from datetime import datetime, timedelta
class CalendarWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Créer le calendrier
        self.cal = Calendar(self, selectmode='day', date_pattern='dd/mm/y')
        self.cal.pack(pady=20, padx=20, anchor='nw', side='left')
        self.cal.bind("<<B1>>", self.on_date_selected)

        # Créer le cadre pour les événements
        events_frame = ctk.CTkFrame(self)
        events_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Créer une étiquette pour afficher la date sélectionnée
        self.label_date = ctk.CTkLabel(events_frame, text="Date sélectionnée : ")
        self.label_date.pack(pady=10)

        # Créer une boîte de texte pour afficher les événements de la date sélectionnée
        self.text_events = ctk.CTkTextbox(events_frame, wrap='word', state='disabled', height=8)
        self.text_events.pack(pady=10, padx=10, fill='both', expand=True)

        # Ajouter un bouton pour simuler le passage à la date suivante
        button_next_day = ctk.CTkButton(events_frame, text="Simuler Jour Suivant", command=self.simulate_next_day)
        button_next_day.pack(pady=10)

        # Ajouter un bouton pour ouvrir la fenêtre de gestion des équipes
        button_open_teams = ctk.CTkButton(events_frame, text="Gestion des Équipes", command=self.master.show_teams_window)
        button_open_teams.pack(pady=10)

    def on_date_selected(self, event):
        selected_date = self.cal.get_date()
        self.label_date.configure(text="Date sélectionnée : " + selected_date)

        if selected_date in self.master.events:
            events_text = "\n".join(self.master.events[selected_date])
        else:
            events_text = "Aucun événement pour cette date."

        self.text_events.configure(state='normal')
        self.text_events.delete('1.0', 'end')
        self.text_events.insert('1.0', events_text)
        self.text_events.configure(state='disabled')

    def update_events_text(self, selected_date):
        if selected_date in self.master.events:
            events_text = "\n".join(self.master.events[selected_date])
        else:
            events_text = "Aucun événement pour cette date."
        self.text_events.configure(state='normal')
        self.text_events.delete('1.0', 'end')
        self.text_events.insert('1.0', events_text)
        self.text_events.configure(state='disabled')

    def simulate_next_day(self):
        current_date = datetime.strptime(self.cal.get_date(), "%d/%m/%Y")
        next_date = current_date + timedelta(days=1)
        next_date_str = next_date.strftime("%d/%m/%Y")
        self.cal.selection_set(next_date_str)
        self.on_date_selected(None)


class TeamsWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        teams_window = ctk.CTkFrame(self)
        teams_window.pack(pady=10, padx=10)

        teams = self.master.load_team_names_from_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\calendar.csv")

        for team_name in teams:
            button = ctk.CTkButton(teams_window, text=team_name, command=lambda name=team_name: self.open_club_window(name))
            button.pack(pady=5)

        back_button = ctk.CTkButton(teams_window, text="Retour", command=self.master.show_calendar_window)
        back_button.pack(pady=10)

    def open_club_window(self, club_name):
        self.master.show_club_window(club_name)


class ClubWindow(ctk.CTkFrame):
    def __init__(self, parent, club_name):
        super().__init__(parent)
        self.club_name = club_name
        self.create_widgets()

    def create_widgets(self):
        club_window = ctk.CTkFrame(self)
        club_window.pack(pady=10, padx=10)

        label = ctk.CTkLabel(club_window, text=f"Club sélectionné : {self.club_name}")
        label.pack(pady=20)

        back_button = ctk.CTkButton(club_window, text="Retour", command=self.master.show_teams_window)
        back_button.pack(pady=10)


class MainWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Calendrier et Classement")
        self.geometry("800x600")

        # Charger les événements à partir du fichier CSV
        self.events = self.load_events_from_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\events_july_2023.csv")

        # Charger le classement des équipes à partir du fichier CSV
        self.standings = self.load_team_standings_from_csv(r"C:\Users\pierr\PycharmProjects\Mercato\data\calendar.csv")

        self.calendar_window = CalendarWindow(self)
        self.teams_window = TeamsWindow(self)
        self.club_window = None

        self.show_calendar_window()

    def show_calendar_window(self):
        if self.club_window:
            self.club_window.pack_forget()
        self.calendar_window.pack()

    def show_teams_window(self):
        self.calendar_window.pack_forget()
        self.teams_window.pack()

    def show_club_window(self, club_name):
        self.teams_window.pack_forget()
        self.club_window = ClubWindow(self, club_name)
        self.club_window.pack()

    def load_events_from_csv(self, file_path):
        events = {}
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignorer la première ligne (en-tête)
            for row in reader:
                date_str, description = row[0], row[1]
                date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")
                events[date] = events.get(date, []) + [description]
        return events

    def load_team_standings_from_csv(self, file_path):
        teams = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignorer la première ligne (en-tête)
            for row in reader:
                teams.append(row)
        return teams

    def load_team_names_from_csv(self, file_path):
        teams = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignorer la première ligne (en-tête)
            for row in reader:
                team_name = row[1]
                teams.append(team_name)
        return teams


def main():
    root = MainWindow()
    root.mainloop()


if __name__ == '__main__':
    main()
