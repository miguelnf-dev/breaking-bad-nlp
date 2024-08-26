# Breaking Bad Theme Classifier (images/bb3.png)

This project analyzes the scripts of the TV series "Breaking Bad" to classify and visualize the prevalence of different themes throughout the show.

## Features

- Loads and processes subtitle files (.srt) from Breaking Bad episodes
- Classifies themes in the scripts using a zero-shot classification model
- Visualizes theme distribution using an interactive Streamlit application

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/breaking-bad-theme-classifier.git
   cd breaking-bad-theme-classifier
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Download the Breaking Bad subtitle files and place them in the `data/subtitles` directory.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Use the interface to select themes, input file paths, and visualize the results.

## Project Structure

```
breaking-bad-theme-classifier/
│
├── app.py
├── Theme/
│   └── theme_classifier.py
├── utils.py
├── data/
│   └── subtitles/
├── images/
│   └── bb2.png
├── README.md
├── requirements.txt
└── LICENSE
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Breaking Bad created by Vince Gilligan
- Hugging Face for the BART-large-mnli model
- Streamlit for the interactive web application framework