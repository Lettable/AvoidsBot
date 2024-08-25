# AvoidsBot

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-blue.svg)](https://docs.pyrogram.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-5.0-green.svg)](https://www.mongodb.com/)

AvoidsBot is a Telegram bot designed to help users report scams efficiently. The bot allows users to submit reports about scammers, which are then reviewed by admins before being published in a public channel. It provides a secure and structured method for reporting scam activities, helping communities stay safe from fraudulent activities.

## Features

- **Create Reports**: Users can easily create scam reports by providing details such as the scammer's username, the deal amount, a summary of the incident, and proof in the form of a channel URL.
- **Report Lookup**: Users can look up scam reports associated with a specific username or user ID.
- **Admin Approval System**: Reports are sent to a private admin channel where they can be approved or rejected.
- **Automated Notifications**: Users are notified whether their report is approved or rejected.
- **Public Reporting**: Approved reports are published in a public channel, making it easier for others to avoid known scammers.

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB instance
- Telegram Bot API token
- Pyrogram

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Lettable/avoidsbot.git
    cd avoidsbot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your environment variables**:
    - Edit the `sample.env` file to add your configuration details. You can use a text editor like `nano`:
        ```bash
        nano sample.env
        ```
   - Add the following environment variables to the `sample.env` file:
        ```bash
        BOT_TOKEN=<Your Telegram Bot Token>
        MONGO_DB_URI=<Your MongoDB Connection URI>
        IMAGE_URL=<Your Image URL to be Used in Public Channel>
        ```
   - Rename the `sample.env` file to `.env`:
        ```bash
        mv sample.env .env
        ```
    
4. **Run the bot**:
    ```bash
    python bot.py
    ```

### Get Image URL

To customize the image used in reports:

1. **Download the Template Image**:
    - Download the template image from [this link](https://graph.org/file/65993f8bdb46060f8495a.png).

2. **Edit the Image**:
    - Use a tool like [polotno](https://studio.polotno.com/) to edit the image with your channel's profile picture or other relevant visuals.

3. **Upload the Edited Image**:
    - Upload the edited image to [graph.org](https://graph.org) or any other image hosting service and get Image URL.



### Usage

#### Commands

- **/start**: Start interacting with the bot and see the main menu.
- **/lookup <username|user_id>**: Look up scam reports associated with a specific username or user ID.
- **/cancel**: Cancel the current report creation process.

#### Inline Buttons

- **Create Report**: Start the process of creating a new scam report.
- **Cancel Report**: Cancel the ongoing report creation process.
- **Approve/Reject**: Admins can approve or reject reports from the private admin channel.

### Report Workflow

1. **User Interaction**:
    - The user initiates the process by clicking "Create Report".
    - The bot guides the user to input details about the scammer and the scam.

2. **Admin Review**:
    - The report is sent to a private admin channel for review.
    - Admins can approve or reject the report with a single click.

3. **Public Announcement**:
    - Approved reports are posted in a public channel with details such as the scammer's display name, username, amount involved, and a summary.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you're the owner of a bot and concerned about your source code being leaked, feel free to reach out to me. You can stop the leak by contacting me directly:

- **Telegram**: [@Lettable](https://t.me/Lettable)
- **GitHub**: [Lettable](https://github.com/Lettable)
