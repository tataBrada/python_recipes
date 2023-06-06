import json


class UserEmails(set):
    @classmethod
    def from_file(cls, path, encoding="utf-8"):
        with open(path, encoding=encoding) as f:
            return cls(line.strip() for line in f if line.strip() != '')

    @classmethod
    def from_json(cls, path, encoding="utf-8"):
        with open(path, encoding=encoding) as f:
            data = json.load(f)
            return cls(email for email in data if isinstance(email, str))


emails = UserEmails.from_file('emails.txt')
print(f'emails from txt: {emails}')
# UserEmails({'bole@example.com', 'jeca@example.com', 'tesa@example.com', 'mari@example.com'})

other_emails = UserEmails.from_json('emails.json')
print(f'emails from json: {other_emails}')
# UserEmails({'kris@example.com', 'mari@example.com', 'zile@example.com', 'vule@example.com', 'jeca@example.com'})

# Get the union of two sets of email addresses
all_emails = emails.union(other_emails)
print(f'all emails: {all_emails}')
# {'mari@example.com', 'kris@example.com', 'zile@example.com', 'vule@example.com',
# 'jeca@example.com', 'tesa@example.com', 'bole@example.com'

# Get the intersection of two sets of email addresses
common_emails = emails.intersection(other_emails)
print(f'common emails: {common_emails}')
# {'mari@example.com', 'jeca@example.com'}

# Get the difference of two sets of email addresses
diff_emails = emails.difference(other_emails)
print(f'diff emails:{diff_emails}')
# {'tesa@example.com', 'bole@example.com'}
