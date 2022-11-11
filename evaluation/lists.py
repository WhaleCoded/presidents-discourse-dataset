PRONOUNS  = [
    "all",
    "another",
    "any",
    "anybody",
    "anyone",
    "anything",
    "as",
    "aught",
    "both",
    "each",
    "each other",
    "either",
    "enough",
    "everybody",
    "everyone",
    "everything",
    "few",
    "he",
    "her",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "I",
    "idem",
    "it",
    "its",
    "itself",
    "many",
    "me",
    "mine",
    "most",
    "my",
    "myself",
    "naught",
    "neither",
    "no one",
    "nobody",
    "none",
    "nothing",
    "nought",
    "one",
    "one another",
    "other",
    "others",
    "ought",
    "our",
    "ours",
    "ourself",
    "ourselves",
    "several",
    "she",
    "some",
    "somebody",
    "someone",
    "something",
    "somewhat",
    "such",
    "suchlike",
    "that",
    "thee",
    "their",
    "theirs",
    "theirself",
    "theirselves",
    "them",
    "themself",
    "themselves",
    "there",
    "these",
    "they",
    "thine",
    "this",
    "those",
    "thou",
    "thy",
    "thyself",
    "us",
    "we",
    "what",
    "whatever",
    "whatnot",
    "whatsoever",
    "whence",
    "where",
    "whereby",
    "wherefrom",
    "wherein",
    "whereinto",
    "whereof",
    "whereon",
    "wherever",
    "wheresoever",
    "whereto",
    "whereunto",
    "wherewith",
    "wherewithal",
    "whether",
    "which",
    "whichever",
    "whichsoever",
    "who",
    "whoever",
    "whom",
    "whomever",
    "whomso",
    "whomsoever",
    "whose",
    "whosever",
    "whosesoever",
    "whoso",
    "whosoever",
    "ye",
    "yon",
    "yonder",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
]

PRONOUNS = set([pronoun.lower() for pronoun in PRONOUNS])

# Load the LIWC pronoun dictionary
import csv
with open("liwc_dictionary.csv", "r") as f:
    reader = csv.reader(f, delimiter="\n")

    # Get the pronoun words
    liwc_pronouns = []
    for row in reader:
        if len(row) > 0:
            pronoun = row[0].lower()
            liwc_pronouns.append(pronoun)

LIWC_PRONOUNS = set(liwc_pronouns)

# Load all the LIWC dictionaries
with open("cleaned_liwc_dictionaries.csv", "r") as f:
    reader = csv.reader(f)

    # Get the pronoun words
    liwc_dictionaries = {}
    for row in reader:
        dataset_name = row[0]

        entries = []
        for entry in row[1:]:
            if entry != "":
                entries.append(entry.lower())
        
        liwc_dictionaries[dataset_name] = set(entries)

LIWC_DICTIONARIES = liwc_dictionaries

PRESIDENTS = [
    "George Washington",
    "John Adams",
    "Thomas Jefferson",
    "James Madison",
    "James Monroe",
    "John Quincy Adams",
    "Andrew Jackson",
    "Martin Van Buren",
    "William Henry Harrison",
    "John Tyler",
    "James K. Polk",
    "Zachary Taylor",
    "Millard Fillmore",
    "Franklin Pierce",
    "James Buchanan",
    "Abraham Lincoln",
    "Andrew Johnson",
    "Ulysses S. Grant",
    "Rutherford B. Hayes",
    "James A. Garfield",
    "Chester A. Arthur",
    "Grover Cleveland",
    "Benjamin Harrison",
    "Grover Cleveland",
    "William McKinley",
    "Theodore Roosevelt",
    "William Howard Taft",
    "Woodrow Wilson",
    "Warren G. Harding",
    "Calvin Coolidge",
    "Herbert Hoover",
    "Franklin D. Roosevelt",
    "Harry S. Truman",
    "Dwight D. Eisenhower",
    "John F. Kennedy",
    "Lyndon B. Johnson",
    "Richard Nixon",
    "Gerald Ford",
    "Jimmy Carter",
    "Ronald Reagan",
    "George H. W. Bush",
    "Bill Clinton",
    "George W. Bush",
    "Barack Obama",
    "Donald Trump",
    "Joe Biden",
]

PRESIDENTS = [president.lower() for president in PRESIDENTS]
PRESIDENTS = set(PRESIDENTS)

from dataset import PresidentsDataset

dataset = PresidentsDataset()
dataset.where(lambda data: "Presidential" in data["categories"]["primary"])

president_speakers = set()
president_last_names = [president.split(" ")[-1].lower() for president in PRESIDENTS]


not_presidents = set()
for data in dataset:
    speaker_last_name = data["speaker"].split(" ")[-1].lower()
    if speaker_last_name in president_last_names:
        president_speakers.add(data["speaker"].lower())
    else:
        not_presidents.add(data["speaker"].lower())

president_speakers.remove("jill biden")
president_speakers.remove("michelle obama")
president_speakers.remove("melania trump")
president_speakers.remove("laura bush")

PRESIDENTS = president_speakers

if __name__ == "__main__":
    print(PRESIDENTS)