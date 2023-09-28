# Chat App
made by yoav mateless
This is a simple chat application built using Python and Tkinter for the GUI. It allows users to chat with each other through a server.

## Features

- Users can enter their name.
- Users can send and receive messages in real-time.
- Users can disconnect from the chat without closing the server.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Tkinter (usually included with Python)

## How to Use

1. Start the server by running `server.py`.

2. Run the client application by executing `client.py`. You will be prompted to enter your name.

3. The chat window will appear, allowing you to send and receive messages with other connected clients.

4. To disconnect from the chat without closing the server, click the "Disconnect" button.

### Server Commands

The server supports the following commands:

- `help`: Display a list of available commands.
- `kick`: Kick a user from the server. You will be prompted to enter the username.
- `mute`: Mute a user on the server. You will be prompted to enter the username.
- `exit`: Exit the server and close all connections.

## Files

- `server.py`: The server script that listens for incoming connections and manages chat messages.

- `client.py`: The client script that connects to the server and allows users to chat.

- `README.md`: This README file explaining how to use the application.

## Acknowledgments

This project was created as a simple demonstration of client-server communication in Python. Feel free to modify and expand it according to your needs.
