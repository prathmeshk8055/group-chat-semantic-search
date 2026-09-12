import json
import random
from datetime import datetime, timedelta
from pathlib import Path


# -----------------------------
# 1. Basic configuration
# -----------------------------

SEED = 42
random.seed(SEED)

NUM_BACKGROUND_MESSAGES = 4000

PARTICIPANTS = [
    "Aman",
    "Priya",
    "Rahul",
    "Sneha",
    "Vikram",
    "Neha",
    "Arjun",
    "Karan",
]

START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 6, 30)


# -----------------------------
# 2. Message templates
# -----------------------------

NORMAL_MESSAGES = [
    "bhai kal college aa raha hai?",
    "haan probably aaunga",
    "kya scene hai?",
    "lecture kitne baje hai?",
    "10 baje wala na?",
    "bro notes bhej dena",
    "haan bhejta hu",
    "ruk zara",
    "okay",
    "done",
    "cool",
    "same here",
    "mai bhi",
    "lol 😂",
    "bhai kya kar raha hai",
    "kuch nahi yaar",
    "assignment complete hua?",
    "abhi toh aadha hua hai",
    "deadline kab hai?",
    "kal tak submit karna hai",
    "💀",
    "bhai ye question samajh nahi aa raha",
    "same problem",
    "prof ne kuch bola kya?",
    "nahi suna maine",
    "attendance ka kya scene hai?",
    "hopefully manage ho jayega",
    "aaj bahut thak gaya",
    "chai peene chale?",
    "5 min mein aata hu",
    "wait",
    "haan bhai",
    "sahi hai",
    "mast",
    "kya bakchodi chal rahi hai 😂",
    "send the photo",
    "network kharab hai",
    "message late aa raha hai",
    "kal milte hain",
    "good night guys",
    "gn",
    "morning everyone",
    "good morning",
]


HINGLISH_MESSAGES = [
    "bhai ye wala idea thoda better lag raha hai",
    "mujhe lagta hai ye kaam kar jayega",
    "abhi decide mat karo",
    "pehle sabki opinion lete hain",
    "yaar budget thoda tight hai",
    "itna expensive toh nahi hona chahiye",
    "mere hisaab se second option sahi hai",
    "chalo dekhte hain",
    "haan mujhe bhi same lag raha",
    "kal discuss kar lenge",
    "aaj mood nahi hai 😂",
    "bhai seriously?",
    "ye toh unexpected tha",
    "thoda wait kar",
    "main check karke batata hu",
    "koi issue nahi hai",
    "sab manage ho jayega",
    "bro ye link open nahi ho raha",
    "ek baar dobara bhej",
    "haan ab chal raha hai",
    "kya final hua?",
    "abhi kuch final nahi hua",
    "sab log online ho jao",
    "meeting start karte hain",
    "bhai jaldi reply kar",
]


TYPOS = [
    "kal milte h",
    "kya scen hai",
    "haan bhai krte hain",
    "mai dekh lunga",
    "ye sahi h",
    "thik h",
    "ruk ek min",
    "bhot acha",
    "mujhe nhi pata",
    "kuch pta chala?",
]


FORWARDED_MESSAGES = [
    "Forwarded: Important notice regarding tomorrow's schedule",
    "Forwarded: Please check the updated timetable",
    "Forwarded: Placement cell announcement",
    "Forwarded: Event registration closes tonight",
    "Forwarded: College circular",
    "Forwarded: Internship opportunity for students",
]


MEDIA_MESSAGES = [
    "[Photo omitted]",
    "[Video omitted]",
    "[Document omitted]",
    "[Voice message omitted]",
    "[Sticker omitted]",
]


ONE_WORD_REPLIES = [
    "haan",
    "nahi",
    "done",
    "okay",
    "sure",
    "yep",
    "nope",
    "exactly",
    "same",
    "lol",
    "confirmed",
    "pending",
]


# -----------------------------
# 3. Generate a random timestamp
# -----------------------------

def random_timestamp():
    total_seconds = int((END_DATE - START_DATE).total_seconds())
    random_seconds = random.randint(0, total_seconds)

    return START_DATE + timedelta(seconds=random_seconds)


# -----------------------------
# 4. Generate one random message
# -----------------------------

def generate_random_text():
    choice = random.random()

    if choice < 0.50:
        return random.choice(NORMAL_MESSAGES)

    elif choice < 0.75:
        return random.choice(HINGLISH_MESSAGES)

    elif choice < 0.85:
        return random.choice(TYPOS)

    elif choice < 0.92:
        return random.choice(ONE_WORD_REPLIES)

    elif choice < 0.97:
        return random.choice(FORWARDED_MESSAGES)

    else:
        return random.choice(MEDIA_MESSAGES)


# -----------------------------
# 5. Create a message object
# -----------------------------

