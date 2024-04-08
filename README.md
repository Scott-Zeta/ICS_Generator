# ICS_Generator Phase 1

## Business Case

### User Story

Recently, I found some organizations and companies sent me event notifications not in a standard RSVP or attached ICS file, but in plain text or images. This makes it hard to manage events, as I have to manually input the event into my Calendar, which can lead to troubles and mistakes. Additionally, a club that I joined mentioned they are facing problems managing and notifying events to members.

So, this project aims to build a non-technical, user-friendly app, helping users manage events more easily with ICS files.

### Target Clients

1. General public who use Calendar apps but often receive and are troubled by "low-compatibility" event notifications, where event information is delivered in natural language text/image inside the email/messages. The app also aims to provide a quicker way to process event information from visual media such as a name card with handwritten booking information, posters, or projecting slides.
2. Event hosts/managers who are seeking a more professional solution to notify event participants using ICS files.

### Main Benefits

1. For the General Public: An ICS file can be read by major Calendar apps, such as Google Calendar, Outlook, and Apple Calendar. Moreover, an ICS file attached in an email can be detected by related email services; for example, Gmail will automatically generate a prompt under the title in the email to add the event to Google Calendar if an ICS file is attached. This will not only accelerate the user experience but also reduce the possibility of mistakes when users manually input the event information. These apps also provide synchronization between different devices, setting up alarms, and checking event conflicts, helping users better manage their events.
2. For Event Hosts/Managers: Delivering events via an ICS file can increase the professionalism of their organization/company, as well as increase the possibility for users to participate in the event. It can also decrease the chance of participants having the wrong start time by memory or manual input.

### Target

At the current stage, I hope the app has the ability to:

1. Take the user's input in plain natural language text or image.
2. Refine the information in natural language into a standard data structure such as a Dictionary or JSON, with key event information included.
3. If a user uploads an image, it should have the ability to identify the text within the image and process the text as natural language, forwarding it to Step Two.
4. Based on the data in the data structure, create an ICS file and deliver it to the client-side for the user to download.

## Architecture

Considering the app will process plenty of private information, although this stage only aims at implementing core function and not preparing for public usage, privacy issues still need to be considered in advance. Therefore, it is expected that any user-related information (Uploaded Text, Image, ICS file for downloading) can stay on the server as short as possible, meanwhile reducing the usage of storage service. A Stateless Architecture is ideal and should be the guideline for the entire development.

Everything in this section can be changed depending on the situation during development.

### Front-End

A simple web browser app is sufficient for this stage.

#### Function

- Have a user interface to handle text input.
- Have a drag-and-drop interface for image uploading, with limitations on image size and number.
- Have client-side input validation.
- Have an interface for users to download the generated ICS file, or directly initiate the download when complete.
- Be able to send HTTP requests with data to the Back-end Server.
- Be able to receive the correct file sent from the Back-end Server.
- (TBD) client-side image compressor.

#### Tools might be used

- Basic Framework: Next.js
- A UI library for drag-and-drop image uploading: TBD
- Input validation: Zod or TBD

### Back-End

The core function of the app, it should handle the incoming data and generate the ICS file based on the refined data structure. And deliver the file to the right client-side.

#### Function

- Have server-side input validation.
- Have the service parse the natural language to refine key information into a standard data structure.
- Have the service identify text on the image, parsing it to natural language text, preferably as a native service.
- Have the ability to generate an ICS file from key information.
- Have the ability to deliver the ICS file to the correct client, or indicate if key information is missing.

#### Tools might be used

- Basic Framework: Django
- Input validation: TBD
- Optical Character Recognition (OCR): Tesseract or TBD
- Natural Language Processing (NLP): OpenAI, Azure AI, or TBD
- ICS file generating: Ics.py

## Challenges

1. Data transmission between client/server ends, especially under Stateless Architecture.
2. Configuring OCR and NLP.
