import cv2
import time
import random
from tkinter import *
from tkinter import messagebox, simpledialog

# Load face and eye detection models
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

cap = cv2.VideoCapture(0)

closed_eyes_start = None
puzzle_active = False
last_puzzle_time = 0
cooldown_time = 10  # seconds before another puzzle can appear

# Puzzle bank
puzzles = [
    ("What is 7 + 8?", "15"),
    ("What is 6 x 4?", "24"),
    ("What is 20 - 9?", "11"),
    ("What is 9 + 6?", "15"),
    ("What is 12 / 3?", "4")
]

def show_puzzle():
    global puzzle_active, last_puzzle_time
    puzzle_active = True

    question, answer = random.choice(puzzles)

    root = Tk()
    root.withdraw()

    user_answer = simpledialog.askstring("Brain Refresh Puzzle", question)

    if user_answer == answer:
        messagebox.showinfo("Correct!", "Great job! Now continue studying.")
    else:
        messagebox.showinfo("Answer", f"The correct answer was {answer}")

    last_puzzle_time = time.time()
    puzzle_active = False


while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    status = "System Monitoring..."

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) == 0:
            if closed_eyes_start is None:
                closed_eyes_start = time.time()
            elif (time.time() - closed_eyes_start > 3 and
                  not puzzle_active and
                  time.time() - last_puzzle_time > cooldown_time):

                status = "Distracted - Refresh Needed"
                show_puzzle()
        else:
            closed_eyes_start = None
            status = "Focused"

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 2)

    # Title
    cv2.putText(frame,
                "AI-Based Study Focus & Cognitive Refresh System",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2)

    # Developer Name
    cv2.putText(frame,
                "Developed by Mihika Vashistha",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                2)

    # Status Display
    cv2.putText(frame,
                "Status: " + status,
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2)

    cv2.imshow("AI Study Focus Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
