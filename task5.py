import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

# ============================================================
# 1. LOAD .ENV FILE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# 2. GET MISTRAL API KEY
# ============================================================

API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError(
        "MISTRAL_API_KEY not found.\n"
        "Please create a .env file in the same folder as task5.py\n"
        "and add:\n"
        "MISTRAL_API_KEY=YOUR_API_KEY"
    )


# ============================================================
# 3. CREATE MISTRAL CLIENT
# ============================================================

client = Mistral(api_key=API_KEY)


# ============================================================
# 4. SUMMARIZATION FUNCTION
# ============================================================

def summarize_text(text, length="Medium", style="Simple"):

    if not text.strip():
        return "Please enter some text."

    # Summary length instructions
    if length == "Short":
        length_instruction = (
            "Create a very short summary in 3 to 5 sentences."
        )

    elif length == "Medium":
        length_instruction = (
            "Create a clear summary in one or two paragraphs."
        )

    else:
        length_instruction = (
            "Create a detailed summary covering all important points."
        )


    # Summary style instructions
    if style == "Simple":
        style_instruction = (
            "Use simple and easy-to-understand English."
        )

    elif style == "Academic":
        style_instruction = (
            "Use formal academic English."
        )

    else:
        style_instruction = (
            "Present the important information as bullet points."
        )


    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are an expert AI text summarization assistant.

Summarize the following text accurately.

Instructions:
- Keep the main ideas.
- Keep important facts.
- Remove unnecessary repetition.
- Do not add information that is not present in the original text.
- Do not change the meaning.
- {length_instruction}
- {style_instruction}

TEXT TO SUMMARIZE:

{text}

Generate only the summary.
"""


    # ========================================================
    # SEND REQUEST TO MISTRAL
    # ========================================================

    response = client.chat.complete(
        model="mistral-large-latest",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional text summarization "
                    "assistant. Provide accurate and concise summaries."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )


    # ========================================================
    # GET SUMMARY
    # ========================================================

    summary = response.choices[0].message.content

    return summary


# ============================================================
# 5. MAIN PROGRAM
# ============================================================

print("=" * 60)
print("        MISTRAL AI TEXT SUMMARIZATION")
print("=" * 60)

print("\nChoose summary length:")
print("1. Short")
print("2. Medium")
print("3. Long")

length_choice = input("\nEnter your choice (1/2/3): ")


if length_choice == "1":
    summary_length = "Short"

elif length_choice == "3":
    summary_length = "Long"

else:
    summary_length = "Medium"


print("\nChoose summary style:")
print("1. Simple")
print("2. Academic")
print("3. Bullet Points")

style_choice = input("\nEnter your choice (1/2/3): ")


if style_choice == "2":
    summary_style = "Academic"

elif style_choice == "3":
    summary_style = "Bullet Points"

else:
    summary_style = "Simple"


# ============================================================
# 6. GET TEXT FROM USER
# ============================================================

print("\n" + "=" * 60)
print("Enter the text you want to summarize.")
print("Type END on a new line when you are finished.")
print("=" * 60)

lines = []

while True:

    line = input()

    if line.strip().upper() == "END":
        break

    lines.append(line)


text = "\n".join(lines)


# ============================================================
# 7. GENERATE SUMMARY
# ============================================================

if not text.strip():

    print("\nPlease enter some text.")

else:

    print("\n" + "=" * 60)
    print("Mistral AI is generating your summary...")
    print("=" * 60)

    try:

        summary = summarize_text(
            text,
            summary_length,
            summary_style
        )

        print("\n" + "=" * 60)
        print("                 SUMMARY")
        print("=" * 60)

        print(summary)

        # ====================================================
        # STATISTICS
        # ====================================================

        original_words = len(text.split())
        summary_words = len(summary.split())

        if original_words > 0:

            reduction = (
                (original_words - summary_words)
                / original_words
            ) * 100

        else:

            reduction = 0


        print("\n" + "=" * 60)
        print("                 STATISTICS")
        print("=" * 60)

        print("Original words :", original_words)
        print("Summary words  :", summary_words)
        print(f"Reduction      : {reduction:.2f}%")

        # ====================================================
        # SAVE SUMMARY
        # ====================================================

        with open(
            "mistral_summary.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(summary)


        print("\nSummary saved as:")
        print("mistral_summary.txt")

        print("\n" + "=" * 60)
        print("              PROJECT COMPLETED")
        print("=" * 60)


    except Exception as error:

        print("\nERROR:")
        print(error)