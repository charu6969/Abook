import sqlite3

conn = sqlite3.connect("data/exams.db")

conn.execute("""
INSERT INTO exams (
    exam_code,
    subject_code,
    subject_name,
    university_name,
    question_text
) VALUES (
    '123456',
    'CS101',
    'Algorithms',
    'VTU',
    'Explain quicksort'
)
""")

conn.commit()
conn.close()

print("✅ Test exam inserted")
