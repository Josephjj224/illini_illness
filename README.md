# Illini Illness


**Team016-SQLnewbs:**  
Emma Chen, Yi-Chia Chang, Joseph Jeong, Tianyang Liao, Yiyang Xu

---

## Summary
Our web app, **Illini Illness**, allows users to track and manage their chronic illnesses or other long-term health conditions and provides that data directly to their doctor. Patients can create accounts to track symptoms, treatments, and record additional factors influencing their health (e.g., sleep schedule, weather, mood). Doctors and healthcare professionals can also create accounts to view their registered patients' symptoms and treatments. The app visualizes how the severity of symptoms changes over time and in response to environmental variables, and it notifies patients when it's time to take their medications.

---

## Description
Managing long-term health conditions can be challenging. Illini Illness offers an accessible way for users to create, view, and analyze their health data. Users can track how conditions affect them, monitor the effectiveness of medications and dosages, and observe symptom changes in relation to environmental factors. This data can be used as a personal record or shared with doctors as a detailed medical history.

Doctors can sign up and view their patients' data in real time. Additionally, users (patients or doctors) can set a treatment schedule and receive medication reminders through SMS, email, or push notifications.

---

## Usefulness
**Illini Illness** is designed for individuals with chronic conditions who want to monitor their health trends over time, and for doctors or healthcare providers managing multiple patients' health data.

Unlike other health apps, such as Flaredown, Illini Illness tracks a broader range of health-related events (e.g., sleep quality) in a dedicated section rather than grouping them in one category. Additionally, Illini Illness supports data sharing with healthcare providers.

Both Illini Illness and Flaredown are free, which is beneficial for users with ongoing medical expenses and those with limited financial resources.

---

## Realness
Our data source is the chronic illness dataset from Kaggle, which includes data on 42,283 unique patients and over 1 million data points. The dataset contains columns for user ID, age, sex, country, symptoms, symptom severity, treatments, HBI index, food, weather, and additional tags for other events.

---

## Functionality

### Main Functionality
Illini Illness uses the TA-recommended chronic illness dataset from Kaggle, which provides data on individuals with chronic illnesses, their symptoms, and treatments. Our app will store patient information (e.g., user ID, age, sex, country) and record details about their health conditions, symptoms, symptom severity, treatments, dosages, HBI index, food intake, weather, and other relevant events. Patients can self-report their daily health status and view their health history in the app.

Doctors and healthcare professionals can view and manage their patients' data. Each patient is assigned to a doctor, or new patients can select a healthcare provider upon signing up. The app also tracks treatment schedules and adherence to treatment plans.

### Reminders for Treatments
To support timely treatment adherence, Illini Illness includes a reminder system with options for SMS, email, and web notifications. This reminder system integrates natural language processing (NLP) to create a friendly, interactive chatbot that engages users about their treatment schedules, ensuring they never miss a medication.

By integrating this reminder system into our web app, we aim to provide a user-centric healthcare solution that fosters continuous support, ultimately leading to better health outcomes.

### Tracking Additional Health Conditions
In addition to core features, we plan to incorporate tools for tracking other health conditions such as acne, sleep patterns, menstrual cycles, and workouts. This will allow users to monitor diverse health aspects, enabling a holistic approach to health tracking.

---

## Key Features

- **User Account Management**: Patients and doctors can create accounts to access the app's features.
- **Health Data Tracking**: Patients can log symptoms, treatments, and various health factors.
- **Data Visualization**: Graphs and charts help users and doctors visualize symptom changes over time.
- **Medication Reminders**: Patients receive reminders through SMS, email, or web notifications.
- **Doctor-Patient Interaction**: Doctors can view their patients' health records and monitor their condition in real-time.

---

## Data Source
**Dataset**: Chronic Illness Dataset from Kaggle  
The dataset includes detailed health records for over 42,000 unique patients, allowing us to create realistic and comprehensive health tracking features.

---

## Technologies Used

- **Frontend**: React, Chakra UI, Axios
- **Backend**: Node.js, Express
- **Database**: MongoDB
- **Notifications**: Twilio (for SMS), Nodemailer (for email)
- **Other**: Natural Language Processing (NLP) for chatbot reminders

---
## Home
![Home Page](https://github.com/user-attachments/assets/177577c9-e445-4984-adb4-ad9c709906f1)
<p align="center">Home page interface displaying the main features and navigation options.</p>

---

## Registration & Login Page
![Registration Page](https://github.com/user-attachments/assets/dc0ff227-77d7-486f-adbf-97498b54d84e)
![Screen Shot 2024-11-02 at 2 36 03 AM](https://github.com/user-attachments/assets/b5c9260f-9d9d-40ac-b995-e7c2ac5bae8b)
![Screen Shot 2024-11-02 at 2 36 28 AM](https://github.com/user-attachments/assets/43728b90-6016-41a9-8006-c5ea1bc607bb)

<p align="center"> User registration and login page where new users can sign up for an account or log into their existing account . </p>

---

## Dashboard
![Dashboard](https://github.com/user-attachments/assets/c947244e-7e57-4b8f-a10e-ed8c0ec4b412)
<p align="center">Dashboard displaying user data, statistics, and analytics for tracking health metrics.</p>
