import customtkinter as ctk
import Charger
import Utility
import TaxiDb

class MainGUI():
    FONT_SIZE = 16  # Size of the text-based taxi icon

    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.ws = ctk.CTk()
        self.ws.title('Taxi cmd')
        self.ws.geometry('1000x500')

        # location
        self.customer_location = ctk.StringVar(value="location")
        self.location_dropdown = ctk.CTkComboBox(master=self.ws, width=200, values=TaxiDb.get_location_list(), variable=self.customer_location)
        self.location_dropdown.place(x=770, y=100)
        self.label_location = ctk.CTkLabel(master=self.ws, text="customer location", width=120, height=25, corner_radius=8)
        self.label_location.place(x=600, y=100)

        # destination
        self.customer_destination = ctk.StringVar(value="destination")
        self.destination_dropdown = ctk.CTkComboBox(master=self.ws, width=200, values=TaxiDb.get_destination_list(), variable=self.customer_destination)
        self.destination_dropdown.place(x=770, y=200)
        self.label_destination = ctk.CTkLabel(master=self.ws, text="customer destination", width=120, height=25, corner_radius=8)
        self.label_destination.place(x=600, y=200)

        # order taxi button
        self.button = ctk.CTkButton(master=self.ws, text="order taxi", command=self.order_taxi)
        self.button.place(x=800, y=260)

        # message label
        self.message_label = ctk.CTkLabel(master=self.ws, text="", text_color="green", width=400, height=40, corner_radius=8, font=("Arial", 16))
        self.message_label.place(x=550, y=320)

        # Canvas
        self.canvas = ctk.CTkCanvas(self.ws, width=1200, height=950, bd=0, highlightthickness=0)
        self.canvas.place(x=60, y=90)
        self.canvas.configure(bg="#C0C0C0")

        # status explanation
        self.canvas.create_oval(1030, 25, 1045, 40, fill="red",outline="red")
        self.canvas.create_text(1090, 31, text="driving", font=("Arial", 16, "bold"), fill="black")
        self.canvas.create_oval(890, 25, 905, 40, fill="yellow",outline="yellow")
        self.canvas.create_text(960, 31, text="charging", font=("Arial", 16, "bold"), fill="black")
        self.canvas.create_oval(750, 25, 765, 40, fill="green",outline="green")
        self.canvas.create_text(820, 31, text="available", font=("Arial", 16, "bold"), fill="black")

        # Render Taxi info
        self.render_taxi_info()

        # Draw a horizontal line
        self.canvas.create_line(1, 470, 1250, 470, fill="black", width=2,  tags="line")

        # charger info
        self.canvas.create_text(30, 540, text=f"available chargers:", fill="black",
                                font=("Arial", self.FONT_SIZE, "bold"),  tags="charger_info", anchor="w")
        self.canvas.create_text(60, 600, text=f"Charger {TaxiDb.get_charger_list()[0]}", fill="black",
                                font=("Arial", self.FONT_SIZE),  tags="charger", anchor="w")
        self.canvas.create_text(60, 660, text=f"Charger {TaxiDb.get_charger_list()[1]}", fill="black",
                                font=("Arial", self.FONT_SIZE), tags="charger", anchor="w")
        self.canvas.create_text(60, 720, text=f"Charger {TaxiDb.get_charger_list()[2]}", fill="black",
                                font=("Arial", self.FONT_SIZE), tags="charger", anchor="w")
        self.canvas.create_text(60, 780, text=f"Charger {TaxiDb.get_charger_list()[3]}", fill="black",
                                font=("Arial", self.FONT_SIZE), tags="charger", anchor="w")
        self.canvas.create_text(60, 840, text=f"Charger {TaxiDb.get_charger_list()[4]}", fill="black",
                                font=("Arial", self.FONT_SIZE), tags="charger", anchor="w")

    def order_taxi(self):
         taxi_id = Utility.find_taxi(self.customer_location.get().split(' ', 1)[1], self.customer_destination.get().split(' ', 1)[1])
         if taxi_id == None:
             self.display_message("Sorry!, there is no available Taxi in your area")
             self.message_label.after(6000, self.clear_message)
         else:
             #**1** display report on GUI
             self.display_message(f"Taxi with ID: {taxi_id}, is on its way to you.\n"
                                  f" the whole journey is {Utility.total_distance_km} km \n"
                                  f"and gonna take {Utility.total_duration_min} minutes")
             self.message_label.after(10000, self.clear_message)  # gonna stay on the GUI 8 seconds

             #**2** update Taxi status
             TaxiDb.update_taxi_status(int(taxi_id), "driving")

             # Start countdown for the journey duration
             self.start_countdown(taxi_id, Utility.total_duration_min * 60)

    def display_message(self, message):
        self.message_label.configure(text=message)

    def clear_message(self):
        self.message_label.configure(text="")

    def update_gui_data(self):
        self.ws.after(5000, self.render_taxi_info)

    def render_taxi_info(self):
        self.canvas.delete("taxi")  # Delete all canvas items with the "taxi" tag

        # Render Taxi info
        self.canvas.create_text(30, 70, text="Taxi info:", fill="black", font=("Arial", self.FONT_SIZE, "bold"), tags="taxi_info", anchor="w")

        for i in range(len(TaxiDb.taxi)):
            taxi_text = f"Taxi {TaxiDb.get_taxi_list()[i]}"
            taxi_color = TaxiDb.get_taxi_font_color(i + 1)
            self.canvas.create_text(60, 130 + 60 * i, text=taxi_text, fill=taxi_color, font=("Arial", self.FONT_SIZE, "bold"), tags="taxi", anchor="w")

        self.ws.after(5000, self.render_taxi_info) # Call this function again after 5000 milliseconds (5 seconds)

    def start_countdown(self, taxi_id, remaining_seconds):
        y = {1: 130, 2: 190, 3: 250, 4: 310, 5: 370}.get(int(taxi_id))
        if remaining_seconds > 0:
            # Calculate minutes and seconds from total seconds
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60

            # Display the countdown on the screen
            countdown_message = f"{minutes:02}:{seconds:02}"  # Ensure double digits for formatting
            self.canvas.delete(f"counter_{int(taxi_id)}") #Remove the previous countdown text
            self.canvas.create_text(1000, y, text=countdown_message, fill="purple",font=("Arial", self.FONT_SIZE), tags=f"counter_{int(taxi_id)}", anchor="w")
            # Update the countdown every second
            self.message_label.after(1000, lambda: self.start_countdown(taxi_id, remaining_seconds - 1))
        else:
            #**1** update taxi battery & status after journey
            TaxiDb.update_taxi_battery_status(int(Utility.total_distance_km), int(taxi_id), self.customer_destination.get().split(' ', 1)[1])
            #**2** delete counter from GUI
            self.canvas.delete(f"counter_{int(taxi_id)}")

if __name__ == "__main__":
    Charger.start_periodic_task()
    gui = MainGUI()
    gui.ws.mainloop()


