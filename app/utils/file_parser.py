import io 
import docx
import pypdf


async def parse_file_content(file_content:bytes,file_name:str)->str:
    """Parses the content of an uploaded file in memory."""
    text = ""
    if file_name.endswith(".pdf"):
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
            for page in pdf_reader.pages:
                text+= page.extract_text()

        except Exception as e:
            raise ValueError(f"Error parsing PDF file: {e}")
        
    elif file_name.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                text += para.text + "\n"

        except Exception as e:
            raise ValueError (f"Error parsing DOCX file: {e}")
        

    elif file_name.endswith(".txt"):
        try:
            text = file_content.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error parsing TXT file: {e}")
        

    else:
        raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT.")

    if not text.strip():
        raise ValueError("Could not extract any text from the file.")
        
    return text    
            