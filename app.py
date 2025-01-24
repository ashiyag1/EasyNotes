from flask import Flask, render_template, request, send_file
from textblob import TextBlob
import nltk
from nltk.corpus import wordnet
from io import BytesIO
from reportlab.pdfgen import canvas

# Download required NLTK data
nltk.download("punkt")
nltk.download("wordnet")

# Initialize Flask app
app = Flask(__name__)

def simplify_text(original_text):
    # Tokenize sentences
    blob = TextBlob(original_text)
    simplified_sentences = []

    for sentence in blob.sentences:
        words = sentence.words
        simplified_words = []

        for word in words:
            # Find synonyms for each word
            synonyms = wordnet.synsets(word)
            if synonyms:
                # Replace the word with its most common synonym
                synonym = synonyms[0].lemmas()[0].name()
                simplified_words.append(synonym)
            else:
                simplified_words.append(word)

        # Join the simplified words into a sentence
        simplified_sentences.append(" ".join(simplified_words))

    # Join simplified sentences into a single text
    return " ".join(simplified_sentences)

# Route to render the HTML form and handle submissions
@app.route("/", methods=["GET", "POST"])
def simplify_text_route():
    original_text = ""
    simplified_text = ""
    error = None

    if request.method == "POST":
        # Get the input text from the form
        original_text = request.form.get("original_text", "").strip()

        if not original_text:
            error = "Input text cannot be empty."
        else:
            try:
                # Simplify the text
                simplified_text = simplify_text(original_text)
            except Exception as e:
                error = f"An error occurred: {str(e)}"

    return render_template(
        "index.html",
        original_text=original_text,
        simplified_text=simplified_text,
        error=error,
    )

# Route to download the simplified text as a PDF
@app.route("/download", methods=["POST"])
def download_pdf():
    simplified_text = request.form.get("simplified_text", "")

    if not simplified_text:
        return "No simplified text available to download.", 400

    # Create an in-memory PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, "Simplified Text Notes")
    pdf.line(100, 790, 500, 790)  # Add a horizontal line

    # Write the simplified text to the PDF
    y_position = 770  # Start position for the text
    for line in simplified_text.split("\n"):
        pdf.drawString(100, y_position, line)
        y_position -= 20  # Move to the next line

        # Check if the text goes beyond the page length
        if y_position < 50:
            pdf.showPage()  # Start a new page
            y_position = 800  # Reset y position

    pdf.save()
    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(
        buffer,
        as_attachment=True,
        download_name="simplified_notes.pdf",
        mimetype="application/pdf",
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
