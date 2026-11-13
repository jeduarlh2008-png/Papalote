# ==================================================
# PRÁCTICA 4 — CRUD EN EQUIPO
# Programación de Redes — UPQ
# ==================================================

# --------------------------
# ✅ Código base (de la Práctica 3)
# --------------------------
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Inventario de Red", version="2.0")

class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True

inventario: List[Dispositivo] = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1", activo=True),
    Dispositivo(nombre="SW1", tipo="switch", ip="10.0.0.2", activo=True),
    Dispositivo(nombre="AP1", tipo="access point", ip="10.0.0.3", activo=True),
]

# --------------------------
# ✅ Paso 4.3 — Función común de búsqueda
# (La agrega y sube primero el integrante C)
# --------------------------
def buscar(nombre: str) -> Dispositivo | None:
    """Devuelve el equipo con ese nombre, o None si no existe."""
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo
    return None

# Rutas GET existentes
@app.get("/dispositivos", summary="Listar todos los dispositivos")
async def listar():
    return inventario

@app.get("/dispositivos/{nombre}", summary="Consultar un dispositivo")
async def obtener(nombre: str):
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(status_code=404, detail=f"No existe el equipo {nombre}")
    return equipo

# ==================================================
# 🔵 INTEGRANTE A — ALTA (POST)
# ==================================================
@app.post("/dispositivos", status_code=201, summary="Crear nuevo dispositivo")
async def crear(nuevo: Dispositivo):
    """Da de alta un dispositivo. Rechaza nombres repetidos."""
    if buscar(nuevo.nombre) is not None:
        raise HTTPException(status_code=409, detail=f"Ya existe el equipo {nuevo.nombre}")
    inventario.append(nuevo)
    return nuevo

# ==================================================
# 🟡 INTEGRANTE B — ACTUALIZACIÓN (PUT + PATCH)
# ==================================================

# Modelo parcial para PATCH
class DispositivoParcial(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None

@app.put("/dispositivos/{nombre}", summary="Reemplazar dispositivo completo")
async def reemplazar(nombre: str, datos: Dispositivo):
    """Sustituye por completo el registro de un dispositivo."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(status_code=404, detail=f"No existe el equipo {nombre}")
    inventario[inventario.index(equipo)] = datos
    return datos

@app.patch("/dispositivos/{nombre}", summary="Modificar campos específicos")
async def modificar(nombre: str, cambios: DispositivoParcial):
    """Modifica solo los campos enviados."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(status_code=404, detail=f"No existe el equipo {nombre}")
    for campo, valor in cambios.model_dump(exclude_unset=True).items():
        setattr(equipo, campo, valor)
    return equipo

# ==================================================
# 🔴 INTEGRANTE C — BAJA (DELETE)
# ==================================================
@app.delete("/dispositivos/{nombre}", status_code=204, summary="Eliminar dispositivo")
async def eliminar(nombre: str):
    """Da de baja un dispositivo del inventario."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(status_code=404, detail=f"No existe el equipo {nombre}")
    inventario.remove(equipo)
    return Response(status_code=204)
