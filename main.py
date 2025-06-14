from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()
#app = FastAPI(openapi_prefix="/api")

# Allow requests from all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    # allow_origins=["https://find-helper.ru",
    #"https://www.find-helper.ru"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пример модели данных психолога
class Psychologist(BaseModel):
    id: Optional[int] = None
    name: str
    specialization: str
    ready_to_talk: bool
    peer_id: str
    web_link: Optional[str] = None


class ReadyStatusUpdate(BaseModel):
    peer_id: str
    ready_to_talk: bool

# Список психологов (для примера)
psychologists: List[Psychologist] = [
    Psychologist(id=1, name="John Doe", specialization="Clinical Psychology", ready_to_talk=False, peer_id="bd0f7d66-7396-4eb7-99ca-63df9800eab7", web_link="https://example.com/john-doe"),
    Psychologist(id=2, name="Jane Smith", specialization="Counseling Psychology", ready_to_talk=False, peer_id="bd0f7d66-7396-4eb7-99ca-63df9800eab7", web_link="https://example.com/jane-smith"),
    Psychologist(id=3, name="Emily Johnson", specialization="Child Psychology", ready_to_talk=False, peer_id="bd0f7d66-7396-4eb7-99ca-63df9800eab7", web_link="https://example.com/emily-johnson"),
]

@app.get("/get_next_psychologist")
def get_next_psychologist():
    # Получение случайного психолога из списка, который готов говорить
    ready_psychologists = [psychologist for psychologist in psychologists if psychologist.ready_to_talk]
    if not ready_psychologists:
        return {"message": "No psychologists are currently ready to talk."}
    random_psychologist = random.choice(ready_psychologists)
    return random_psychologist

@app.post("/store_my_peer_id")
def store_my_peer_id(psychologist: Psychologist):
    # Поиск психолога в списке по ID
    for i, p in enumerate(psychologists):
        if p.id == psychologist.id:
            # Обновление peer_id психолога
            psychologists[i].peer_id = psychologist.peer_id
            return {"message": f"Peer ID for {psychologist.name} updated successfully."}
    return {"message": "Psychologist not found."}

@app.get("/get_all_psychologists")
def get_all_psychologists():
    return psychologists

@app.get("/get_ready_to_talk_psychologists")
def get_ready_to_talk_psychologists():
    ready_psychologists = [psychologist for psychologist in psychologists if psychologist.ready_to_talk]
    return ready_psychologists




@app.post("/add_new_psychologist")
def add_new_psychologist(psychologist: Psychologist):
    # Check if a psychologist with this peer_id already exists
    for p in psychologists:
        if p.peer_id == psychologist.peer_id:
            p.name = psychologist.name  # Update name
            return {
                "message": f"Updated name for psychologist with peer_id {p.peer_id} to '{p.name}'.",
                "psychologist": p
            }

    # Assign a new ID
    new_id = max((p.id for p in psychologists), default=0) + 1

    # Create and add new psychologist
    new_psychologist = Psychologist(
        id=new_id,
        name=psychologist.name,
        specialization=psychologist.specialization,
        ready_to_talk=psychologist.ready_to_talk,
        peer_id=psychologist.peer_id,
        web_link=psychologist.web_link
    )

    psychologists.append(new_psychologist)

    return {
        "message": f"Psychologist {new_psychologist.name} added successfully.",
        "psychologist": new_psychologist
    }





@app.post("/remove_psychologist")
def remove_psychologist(psychologist_id: int):
    # Поиск психолога в списке по ID и его удаление
    for i, p in enumerate(psychologists):
        if p.id == psychologist_id:
            del psychologists[i]
            return {"message": f"Psychologist with ID {psychologist_id} removed successfully."}
    return {"message": "Psychologist not found."}

@app.get("/get_psychologist/{psychologist_id}")
def get_psychologist(psychologist_id: int):
    # Поиск психолога в списке по ID
    for p in psychologists:
        if p.id == psychologist_id:
            return p
    return {"message": "Psychologist not found."}


# Метод для изменения всех атрибутов психолога по его ID
@app.post("/psychologists/{psychologist_id}")
def update_psychologist(psychologist_id: int, updated_psychologist: Psychologist):
    for i, psychologist in enumerate(psychologists):
        if psychologist.id == psychologist_id:
            psychologists[i] = updated_psychologist
            return updated_psychologist
    raise HTTPException(status_code=404, detail="Psychologist not found")

@app.post("/update_ready_status")
def update_ready_status(update: ReadyStatusUpdate):
    for psychologist in psychologists:
        if psychologist.peer_id == update.peer_id:
            psychologist.ready_to_talk = update.ready_to_talk
            return {"message": f"Psychologist {psychologist.name}'s status updated to {update.ready_to_talk}"}
    
    raise HTTPException(status_code=404, detail="Psychologist not found")

