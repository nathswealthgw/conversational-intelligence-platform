from app.core.security import create_access_token, hash_password, verify_password


class AuthService:
    def create_user(self, email: str, password: str) -> dict:
        return {"email": email, "password_hash": hash_password(password)}

    def authenticate(self, email: str, password: str, password_hash: str) -> str | None:
        if email and verify_password(password, password_hash):
            return create_access_token(email)
        return None
