#!/usr/bin/python
"""
Module pertaining to email properties and functionalities
"""
import pickle
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class EmailFailure(Exception):
    """Raise this error when service failed to send email

    :param Exception: Base Exception Class object
    :type Exception: (Exception)
    """


def create_message(sender_email, to_email, subject, message_text):
    """Function to generate a raw format utf-8 message based on given inputs

    :param sender_email: Email of the sender
    :type sender_email: (str)
    :param to_email: Email of the receiver
    :type to_email: (str)
    :param subject: Subject of the email to be sent
    :type subject: (str)
    :param message_text: Text to be included in the email body
    :type message_text: (str)
    :return: Raw formateed utf-8 message generated based on given inputs
    :rtype: (dict)
    """
    message = MIMEText(message_text)
    message["to"] = to_email
    message["from"] = sender_email
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {"raw": raw_message.decode("utf-8")}


class EmailClient:
    """
    Main class to perform operations pertaining to email
    """

    def __init__(self):
        self.service = build("gmail", "v1", credentials=self._get_creds())

    def _get_creds(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("configs/token.pickle"):
            with open("configs/token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "configs/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("configs/token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return creds

    def send_message(self, message, user_id="me"):
        """Function to send email based on message body generated from lib_email.create_message

        :param message: Email body including message, body, subject
        :type message: (dict)
        :param user_id: [description], defaults to "me"
        :type user_id: str, optional
        :return: ID of the email sent if successful | None if failed to send email
        :rtype: (id | None)
        """
        message = (
            self.service.users()
            .messages()
            .send(userId=user_id, body=message)
            .execute()
        )
        return message.get("id", EmailFailure("Failed to send email to address={}".format(user_id)))
