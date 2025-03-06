from src.domain.interfaces.entity import BaseDTO


class UserInterestedDTO(BaseDTO["UserInterested"]):
    id: int = None
    user_id: int = None
    interest_id: int = None
