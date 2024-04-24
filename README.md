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
- Transmission Protocal: Django REST Framework (HTTP), Django Channels (WebSocket)
- Input validation: Django Serializer, Pillow(for image)
- Asynchronous Task: Celery or TBD
- Optical Character Recognition (OCR): Tesseract, Azure Computer Vision for handwriting
- Natural Language Processing (NLP): OpenAI, Azure AI, or TBD
- ICS file generating: Ics.py
- File temporary storage: Redis

#### Architecture Design and Workflow

1. Server recieve HTTP POST Request from client-side, start do validation
2. If data pass the validation, start do Async processing, Return 201 to client-side. If not, Return 400, session terminated.

##### Async Porcessing

    1. Only data pass the validation can get in, processing start. WebSocket cosumer will sent progress info via WebSocket connection.
    2. Image is under OCR processing if applied. Output plain text that in image.
    3. Text from last step combined with text input, sent to Big Language Model for NLP. Output refined information in standard data structure (JSON/Python Dict)
    4. Ics.py generate the ICS file based on refined infomation, ready for delivery.
    5. Progress info and file will be dump in reasonable time if Websocket connection delayed not established, leave the system clean.

3. Once client-side get 201 response, establishing WebSocekt connection to server-side.
4. Associate the Websocket connection and initial POST Request with a session ID. There are two options:
   - If allow anonymous access or solely focusing on core functions, generate a session id and sent it back in POST initial response. Client-side will establish connection with the ID, and validate by server-side.
   - If authentication system required and implemented, use user session ID directly.
5. File deliver by Websocket connection. Once delivery complete, connection terminated.

## Challenges

1. Have a more clear design of architecture for info transimisson, but still many issue may need clarify and overcome during implementation.
2. Configuring OCR and NLP.
3. Have a brief idea of testing, but not sure can do it reliably for every components.

# Logs

## Day 1 08/04/2024

### Finshed

- Desgin and Plan

### Doing

- Django server initial and config

### Read and Research

- [Basic strcuture and workflow of Django app](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)

- [DB and ORM config in Django](https://docs.djangoproject.com/en/5.0/intro/tutorial02/)

## Day 2 09/04/2024

### Finshed

- Implement a crud dash board on index by applying concept acquired in Day 1.

### Doing

- Django server config

### Read and Research

- [View Page and Template, url setting](https://docs.djangoproject.com/en/5.0/intro/tutorial03/)

- [Form and Basic request handle, F functions for race condition in DB operation](https://docs.djangoproject.com/en/5.0/intro/tutorial04/)

## Day 3 15/04/2024

### Finshed

- Implement a basic Rest API structure

### Doing

- Server Side input validation

### Read and Research

- [Generic View](https://docs.djangoproject.com/en/5.0/intro/tutorial04/)

- [Rest API for Django](https://radixweb.com/blog/create-rest-api-using-django-rest-framework)

- [Input Paser, validation and Serializers](https://www.django-rest-framework.org/)

## Day 4 18/04/2024

### Finshed

- Serializaer for Server side input validation

- TestCase for Serializaer

### Doing

- Testing Upload API Entry Point request and response, combine with Serializaer

### Read and Research

- [Django Testing](https://docs.djangoproject.com/en/5.0/topics/testing/overview/)

- [Form fields and SimpleUploadedFile](https://docs.djangoproject.com/en/5.0/ref/forms/fields/)

## Day 5 22/04/2024

### Finshed

- TestCase for API Upload entry point

- Testing for entire server input validation

- Detailed Architecture Design

### Doing

There is two path can do seperately

- For API Architecture, look deeper into WebSocket, Celery and Asynchronous Tasks, Redis
- For function components, Optical Characters Recognition(OCR), Nature Language Processing(NLP)

### Read and Research

- [Django Channels](https://channels.readthedocs.io/en/stable/index.html)

- [WebSocekt API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

## Day 6 24/04/2024

### Finshed

- OCR studying and tech stack comparison

Tested many option for OCR. Since most open-source OCR libraries don't perform well on handwriting content. Current plan is add a option to pass image to Azure Computer Vision, for handwriting and error case.

### Doing

Implement Native and Cloud base OCR function

### Read and Research

- [OCR Unlocked: A Guide to Tesseract in Python with Pytesseract and OpenCV](https://nanonets.com/blog/ocr-with-tesseract/)

- [How to easily do Handwriting Recognition using Machine Learning](https://nanonets.com/blog/handwritten-character-recognition/)

- [pytesseract 0.3.10](https://pypi.org/project/pytesseract/)

- [Tesseract documentation](https://tesseract-ocr.github.io/)

- [2023 review of tools for Handwritten Text Recognition HTR — OCR for handwriting](https://www.reddit.com/r/computervision/comments/15er2y7/2023_review_of_tools_for_handwritten_text/)

- [EasyOCR](https://www.jaided.ai/easyocr/tutorial/)

- [Azure OCR - Optical Character Recognition](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-ocr)
