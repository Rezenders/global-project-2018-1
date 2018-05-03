def send_hours():
    mail.send(to=['testidlab@gmail.com'],
            subject='hello',
            message='Student\'s hours')
    return "Email sent!"
