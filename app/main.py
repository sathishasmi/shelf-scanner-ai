from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.services.image_service import ImageService
from app.services.gemini_service import GeminiService

# Setting up structured enterprise logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("shelf-scanner-backend")

app = FastAPI(title="Shelf Scanner AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate our core AI service
gemini_service = GeminiService()


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "shelf-scanner-api"}


@app.post("/api/v1/scan")
async def scan_shelf(
    file: UploadFile = File(...), preferences: str = Form("General Reading")
):
    logger.info(f"Received scan request for file: {file.filename}")

    # Simple input validation guardrail
    if not file.content_type.startswith("image/"):
        logger.warning(f"Rejected invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        # Read file stream into memory
        file_bytes = await file.read()

        optimized_image = ImageService.process_upload(file_bytes)

        ai_recommendations = await gemini_service.analyze_shelf(
            optimized_image, preferences
        )

        return {"status": "success", "recommendations": ai_recommendations}

    except Exception as e:
        logger.error(f"Internal processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the shelf image.",
        )
