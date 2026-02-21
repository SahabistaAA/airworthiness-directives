# Short Report
---
## Approach
I am using hybrid approach to extract the information from the ADS. In this case I am using `ExtractorService` to extract the text from the PDF and then utilize `LLMParser` to parse the text and extract the information. I have also added `VLMParser` compliment with `OCRService`to extract the information from the images, tables, and other visual elements. However, 'VLMParser' and 'OCRService' are not fully implemented yet, so they are not used in the current implementation.

**Why I choose this approach?**
I choose this approach because it is a good balance between accuracy and performance. I used `pymupdf` library as the base for text extaction on `ExtractorService` as it is fast, efficient, and highly accurate for text extraction from PDFs. The utilization of this library based on my quick research as it is one of the best pdf extractor for Python.

Here's the benchmark:
| Library      | Speed              | Accuracy    | Features                                    | Performance (Practical Use)                                              | Rating (⭐ /5) | 
| ------------ | ------------------ | ----------- | ------------------------------------------- | ------------------------------------------------------------------------ | ------------- |
| PyPDF2       | Slow (large files) | Low–Medium  | Basic PDF manipulation (split, merge, read) | Struggles with complex layouts; not optimized for structured extraction  | ⭐⭐☆☆☆ (2/5)   | 
| pdfminer.six | Medium             | Medium–High | Detailed layout-aware text extraction       | Good for structured text but slower for large-scale batch processing     | ⭐⭐⭐☆☆ (3/5)   |
| PyMuPDF      | Fast               | High        | Text, images, annotations, metadata         | Excellent speed and reliable extraction; strong for production pipelines | ⭐⭐⭐⭐⭐ (5/5)   |
| pdfplumber   | Medium             | High        | Layout-aware text + table extraction        | Very strong layout handling; slightly slower than PyMuPDF                | ⭐⭐⭐⭐☆ (4/5)   |

As for `gemini-2.5-flash` I used it because it is powerful enough as the `LLMParser` and `VLMParser` as the same time. Moreover, it's free to use for non-commercial purposes. It can well handled both text and images, which makes it a good choice fot this task.

---
## Challenges

The most challenging part that I faced during this task is to extract the information correctly from PDF file given. The problem is due to logical problem while extracting the information from the PDF file. However, I was able to extract the information correctly by using `ExtractorService` and `LLMParser`.

As it is a pipeline, I handle ambiguity or edge case by using validation and fallback mechanism. I use `pydantic` to validate the extracted information, so it will avoid the ambiguity. While on the other hands, I am implemented fallback mechanism to handle the edge cases. There also `VLMParser` and `OCRService` that can be used to extract the information from the scanned documents.

---
## Limitations

As I am using `ExtractorService` to extract the text from the PDF file, it won't working on scanned documents. To handle this kind of issue, I would like to fully implement the `VLMParser` and `OCRService` to extract the information from the scanned documents, especially for the legacy documents that couldn't be handled by `ExtractorService` and `LLMParser`. To make it flexible, I also put the `HybridParser` which makes the `LLMParser` and `VLMParser` can be used together to extract the information from the PDF file. 

---
## Trade-offs

As I mentioned above, I am using LLM, exactly `gemini-2.5-flash` models to parse and extract the information from the PDF file through `LLMParser`. Using LLM for this case is a good choice because it is powerful enough to extract the information and it could handle the ambiguity and edge cases by the extracted text produces by `ExtractorService`. So on my implementation, I am using both of them to enhance the accuracy, quality, and performance of the extraction process.

For current case, using `ExtractorService` and `LLMParser` is enough to extract the information from the PDF file. However, if the PDF file is scanned document, then I would like to use `VLMParser` and `OCRService` to extract the information from the PDF file.
