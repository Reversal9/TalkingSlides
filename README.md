# TalkingSlides

![Alt text](frontend/public/logo.PNG)
## Inspiration
Students spend a significant portion of their day commuting, walking, or engaging in tasks that make traditional studying difficult. Talking Slides was created to help them learn on the go, transforming study materials into easily digestible audio. By enabling students to listen to lectures, notes, or presentations anytime, they can maximize productivity without sacrificing balance. This approach allows for a more flexible learning experience, helping them stay prepared while also freeing up time for other aspects of life. With Talking Slides, students can stay ahead—anytime, anywhere.

## What it does
Talking Slides transforms PDFs into podcast-style audio, allowing students to listen, learn, and stay prepared on the go. Users can upload a PDF, generate an AI-powered script, and convert it into speech using a selection of voices—or even multiple voices at once for a dynamic experience! Students can listen directly on the web app or download the audio for offline use, empowering every moment to become a launchpad for academic excellence and personal growth.

## How we built it
Talking Slides transforms PDFs into audio-based presentations or podcasts, enabling students to learn on the go. The backend, powered by Django and Django REST Framework (DRF), handles authentication, API endpoints, and seamless frontend communication. MongoDB (via Djongo and Pymongo) provides flexible document storage, while GridFS efficiently manages large files like PDFs, videos, and audio. Redis caching optimizes performance by reducing redundant queries.

The frontend, built with React, integrates React Router for navigation and Framer Motion for smooth animations. Axios manages API calls, and Auth0 ensures secure authentication. OpenAI's API powers text-to-speech conversion, while PyMuPDF (Fitz) extracts and processes PDF content.

Gunicorn handles concurrent requests for deployment, and python-dotenv secures environment variables. This modern, efficient stack ensures Talking Slides is scalable, performant, and user-friendly, making learning more accessible.

## Challenges we ran into
One of the biggest challenges we faced was the deployment of the app. Originally, we aimed to build a generative video feature using Sync for AI-powered lip-syncing. However, Sync requires a URL, which can only be accessed through a third-party deployment service or if the app is already live. Due to the monorepo structure and technical limitations we encountered with Netlify, Vercel, and Render, we had to postpone this feature at the last minute. While this was a setback, it reinforced the importance of finding a scalable deployment solution, which we plan to revisit in the future.

## Accomplishments that we're proud of


## What we learned


## What's next for Talking Slides
The next step for Talking Slides is launching a fully functional web and mobile app, making it truly accessible on the go. This will give students the flexibility to engage with their study materials anytime, anywhere—whether commuting, walking, or multitasking. As we scale, we’re also prioritizing security to ensure user data remains protected.

Looking ahead, Talking Slides won’t just talk—it’ll move! Our ambitious goal is to go beyond audio and introduce a feature that generates educational videos from PDFs with a single click. Imagine turning your notes into a dynamic lecture, making missed classes a thing of the past. Life happens, but with Talking Slides, you’ll always be covered.
