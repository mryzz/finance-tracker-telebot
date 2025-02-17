def format_input(message):
    amount = message.text.split(',')[0].strip()
    purpose = message.text.split(',')[1].strip().lower()
    remarks = message.text.split(',')[2].strip() if 'BSF' in purpose else ''
    if not(amount.isdigit()):
        return False
    if int(amount) <= 0:
        return False
    if purpose == '':
        purpose = 'Others'
    if purpose == 'f':
        purpose = 'Food'
    if purpose == 'b':
        purpose = 'Bills'
    if purpose == 't':
        purpose = 'Transport'
    if purpose == 'o':
        purpose = 'Others'
    if purpose == 'e':
        purpose = 'Entertainment'
    if purpose == 's':
        purpose = 'Shopping'
    if purpose == 'h':
        purpose = 'Healthcare'
    if purpose == 'l':
        purpose = 'Learning'
    if remarks == '':
        remarks = ' '
    return amount, purpose, remarks