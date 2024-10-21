import tkinter as tk
from tkinter import messagebox
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        messagebox.showinfo("Speak Now", "Please speak something...")
        audio_data = recognizer.listen(source)
        try:
            # Convert audio to text
            text = recognizer.recognize_google(audio_data)
            text_entry.delete(0, tk.END)
            text_entry.insert(0, text)
            analyze_sentiment(text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results; {e}")

def analyze_sentiment(text):
    if not text.strip():
        messagebox.showwarning("Input Error", "Please enter some text.")
        return
    # Perform sentiment analysis
    scores = analyzer.polarity_scores(text)
    # Save the results to a CSV file
    save_to_csv(text, scores)
    # Display the results
    display_results(text, scores)

def analyze_from_entry():
    text = text_entry.get()
    analyze_sentiment(text)

def save_to_csv(text, scores, filename="analyzed_sentences.csv"):
    # Create a DataFrame with the current analysis results
    df = pd.DataFrame([{
        "Sentence": text,
        "Positive": scores["pos"],
        "Neutral": scores["neu"],
        "Negative": scores["neg"],
        "Compound": scores["compound"]
    }])
    # Append to the CSV file, creating it if it doesn't exist
    df.to_csv(filename, mode='a', index=False, header=not pd.io.common.file_exists(filename))

def display_results(text, scores):
    # Display results in a message box
    result = f"Sentiment Analysis Results:\n\n" \
             f"Positive: {scores['pos']}\n" \
             f"Neutral: {scores['neu']}\n" \
             f"Negative: {scores['neg']}\n" \
             f"Compound: {scores['compound']}"
    messagebox.showinfo("Sentiment Analysis", result)

    # Show results as a bar graph
    plot_bar_graph(scores)

def plot_bar_graph(scores):
    # Prepare data for the bar chart
    categories = ['Positive', 'Neutral', 'Negative', 'Compound']
    values = [scores['pos'], scores['neu'], scores['neg'], scores['compound']]

    # Plot the bar graph
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color=['green', 'blue', 'red', 'orange'])
    plt.title('Sentiment Analysis Results')
    plt.xlabel('Sentiment Categories')
    plt.ylabel('Scores')
    plt.show()

# Create the main window
window = tk.Tk()
window.title("Speech and Text Sentiment Analysis")
window.geometry("400x300")

# Create the text entry field
text_entry = tk.Entry(window, width=40)
text_entry.pack(pady=10)

# Create buttons for speech recognition and text analysis
speak_button = tk.Button(window, text="Speak", command=recognize_speech, width=20)
speak_button.pack(pady=10)

analyze_button = tk.Button(window, text="Analyze Text", command=analyze_from_entry, width=20)
analyze_button.pack(pady=10)

# Run the application
window.mainloop()
