import enum

class UserGender(enum.Enum):
    Male = "Male"
    Female = "Female"

class UserRole(enum.Enum):
    Admin = "Admin"
    User = "User"

class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
