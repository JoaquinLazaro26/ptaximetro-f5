import os
import logging
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from dotenv import load_dotenv

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Config")

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class FirebaseManager:
    _db = None

    @classmethod
    def get_db(cls):
        """Patrón Singleton para devolver la instancia de la BD."""
        if cls._db is None:
            cls._initialize()
        return cls._db

    @classmethod
    def _initialize(cls):
        try:
            # Obtener variables de entorno
            cred_path = os.getenv("FIREBASE_CRED_PATH", "firebase_credentials.json")
            db_name = os.getenv("FIREBASE_DB_NAME", "(default)")

            logger.info(f"🔧 Configurando Firebase. DB: {db_name}")

            # Inicializar la App de Firebase (Admin SDK)
            # Solo la inicializamos si no existe ya (para evitar errores en recargas)
            if not firebase_admin._apps:
                if not os.path.exists(cred_path):
                    raise FileNotFoundError(f"No se encuentra el archivo de credenciales: {cred_path}")
                
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                logger.info("🔥 Firebase Admin App inicializada.")
            else:
                # Si ya existe, recuperamos las credenciales de la app activa
                cred = firebase_admin.get_app().credential

            # Conectar específicamente a la base de datos nombrada
            cls._db = firestore.Client(
                credentials=cred.get_credential(),
                project=cred.project_id,
                database=db_name
            )
            
            logger.info(f"💾 Conexión establecida a Firestore: '{db_name}'")
            
        except Exception as e:
            logger.critical(f"❌ Error fatal conectando a Firebase: {e}")
            raise e

# Función helper para inyección de dependencias en FastAPI
def get_firestore_db():
    return FirebaseManager.get_db()