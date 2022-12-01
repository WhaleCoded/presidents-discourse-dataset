import csv
import os

# Load all the LIWC dictionaries
relative_path = os.path.join(os.path.curdir, "cleaned_liwc_dictionaries.csv")
with open(relative_path, "r") as f:
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
    "andrew johnson",
    "franklin pierce",
    "barack obama",
    "george washington",
    "thomas jefferson",
    "donald j. trump",
    "martin van buren",
    "jimmy carter",
    "william howard taft",
    "james a. garfield",
    "benjamin harrison",
    "lyndon b. johnson",
    "james buchanan",
    "ronald reagan",
    "warren g. harding",
    "john adams",
    "herbert hoover",
    "abraham lincoln",
    "james k. polk",
    "grover cleveland",
    "zachary taylor",
    "john quincy adams",
    "george w. bush",
    "andrew jackson",
    "william j. clinton",
    "john f. kennedy",
    "millard fillmore",
    "chester a. arthur",
    "james madison",
    "james monroe",
    "john tyler",
    "william henry harrison",
    "gerald r. ford",
    "franklin d. roosevelt",
    "rutherford b. hayes",
    "woodrow wilson",
    "ulysses s. grant",
    "george bush",
    "calvin coolidge",
    "richard nixon",
    "harry s. truman",
    "theodore roosevelt",
    "dwight d. eisenhower",
    "joseph r. biden",
    "william mckinley",
]
PRESIDENTS = set(PRESIDENTS)

PRESIDENT_POLITICAL_PARTIES = {}
PRESIDENT_POLITICAL_PARTIES["george washington"] = "unaffiliated"
PRESIDENT_POLITICAL_PARTIES["john adams"] = "federalist"
PRESIDENT_POLITICAL_PARTIES["thomas jefferson"] = "democratic-republican"
PRESIDENT_POLITICAL_PARTIES["james madison"] = "democratic-republican"
PRESIDENT_POLITICAL_PARTIES["james monroe"] = "democratic-republican"
PRESIDENT_POLITICAL_PARTIES["john quincy adams"] = "democratic-republican"
PRESIDENT_POLITICAL_PARTIES["andrew jackson"] = "democrat-pre-1900"
PRESIDENT_POLITICAL_PARTIES["martin van buren"] = "democrat-pre-1900"
PRESIDENT_POLITICAL_PARTIES["william henry harrison"] = "whig"
PRESIDENT_POLITICAL_PARTIES["john tyler"] = "whig"
PRESIDENT_POLITICAL_PARTIES["james k. polk"] = "democrat-pre-1900"
PRESIDENT_POLITICAL_PARTIES["zachary taylor"] = "whig"
PRESIDENT_POLITICAL_PARTIES["millard fillmore"] = "whig"
PRESIDENT_POLITICAL_PARTIES["franklin pierce"] = "democrat-pre-1900"
PRESIDENT_POLITICAL_PARTIES["james buchanan"] = "democrat-pre-1900"
PRESIDENT_POLITICAL_PARTIES["abraham lincoln"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["andrew johnson"] = "national-union"
PRESIDENT_POLITICAL_PARTIES["ulysses s. grant"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["rutherford b. hayes"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["james a. garfield"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["chester a. arthur"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["grover cleveland"] = "democrat-pre-1900"
PRESIDENT_POLITICAL_PARTIES["benjamin harrison"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["william mckinley"] = "republican-pre-1900"
PRESIDENT_POLITICAL_PARTIES["theodore roosevelt"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["william howard taft"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["woodrow wilson"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["warren g. harding"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["calvin coolidge"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["herbert hoover"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["franklin d. roosevelt"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["harry s. truman"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["dwight d. eisenhower"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["john f. kennedy"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["lyndon b. johnson"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["richard nixon"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["gerald r. ford"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["jimmy carter"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["ronald reagan"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["george w. bush"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["william j. clinton"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["george bush"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["barack obama"] = "democrat-post-1900"
PRESIDENT_POLITICAL_PARTIES["donald j. trump"] = "republican-post-1900"
PRESIDENT_POLITICAL_PARTIES["joseph r. biden"] = "democrat-post-1900"


# PRONOUNS = [
#     "all",
#     "another",
#     "any",
#     "anybody",
#     "anyone",
#     "anything",
#     "as",
#     "aught",
#     "both",
#     "each",
#     "each other",
#     "either",
#     "enough",
#     "everybody",
#     "everyone",
#     "everything",
#     "few",
#     "he",
#     "her",
#     "hers",
#     "herself",
#     "him",
#     "himself",
#     "his",
#     "I",
#     "idem",
#     "it",
#     "its",
#     "itself",
#     "many",
#     "me",
#     "mine",
#     "most",
#     "my",
#     "myself",
#     "naught",
#     "neither",
#     "no one",
#     "nobody",
#     "none",
#     "nothing",
#     "nought",
#     "one",
#     "one another",
#     "other",
#     "others",
#     "ought",
#     "our",
#     "ours",
#     "ourself",
#     "ourselves",
#     "several",
#     "she",
#     "some",
#     "somebody",
#     "someone",
#     "something",
#     "somewhat",
#     "such",
#     "suchlike",
#     "that",
#     "thee",
#     "their",
#     "theirs",
#     "theirself",
#     "theirselves",
#     "them",
#     "themself",
#     "themselves",
#     "there",
#     "these",
#     "they",
#     "thine",
#     "this",
#     "those",
#     "thou",
#     "thy",
#     "thyself",
#     "us",
#     "we",
#     "what",
#     "whatever",
#     "whatnot",
#     "whatsoever",
#     "whence",
#     "where",
#     "whereby",
#     "wherefrom",
#     "wherein",
#     "whereinto",
#     "whereof",
#     "whereon",
#     "wherever",
#     "wheresoever",
#     "whereto",
#     "whereunto",
#     "wherewith",
#     "wherewithal",
#     "whether",
#     "which",
#     "whichever",
#     "whichsoever",
#     "who",
#     "whoever",
#     "whom",
#     "whomever",
#     "whomso",
#     "whomsoever",
#     "whose",
#     "whosever",
#     "whosesoever",
#     "whoso",
#     "whosoever",
#     "ye",
#     "yon",
#     "yonder",
#     "you",
#     "your",
#     "yours",
#     "yourself",
#     "yourselves",
# ]

# PRONOUNS = set([pronoun.lower() for pronoun in PRONOUNS])

# # Load the LIWC pronoun dictionary
# import csv

# with open("liwc_dictionary.csv", "r") as f:
#     reader = csv.reader(f, delimiter="\n")

#     # Get the pronoun words
#     liwc_pronouns = []
#     for row in reader:
#         if len(row) > 0:
#             pronoun = row[0].lower()
#             liwc_pronouns.append(pronoun)

# LIWC_PRONOUNS = set(liwc_pronouns)
# PRESIDENTS = [
#     "George Washington",
#     "John Adams",
#     "Thomas Jefferson",
#     "James Madison",
#     "James Monroe",
#     "John Quincy Adams",
#     "Andrew Jackson",
#     "Martin Van Buren",
#     "William Henry Harrison",
#     "John Tyler",
#     "James K. Polk",
#     "Zachary Taylor",
#     "Millard Fillmore",
#     "Franklin Pierce",
#     "James Buchanan",
#     "Abraham Lincoln",
#     "Andrew Johnson",
#     "Ulysses S. Grant",
#     "Rutherford B. Hayes",
#     "James A. Garfield",
#     "Chester A. Arthur",
#     "Grover Cleveland",
#     "Benjamin Harrison",
#     "Grover Cleveland",
#     "William McKinley",
#     "Theodore Roosevelt",
#     "William Howard Taft",
#     "Woodrow Wilson",
#     "Warren G. Harding",
#     "Calvin Coolidge",
#     "Herbert Hoover",
#     "Franklin D. Roosevelt",
#     "Harry S. Truman",
#     "Dwight D. Eisenhower",
#     "John F. Kennedy",
#     "Lyndon B. Johnson",
#     "Richard Nixon",
#     "Gerald Ford",
#     "Jimmy Carter",
#     "Ronald Reagan",
#     "George H. W. Bush",
#     "Bill Clinton",
#     "George W. Bush",
#     "Barack Obama",
#     "Donald Trump",
#     "Joe Biden",
# ]

# PRESIDENTS = [president.lower() for president in PRESIDENTS]
# PRESIDENTS = set(PRESIDENTS)

# from dataset import PresidentsDataset

# dataset = PresidentsDataset()
# dataset.where(lambda data: "Presidential" in data["categories"]["primary"])

# president_speakers = set()
# president_last_names = [president.split(" ")[-1].lower() for president in PRESIDENTS]


# not_presidents = set()
# for data in dataset:
#     speaker_last_name = data["speaker"].split(" ")[-1].lower()
#     if speaker_last_name in president_last_names:
#         president_speakers.add(data["speaker"].lower())
#     else:
#         not_presidents.add(data["speaker"].lower())

# president_speakers.remove("jill biden")
# president_speakers.remove("michelle obama")
# president_speakers.remove("melania trump")
# president_speakers.remove("laura bush")

# PRESIDENTS = president_speakers


if __name__ == "__main__":
    print(PRESIDENTS)

    for president in PRESIDENTS:
        print(president, PRESIDENT_POLITICAL_PARTIES[president])

    print(set(PRESIDENT_POLITICAL_PARTIES.values()))