def create_message(message_id, timestamp, sender, text, thread=None):
    return {
        "id": message_id,
        "timestamp": timestamp.isoformat(),
        "sender": sender,
        "text": text,
        "thread": thread,
    }


# -----------------------------
# 6. Create the three important
#    decision threads
# -----------------------------

def create_decision_threads(start_id):
    messages = []
    decision_ids = {}

    current_id = start_id

    # =====================================
    # THREAD 1: TRIP DECISION
    # =====================================

    thread_name = "trip_decision"

    trip_conversation = [
        ("Rahul", "Guys summer trip ka kya scene hai?"),
        ("Aman", "Goa chale kya?"),
        ("Priya", "Goa thoda expensive padega."),
        ("Sneha", "Manali bhi option hai."),
        ("Karan", "Manali sounds good actually."),
        ("Vikram", "Travel ka cost kitna aayega?"),
        ("Neha", "Train se jayenge toh manageable hoga."),
        ("Arjun", "Mujhe dates ka issue ho sakta hai."),
        ("Rahul", "June second week kaisa hai?"),
        ("Priya", "14th ke around I should be free."),
        ("Aman", "Goa mein weather bhi weird ho sakta hai."),
        ("Sneha", "Manali mein better rahega."),
        ("Karan", "Hotel options check kiye kya?"),
        ("Vikram", "I found one near Mall Road."),
        ("Neha", "Price?"),
        ("Vikram", "Around 1800 per person."),
        ("Priya", "That's actually okay."),
        ("Arjun", "Food ka kya karenge?"),
        ("Rahul", "Breakfast included hai apparently."),
        ("Aman", "Then not bad."),
        ("Sneha", "Bus ya train?"),
        ("Karan", "Train better imo."),
        ("Neha", "Tickets jaldi book karne padenge."),
        ("Rahul", "Haan warna prices badh jayenge."),
        ("Priya", "Everyone comfortable with Manali?"),
        ("Aman", "Mereko toh chalega."),
        ("Arjun", "Same."),
        ("Vikram", "Works for me."),
        ("Sneha", "I'm in."),
        ("Karan", "Let's do it."),
        # Decision message deliberately phrased in Hinglish
        ("Rahul", "Chalo Manali fix hai. Hotel option 2 book kar dete hain."),
        ("Priya", "Done, main apna share transfer kar dungi."),
        ("Aman", "Perfect."),
        ("Neha", "Finally 😂"),
        ("Arjun", "Tickets bhi dekh leta hu."),
        ("Vikram", "Sorted then."),
        ("Sneha", "Lessgooo."),
        ("Karan", "Done bhai."),
        ("Rahul", "I'll make the booking tonight."),
        ("Priya", "Send confirmation here."),
    ]

    base_time = datetime(2026, 5, 18, 18, 0)

    for index, (sender, text) in enumerate(trip_conversation):
        timestamp = base_time + timedelta(minutes=index * 3)

        msg_id = f"msg_{current_id}"
        messages.append(
            create_message(
                msg_id,
                timestamp,
                sender,
                text,
                thread_name,
            )
        )

        if "Manali fix" in text:
            decision_ids["trip"] = msg_id

        current_id += 1

    # =====================================
    # THREAD 2: PROJECT DECISION
    # =====================================

    thread_name = "project_decision"

    project_conversation = [
        ("Aman", "Project ke liye technology decide karni hai."),
        ("Priya", "Java use kar sakte hain."),
        ("Rahul", "Python would be faster for us."),
        ("Sneha", "But backend stability bhi chahiye."),
        ("Vikram", "Database ka kya plan hai?"),
        ("Neha", "SQLite initially enough hai."),
        ("Arjun", "Python mein ML integration easy rahega."),
        ("Karan", "True."),
        ("Priya", "But everyone knows Java better."),
        ("Rahul", "We can learn the required part."),
        ("Aman", "Deadline bhi close hai."),
        ("Sneha", "Then development speed matters."),
        ("Vikram", "Python ka prototype bana sakte hain."),
        ("Neha", "Frontend simple rakhenge."),
        ("Arjun", "Streamlit bhi option hai."),
        ("Karan", "That would save time."),
        ("Priya", "Hmm makes sense."),
        ("Rahul", "Let's compare both quickly."),
        ("Aman", "Java mein boilerplate zyada hoga."),
        ("Sneha", "Python mein implementation straightforward hai."),
        ("Vikram", "Testing bhi easy rahegi."),
        ("Neha", "Deployment ka issue toh nahi?"),
        ("Arjun", "Basic deployment manageable hai."),
        ("Karan", "I vote Python."),
        ("Priya", "Okay I'm convinced."),
        ("Rahul", "Everyone agreed then?"),
        ("Aman", "Yes."),
        ("Sneha", "Yes."),
        ("Vikram", "Yep."),
        ("Neha", "Confirmed."),
        # Decision message
        ("Priya", "Okay final hai, Python wala approach lenge."),
        ("Arjun", "Great, I'll start the model part."),
        ("Rahul", "I'll handle the data."),
        ("Aman", "I'll work on UI."),
        ("Karan", "I'll setup the repository."),
        ("Vikram", "Done."),
        ("Sneha", "Let's finish this."),
    ]

    base_time = datetime(2026, 4, 7, 20, 0)

    for index, (sender, text) in enumerate(project_conversation):
        timestamp = base_time + timedelta(minutes=index * 4)

        msg_id = f"msg_{current_id}"
        messages.append(
            create_message(
                msg_id,
                timestamp,
                sender,
                text,
                thread_name,
            )
        )

        if "final hai" in text:
            decision_ids["project"] = msg_id

        current_id += 1

    # =====================================
    # THREAD 3: EVENT DECISION
    # =====================================

    thread_name = "event_decision"

    event_conversation = [
        ("Neha", "College farewell ka venue decide hua?"),
        ("Priya", "Hotel expensive lag raha hai."),
        ("Rahul", "Community hall check kiya."),
        ("Aman", "Capacity enough hai?"),
        ("Rahul", "Around 150 people."),
        ("Sneha", "That's enough."),
        ("Vikram", "Parking ka scene?"),
        ("Rahul", "Parking available hai."),
        ("Karan", "Food vendor kaun hai?"),
        ("Neha", "Three options mile hain."),
        ("Arjun", "Budget per person kitna?"),
        ("Priya", "Around 500 if we choose option 2."),
        ("Aman", "That sounds reasonable."),
        ("Sneha", "Timing kya rakhen?"),
        ("Vikram", "Saturday evening."),
        ("Karan", "6 to 10 maybe."),
        ("Neha", "Everyone okay with Saturday?"),
        ("Arjun", "Works."),
        ("Priya", "Yes."),
        ("Rahul", "I'll call the venue."),
        ("Aman", "Ask about decoration too."),
        ("Rahul", "They have a basic package."),
        ("Sneha", "Nice."),
        ("Vikram", "Advance kitna hai?"),
        ("Rahul", "20 percent."),
        ("Karan", "Manageable."),
        ("Neha", "Then what's stopping us?"),
        ("Priya", "Nothing from my side."),
        ("Arjun", "Let's finalize."),
        ("Aman", "Agreed."),
        ("Sneha", "Go ahead."),
        # Decision message
        ("Rahul", "Booked. Saturday evening, community hall. Basic decoration included."),
        ("Priya", "Perfect."),
        ("Neha", "Finally sorted."),
        ("Karan", "I'll handle the food."),
        ("Vikram", "I'll coordinate transport."),
        ("Arjun", "Done."),
        ("Aman", "Nice work guys."),
    ]

    base_time = datetime(2026, 3, 21, 17, 30)

    for index, (sender, text) in enumerate(event_conversation):
        timestamp = base_time + timedelta(minutes=index * 4)

        msg_id = f"msg_{current_id}"
        messages.append(
            create_message(
                msg_id,
                timestamp,
                sender,
                text,
                thread_name,
            )
        )

        if "Booked." in text:
            decision_ids["event"] = msg_id

        current_id += 1

    return messages, decision_ids


