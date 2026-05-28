# Imports
import fitz, os, dotenv
from google import genai

# Load environment variables and the chatbot
dotenv.load_dotenv()
api_key = os.getenv("GEMINI-API-KEY") or os.getenv("GEMINI_API_KEY")
model = "gemini-3.5-flash"
client = genai.Client(api_key=api_key)

if not api_key: # If the api key is not found
    print("Warning: API Key not found. Please check your .env file.")

def extract_files(filepath): # Extract files from the "input" folder
    if os.path.exists(filepath):
        extracted_files = os.listdir(filepath)
        processed_filess = [os.path.join(filepath, file) for file in extracted_files if file.endswith(".pdf")]
        return processed_filess
    else:
        print(f"File path, {filepath} does not exist.")
        return None

def extract_text(file): # Extract text from a PDF file
    list_of_strs = []
    
    with fitz.open(file) as reader:
        for page in reader:
            page_text = page.get_text().strip()
            if page_text:
                lines = page_text.split('\n')
                list_of_strs.extend([line.strip() for line in lines if line.strip()])
    return list_of_strs

def extract_text_from_pdf(file): # Extract text from a PDF file
    list_of_strs = []
    try:
        text = extract_text(file)
        list_of_strs.extend(text)
    except Exception as e:
        print(f"Error while extracting text from the file: {e}")
    return list_of_strs

def process_text(sentences): # Process text into paragraphs
    return "\n".join(sentences)

def summarize_pdf(paragraphs): # Summarizes PDFs
    try:
        response = client.models.generate_content(model=model, contents=paragraphs)
        print(response.text)
    except Exception as e:
        print(f"Error while summarizing PDF: {e}")


if __name__ == "__main__": # If running directly run the script
    if not os.path.exists("input"): # If there's no dir named "input" create it
        os.makedirs("input")
    
    files = extract_files("input")
    
    if files: # If there are files in the input folder
        print("Welcome to the PDF Summarizer!")
        while True: # Loop until user exits
            print("Please select an option:")
            print("1. Summarize a PDF")
            print("2. Exit")
            choice = input("Enter your option: ").strip()
            
            if choice == "1": # If user wants to summarize a PDF
                print("\nChoose a PDF to summarize:")
                for i, file in enumerate(files, 1): # For each file in the input folder
                    print(f"{i}. {os.path.basename(file)}")
                
                pdf_input = input("Enter the number of the PDF to summarize: ").strip()
                
                if not pdf_input.isdigit(): # If the input is not a number
                    print("Invalid input. Please enter a valid number.\n")
                    continue
                
                selection_idx = int(pdf_input) - 1 # Get the index of the file
                
                if selection_idx < 0 or selection_idx >= len(files): # If the index is out of bounds
                    print("Invalid choice. That number is not on the list.\n")
                    continue
                
                file = files[selection_idx] # Processes the PDF
                print(f"\nReading {os.path.basename(file)}...")
                text = extract_text_from_pdf(file)
                paragraphs = process_text(text)
                
                print("Summarizing with Gemini...") # Summarizes the PDF
                summarize_pdf(paragraphs)
            
            elif choice == "2":
                print("Goodbye!")
                break # Destroys the loop
            else: # If the input is not 1 or 2
                print("Invalid option. Please try again.\n")
    else: # If there's no PDFs
        print("No PDFs found to summarize. Place your PDFs in the 'input' folder and rerun the script.")