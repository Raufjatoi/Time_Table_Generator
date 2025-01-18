#pip install langchain langchain python-dotenv

import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

prompt_template = ChatPromptTemplate.from_template("""
You are a timetable generator. Allocate subjects to available timeslots.

Timeslots: {timeslots}
Subjects: {subjects}

Constraints:
- Each subject must be assigned to one timeslot.
- A timeslot can have only one subject.
- Generate only the timetable, no additional text should be in the information
- Classes are from 8:30am-3:00pm
- One class is of minimum one hour
- 10:30am-11:00am every day except friday is break
- Classes start from 8:30 then go upto 10:30 then there is the break, then classes start from 11:00 and go upto 2:00
- On friday, the ending time is 12:30am no classes after that
- There is no break on fridays classes
- subject's duration in the subjects is the credit hours of that subjects meaning there would be duration classes of that subject no more no less
- if all the credit hours are completed then make the rest free
- there should be no more than 2 classes of the same subject continously. if credit hours are remaining classes should be moved to next day
- be sure of the credit hours and classes per week, classes should not be more or less than credit hours
- the classes should not be same continous like it should have science in the current timeslot if it is already in the previous timeslot

Output a timetable in this format:
Day       | Time       | Subject
""")

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile")

generator = prompt_template | llm

data = {
    "timeslots": [
        {"day": "Monday", "start": "8:30", "end": "9:30"},
        {"day": "Monday", "start": "9:30", "end": "10:30"},
        {"day": "Monday", "start": "11:00", "end": "12:00"},
        {"day": "Monday", "start": "12:00", "end": "1:00"},
        {"day": "Monday", "start": "1:00", "end": "2:00"},

        {"day": "Tuesday", "start": "8:30", "end": "9:30"},
        {"day": "Tuesday", "start": "9:30", "end": "10:30"},
        {"day": "Tuesday", "start": "11:00", "end": "12:00"},
        {"day": "Tuesday", "start": "12:00", "end": "1:00"},
        {"day": "Tuesday", "start": "1:00", "end": "2:00"},

        {"day": "Wednesday", "start": "8:30", "end": "9:30"},
        {"day": "Wednesday", "start": "9:30", "end": "10:30"},
        {"day": "Wednesday", "start": "11:00", "end": "12:00"},
        {"day": "Wednesday", "start": "12:00", "end": "1:00"},
        {"day": "Wednesday", "start": "1:00", "end": "2:00"},

        {"day": "Thursday", "start": "8:30", "end": "9:30"},
        {"day": "Thursday", "start": "9:30", "end": "10:30"},
        {"day": "Thursday", "start": "11:00", "end": "12:00"},
        {"day": "Thursday", "start": "12:00", "end": "1:00"},
        {"day": "Thursday", "start": "1:00", "end": "2:00"},

        {"day": "Friday", "start": "8:30", "end": "9:30"},
        {"day": "Friday", "start": "9:30", "end": "10:30"},
        {"day": "Friday", "start": "10:30", "end": "11:30"},
        {"day": "Friday", "start": "11:30", "end": "12:30"},
    ],
    "subjects": [
        {"name": "DLD", "credit_hours": 3},
        {"name": "DS", "credit_hours": 3},
        {"name": "History", "credit_hours": 3},
        {"name": "Physics", "credit_hours": 3},
        {"name": "Chemistry", "credit_hours": 3},
        {"name": "DLDLAB", "credit_hours": 3},
        {"name": "DSLAB", "credit_hours": 3},
        {"name": "DBSLAB", "credit_hours": 3},
    ]
}



x = generator.invoke(data)

print(x.content)