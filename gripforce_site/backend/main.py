from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, func, cast, Date
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from config import DATABASE_URL, USERS
from models import Base, User, Commande, Paiement, Livraison, StatutCommande, MethodePaiement, StatutPaiement, StatutLivraison
from auth import hash_password, verify_password, create_access_token, get_current_user
from pydantic import BaseModel

# Init
app = FastAPI(title="GripForce Admin API")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.grip.2mkbusiness.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Pydantic schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class CommandeCreate(BaseModel):
    client_name: str
    client_whatsapp: str
    client_address: Optional[str] = ""
    color: str = "Noir"
    quantity: int = 1
    amount: int = 4500
    notes: Optional[str] = ""

class CommandeUpdate(BaseModel):
    client_name: Optional[str] = None
    client_whatsapp: Optional[str] = None
    client_address: Optional[str] = None
    color: Optional[str] = None
    quantity: Optional[int] = None
    amount: Optional[int] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    notes: Optional[str] = None

class PaiementCreate(BaseModel):
    commande_id: int
    methode: str
    montant: int
    statut: str = "en_attente"
    preuve_url: Optional[str] = ""
    notes: Optional[str] = ""

class LivraisonUpdate(BaseModel):
    zone: Optional[str] = None
    adresse_complete: Optional[str] = None
    statut: Optional[str] = None
    tracking_notes: Optional[str] = None

# --- AUTH ---
@app.post("/api/login")
def login(data: LoginRequest):
    u = data.username.lower()
    if u not in USERS or data.password != USERS[u]["password"]:
        raise HTTPException(401, "Identifiants invalides")
    token = create_access_token(u)
    return {"token": token, "user": {"username": u, "full_name": USERS[u]["full_name"]}}

@app.get("/api/me")
def me(username: str = Depends(get_current_user)):
    return {"username": username, "full_name": USERS[username]["full_name"]}