# -----------------------------
# 7. Main generation function
# -----------------------------

def main():
    messages = []

    # Generate background chat
    for i in range(NUM_BACKGROUND_MESSAGES):
        timestamp = random_timestamp()
        sender = random.choice(PARTICIPANTS)
        text = generate_random_text()

        messages.append(
            create_message(
                f"msg_{i + 1}",
                timestamp,
                sender,
                text,
            )
        )

    # Add important threads
    thread_messages, decision_ids = create_decision_threads(
        NUM_BACKGROUND_MESSAGES + 1
    )

    messages.extend(thread_messages)

    # Sort chronologically
    messages.sort(key=lambda x: x["timestamp"])

    # Output paths
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"

    data_dir.mkdir(exist_ok=True)

    messages_path = data_dir / "messages.json"
    ground_truth_path = data_dir / "decision_messages.json"

    # Save messages
    with open(messages_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    # Save important message IDs for our evaluation later
    with open(ground_truth_path, "w", encoding="utf-8") as f:
        json.dump(decision_ids, f, indent=2)

    print("=" * 50)
    print("Synthetic group chat generated successfully!")
    print("=" * 50)
    print(f"Total messages: {len(messages)}")
    print(f"Participants: {len(PARTICIPANTS)}")
    print(f"Date range: {START_DATE.date()} → {END_DATE.date()}")
    print()
    print("Decision messages:")
    for name, message_id in decision_ids.items():
        print(f"  {name}: {message_id}")

    print()
    print(f"Saved to: {messages_path}")
    print(f"Saved to: {ground_truth_path}")


if __name__ == "__main__":
    main()