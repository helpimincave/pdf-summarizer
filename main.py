import fitz, os, dotenv
from google import genai

dotenv.load_dotenv()
api_key = dotenv.get_key(".env", "GEMINI-API-KEY")
model = "gemini-3.5-flash"
client = genai.Client(api_key=api_key)

def extract_files(filepath):
    if os.path.exists(filepath):
        files = os.listdir(filepath)
        processed_files = [os.path.join(filepath, file) for file in files if file.endswith(".pdf")]
        return processed_files
    else:
        print(f"File path, {filepath} does not exist.")
        return None

def extract_text(file):
    list_of_strs = []
    reader = fitz.open(file)
    for page in reader.pages():
        page_text = page.get_text().strip()
        if page_text:
            lines = page_text.split('\n')
            list_of_strs.extend([line.strip() for line in lines if line.strip()])
    reader.close()
    return list_of_strs

def extract_text_from_pdf(files):
    list_of_strs = []
    for file in range(len(files)):
        try:
            text = extract_text(files[file])
            list_of_strs.extend(text)
        except Exception as e:
            print(f"Error while extracting text from the {file + 1} file: {e}")
            continue
    return list_of_strs

def process_text(sentences):
    paragraph = ""
    
    for sentence in sentences:
        paragraph += sentence + "\n"
    return paragraph

def summarize_pdf(paragraph):
    response = client.models.generate_content(model=model, contents=f"{paragraph}")
    print(response.text)

if __name__ == "__main__":
    files = extract_files()