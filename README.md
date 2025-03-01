# AI Vocal Assistant for Delivery

This project implements an AI-powered vocal assistant that helps delivery personnel manage key tasks using the Orange Telecommunications services - CAMARA API. The assistant leverages voice interaction, OpenAI's GPT-4-turbo model for natural language understanding, and several API integrations to streamline delivery operations.

## Features

- **Voice Interaction:**  
  Uses `speech_recognition` for capturing user input and `pyttsx3` for text-to-speech, enabling hands-free operation.

- **Location Services:**  
  Retrieves device location using the Orange Location Retrieval API and verifies if the device is within a specific delivery zone.

- **Geofencing:**  
  Sets up subscriptions for geofencing notifications to monitor area entry events.

- **Network Quality Boost:**  
  Requests a temporary boost in network quality via the Quality on Demand API.

- **Device Connectivity:**  
  Checks if the device is reachable using the Device Reachability Status API.

- **KYC Verification:**  
  Validates the identity of the user through the KYC Match API.

- **AI-based Command Processing:**  
  Uses OpenAI's GPT-4-turbo model to analyze spoken commands and determine the appropriate actions.

## Prerequisites

- Python 3.7 or higher
- An Orange API account with access to:
  - OAuth token generation
  - Location Retrieval
  - Location Verification
  - Geofencing
  - Quality on Demand
  - Device Reachability Status
  - KYC Match APIs
- An OpenAI API key for GPT-4-turbo access
