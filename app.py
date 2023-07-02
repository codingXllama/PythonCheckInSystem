# current main

import csv
import datetime
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk


class User:
    def __init__(self, name, pin):
        self.Name = name
        self.Pin = pin
        self.CheckInDateTime = None
        self.TotalDuration = datetime.timedelta()
        self.IsCheckedIn = False


class AttendanceManagementSystem:
    def __init__(self):
        self.users = []
        self.checked_in_users = []
        self.loadUsers()

        self.root = ctk.CTk()
        self.root.geometry("1000x5000")
        self.root.attributes("-fullscreen", True)
        self.root.title("AlBerr Mosque Attendance Management System")

        title_label = ctk.CTkLabel(
            self.root,
            text="AlBerr Mosque Attendance Management System",
            font=ctk.CTkFont(size=30, weight="bold", family="Dank Mono"),
        )
        title_label.pack(padx=10, pady=(40, 20))

        self.scrollable_frame = ctk.CTkScrollableFrame(self.root)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.pin_label = tk.Label(
            self.scrollable_frame,
            # text="Enter your 4-digit PIN (0 to exit)",
            text="Enter your PIN to Clock In & Out",
            font=ctk.CTkFont(size=20, weight="bold", family="Dank Mono"),
            background="#2b2b2b",
            foreground="white",
            width=200,
            anchor="center",
        )
        self.pin_label.pack(padx=10, pady=(40, 10), anchor="c")

        self.pin_entry = ctk.CTkEntry(
            self.scrollable_frame,
            width=425,
            height=50,
            placeholder_text="\tEnter PIN\t",
            font=ctk.CTkFont(size=30),
            show="*",
        )
        self.pin_entry.pack(padx=30, pady=(0, 0))

        self.check_in_button = ctk.CTkButton(
            self.scrollable_frame,
            text="CLOCK-IN/OUT",
            font=ctk.CTkFont(size=20, weight="bold", family="Dank Mono"),
            command=self.checkInOrOut,
            anchor="center",
            width=150,
            height=50,
        )

        self.check_in_button.pack(padx=150, pady=(30, 10))

        self.checked_in_users_label = tk.Label(
            self.scrollable_frame,
            text="",
            font=ctk.CTkFont(size=15, weight="bold", family="Dank Mono"),
            background="#2b2b2b",
            foreground="white",
        )
        self.checked_in_users_label.pack()

        self.checked_in_users_listbox = tk.Listbox(
            self.scrollable_frame,
            width=30,
            height=10,
            background="#2d2a2e",
            borderwidth=0,
            justify="center",
            foreground="white",
            font=ctk.CTkFont(
                size=40,
                weight="bold",
                family="Dank Mono",
            ),
        )
        self.checked_in_users_listbox.pack(padx=10, pady=(10, 10))

        footer = ctk.CTkLabel(
            self.root,
            text="Made with 💖 by Osama Al-Chalabi.",
            font=ctk.CTkFont(size=20, weight="bold", family="Dank Mono"),
        )
        footer.pack(padx=10, pady=(10, 10))

        # uncommented this to remove binding for the checkout based on user list select
        # self.checked_in_users_listbox.bind("<<ListboxSelect>>", self.onUserSelect)

        # self.duration_label = tk.Label(self.scrollable_frame, text="Duration: 00:00")
        # self.duration_label.pack()

        self.users_status_label = tk.Label(self.scrollable_frame, text="")
        self.users_status_label.pack()

        self.updateCheckedInUsersListbox()
        self.update_duration()
        self.updateUsersStatus()

        self.root.mainloop()

    def loadUsers(self):
        # Hardcode user data
        self.users.append(User("John", 1234))
        self.users.append(User("Jane CD.", 5678))
        self.users.append(User("Vic S.", 44444))
        self.users.append(User("Nuca.", 1235))

    def checkInOrOut(self):
        pin = int(self.pin_entry.get())

        # if pin == 0:
        #     self.root.quit()
        #     return

        user = next((u for u in self.users if u.Pin == pin), None)

        if user is not None:
            currentDate = datetime.datetime.now().date()

            if user.IsCheckedIn and user.CheckInDateTime.date() == currentDate:
                # User wants to check out
                duration = datetime.datetime.now() - user.CheckInDateTime
                totalDuration = user.TotalDuration + duration

                messagebox.showinfo(
                    "Check Out",
                    # f"You have been checked out, {user.Name}! Your check-in time was {user.CheckInDateTime.strftime('%H:%M:%S')}. Total duration: {totalDuration.days * 24 + totalDuration.seconds // 3600}:{(totalDuration.seconds % 3600) // 60:02}",
                    f"You have been checked out, {user.Name}! Your Total duration is {totalDuration.days * 24 + totalDuration.seconds // 3600}:{(totalDuration.seconds % 3600) // 60:02}. Have a good day!",
                )

                user.TotalDuration = totalDuration
                user.IsCheckedIn = False
                self.checked_in_users.remove(user)
                self.exportDataToCSV(user)
            else:
                # User wants to check in
                user.CheckInDateTime = datetime.datetime.now()
                user.TotalDuration = datetime.timedelta()
                user.IsCheckedIn = True

                messagebox.showinfo(
                    "Check In", f"Welcome, {user.Name}! You have been checked in."
                )

                self.checked_in_users.append(user)
                self.exportDataToCSV(user)

        self.updateCheckedInUsersListbox()
        self.update_duration()
        self.updateUsersStatus()

    def onUserSelect(self, event):
        selected_user_index = self.checked_in_users_listbox.curselection()

        if selected_user_index:
            selected_user = self.checked_in_users[selected_user_index[0]]

            check_out = messagebox.askyesno(
                "Check Out Confirmation",
                f"Do you want to check out {selected_user.Name}?",
            )

            if check_out:
                duration = datetime.datetime.now() - selected_user.CheckInDateTime
                total_duration = selected_user.TotalDuration + duration

                messagebox.showinfo(
                    "Check Out",
                    f"You have been checked out, {selected_user.Name}! Your check-in time was {selected_user.CheckInDateTime.strftime('%H:%M:%S')}. Total duration: {total_duration.days * 24 + total_duration.seconds // 3600}:{(total_duration.seconds % 3600) // 60:02}",
                )

                selected_user.TotalDuration = total_duration
                selected_user.IsCheckedIn = False
                self.checked_in_users.remove(selected_user)
                self.exportDataToCSV(selected_user)

        self.updateCheckedInUsersListbox()
        self.update_duration()
        self.updateUsersStatus()

    def updateEntryField(self):
        self.pin_entry.delete(0, ctk.END)

    def updateCheckedInUsersListbox(self):
        self.checked_in_users_listbox.delete(0, tk.END)

        for user in self.checked_in_users:
            self.checked_in_users_listbox.insert(tk.END, user.Name)

    def update_duration(self):
        if self.checked_in_users:
            current_duration = (
                datetime.datetime.now() -
                self.checked_in_users[0].CheckInDateTime
            )
            # self.duration_label.config(
            #     text=f"Duration: {current_duration.days * 24 + current_duration.seconds // 3600}:{(current_duration.seconds % 3600) // 60:02}"
            # )

        self.root.after(1000, self.update_duration)

    def updateUsersStatus(self):
        total_users = len(self.users)
        checked_in_users = len(self.checked_in_users)
        self.users_status_label.config(
            text=f"✓CHECKED-IN EMPLOYEES: {checked_in_users}⁄{total_users}",
            background="#2b2b2b",
            foreground="white",
            font=ctk.CTkFont(
                size=30,
                weight="bold",
                family="Dank Mono",
                # width=200,
                # anchor="center",
            ),
        )
        self.updateEntryField()

    def exportDataToCSV(self, user):
        csvFilePath = "attendance.csv"
        data = f"{user.CheckInDateTime.date()},{user.Name},{user.Pin},{user.CheckInDateTime.strftime('%H:%M:%S')},{user.TotalDuration.days * 24 + user.TotalDuration.seconds // 3600}:{(user.TotalDuration.seconds % 3600) // 60:02}"

        fileExists = os.path.exists(csvFilePath)

        with open(csvFilePath, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not fileExists:
                writer.writerow(
                    ["Date", "Name", "Pin", "CheckInTime", "TotalDuration"])
            writer.writerow(data.split(","))


if __name__ == "__main__":
    AttendanceManagementSystem()
