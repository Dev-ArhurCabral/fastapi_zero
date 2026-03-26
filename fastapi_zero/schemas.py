from pydantic import BaseModel


# Documantando schema de troca de mensagem
class Message(BaseModel):
    message: str
