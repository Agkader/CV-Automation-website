from pydantic import BaseModel

class Joboffer (BaseModel):
    titre : str
    entreprise : str
    description : str 

class jobofferResponse (Joboffer):
    id : int
    class config :
        from_attributes = True
        
class SwipeAction(BaseModel):
    joboffer_id : int
    action : str

