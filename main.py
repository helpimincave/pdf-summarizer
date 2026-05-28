import fitz, os, dotenv
from google import genai

dotenv.load_dotenv()
api_key = dotenv.get_key(".env", "GEMINI-API-KEY")
model = "gemini-3.5-flash"
client = genai.Client(api_key=api_key)

def extract_files(filepath):
    if os.path.exists(filepath):
        extracted_files = os.listdir(filepath)
        processed_filess = [os.path.join(filepath, file) for file in extracted_files if file.endswith(".pdf")]
        return processed_filess
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

def extract_text_from_pdf(file):
    list_of_strs = []
    try:
        text = extract_text(file)
        list_of_strs.extend(text)
    except Exception as e:
        print(f"Error while extracting text from the file: {e}")
    return list_of_strs

def process_text(sentences):
    paragraphs = ""
    
    for sentence in sentences:
        try:
            paragraphs += sentence + "\n"
        except Exception as e:
            print(f"Error while processing sentence: {e}")
    return paragraphs

def summarize_pdf(paragraphs):
    try:
        response = client.models.generate_content(model=model, contents=paragraphs)
        print(response.text)
    except Exception as e:
        print(f"Error while summarizing PDF: {e}")

if __name__ == "__main__":
    files = extract_files("input")
    if files:
        try:
            while True:
                print("Welcome to the PDF Summarizer!")
                print("Please select a option:")
                print("1. Summarize a PDF")
                print("2. Exit")
                choice = input("Enter your option: ")
                
                if choice == "1":
                    print("Choose a PDF to summarize:")
                    for i, file in enumerate(files, 1):
                        file = os.path.basename(file)
                        print(f"{i}. {file}")
                    pdf = input("Enter the number of the PDF to summarize: ")
                    
                    if pdf.isalpha():
                        print("Invalid input. Please enter a number.")
                        continue
                    elif (int(pdf) - 1) > len(files):
                        print("Invalid input. Please enter a valid number.")
                        continue
                    else:
                        file = files[int(pdf) - 1]
                        text = extract_text_from_pdf(file)
                        paragraphs = process_text(text)
                        print("Summarizing...")
                        summarize_pdf(paragraphs)
                elif choice == "2":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
                    
        except Exception as e:
            print(f"Error while loading in the project.")
    else:
        print("No PDFs to summarize. (Place the PDFs in the 'input' folder.)")