# Tutorial: Creating Tutorials for Cartesi Projects

Welcome to the Tutorial: Creating Tutorials for Cartesi Projects! In this tutorial, we will walk you through the process of creating comprehensive tutorials for projects developed on the Cartesi platform. By following this guide, you'll learn how to effectively document your Cartesi project, allowing users to understand its functionality, interact with its components, and replicate your work seamlessly.

---

## General Idea

This tutorial aims to demonstrate the methodology for documenting Cartesi projects effectively. It provides a structured approach to explaining project functionalities, system architecture, and deployment instructions. By following this template, developers can create informative and user-friendly documentation for their Cartesi projects.

---

## Components Interaction

Initially, you'll encounter the Home screen, offering options to filter tutorials either by created tags or through a search function.
<br><br>
<img src="src/assets/images/Home.png" alt="drawing" width="800" heigth="800"/>
<br><br>
Subsequently, you can navigate into tutorials by clicking on the cards with the 'start' button.
<br><br>
<img src="src/assets/images/See_Tutorial.png" alt="drawing" width="800" heigth="800"/>
<br><br>
Additionally, you have the option to contribute your own tutorial by accessing the "Add tutorial" button in the navigation bar. So, you will be redirected to the tutorial creation page, which is divided into two parts, as shown in the images below.
<br><br>
Step 1:
<br><br>
<img src="src/assets/images/Add_tutorial_1.png" alt="drawing" width="800" heigth="800"/>
<br><br>
Step 2:
<br><br>
<img src="src/assets/images/Add_tutorial_2.png" alt="drawing" width="800"/>

---

### Prerequisites

- Node.js installed (preferably the latest stable version)
- Git installed on your machine
- Docker installed on your machine
- Python3 installed on your machine
- Sunodo installed on your machine

---

### Installation

Clone the projects repository:

git clone [cartesi-front](https://github.com/leocoreixas/cartesi-labs)
git clone [cartesi-api](https://github.com/jsimonassi/cartesi-labs)

---

### Setting up the Frontend

1. Navigate to the directory:

   `cd cartesi-labs`

2. Install the project dependencies:

   `npm install`

3. Run the frontend:

   `npm start`

---

### Setting up the Backend

1. Initiate the container with sunodo framework:

   `sunodo build` and `sunodo run --no-backend`

2. Navigate to the directory:

   `cd cartesi-labs`

3. Run the backend:

This DApp's back-end is written in Python, so to run it in your machine you need to have python3 installed.

In order to start the back-end, run the following commands in a dedicated terminal:

    cd dapp.py
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    ROLLUP_HTTP_SERVER_URL="http://localhost:8080/host-runner" python3 dapp.py

### Testing the Solution

1. Open your browser and navigate to the following URL:

   `http://localhost:3000/`

2. Interact with the project's functionalities and test its features.
3. Verify that the project is running correctly and that all components are functioning as expected.
4. If you encounter any issues, refer to the project's documentation or seek assistance from the development team.

## Conclusion

In this tutorial, we have covered the process of creating tutorials for Cartesi projects. By following the outlined steps, developers can effectively document their projects, enabling users to understand, interact with, and replicate their work. This structured approach to documentation ensures that project functionalities, system architecture, and deployment instructions are clearly explained, facilitating a seamless user experience. We hope this tutorial has been helpful in guiding you through the process of creating comprehensive tutorials for Cartesi projects. If you have any questions or require further assistance, please feel free to reach out to the Cartesi team or community for support. Thank you for your interest in Cartesi, and we look forward to seeing the tutorials you create for your projects!

## Future Work

As we continue to evolve and improve our tutorial creation platform, we envision several exciting features and enhancements to enrich the user experience and foster community engagement. Here are some ideas for future work:

### 1. Enhanced User Interaction
   - **Like Feature**: Implement a feature allowing users to like tutorials. This functionality not only provides positive feedback to contributors but also helps the community discover high-quality tutorials more easily.

### 2. Advanced Tutorial Creation Tools
   - **Interactive Elements**: Introduce interactive elements within tutorials, such as quizzes or exercises, to make the learning process more engaging and effective.


These future work and enhancements aim to make our tutorial creation platform more dynamic, inclusive, and user-centric. By continuously innovating and incorporating feedback from the community, we aspire to create a vibrant ecosystem where knowledge sharing thrives and learners can excel. Let's build the future of tutorial creation together!



## References

---

- [Cartesi Website](https://cartesi.io/)
- [Node.js Documentation](https://nodejs.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/3/)

👥 Team Members

---

- [Leonardo Coreixas](https://github.com/leocoreixas)
- [Joao Simonassi](https://github.com/jsimonassi)
- [Gustavo Luppi](https://github.com/gustavoluppi)
- [Bernardo Cerqueira](https://github.com/bernardocerq)
- [Marcos Mendonça](https://github.com/marcoscezar1)

---

© 2024 Cartesi Labs. All Rights Reserved.
