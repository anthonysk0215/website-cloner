from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from ..services.clone_service import CloneService

router = APIRouter()
clone_service = CloneService()

class CloneRequest(BaseModel):
    url: HttpUrl

class CloneResponse(BaseModel):
    html: str

@router.post("/clone", response_model=CloneResponse)
async def clone_website(request: CloneRequest):
    try:
        # Scrape the website
        context = await clone_service.scrape_website(str(request.url))
        if not context:
            raise HTTPException(status_code=400, detail="Failed to scrape website")
        
        # Generate clone
        cloned_html = await clone_service.generate_clone(context)
        if not cloned_html:
            raise HTTPException(status_code=500, detail="Failed to generate clone")
        
        return CloneResponse(html=cloned_html)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 