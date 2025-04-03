import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('2020 CNCF Annual Report', 'The Cloud Native Computing Foundation (CNCF) is an open source software foundation that promotes the adoption of cloud native computing.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Kubernetes Certification', 'The Certified Kubernetes Administrator (CKA) program was created by the Cloud Native Computing Foundation (CNCF), in collaboration with The Linux Foundation, to help develop the Kubernetes ecosystem.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Kubernetes and Cloud Native Operations', 'Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Cloud Native DevOps', 'DevOps is a set of practices that combines software development (Dev) and IT operations (Ops).')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Kubernetes and Cloud Native Security', 'Kubernetes provides several security features to ensure that your applications are secure.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('CNCF Cloud Native Interactive Landscape', 'The Cloud Native Interactive Landscape is CNCF recommended path through the cloud native ecosystem.')
            )

connection.commit()
connection.close()

print("Initialized the database.")