# --- STATS ---
@app.get("/api/stats")
def stats(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    today = now.date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    total_cmd = db.query(Commande).count()
    cmd_jour = db.query(Commande).filter(cast(Commande.created_at, Date) == today).count()
    cmd_semaine = db.query(Commande).filter(cast(Commande.created_at, Date) >= week_ago).count()

    ca_total = db.query(func.coalesce(func.sum(Commande.amount * Commande.quantity), 0)).filter(Commande.status != "annule").scalar()
    ca_jour = db.query(func.coalesce(func.sum(Commande.amount * Commande.quantity), 0)).filter(cast(Commande.created_at, Date) == today, Commande.status != "annule").scalar()

    en_attente = db.query(Commande).filter(Commande.status.in_(["nouveau", "confirme"])).count()
    a_livrer = db.query(Livraison).filter(Livraison.statut.in_(["en_attente", "en_cours"])).count()
    livrees = db.query(Livraison).filter(Livraison.statut == "livre").count()

    # Commandes récentes
    recentes = db.query(Commande).order_by(Commande.created_at.desc()).limit(8).all()

    return {
        "total_commandes": total_cmd,
        "commandes_jour": cmd_jour,
        "commandes_semaine": cmd_semaine,
        "ca_total": int(ca_total or 0),
        "ca_jour": int(ca_jour or 0),
        "en_attente": en_attente,
        "a_livrer": a_livrer,
        "livrees": livrees,
        "recentes": [
            {
                "id": c.id,
                "client_name": c.client_name,
                "client_whatsapp": c.client_whatsapp,
                "color": c.color,
                "quantity": c.quantity,
                "amount": int(c.amount),
                "status": c.status,
                "created_at": c.created_at.isoformat()
            } for c in recentes
        ]
    }

# --- COMMANDES CRUD ---
@app.get("/api/commandes")
def list_commandes(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    q = db.query(Commande)
    if status:
        q = q.filter(Commande.status == status)
    if search:
        q = q.filter(
            (Commande.client_name.ilike(f"%{search}%")) |
            (Commande.client_whatsapp.ilike(f"%{search}%"))
        )
    total = q.count()
    items = q.order_by(Commande.created_at.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "items": [
            {
                "id": c.id,
                "client_name": c.client_name,
                "client_whatsapp": c.client_whatsapp,
                "client_address": c.client_address,
                "color": c.color,
                "quantity": c.quantity,
                "amount": int(c.amount),
                "status": c.status,
                "notes": c.notes,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                "paiements": [
                    {"id": p.id, "methode": p.methode, "montant": int(p.montant), "statut": p.statut}
                    for p in c.paiements
                ],
                "livraisons": [
                    {"id": l.id, "zone": l.zone, "statut": l.statut, "adresse_complete": l.adresse_complete}
                    for l in c.livraisons
                ]
            } for c in items
        ]
    }

@app.get("/api/commandes/{id}")
def get_commande(id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = db.query(Commande).filter(Commande.id == id).first()
    if not c:
        raise HTTPException(404, "Commande non trouvée")
    return {
        "id": c.id,
        "client_name": c.client_name,
        "client_whatsapp": c.client_whatsapp,
        "client_address": c.client_address,
        "color": c.color,
        "quantity": c.quantity,
        "amount": int(c.amount),
        "status": c.status,
        "notes": c.notes,
        "created_at": c.created_at.isoformat(),
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        "paiements": [
            {"id": p.id, "methode": p.methode, "montant": int(p.montant), "statut": p.statut, "preuve_url": p.preuve_url, "notes": p.notes, "created_at": p.created_at.isoformat()}
            for p in c.paiements
        ],
        "livraisons": [
            {"id": l.id, "zone": l.zone, "adresse_complete": l.adresse_complete, "statut": l.statut, "tracking_notes": l.tracking_notes, "delivered_at": l.delivered_at.isoformat() if l.delivered_at else None}
            for l in c.livraisons
        ]
    }

@app.post("/api/commandes")
def create_commande(data: CommandeCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = Commande(**data.model_dump(), status=StatutCommande.NOUVEAU)
    db.add(c)
    # Créer une livraison automatiquement
    db.flush()
    livraison = Livraison(commande_id=c.id, zone="Dakar", adresse_complete=data.client_address, statut=StatutLivraison.EN_ATTENTE)
    db.add(livraison)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "message": "Commande créée"}

@app.put("/api/commandes/{id}")
def update_commande(id: int, data: CommandeUpdate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = db.query(Commande).filter(Commande.id == id).first()
    if not c:
        raise HTTPException(404, "Commande non trouvée")
    update_data = data.model_dump(exclude_unset=True)
    # Si status passe à "livre", mettre à jour la livraison
    if update_data.get("status") == "livre":
        for l in c.livraisons:
            l.statut = StatutLivraison.LIVRE
            l.delivered_at = datetime.now(timezone.utc)
    for k, v in update_data.items():
        setattr(c, k, v)
    db.commit()
    return {"message": "Commande mise à jour"}

@app.delete("/api/commandes/{id}")
def delete_commande(id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = db.query(Commande).filter(Commande.id == id).first()
    if not c:
        raise HTTPException(404, "Commande non trouvée")
    db.delete(c)
    db.commit()
    return {"message": "Commande supprimée"}

# --- PAIEMENTS ---
@app.get("/api/paiements")
def list_paiements(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    items = db.query(Paiement).order_by(Paiement.created_at.desc()).limit(100).all()
    return [
        {
            "id": p.id,
            "commande_id": p.commande_id,
            "methode": p.methode,
            "montant": int(p.montant),
            "statut": p.statut,
            "preuve_url": p.preuve_url,
            "notes": p.notes,
            "created_at": p.created_at.isoformat()
        } for p in items
    ]

@app.post("/api/paiements")
def create_paiement(data: PaiementCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    p = Paiement(**data.model_dump())
    db.add(p)
    # Si paiement reçu, passer commande en "confirme"
    if data.statut == "recu":
        c = db.query(Commande).filter(Commande.id == data.commande_id).first()
        if c and c.status == StatutCommande.NOUVEAU:
            c.status = StatutCommande.CONFIRME
    db.commit()
    db.refresh(p)
    return {"id": p.id, "message": "Paiement enregistré"}

@app.put("/api/paiements/{id}")
def update_paiement(id: int, statut: str = Query(...), db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    p = db.query(Paiement).filter(Paiement.id == id).first()
    if not p:
        raise HTTPException(404)
    p.statut = statut
    if statut == "recu":
        c = db.query(Commande).filter(Commande.id == p.commande_id).first()
        if c and c.status == StatutCommande.NOUVEAU:
            c.status = StatutCommande.CONFIRME
    db.commit()
    return {"message": "Paiement mis à jour"}

# --- LIVRAISONS ---
@app.get("/api/livraisons")
def list_livraisons(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    items = db.query(Livraison).order_by(Livraison.commande_id.desc()).limit(100).all()
    return [
        {
            "id": l.id,
            "commande_id": l.commande_id,
            "zone": l.zone,
            "adresse_complete": l.adresse_complete,
            "statut": l.statut,
            "tracking_notes": l.tracking_notes,
            "delivered_at": l.delivered_at.isoformat() if l.delivered_at else None
        } for l in items
    ]

@app.put("/api/livraisons/{id}")
def update_livraison(id: int, data: LivraisonUpdate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    l = db.query(Livraison).filter(Livraison.id == id).first()
    if not l:
        raise HTTPException(404)
    update_data = data.model_dump(exclude_unset=True)
    if update_data.get("statut") == "livre":
        update_data["delivered_at"] = datetime.now(timezone.utc)
        # Mettre la commande en "livre" aussi
        c = db.query(Commande).filter(Commande.id == l.commande_id).first()
        if c:
            c.status = StatutCommande.LIVRE
    for k, v in update_data.items():
        setattr(l, k, v)
    db.commit()
    return {"message": "Livraison mise à jour"}

# --- INIT DB ---
@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)
    # Créer les users si pas existants
    db = SessionLocal()
    for username, info in USERS.items():
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            db.add(User(
                username=username,
                password_hash=hash_password(info["password"]),
                full_name=info["full_name"],
                role="admin"
            ))
    db.commit()
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
