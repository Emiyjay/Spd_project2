import os, json, csv, smtplib
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

# ================= CONFIG =================
SENDER_EMAIL  = "spdregistration@gmail.com"
APP_PASSWORD  = "awnl locz flxk mfwe"
SENDER_NAME   = "John Emmanuel Sani"
PROGRAM_NAME  = "SPD Project ICT Training Hub"
DATA_FILE     = "students.csv"
USERS_FILE    = "users.json"

# ================= USER SYSTEM =================
def load_users():
    if not os.path.exists(USERS_FILE):
        users = {"admin": "1234"}
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def authenticate(username, password):
    return load_users().get(username) == password

# ================= DATABASE =================
def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name","email","amount","status"])

def read_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return list(csv.DictReader(f))

# ================= EMAIL =================
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"]   = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ================= LOGIN =================
class LoginScreen(BoxLayout):
    def __init__(self, app, **kw):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kw)
        self.app = app

        self.add_widget(Label(text=f"{PROGRAM_NAME}\nLogin", halign="center"))

        self.user = TextInput(hint_text="Username")
        self.pwd  = TextInput(hint_text="Password", password=True)

        btn = Button(text="Login")
        btn.bind(on_press=self.login)

        self.status = Label(text="")

        self.add_widget(self.user)
        self.add_widget(self.pwd)
        self.add_widget(btn)
        self.add_widget(self.status)

    def login(self, instance):
        if authenticate(self.user.text, self.pwd.text):
            self.app.load_main()
        else:
            self.status.text = "Invalid login"

# ================= MAIN UI =================
class MainUI(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', **kw)

        tabs = TabbedPanel()

        # Dashboard
        dash = TabbedPanelItem(text="Dashboard")
        dash.content = Label(text=f"Welcome to {PROGRAM_NAME}\nSender: {SENDER_NAME}")
        tabs.add_widget(dash)

        # Students
        students = TabbedPanelItem(text="Students")
        students.content = Label(text=self.get_students())
        tabs.add_widget(students)

        # Send
        send = TabbedPanelItem(text="Send")
        btn = Button(text="Send Emails")
        btn.bind(on_press=self.send_all)
        send.content = btn
        tabs.add_widget(send)

        self.add_widget(tabs)

    def get_students(self):
        data = read_students()
        return "\n".join([s["name"] for s in data]) or "No students"

    def send_all(self, instance):
        def task():
            for s in read_students():
                subject = f"{PROGRAM_NAME} — Payment Confirmation"
                body    = (
                    f"Dear {s['name']},\n\n"
                    f"Thank you for your payment to {PROGRAM_NAME}.\n\n"
                    f"Regards,\n{SENDER_NAME}"
                )
                send_email(s["email"], subject, body)
        Thread(target=task).start()

# ================= ROOT =================
class AppRoot(App):
    def build(self):
        init_db()
        self.root_layout = BoxLayout()
        self.show_login()
        return self.root_layout

    def show_login(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(LoginScreen(self))

    def load_main(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(MainUI())

if __name__ == "__main__":
    AppRoot().run()
