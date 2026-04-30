import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Configuración de la Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL") # Render nos dará esto
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la Tabla Cursos
class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    duracion = Column(String(50))
    tasa_desaprobacion = Column(String(50))
    requisitos = Column(Text)
    instructores = Column(String(255))
    foto_url = Column(Text)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

# Modelo de la Tabla Personas
class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    rango = Column(String(100))
    estado = Column(String(50))
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

# ESTA LÍNEA CREA LAS TABLAS AUTOMÁTICAMENTE
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "API Activa", "mensaje": "Tablas verificadas/creadas"}

@app.get("/api/cursos/")
def get_cursos():
    db = SessionLocal()
    cursos = db.query(Curso).all()
    return cursos
from pydantic import BaseModel

# Esquema para recibir datos del Bot
class CursoCreate(BaseModel):
    titulo: str
    descripcion: str
    duracion: str
    tasa_desaprobacion: str
    requisitos: str
    instructores: str
    foto_url: str

# RUTA PARA QUE EL BOT GUARDE DATOS
@app.post("/api/cursos/")
def create_curso(curso: CursoCreate):
    db = SessionLocal()
    nuevo_curso = Curso(
        titulo=curso.titulo,
        descripcion=curso.descripcion,
        duracion=curso.duracion,
        tasa_desaprobacion=curso.tasa_desaprobacion,
        requisitos=curso.requisitos,
        instructores=curso.instructores,
        foto_url=curso.foto_url
    )
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    return {"mensaje": "Curso guardado con éxito", "id": nuevo_curso.id}
