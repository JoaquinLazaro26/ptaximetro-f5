from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import logging

logger = logging.getLogger("Auth")
security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Valida el ID Token de Firebase enviado en el header Authorization.
    Formato esperado: Authorization: Bearer <token>
    """
    token = credentials.credentials
    try:
        # Decodificar y verificar el token con Firebase
        decoded_token = auth.verify_id_token(token)
        
        # Extraer información útil
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        
        logger.info(f"🔑 Acceso autorizado: {email} ({uid})")
        return {"uid": uid, "email": email}
        
    except auth.ExpiredIdTokenError:
        logger.warning("⛔ Token expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado. Por favor, inicia sesión de nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"⛔ Token inválido: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )