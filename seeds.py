import datetime

def create_default_tutorial(con):
    cur = con.cursor()
    tutorial = {
                "title": "Creating a react App",
                "description": "How to create a react app",
                "approximatedTime": "",
                "address": "",
                "likes": 0,
                "updatedAt": None,
                "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    tutorial_steps = [{'title': 'Set Up Your Environment', 'content': """
                               - Make sure you have Node.js installed on your system. You can download and install it from the official Node.js website.

- Open your terminal (or command prompt) and navigate to the directory where you want to create your project.
"""}, {'title': 'Create a React Project', 'content': """
       - To create a new React project, you can use ```create-react-app```, which is an official tool for quickly starting React projects. Run the following command in your terminal:

```npx create-react-app my-project```

This will create a new folder named my-project with the initial structure of a React project.
       
- Navigate to the project directory:
```cd my-project```

"""}, {'title': 'Run Your Project', 'content': """
       - Run your React project:

```npm start```
This will start the development server and open your React application in your default browser. Any changes to the files will be automatically reflected in the browser.
"""}]
    tool_tags = [{'name': "React"}]

    # Insert tutorial into the database
    cur.execute("INSERT INTO tutorial (title, description, approximatedTime, address, likes, updatedAt, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (tutorial["title"], tutorial["description"], tutorial["approximatedTime"], tutorial["address"], tutorial["likes"], tutorial["updatedAt"], tutorial["createdAt"]))
    tutorial_id = cur.lastrowid

    # Insert tutorial steps into the database
    for step in tutorial_steps:
            cur.execute("INSERT INTO tutorial_step (title, content, tutorial_id) VALUES (?, ?, ?)",
                        (step["title"], step["content"], tutorial_id))

    # Insert tool tags into the database
    for tag in tool_tags:
        cur.execute("INSERT INTO tool_tag (name, tutorial_id, icon) VALUES (?, ?, ?)",
                            (tag["name"], tutorial_id, ""))
                
    tutorial = {
                "title": "What is Web3",
                "description": "Show topics of web3",
                "approximatedTime": "",
                "address": "",
                "likes": 0,
                "updatedAt": None,
                "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    tutorial_steps = [{'title': 'Blockchain', 'content': """

- Decentralized record of transactions.
- Data immutability.
- Security through cryptography.
- Examples: Bitcoin, Ethereum.
- 
![Blockchain](https://vivomoney-blog.telefonicabigdata.com/wp-content/uploads/2022/07/21-Artigo-Longo-O-que-e-blockchain-1.webp)
"""}, {'title': 'Smart Contracts', 'content': """

- Self-executing protocols that define contractual conditions.
- Automation of processes without intermediaries.
- Executed on the blockchain.

![Smart Contracts](https://t.jus.com.br/R8IHJsRjfPm43eMrnGYfGsHKQhM=/704x400/smart/assets.jus.com.br/system/file/913/8a0a9c174e12be6bddd524509c8ac5e6.png)
"""}, {'title': 'DApps', 'content': """

- Applications that run on the blockchain.
- Not controlled by a single centralized entity.
- Use smart contracts for business logic.

![DApps](https://hermes.dio.me/articles/cover/1ff1dbc2-7330-4375-90e0-ded734a63435.jpg)
"""}]
    tool_tags = []

    # Insert tutorial into the database
    cur.execute("INSERT INTO tutorial (title, description, approximatedTime, address, likes, updatedAt, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (tutorial["title"], tutorial["description"], tutorial["approximatedTime"], tutorial["address"], tutorial["likes"], tutorial["updatedAt"], tutorial["createdAt"]))
    tutorial_id = cur.lastrowid

    # Insert tutorial steps into the database
    for step in tutorial_steps:
            cur.execute("INSERT INTO tutorial_step (title, content, tutorial_id) VALUES (?, ?, ?)",
                        (step["title"], step["content"], tutorial_id))

    # Insert tool tags into the database
    for tag in tool_tags:
        cur.execute("INSERT INTO tool_tag (name, tutorial_id, icon) VALUES (?, ?, ?)",
                            (tag["name"], tutorial_id, ""))